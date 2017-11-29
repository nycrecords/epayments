import os
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import current_app
from app import db, scheduler
from app.models import Order, Event, BirthSearch, BirthCertificate, MarriageCertificate, \
    MarriageSearch, DeathCertificate, DeathSearch, PhotoGallery, PhotoTax, PropertyCard, Customer, Suborder
from app.date_utils import utc_to_local
from app.file_utils import sftp_ctx
from app.constants import status
from app.constants.client_agency_names import CLIENT_AGENCY_NAMES
from app.constants import order_types, event_type
from flask_login import current_user


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

    return [CLIENT_AGENCY_NAMES[suborder[0]] for suborder in clients_data_suborders]


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
    order = Order(
        id=order_number,
        date_submitted=date_submitted,
        date_received=date_received,
        confirmation_message=confirmation_message,
        client_data=clients_data,
        order_types=_order_types,
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
    customer = Customer(billing_name=billing_name,
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
    # In the XML the type of order is kept up with the ClientID

    clients_data_items = clients_data.split('ClientID')[1:]
    clients_data_items = ['ClientID' + client for client in clients_data_items]
    for clients_data_item in clients_data_items:
        clients_data_list = clients_data_item.split('|')
        client_id = clients_data_list[clients_data_list.index("ClientID") + 1]
        client_agency_name = CLIENT_AGENCY_NAMES[client_id]

        # Suborder Number used to identify multi-part orders
        suborder_number = clients_data_list[clients_data_list.index("OrderNo") + 1]

        # Check for duplicate in database
        duplicate = Suborder.query.filter_by(id=suborder_number).first()

        if duplicate:
            print("Order %s already exists in the database." % order_number)
            return

        suborder = Suborder(id=suborder_number,
                            client_id=client_id,
                            client_agency_name=client_agency_name,
                            order_number=order_number,
                            status=status.RECEIVED)

        db.session.add(suborder)
        db.session.commit()

        # Insert into the StatusTracker Table
        insert_event = Event(suborder_number=suborder_number,
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
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender type
            gender_type = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

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

            customer_order = BirthSearch(
                first_name=first_name,
                last_name=last_name,
                mid_name=mid_name,
                gender_type=gender_type,
                father_name=father_name,
                mother_name=mother_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                birth_place=birth_place,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

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

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

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

            customer_order = MarriageSearch(
                groom_last_name=groom_last_name,
                groom_first_name=groom_first_name,
                bride_last_name=bride_last_name,
                bride_first_name=bride_first_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                marriage_place=marriage_place,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Death Search
        if client_id == '10000103':
            # Retrieve the decedents name (First Name, Last Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

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

            # Retrieve the Age of Death
            age_of_death = clients_data_list[
                clients_data_list.index("AGEOFDEATH") + 1] if "AGEOFDEATH" in clients_data_list else None

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

            customer_order = DeathSearch(
                last_name=last_name,
                first_name=first_name,
                mid_name=mid_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                cemetery=cemetery,
                month=month,
                day=day,
                years=years,
                death_place=death_place,
                age_of_death=age_of_death,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Birth Certificate
        if client_id == '10000147':
            # Retrieve the Certificate Number
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the Certificate Name (First Name, Last Name, Middle Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender type
            gender_type = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Retrieve Fathers Name
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None

            # Retrieve Mother's Name
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

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

            customer_order = BirthCertificate(
                certificate_no=certificate_no,
                first_name=first_name,
                last_name=last_name,
                mid_name=mid_name,
                gender_type=gender_type,
                father_name=father_name,
                mother_name=mother_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                birth_place=birth_place,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Marriage Certificate
        if client_id == '10000181':
            # Retreive the Certificate Number
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the Groom's Information (First and Last Name)
            groom_last_name = clients_data_list[clients_data_list.index("LASTNAME_G") + 1]
            groom_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_G") + 1] if "FIRSTNAME_G" in clients_data_list else None

            # Retreive the Bride's Information (First and Last Name
            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

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

            customer_order = MarriageCertificate(
                certificate_no=certificate_no,
                groom_last_name=groom_last_name,
                groom_first_name=groom_first_name,
                bride_last_name=bride_last_name,
                bride_first_name=bride_first_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                month=month,
                day=day,
                years=years,
                marriage_place=marriage_place,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Death Certificate
        if client_id == '10000182':
            # Retrieve the Certificate Number
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Retrieve the decedents name (First Name, Last Name)
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Retrieve the Customer's Relationship to Certificate Person
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None

            # Retrieve Research Purpose
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else 1

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

            # Retrieve the Age of Death
            age_of_death = clients_data_list[
                clients_data_list.index("AGEOFDEATH") + 1] if "AGEOFDEATH" in clients_data_list else None

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

            customer_order = DeathCertificate(
                certificate_no=certificate_no,
                last_name=last_name,
                first_name=first_name,
                mid_name=mid_name,
                relationship=relationship,
                purpose=purpose,
                num_copies=num_copies,
                cemetery=cemetery,
                month=month,
                day=day,
                years=years,
                death_place=death_place,
                age_of_death=age_of_death,
                borough=borough,
                letter=letter,
                comment=comment,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Property Card
        if client_id == '10000058':
            # Retrieve Building Address
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None
            building_no = clients_data_list[clients_data_list.index("BUILDING_NO") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Retrieve Building Description
            description = clients_data_list[clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in \
                                                                                           clients_data_list else None

            # Retrieve Certification Value (True or False)
            certified = clients_data_list[clients_data_list.index("CERTIFIED") + 1]

            # Retrieve Mail / Pickup Status
            if clients_data_list[
                        clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            # Retrieve Pickup Contact Information
            contact_info = clients_data_list[
                clients_data_list.index("EMAIL") + 1] if "EMAIL" in clients_data_list else None

            customer_order = PropertyCard(
                borough=borough,
                block=block,
                lot=lot,
                building_no=building_no,
                street=street,
                description=description,
                certified=certified,
                mail_pickup=mail_pickup,
                contact_info=contact_info,
                suborder_number=suborder_number
            )

            db.session.add(customer_order)
            db.session.commit()

        # Tax Photo
        if client_id == '10000048':
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
            street_number = clients_data_list[clients_data_list.index("STREET_NUMBER") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Retrieve Building  Description
            description = clients_data_list[
                clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in clients_data_list else None

            # Retrieve Print Size
            type_ = clients_data_list[clients_data_list.index("TYPE") + 1]
            size = clients_data_list[clients_data_list.index("SIZE") + 1] if "SIZE" in clients_data_list else None

            # Retrieve Number of Copies
            num_copies = clients_data_list[
                clients_data_list.index("COPIES") + 1] if "COPIES" in clients_data_list else 1

            # Retrieve Mail / Pickup Status
            if clients_data_list[
                        clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            if collection == 'Both':
                # Remove old Suborder
                Suborder.query.filter_by(id=suborder_number).delete()
                db.session.commit()

                # Create Suborder for 1940 Request
                suborder_1940 = Suborder(
                    id="{}-1940".format(suborder_number),
                    client_id=client_id,
                    client_agency_name=client_agency_name,
                    order_number=order_number,
                    status=status.RECEIVED
                )
                db.session.add(suborder_1940)

                # Create Suborder for 1980 Request
                suborder_1980 = Suborder(
                    id="{}-1980".format(suborder_number),
                    client_id=client_id,
                    client_agency_name=client_agency_name,
                    order_number=order_number,
                    status=status.RECEIVED
                )
                db.session.add(suborder_1980)

                db.session.commit()

                # Create PhotoTax entry for 1940 print
                customer_order_1940 = PhotoTax(
                    borough=borough,
                    collection="1940",
                    roll=roll,
                    block=block,
                    lot=lot,
                    street_number=street_number,
                    street=street,
                    description=description,
                    type=type_,
                    size=size,
                    num_copies=num_copies,
                    mail_pickup=mail_pickup,
                    contact_number=contact_number,
                    comment=comment,
                    suborder_number="{}-1940".format(suborder_number)
                )
                db.session.add(customer_order_1940)

                # Create PhotoTax entry for 1980 print
                customer_order_1980 = PhotoTax(
                    borough=borough,
                    collection="1980",
                    roll="N/A",
                    block=block,
                    lot=lot,
                    street_number=street_number,
                    street=street,
                    description=description,
                    type=type_,
                    size=size,
                    num_copies=num_copies,
                    mail_pickup=mail_pickup,
                    contact_number=contact_number,
                    comment=comment,
                    suborder_number="{}-1980".format(suborder_number)
                )
                db.session.add(customer_order_1980)

                insert_event = Event(suborder_number=suborder_1940.id,
                                     type_=event_type.INITIAL_IMPORT,
                                     # user_email=current_user.email,
                                     previous_value=None,
                                     new_value={
                                         'status': status.RECEIVED,
                                     })
            else:
                customer_order = PhotoTax(
                    borough=borough,
                    collection=collection,
                    roll=roll,
                    block=block,
                    lot=lot,
                    street_number=street_number,
                    street=street,
                    description=description,
                    type=type_,
                    size=size,
                    num_copies=num_copies,
                    mail_pickup=mail_pickup,
                    contact_number=contact_number,
                    comment=comment,
                    suborder_number=suborder_number)
                db.session.add(customer_order)

                insert_event = Event(suborder_number=suborder_number,
                                     type_=event_type.INITIAL_IMPORT,
                                     # user_email=current_user.email,
                                     previous_value=None,
                                     new_value={
                                         'status': status.RECEIVED,
                                     })

            db.session.add(insert_event)
            db.session.commit()

        # Insert into the PhotoGallery table
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

            # Retrieve Mail / Pickup Status
            if clients_data_list[
                        clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            # Retrieve Pickup Contact Information
            contact_number = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            # Retrieve Comment
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # Retrieve Personal Use Agreement
            if clients_data_list[
                        clients_data_list.index("PERSONAL_USE_AGREEMENT") + 1] \
                    if "PERSONAL_USE_AGREEMENT" in clients_data_list else None:
                personal_use_agreement = True
            else:
                personal_use_agreement = False

            customer_order = PhotoGallery(
                image_id=image_id,
                description=description,
                additional_description=additional_description,
                size=size,
                num_copies=num_copies,
                mail_pickup=mail_pickup,
                contact_number=contact_number,
                personal_use_agreement=personal_use_agreement,
                comment=comment,
                suborder_number=suborder_number)

            db.session.add(customer_order)
            db.session.commit()
    return True
