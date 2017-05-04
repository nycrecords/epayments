import os
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import current_app
from app import db, scheduler
from app.models import Orders, StatusTracker, BirthSearch, BirthCertificate, MarriageCertificate,\
    MarriageSearch, DeathCertificate, DeathSearch, PhotoGallery, PhotoTax, PropertyCard, Shipping
from app.file_utils import sftp_ctx
from app._constants_ import borough, collection, gender, purpose, size, status


def import_xml_folder(scheduled=False, path=None):
    """
    Function is called from scheduler at 3AM everyday.
    Downloads all xml files from a remote folder to local folder.
    Imports xml files from local folder to database.
    :param scheduled: Boolean determines whether this is running as a Cron job or manually
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
                        print("Imported {}".format(file_)) if import_file(file_) else print(
                            "Failed to Import {}".format(file_))
        else:
            for file_ in os.listdir(local_path):
                if not file_.startswith('.'):
                    file_ = os.path.join(local_path, file_)
                    print("Imported {}".format(file_)) if import_file(file_) else print(
                        "Failed to Import {}".format(file_))


def import_file(file_name):
    """
        Inserts a single order from an XML file into the database.
        :param file_name: XML file to import
        :return: Bool
    """

    # 1 - Populate the XML Parser
    tree = ET.parse(file_name)
    root = tree.getroot()

    # 2 - Get the Order number
    #     a) Remove CPY from orderno
    order_no = root.find("EPaymentReq").find("OrderNo").text

    if "CPY" in order_no:
        order_no = order_no.strip('CPY')

    # In the XML the type of order is keep up with the ClientID

    clients_data = root.find('ClientsData').text
    clients_data_items = clients_data.split('ClientID')[1:]
    clients_data_items = ['ClientID' + client for client in clients_data_items]

    for i in clients_data_items:
        clients_data_list = i.split('|')
        client_id = clients_data_list[clients_data_list.index("ClientID") + 1]

        # Sub order Number used to identify multi-part orders
        sub_order_no = clients_data_list[clients_data_list.index("OrderNo") + 1]

        # Check for duplicate in database
        duplicate = Orders.query.filter_by(sub_order_no=sub_order_no).first()

        if duplicate:
            print("Order %s already exists in the database." % order_no)
            continue

        # Get Customer Information
        # Name for Billing Information
        billing_name = root.find("EPaymentRes").find("BillingInfo").find("BillingName").text

        # Customer Email: Email for person who placed order
        customer_email = root.find("EPaymentReq").find("CustomerEmail").text

        # Message sent to customer
        confirmation_message = root.find('ConfirmationMessage').text

        # Get Order Date Information
        date_received = date.today()
        date_last_modified = datetime.fromtimestamp(
            os.path.getmtime(file_name)).strftime('%Y-%m-%d %H:%M:%S')

        # Get Shipping Information
        shipping_add = root.find("EPaymentRes").find("ShippingAdd")
        ship_to_name = shipping_add.find("ShipToName").text
        ship_to_street_add = shipping_add.find("ShipToStreetAdd").text
        ship_to_street_add_2 = shipping_add.find("ShipToStreetAdd2").text
        ship_to_city = shipping_add.find("ShipToCity").text
        ship_to_state = shipping_add.find("ShipToState").text
        ship_to_zipcode = shipping_add.find("ShipToZipCode").text
        ship_to_country = shipping_add.find("ShipToCountry").text
        ship_to_phone = shipping_add.find("ShipToPhone").text

        if '-' in ship_to_phone:
            ship_to_phone = ship_to_phone.strip('-')
            print("Stripped the -")

        shipping_instructions = shipping_add.find("ShippingInstructions").text

        # Get info for the BirthSearch/BirthCert



        # Insert into the Orders Table
        insert_order = Orders(order_no=order_no,
                              sub_order_no=sub_order_no,
                              date_submitted=date.today(),
                              date_receivied=date_received,
                              billing_name=billing_name,
                              customer_email=customer_email,
                              confirmation_message=confirmation_message,
                              client_data=clients_data)

        db.session.add(insert_order)
        db.session.commit()

        # Insert into the StatusTracker Table
        insert_status = StatusTracker(sub_order_no=sub_order_no)

        db.session.add(insert_status)
        db.session.commit()

        # Insert into the Shipping Table
        insert_Shipping = Shipping(name=ship_to_name,
                                   address_line_1=ship_to_street_add,
                                   address_line_2=ship_to_street_add_2,
                                   city=ship_to_city,
                                   state=ship_to_state,
                                   zip_code=ship_to_zipcode,
                                   country=ship_to_country,
                                   phone=ship_to_phone,
                                   instructions=shipping_instructions)

        db.session.add(insert_Shipping)
        db.session.commit()

        # Insert into the BirthSearch Table
        # For all the other table check the Client Agency Names
        # Use their ID's to know which table to insert into

        # Use a switch statement to figure out which table go add to
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


        # Marriage Search
        if client_id == '10000102':
            # We are now in the a sub Order that is of type Birth Search
            # Find all the necessary info for birth search

            # sub_order_no = clients_data_list[clients_data_list.index("OrderNo") + 1]

            # Pull the name
            first_name = clients_data_list[clients_data_list.index("FIRSTNAME") + 1]
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            mid_name = clients_data_list[clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender Type
            gender_type = clients_data_list[clients_data_list.index("GENDER") + 1]

            # Get the Parent's names/relationship && purpose
            father_name = clients_data_list[clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None
            mother_name = clients_data_list[clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None
            relationship = clients_data_list[clients_data_list.index("RELATIONSHIP") + 1]
            purpose = clients_data_list[clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None


            # Number of Copies
            additional_copy = clients_data_list[clients_data_list.index("ADDITIONAL_COPY") + 1]

            # Pull the Date(M/D/Y)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1]

            # Indivdual Info
            birth_place = clients_data_list[clients_data_list.index("BIRTH_PLACE") + 1] if "BIRTH_PLACE" in clients_data_list else None
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            comment = clients_data_list[clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            letter = clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None

            insert_birthsearch = BirthSearch(first_name=first_name,
                                             last_name=last_name,
                                             mid_name=mid_name,
                                             gender_type=gender_type,
                                             father_name=father_name,
                                             mother_name=mother_name,
                                             relationship=relationship,
                                             purpose=purpose,
                                             additional_copy=additional_copy,
                                             month=month,
                                             day=day,
                                             years=years,
                                             birth_place=birth_place,
                                             borough=borough,
                                             letter=letter,
                                             comment=comment,
                                             sub_order_no=sub_order_no)

            print("Let add this to the birthsearch table")
            db.session.add(insert_birthsearch)
            db.session.commit()



    return True
