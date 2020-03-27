import xml.etree.ElementTree as ET
from datetime import datetime, date

import os
from flask import current_app

from app import db, scheduler
from app.constants import delivery_method
from app.constants import event_type
from app.constants import status
from app.constants.order_types import CLIENT_ID_DICT
from app.email_utils import send_email
from app.file_utils import sftp_ctx
from app.models import Orders, Events, BirthSearch, BirthCertificate, MarriageCertificate, \
    MarriageSearch, DeathCertificate, DeathSearch, PhotoGallery, TaxPhoto, PropertyCard, Customers, Suborders
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
        file_path = current_app.config['REMOTE_FILE_PATH']
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
            for file_ in os.listdir(local_path):
                if not file_.startswith('.'):
                    file_ = os.path.join(local_path, file_)
                    if import_file(file_):
                        print("Imported {}".format(file_))
                    else:
                        print("Failed to Import {}".format(file_))


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


def import_file(file_name):
    """
        Inserts a single order from an XML file into the database.
        :param file_name: XML file to import
        :return: Bool
    """
    # 1. Populate the XML Parser
    tree = ET.parse(file_name)
    root = tree.getroot()

    # 2. Retrieve the order number.
    order_number = _get_order_number(root.find("EPaymentReq"))

    if Orders.query.filter_by(id=order_number).one_or_none() is not None:
        print("Order {} already exists".format(order_number))
        return False

    # 3. Message sent to customer
    confirmation_message = root.find('ConfirmationMessage').text

    # 4. Get Order Date Information in EST.
    date_received = date.today()

    # For DEV where vagrant RHEL environment is UTC
    # date_submitted = utc_to_local(
    #     datetime.fromtimestamp(
    #         os.path.getmtime(file_name)
    #     ),
    #     'US/Eastern'
    # )

    # For servers where RHEL environment is EST
    date_submitted = datetime.fromtimestamp(
        os.path.getmtime(file_name)
    )

    # 5. Get Client Data information
    clients_data = root.find('ClientsData').text

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
    billing_name = root.find("EPaymentRes").find("BillingInfo").find("BillingName").text

    # 8-b: Customer Email: Email for person who placed order
    customer_email = root.find("EPaymentReq").find("CustomerEmail").text

    # 8-c: Get Shipping Information
    shipping_add = root.find("EPaymentRes").find("ShippingAdd")
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

    mail_order = False

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
        #     "10000058": "Property Card"
        # }

        # Birth Search
        if client_id == '10000102':
            # Retrieve the Certificate Name (First Name, Last Name, Middle Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender type
            gender = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

            # Retrieve the Birth Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Birth Place
            birth_place = clients_data_list[
                clients_data_list.index("BIRTH_PLACE") + 1] if "BIRTH_PLACE" in clients_data_list else None

            # Retrieve Birth Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = BirthSearch(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                gender=gender,
                father_name=father_name,
                mother_name=mother_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                birth_place=birth_place,
                borough=borough,
                letter=letter,
                comment=comment,
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

            # Retreive the Bride's Information (First and Last Name
            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Marriage Location
            marriage_place = clients_data_list[
                clients_data_list.index("MARRIAGE_PLACE") + 1] if "MARRIAGE_PLACE" in clients_data_list else None

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = MarriageSearch(
                groom_last_name=groom_last_name,
                groom_first_name=groom_first_name,
                bride_last_name=bride_last_name,
                bride_first_name=bride_first_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                marriage_place=marriage_place,
                borough=borough,
                letter=letter,
                comment=comment,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
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

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve the Cemetery
            cemetery = clients_data_list[
                clients_data_list.index("CEMETERY") + 1] if "CEMETERY" in clients_data_list else None

            # Retrieve the Place of Death
            death_place = clients_data_list[
                clients_data_list.index("DEATH_PLACE") + 1] if "DEATH_PLACE" in clients_data_list else None

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = DeathSearch(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                num_copies=num_copies,
                cemetery=cemetery,
                month=month,
                day=day,
                years=years,
                death_place=death_place,
                borough=borough,
                letter=letter,
                comment=comment,
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
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            middle_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender type
            gender = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

            # Retrieve the Birth Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR1") + 1] if "YEAR1" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Birth Place
            birth_place = clients_data_list[
                clients_data_list.index("BIRTH_PLACE") + 1] if "BIRTH_PLACE" in clients_data_list else None

            # Retrieve Birth Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = BirthCertificate(
                certificate_number=certificate_number,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                gender=gender,
                father_name=father_name,
                mother_name=mother_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                birth_place=birth_place,
                borough=borough,
                letter=letter,
                comment=comment,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Marriage Certificate
        if client_id == '10000181':
            # Retreive the Certificate Number
            certificate_number = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the Groom's Information (First and Last Name)
            groom_last_name = clients_data_list[clients_data_list.index("LASTNAME_G") + 1]
            groom_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_G") + 1] if "FIRSTNAME_G" in clients_data_list else None

            # Retreive the Bride's Information (First and Last Name
            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1] if "YEAR" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve Marriage Location
            marriage_place = clients_data_list[
                clients_data_list.index("MARRIAGE_PLACE") + 1] if "MARRIAGE_PLACE" in clients_data_list else None

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = MarriageCertificate(
                certificate_number=certificate_number,
                groom_last_name=groom_last_name,
                groom_first_name=groom_first_name,
                bride_last_name=bride_last_name,
                bride_first_name=bride_first_name,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                marriage_place=marriage_place,
                borough=borough,
                letter=letter,
                comment=comment,
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

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPY_REQ") + 1] if "COPY_REQ" in clients_data_list else 1

            # Retrieve the Marriage Date (Month, Day, Years)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1] if "YEAR" in clients_data_list else None
            if years:
                years = years.split(',')
                years = list(filter(bool, years))

            # Retrieve the Cemetery
            cemetery = clients_data_list[
                clients_data_list.index("CEMETERY") + 1] if "CEMETERY" in clients_data_list else None

            # Retrieve the Place of Death
            death_place = clients_data_list[
                clients_data_list.index("DEATH_PLACE") + 1] if "DEATH_PLACE" in clients_data_list else None

            # Retrieve Marriage Borough
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            borough = borough.split(',')
            borough = list(filter(bool, borough))

            # Retrieve Comments
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Exemplification Letter Requested
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = DeathCertificate(
                certificate_number=certificate_number,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                num_copies=num_copies,
                cemetery=cemetery,
                month=month,
                day=day,
                years=years,
                death_place=death_place,
                borough=borough,
                letter=letter,
                comment=comment,
                _delivery_method=_delivery_method,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        # Property Card
        if client_id == '10000058':
            # Retrieve Building Address
            borough = clients_data_list[
                clients_data_list.index("BOROUGH") + 1] if "BOROUGH" in clients_data_list else None
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None
            building_number = clients_data_list[
                clients_data_list.index("STREET_NUMBER") + 1] if "STREET_NUMBER" in clients_data_list else None
            street = clients_data_list[clients_data_list.index("STREET") + 1] if "STREET" in clients_data_list else None

            # Retrieve Building Description
            description = clients_data_list[clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in \
                                                                                           clients_data_list else None

            # Retrieve Certification Value (True or False)
            certified = clients_data_list[
                clients_data_list.index("COPY_OPTIONS") + 1] if "COPY_OPTIONS" in clients_data_list else None

            # Retrieve Mail / Pickup Status
            if "MAIL_PICKUP" in clients_data_list:
                if clients_data_list[clients_data_list.index("MAIL_PICKUP") + 1] == 'Mail':
                    mail = True
                else:
                    mail = False
            else:
                # TODO: Fix this. mail column is BOOLEAN
                mail = None

            # Retrieve Pickup Contact Information
            contact_info = clients_data_list[
                clients_data_list.index("CONTACT_EMAIL") + 1] if "CONTACT_EMAIL" in clients_data_list else None

            customer_order = PropertyCard(
                borough=borough,
                block=block,
                lot=lot,
                building_number=building_number,
                street=street,
                description=description,
                certified=certified,
                mail=mail,
                contact_info=contact_info,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Tax Photo
        if client_id == '10000048':
            # Retrieve Photo ID
            image_id = None
            if "IMAGE_IDENTIFIER" in clients_data_list:
                image_id = clients_data_list[clients_data_list.index("IMAGE_IDENTIFIER") + 1]

            # Retrieve Collection Information (1940's, 1980's, Both)
            collection = clients_data_list[clients_data_list.index("Collection") + 1]

            # Retrieve Borough Information
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            # Retrieve Roll Information
            roll = clients_data_list[clients_data_list.index("ROLL") + 1] if "ROLL" in clients_data_list else None

            # Retrieve Block and Lot of Building
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None

            # Retrieve Street Address
            building_number = clients_data_list[clients_data_list.index("STREET_NUMBER") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Retrieve Building  Description
            description = clients_data_list[
                clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in clients_data_list else None

            # Retrieve Print Size
            size = clients_data_list[clients_data_list.index("TYPE") + 1]

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1] if "COPIES" in clients_data_list else 1

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            if collection == 'Both':
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

                # This is to handle "Both" collection choices
                image_id_1940 = None
                image_id_1980 = None
                if image_id is not None and image_id.startswith('nynyma'):
                    image_id_1940 = image_id
                else:
                    image_id_1980 = image_id

                # Create TaxPhoto entry for 1940 print
                customer_order_1940 = TaxPhoto(
                    borough=borough,
                    collection="1940",
                    image_id=image_id_1940,
                    roll=roll,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    description=description,
                    size=size,
                    num_copies=num_copies,
                    _delivery_method=_delivery_method,
                    contact_number=contact_number,
                    suborder_number=suborder_1940.id
                )
                db.session.add(customer_order_1940)
                suborder_1940.es_update(customer_order_1940.serialize)

                # Create TaxPhoto entry for 1980 print
                customer_order_1980 = TaxPhoto(
                    borough=borough,
                    collection="1980",
                    image_id=image_id_1980,
                    roll=None,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    description=description,
                    size=size,
                    num_copies=num_copies,
                    _delivery_method=_delivery_method,
                    contact_number=contact_number,
                    suborder_number=suborder_1980.id
                )
                db.session.add(customer_order_1980)
                suborder_1980.es_update(customer_order_1980.serialize)

                insert_event = [
                    Events(suborder_number=suborder_1940.id,
                           type_=event_type.INITIAL_IMPORT,
                           # user_email=current_user.email,
                           previous_value=None,
                           new_value={
                               'status': status.RECEIVED,
                           }),
                    Events(suborder_number=suborder_1980.id,
                           type_=event_type.INITIAL_IMPORT,
                           # user_email=current_user.email,
                           previous_value=None,
                           new_value={
                               'status': status.RECEIVED,
                           })
                ]
                db.session.bulk_save_objects(insert_event)

            else:
                customer_order = TaxPhoto(
                    borough=borough,
                    collection=collection,
                    image_id=image_id,
                    roll=roll,
                    block=block,
                    lot=lot,
                    building_number=building_number,
                    street=street,
                    description=description,
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

            # Retrieve Photo Description
            description = clients_data_list[
                clients_data_list.index("IMAGE_DESCRIPTION") + 1] \
                if "IMAGE_DESCRIPTION" in clients_data_list else None

            # Retrieve Additional Description
            additional_description = clients_data_list[
                clients_data_list.index("ADDITIONAL_DESCRIPTION") + 1] \
                if "ADDITIONAL_DESCRIPTION" in clients_data_list else None

            # Retrieve Print size
            size = clients_data_list[clients_data_list.index("SIZE") + 1]

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1] if "COPIES" in clients_data_list else 1

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            # Retrieve Comment
            comment = clients_data_list[
                clients_data_list.index("COMMENTS") + 1] if "COMMENTS" in clients_data_list else None

            # Retrieve Personal Use Agreement
            if clients_data_list[
                clients_data_list.index("PERSONAL_USE_AGREEMENT") + 1] \
                    if "PERSONAL_USE_AGREEMENT" in clients_data_list else None:
                personal_use_agreement = True
            else:
                personal_use_agreement = False

            # Retrieve delivery method
            _delivery_method = clients_data_list[clients_data_list.index('DELIVERY') + 1].lower()
            if _delivery_method == delivery_method.MAIL:
                mail_order = True

            customer_order = PhotoGallery(
                image_id=image_id,
                description=description,
                additional_description=additional_description,
                size=size,
                num_copies=num_copies,
                _delivery_method=_delivery_method,
                contact_number=contact_number,
                personal_use_agreement=personal_use_agreement,
                comment=comment,
                suborder_number=suborder_number)

            db.session.add(customer_order)
            db.session.commit()
            suborder.es_update(customer_order.serialize)

        if mail_order:
            send_email(
                customer.email,
                "Department of Records and Information Services - Your Municipal Archives Online Order ({})".format(order.id),
                "email_templates/convert_mail_to_email",
                order=order,
            )

    return True
