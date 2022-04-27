import os
import smtplib
import xml.etree.ElementTree as ET
from datetime import datetime
from time import localtime, strftime

from flask import current_app

from app import db, scheduler
from app.constants import event_type
from app.constants import status
from app.constants.order_types import CLIENT_ID_DICT
from app.date_utils import calculate_date_received
from app.file_utils import sftp_ctx
from app.models import Orders, Events, BirthSearch, BirthCertificate, HVR, MarriageCertificate, \
    MarriageSearch, DeathCertificate, DeathSearch, PhotoGallery, TaxPhoto, PropertyCard, Customers, Suborders, OCME, \
    NoAmends
from app.search.utils import delete_doc


def import_xml_folder(scheduled=False, path=None):
    """
    Function is called from scheduler at 3AM everyday.
    Downloads all xml files from a remote folder to local folder.
    Imports xml files from local folder to database.
    :param scheduled: Boolean determines whether this is running as a Cron job or manually
    :param path: Path to folder.
    """

    with scheduler.app.app_context():
        local_path = path or current_app.config['LOCAL_FILE_PATH']

        if scheduled:
            file_path = current_app.config['REMOTE_FILE_PATH']
            local_path = current_app.config['LOCAL_FILE_PATH']

            # Create new folder with date of download and download all files
            import_folder = path or os.path.join(local_path,
                                                 'DOR-{date_time}/'.format(
                                                     date_time=datetime.now().strftime('%m-%d-%Y')))

            if current_app.config['USE_SFTP']:

                with sftp_ctx() as sftp:
                    if not os.path.isdir(import_folder):
                        sftp.mkdir(import_folder)
                        print("SFTP Created Directory: " + import_folder)
                    for file in os.listdir(file_path):
                        if os.path.isfile(os.path.join(file_path, file)) \
                                and not os.path.exists(os.path.join(import_folder, file)):
                            sftp.get(os.path.join(file_path, file), os.path.join(import_folder, file))
                            print("SFTP Transferred File: " + file)
                    sftp.close()

                for file_ in os.listdir(import_folder):
                    if not file_.startswith('.'):
                        file_ = os.path.join(import_folder, file_)
                        if import_file(file_):
                            print("Imported {}".format(file_))
                        else:
                            print("Failed to Import {}".format(file_))
        else:
            sender = 'appdev@records.nyc.gov'
            receivers = ['epayments@records.nyc.gov']

            email = f"""\
Subject: ePayments Import %s
From: DORIS AppDev <appdev@records.nyc.gov>
To: ePayments Staff <epayments@records.nyc.gov>

""" % strftime("%Y-%m-%d %H-%M-%S", localtime())

            for file_ in os.listdir(local_path):
                if not file_.startswith('.'):
                    file_path = os.path.join(local_path, file_)
                    et = ET.parse(file_path)
                    tree = et.getroot()

                    date_submitted = datetime.fromtimestamp(
                        os.path.getmtime(file_path)
                    )

                    if import_file(tree, date_submitted):
                        email += "Successfully Imported {}".format(file_) + "\n"
                    else:
                        email += "Failed to Import {}".format(file_) + "\n"
            smtpObj = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
            smtpObj.sendmail(sender, receivers, email)


def _get_order_number(node):
    """
    Given an XML node, retrieve the order number (numeric portion only.
    :param node: XML Node.
    :return: Order Number
    """
    order_number = node.find("OrderNo").text
    if 'CPY' in order_number:
        order_number = order_number.strip('CPY')

    return order_number


def _get_order_types(clients_data):
    """
    Given a pipe-delimited string of ClientsData, determine the Order Types in the Customer's order.
    :param node: pipe-delimiteed string
    :return: ClientsData dictionary
    """
    clients_data_suborders = list(filter(bool, clients_data.split('ClientID|')))
    clients_data_suborders = [item.split('|') for item in clients_data_suborders]

    return [CLIENT_ID_DICT[suborder[0]] for suborder in clients_data_suborders]


def import_file(tree, date_submitted):
    """
        Inserts a single order from an XML file into the database.
        :param file_name: XML file to import
        :return: Bool
    """
    # 1. Populate the XML Parser
    # tree = ET.parse(file_name)
    # root = tree.getroot()

    # 2. Retrieve the order number.
    order_number = _get_order_number(tree.find("EPaymentReq"))

    if Orders.query.filter_by(id=order_number).one_or_none() is not None:
        print("Order {} already exists".format(order_number))
        return False

    # 3. Message sent to customer
    confirmation_message = tree.find('ConfirmationMessage').text

    # 4. Get Order Date Information in EST.
    date_received = calculate_date_received()

    # 5. Get Client Data information
    clients_data = tree.find('ClientsData').text

    # 6. Get Order Types
    _order_types = _get_order_types(clients_data)

    # 7. Add Orders Object to DB Session
    order = Orders(
        _id=order_number,
        date_submitted=date_submitted,
        date_received=date_received,
        confirmation_message=confirmation_message,
        client_data=clients_data,
        _order_types=_order_types,
        multiple_items=(len(_order_types) > 1)
    )
    db.session.add(order)

    # 8. Get Customer Information
    # 8-a: Customer Name
    billing_name = tree.find("EPaymentRes").find("BillingInfo").find("BillingName").text

    # 8-b: Customer Email: Email for person who placed order
    customer_email = tree.find("EPaymentReq").find("CustomerEmail").text

    # 8-c: Get Shipping Information
    shipping_add = tree.find("EPaymentRes").find("ShippingAdd")
    ship_to_name = shipping_add.find("ShipToName").text
    ship_to_street_add = shipping_add.find("ShipToStreetAdd").text
    ship_to_street_add_2 = shipping_add.find("ShipToStreetAdd2").text
    ship_to_city = shipping_add.find("ShipToCity").text
    ship_to_state = shipping_add.find("ShipToState").text
    ship_to_zipcode = shipping_add.find("ShipToZipCode").text
    ship_to_country = shipping_add.find("ShipToCountry").text
    ship_to_phone = shipping_add.find("ShipToPhone").text
    shipping_instructions = shipping_add.find("ShippingInstructions").text

    # Insert into Customer table
    customer = Customers(billing_name=billing_name,
                         email=customer_email,
                         shipping_name=ship_to_name,
                         address_line_1=ship_to_street_add,
                         address_line_2=ship_to_street_add_2,
                         city=ship_to_city,
                         state=ship_to_state,
                         zip_code=ship_to_zipcode,
                         country=ship_to_country,
                         phone=ship_to_phone,
                         instructions=shipping_instructions,
                         order_number=order_number)

    db.session.add(customer)
    db.session.commit()

    # In the XML the type of order is kept up with the ClientID
    clients_data_items = clients_data.split('ClientID')[1:]
    clients_data_items = ['ClientID' + client for client in clients_data_items]
    for clients_data_item in clients_data_items:
        clients_data_list = clients_data_item.split('|')
        client_id = clients_data_list[clients_data_list.index("ClientID") + 1]
        order_type = CLIENT_ID_DICT[client_id]

        # Suborder Number used to identify multi-part orders
        suborder_number = clients_data_list[clients_data_list.index("OrderNo") + 1]

        # Check for duplicate in database
        duplicate = Suborders.query.filter_by(id=suborder_number).first()

        if duplicate:
            print("Order %s already exists in the database." % order_number)
            return

        suborder = Suborders(id=suborder_number,
                             client_id=client_id,
                             order_type=order_type,
                             order_number=order_number,
                             _status=status.RECEIVED)

        db.session.add(suborder)
        db.session.commit()
        suborder.es_create()

        # Insert into the StatusTracker Table
        insert_event = Events(suborder_number=suborder_number,
                              type_=event_type.INITIAL_IMPORT,
                              # user_email=current_user.email,
                              previous_value=None,
                              new_value={
                                  'status': status.RECEIVED,
                              })

        db.session.add(insert_event)

        # Insert into the BirthSearch Table
        # For all the other table check the Client Agency Names
        # Use their ID's to know which table to insert into

        # Do this from ClientID

        # CLIENT_AGENCY_NAMES = {
        #     "10000048": "Photo Tax",
        #     "10000060": "Photo Gallery",
        #     "10000102": "Birth Search",
        #     "10000147": "Birth Cert",
        #     "10000104": "Marriage Search",
        #     "10000181": "Marriage Cert",
        #     "10000103": "Death Search",
        #     "10000182": "Death Cert",
        #     "10000110": "Property Card",
        #     "10000120": "OCME",
        #     "10000106": "No Amends",
        #     "10000107": "HVR",
        # }

        # Birth Search
        if client_id == '10000102':
            # Retrieve the Certificate Name (First Name, Last Name, Middle Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            alt_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME") + 1] if "ALTFIRSTNAME" in clients_data_list else None
            alt_last_name = clients_data_list[
                clients_data_list.index("ALTLASTNAME") + 1] if "ALTLASTNAME" in clients_data_list else None
            alt_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME") + 1] if "ALTMIDDLENAME" in clients_data_list else None

            # Pull the gender type
            gender = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHERNAME") + 1] if "FATHERNAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHERNAME") + 1] if "MOTHERNAME" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1] if "COPIES" in clients_data_list else 1

            # Retrieve the Birth Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1]
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Birth Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = BirthSearch(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                alt_first_name=alt_first_name,
                alt_last_name=alt_last_name,
                alt_middle_name=alt_middle_name,
                gender=gender,
                father_name=father_name,
                mother_name=mother_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                borough=borough,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Marriage Search
        if client_id == '10000104':
            # Retrieve the Groom's Information (First and Last Name)
            groom_last_name = clients_data_list[clients_data_list.index("LASTNAME_G") + 1]
            groom_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_G") + 1] if "FIRSTNAME_G" in clients_data_list else None
            groom_middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME_G") + 1] if "MIDDLENAME_G" in clients_data_list else None
            alt_groom_last_name = clients_data_list[clients_data_list.index("ALTLASTNAME_G") + 1]
            alt_groom_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME_G") + 1] if "ALTFIRSTNAME_G" in clients_data_list else None
            alt_groom_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME_G") + 1] if "ALTMIDDLENAME_G" in clients_data_list else None

            # Retreive the Bride's Information (First and Last Name
            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None
            bride_middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME_B") + 1] if "MIDDLENAME_B" in clients_data_list else None
            alt_bride_last_name = clients_data_list[clients_data_list.index("ALTLASTNAME_B") + 1]
            alt_bride_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME_B") + 1] if "ALTFIRSTNAME_B" in clients_data_list else None
            alt_bride_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME_B") + 1] if "ALTMIDDLENAME_B" in clients_data_list else None

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1]
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = MarriageSearch(
                bride_last_name=bride_last_name,
                bride_middle_name=bride_middle_name,
                bride_first_name=bride_first_name,
                alt_bride_last_name=alt_bride_last_name,
                alt_bride_middle_name=alt_bride_middle_name,
                alt_bride_first_name=alt_bride_first_name,
                groom_last_name=groom_last_name,
                groom_middle_name=groom_middle_name,
                groom_first_name=groom_first_name,
                alt_groom_last_name=alt_groom_last_name,
                alt_groom_middle_name=alt_groom_middle_name,
                alt_groom_first_name=alt_groom_first_name,
                month=month,
                day=day,
                years=years,
                borough=borough,
                num_copies=num_copies,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number,
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Death Search
        if client_id == '10000103':
            # Retrieve the decedents name (First Name, Last Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            alt_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME") + 1] if "ALTFIRSTNAME" in clients_data_list else None
            alt_last_name = clients_data_list[
                clients_data_list.index("ALTLASTNAME") + 1] if "ALTLASTNAME" in clients_data_list else None
            alt_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME") + 1] if "ALTMIDDLENAME" in clients_data_list else None

            # Retrieve age at death
            age_at_death = clients_data_list[
                clients_data_list.index("AGE_AT_DEATH") + 1] if "AGE_AT_DEATH" in clients_data_list else None

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1]
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHERNAME") + 1] if "FATHERNAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHERNAME") + 1] if "MOTHERNAME" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1]

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = DeathSearch(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                num_copies=num_copies,
                alt_first_name=alt_first_name,
                alt_last_name=alt_last_name,
                alt_middle_name=alt_middle_name,
                age_at_death=age_at_death,
                month=month,
                day=day,
                years=years,
                borough=borough,
                father_name=father_name,
                mother_name=mother_name,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Birth Certificate
        if client_id == '10000147':
            # Retrieve the Certificate Number
            certificate_number = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the Certificate Name (First Name, Last Name, Middle Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            alt_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME") + 1] if "ALTFIRSTNAME" in clients_data_list else None
            alt_last_name = clients_data_list[
                clients_data_list.index("ALTLASTNAME") + 1] if "ALTLASTNAME" in clients_data_list else None
            alt_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME") + 1] if "ALTMIDDLENAME" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # Retrieve the Birth Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1] if "YEAR" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Birth Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = BirthCertificate(
                certificate_number=certificate_number,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                alt_first_name=alt_first_name,
                alt_last_name=alt_last_name,
                alt_middle_name=alt_middle_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                borough=borough,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Marriage Certificate
        if client_id == '10000181':
            # Retrieve the Certificate Number
            certificate_number = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the Groom's Information (First and Last Name)
            groom_last_name = clients_data_list[clients_data_list.index("LASTNAME_G") + 1]
            groom_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_G") + 1] if "FIRSTNAME_G" in clients_data_list else None
            groom_middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME_G") + 1] if "MIDDLENAME_G" in clients_data_list else None
            alt_groom_last_name = clients_data_list[clients_data_list.index("ALTLASTNAME_G") + 1]
            alt_groom_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME_G") + 1] if "ALTFIRSTNAME_G" in clients_data_list else None
            alt_groom_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME_G") + 1] if "ALTMIDDLENAME_G" in clients_data_list else None

            # Retreive the Bride's Information (First and Last Name
            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None
            bride_middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME_B") + 1] if "MIDDLENAME_B" in clients_data_list else None
            alt_bride_last_name = clients_data_list[clients_data_list.index("ALTLASTNAME_B") + 1]
            alt_bride_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME_B") + 1] if "ALTFIRSTNAME_B" in clients_data_list else None
            alt_bride_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME_B") + 1] if "ALTMIDDLENAME_B" in clients_data_list else None

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1]
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = MarriageCertificate(
                certificate_number=certificate_number,
                bride_last_name=bride_last_name,
                bride_middle_name=bride_middle_name,
                bride_first_name=bride_first_name,
                alt_bride_last_name=alt_bride_last_name,
                alt_bride_middle_name=alt_bride_middle_name,
                alt_bride_first_name=alt_bride_first_name,
                groom_last_name=groom_last_name,
                groom_middle_name=groom_middle_name,
                groom_first_name=groom_first_name,
                alt_groom_last_name=alt_groom_last_name,
                alt_groom_middle_name=alt_groom_middle_name,
                alt_groom_first_name=alt_groom_first_name,
                month=month,
                day=day,
                years=years,
                borough=borough,
                num_copies=num_copies,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Death Certificate
        if client_id == '10000182':
            # Retrieve the Certificate Number
            certificate_number = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the decedents name (First Name, Last Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            alt_first_name = clients_data_list[
                clients_data_list.index("ALTFIRSTNAME") + 1] if "ALTFIRSTNAME" in clients_data_list else None
            alt_last_name = clients_data_list[
                clients_data_list.index("ALTLASTNAME") + 1] if "ALTLASTNAME" in clients_data_list else None
            alt_middle_name = clients_data_list[
                clients_data_list.index("ALTMIDDLENAME") + 1] if "ALTMIDDLENAME" in clients_data_list else None

            # Retrieve age at death
            age_at_death = clients_data_list[
                clients_data_list.index("AGE_AT_DEATH") + 1] if "AGE_AT_DEATH" in clients_data_list else None

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1]
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1]

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            customer_order = DeathCertificate(
                certificate_number=certificate_number,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                alt_first_name=alt_first_name,
                alt_last_name=alt_last_name,
                alt_middle_name=alt_middle_name,
                age_at_death=age_at_death,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                borough=borough,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Property Card
        if client_id == '10000110':
            # Retrieve Building Address
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            block = clients_data_list[clients_data_list.index("BLOCK") + 1]
            lot = clients_data_list[clients_data_list.index("LOT") + 1]
            building_number = clients_data_list[
                clients_data_list.index("STREET_NUMBER") + 1] if "STREET_NUMBER" in clients_data_list else None
            street = clients_data_list[clients_data_list.index("STREET") + 1] if "STREET" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # Retrieve Raised Seal
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            # Retrieve Pickup Number Information
            contact_number = clients_data_list[
                clients_data_list.index("PICKUP_PHONE") + 1] if "PICKUP_PHONE" in clients_data_list else None

            # Retrieve Pickup Email Information
            contact_email = clients_data_list[
                clients_data_list.index("PICKUP_EMAIL") + 1] if "PICKUP_EMAIL" in clients_data_list else None

            property_card = PropertyCard(
                borough=borough,
                block=block,
                lot=lot,
                building_number=building_number,
                street=street,
                num_copies=num_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                delivery_method=_delivery_method,
                contact_number=contact_number,
                contact_email=contact_email,
                suborder_number=suborder_number
            )

            db.session.add(property_card)
            db.session.commit()
            suborder.es_update(property_card.serialize)

        # Tax Photo
        if client_id == '10000048':
            # Retrieve Photo ID
            image_id = None
            if "IMAGE_IDENTIFIER" in clients_data_list:
                image_id = clients_data_list[clients_data_list.index("IMAGE_IDENTIFIER") + 1]

            # Retrieve Collection Information (1940 or 1980 or 1940,1980)
            collection = clients_data_list[clients_data_list.index("COLLECTION") + 1]

            # Retrieve Borough Information
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            # Retrieve Street Address
            building_number = clients_data_list[clients_data_list.index("STREET_NUMBER") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Retrieve Block and Lot of Building
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("PICKUP_PHONE") + 1] if "PICKUP_PHONE" in clients_data_list else None

            contact_email = clients_data_list[
                clients_data_list.index("PICKUP_EMAIL") + 1] if "PICKUP_EMAIL" in clients_data_list else None

            if collection == '1940,1980':
                # Remove old Suborder
                Suborders.query.filter_by(id=suborder_number).delete()
                db.session.commit()
                delete_doc(suborder_number)

                # Create Suborder for 1940 Request
                suborder_1940 = Suborders(
                    id="{}-1940".format(suborder_number),
                    client_id=client_id,
                    order_type=order_type,
                    order_number=order_number,
                    _status=status.RECEIVED
                )
                db.session.add(suborder_1940)

                # Create Suborder for 1980 Request
                suborder_1980 = Suborders(
                    id="{}-1980".format(suborder_number),
                    client_id=client_id,
                    order_type=order_type,
                    order_number=order_number,
                    _status=status.RECEIVED
                )
                db.session.add(suborder_1980)

                db.session.commit()
                suborder_1940.es_create()
                suborder_1980.es_create()

                # Retrieve Print Size
                size_1940 = clients_data_list[clients_data_list.index("SIZE_1") + 1]

                # Retrieve Number of Copies
                num_copies_1940 = clients_data_list[clients_data_list.index("COPIES_1") + 1]

                # Retrieve delivery method
                delivery_method_1940 = clients_data_list[clients_data_list.index('DELIVERY_1') + 1].lower()

                # Create TaxPhoto entry for 1940 print
                customer_order_1940 = TaxPhoto(
                    borough=borough,
                    collection="1940",
                    image_id=image_id,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    size=size_1940,
                    num_copies=num_copies_1940,
                    _delivery_method=delivery_method_1940,
                    contact_number=contact_number,
                    contact_email=contact_email,
                    suborder_number=suborder_1940.id
                )
                db.session.add(customer_order_1940)
                suborder_1940.es_update(customer_order_1940.serialize)

                # Retrieve Print Size
                size_1980 = clients_data_list[clients_data_list.index("SIZE_2") + 1]

                # Retrieve Number of Copies
                num_copies_1980 = clients_data_list[clients_data_list.index("COPIES_2") + 1]

                # Retrieve delivery method
                delivery_method_1980 = clients_data_list[clients_data_list.index('DELIVERY_2') + 1].lower()

                # Create TaxPhoto entry for 1980 print
                customer_order_1980 = TaxPhoto(
                    borough=borough,
                    collection="1980",
                    image_id=image_id,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    size=size_1980,
                    num_copies=num_copies_1980,
                    _delivery_method=delivery_method_1980,
                    contact_number=contact_number,
                    suborder_number=suborder_1980.id
                )
                db.session.add(customer_order_1980)
                suborder_1980.es_update(customer_order_1980.serialize)

                insert_event = [
                    Events(suborder_number=suborder_1940.id,
                           type_=event_type.INITIAL_IMPORT,
                           previous_value=None,
                           new_value={
                               'status': status.RECEIVED,
                           }),
                    Events(suborder_number=suborder_1980.id,
                           type_=event_type.INITIAL_IMPORT,
                           previous_value=None,
                           new_value={
                               'status': status.RECEIVED,
                           })
                ]
                db.session.bulk_save_objects(insert_event)

            else:
                # Retrieve Print Size
                size = clients_data_list[clients_data_list.index("SIZE_1") + 1]

                # Retrieve Number of Copies
                num_copies = clients_data_list[clients_data_list.index("COPIES_1") + 1]

                # Retrieve delivery method
                _delivery_method = clients_data_list[clients_data_list.index('DELIVERY_1') + 1].lower()

                customer_order = TaxPhoto(
                    borough=borough,
                    collection=collection,
                    image_id=image_id,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    size=size,
                    num_copies=num_copies,
                    _delivery_method=_delivery_method,
                    contact_number=contact_number,
                    suborder_number=suborder_number)
                db.session.add(customer_order)
                suborder.es_update(customer_order.serialize)
            db.session.commit()

        # Photo Gallery
        if client_id == '10000060':
            # Retrieve Photo ID
            image_id = clients_data_list[clients_data_list.index("IMAGE_IDENTIFIER") + 1]

            # Retrieve Print size
            size = clients_data_list[clients_data_list.index("SIZE") + 1]

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1] if "COPIES" in clients_data_list else 1

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("PICKUP_PHONE") + 1] if "PICKUP_PHONE" in clients_data_list else None

            # Retrieve Pickup Contact Information
            contact_email = clients_data_list[
                clients_data_list.index("PICKUP_EMAIL") + 1] if "PICKUP_EMAIL" in clients_data_list else None

            # Retrieve Personal Use Agreement
            if clients_data_list[
                clients_data_list.index("PERSONAL_USE_AGREEMENT") + 1] \
                    if "PERSONAL_USE_AGREEMENT" in clients_data_list else None:
                personal_use_agreement = True
            else:
                personal_use_agreement = False

            photo_gallery = PhotoGallery(
                image_id=image_id,
                size=size,
                num_copies=num_copies,
                _delivery_method=_delivery_method,
                contact_number=contact_number,
                contact_email=contact_email,
                personal_use_agreement=personal_use_agreement,
                suborder_number=suborder_number)

            db.session.add(photo_gallery)
            db.session.commit()
            suborder.es_update(photo_gallery.serialize)

        # OCME
        if client_id == "10000120":
            # Retrieve the borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            month = clients_data_list[clients_data_list.index("MONTH") + 1]
            day = clients_data_list[clients_data_list.index("DAY") + 1]
            year = clients_data_list[clients_data_list.index("YEAR") + 1]

            first_name = clients_data_list[clients_data_list.index("FIRSTNAME") + 1]
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            age = clients_data_list[
                clients_data_list.index("AGE_AT_DEATH") + 1] if "AGE_AT_DEATH" in clients_data_list else None

            certificate_number = clients_data_list[
                clients_data_list.index("CERTIFICATE_NUMBER") + 1] if "CERTIFICATE_NUMBER" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            # Retrieve Pickup Number Information
            contact_number = clients_data_list[
                clients_data_list.index("PICKUP_PHONE") + 1] if "PICKUP_PHONE" in clients_data_list else None

            # Retrieve Pickup Email Information
            contact_email = clients_data_list[
                clients_data_list.index("PICKUP_EMAIL") + 1] if "PICKUP_EMAIL" in clients_data_list else None

            ocme = OCME(
                borough=borough,
                date=datetime(int(year), int(month), int(day)),
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                age=age,
                certificate_number=certificate_number,
                num_copies=num_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                delivery_method=_delivery_method,
                contact_number=contact_number,
                contact_email=contact_email,
                suborder_number=suborder_number
            )

            db.session.add(ocme)
            db.session.commit()
            suborder.es_update(ocme.serialize)

        # No Amends
        if client_id == '10000106':
            # Retrieve Number of Copies
            num_copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            # Retrieve delivery method
            file_name = clients_data_list[clients_data_list.index('FILE') + 1]

            no_amends = NoAmends(
                num_copies=num_copies,
                filename=file_name,
                delivery_method=_delivery_method,
                suborder_number=suborder_number,
            )

            db.session.add(no_amends)
            db.session.commit()
            suborder.es_update(no_amends.serialize)

        # HVR
        if client_id == '10000107':
            # Retrieve link
            link = clients_data_list[clients_data_list.index("LINK") + 1]

            # Retrieve record id
            record_id = clients_data_list[clients_data_list.index("RECORDID") + 1]

            # Retrieve type
            _type = clients_data_list[clients_data_list.index("TYPE") + 1]

            # Retrieve Number of Copies
            num_copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("EXEMPLIFICATION_LETTER") + 1] == "Yes":
                exemplification = True
                exemplification_copies = clients_data_list[clients_data_list.index("LOE_COPIES") + 1]
            else:
                exemplification = False
                exemplification_copies = None

            # Retrieve Raised Seal Requested
            if clients_data_list[clients_data_list.index("RAISEDSEAL") + 1] == "Yes":
                raised_seal = True
                raised_seal_copies = clients_data_list[clients_data_list.index("RAISEDSEAL_COPIES") + 1]
            else:
                raised_seal = False
                raised_seal_copies = None

            # Retrieve No Amends Requested
            if clients_data_list[clients_data_list.index("NOAMENDS_LETTER") + 1] == "Yes":
                no_amends = True
                no_amends_copies = clients_data_list[clients_data_list.index("NOAMENDS_COPIES") + 1]
            else:
                no_amends = False
                no_amends_copies = None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()

            hvr = HVR(
                link=link,
                record_id=record_id,
                _type=_type,
                num_copies=num_copies,
                exemplification=exemplification,
                exemplification_copies=exemplification_copies,
                raised_seal=raised_seal,
                raised_seal_copies=raised_seal_copies,
                no_amends=no_amends,
                no_amends_copies=no_amends_copies,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number,
            )

            db.session.add(hvr)
            db.session.commit()
            suborder.es_update(hvr.serialize)

    return True
