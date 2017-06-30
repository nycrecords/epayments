import os
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import current_app
from app import db, scheduler
from app.models import Orders, StatusTracker, BirthSearch, BirthCertificate, MarriageCertificate,\
    MarriageSearch, DeathCertificate, DeathSearch, PhotoGallery, PhotoTax, PropertyCard, Customer
from app.file_utils import sftp_ctx
from app.constants import borough, collection, gender, purpose, size, status


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
                              date_received=date_received,
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
        insert_Customer = Customer(name=ship_to_name,
                                   address_line_1=ship_to_street_add,
                                   address_line_2=ship_to_street_add_2,
                                   city=ship_to_city,
                                   state=ship_to_state,
                                   zip_code=ship_to_zipcode,
                                   country=ship_to_country,
                                   phone=ship_to_phone,
                                   instructions=shipping_instructions)

        db.session.add(insert_Customer)
        db.session.commit()

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
            # We are now in the a sub Order that is of type Birth Search
            # Find all the necessary info for birth search

            # sub_order_no = clients_data_list[clients_data_list.index("OrderNo") + 1]

            # Pull the name
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender Type
            gender_type = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Get the Parent's names/relationship && purpose
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None


            # Number of Copies
            additional_copy = clients_data_list[clients_data_list.index("ADDITIONAL_COPY") + 1]

            # Pull the Date(M/D/Y)
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None

            # Indivdual Info
            birth_place = clients_data_list[
                clients_data_list.index("BIRTH_PLACE") + 1] if "BIRTH_PLACE" in clients_data_list else None
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

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

        # Insert into the MarriageSearch table
        if client_id == '10000104':

            # Pull the Groom & Bride info
            groom_last_name = clients_data_list[clients_data_list.index("LASTNAME_G") + 1]
            groom_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_G") + 1] if "FIRSTNAME_G" in clients_data_list else None

            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "FIRSTNAME_B" in clients_data_list else None

            # Realtionship + the purpose
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Amount of copies requested
            copy_req = clients_data_list[clients_data_list.index("COPY_REQ") + 1]

            # Get the Date
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None

            # Pull the info about the Marriage location
            marriage_place = clients_data_list[
                clients_data_list.index("MARRIAGE_PLACE") + 1] if "MARRIAGE_PLACE" in clients_data_list else None

            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            insert_marriagesearch = MarriageSearch(groom_last_name=groom_last_name,
                                                   groom_first_name=groom_first_name,
                                                   bride_last_name=bride_last_name,
                                                   bride_first_name=bride_first_name,
                                                   relationship=relationship,
                                                   purpose=purpose,
                                                   copy_req=copy_req,
                                                   month=month,
                                                   day=day,
                                                   years=years,
                                                   marriage_place=marriage_place,
                                                   borough=borough,
                                                   letter=letter,
                                                   comment=comment,
                                                   sub_order_no=sub_order_no)

            print("Let add this to the marriagesearch table")
            db.session.add(insert_marriagesearch)
            db.session.commit()

        # Insert into the DeathSearch table
        if client_id == '10000103':

            # Pull the Name
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[clients_data_list.index("LASTNAME") + 1]
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # The relationship && purpose
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Amount of copies requested
            copy_req = clients_data_list[clients_data_list.index("COPY_REQ") + 1]

            # Cemetery they are in
            cemetery = clients_data_list[
                clients_data_list.index("CEMETERY") + 1] if "CEMETERY" in clients_data_list else None

            # Get the Date
            month = clients_data_list[clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR_") + 1] if "YEAR_" in clients_data_list else None

            # Death place and Age of Death
            death_place = clients_data_list[
                clients_data_list.index("DEATH_PLACE") + 1] if "DEATH_PLACE" in clients_data_list else None
            age_of_death = clients_data_list[
                clients_data_list.index("AGEOFDEATH") + 1] if "AGEOFDEATH" in clients_data_list else None

            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False
            # letter = clients_data_list[clients_data_list.find("LETTER") + 1]
            # if "LETTER" in clients_data_list else False

            insert_deathsearch = DeathSearch(last_name=last_name,
                                             first_name=first_name,
                                             mid_name=mid_name,
                                             relationship=relationship,
                                             purpose=purpose,
                                             copy_req=copy_req,
                                             cemetery=cemetery,
                                             month=month,
                                             day=day,
                                             years=years,
                                             death_place=death_place,
                                             age_of_death=age_of_death,
                                             borough=borough,
                                             letter=letter,
                                             comment=comment,
                                             sub_order_no=sub_order_no)

            print("Let add this to the deathsearch table")
            db.session.add(insert_deathsearch)
            db.session.commit()

        # Birth Cert
        if client_id == '10000147':

            # Get the Certificate No
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Pull the name
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # Pull the gender Type
            gender_type = clients_data_list[
                clients_data_list.index("GENDER") + 1] if "GENDER" in clients_data_list else None

            # Get the Parent's names/relationship && purpose
            father_name = clients_data_list[
                clients_data_list.index("FATHER_NAME") + 1] if "FATHER_NAME" in clients_data_list else None
            mother_name = clients_data_list[
                clients_data_list.index("MOTHER_NAME") + 1] if "MOTHER_NAME" in clients_data_list else None
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Number of Copies
            additional_copy = clients_data_list[
                clients_data_list.index("ADDITIONAL_COPY") + 1] if "ADDITIONAL_COPY" in clients_data_list else None

            # Pull the Date(M/D/Y)
            month = clients_data_list[
                clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR1") + 1] if "YEAR1" in clients_data_list else None

            # Indivdual Info
            birth_place = clients_data_list[
                clients_data_list.index("BIRTH_PLACE") + 1] if "BIRTH_PLACE" in clients_data_list else None
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            insert_birthcert = BirthCertificate(certificate_no=certificate_no,
                                                first_name=first_name,
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

            print("Let add this to the birthcert table")
            db.session.add(insert_birthcert)
            db.session.commit()

        # Insert into the MarriageCert table
        if client_id == '10000181':

            # Get the Certificate No
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Pull the Groom & Bride info
            groom_last_name = clients_data_list[
                clients_data_list.index("LASTNAME_G") + 1] if "LASTNAME_G" in clients_data_list else None
            groom_first_name = clients_data_list[clients_data_list.index("FIRSTNAME_G") + 1]

            bride_last_name = clients_data_list[clients_data_list.index("LASTNAME_B") + 1]
            bride_first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME_B") + 1] if "LASTNAME_B" in clients_data_list else None

            # Realtionship + the purpose
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Amount of copies requested
            copy_req = clients_data_list[clients_data_list.index("COPY_REQ") + 1]

            # Get the Date
            month = clients_data_list[
                clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[clients_data_list.index("YEAR") + 1] if "YEAR" in clients_data_list else None

            # Pull the info about the Marriage location
            marriage_place = clients_data_list[
                clients_data_list.index("MARRIAGE_PLACE") + 1] if "MARRIAGE_PLACE" in clients_data_list else None

            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False

            insert_marriagecert = MarriageCertificate(certificate_no=certificate_no,
                                                      groom_last_name=groom_last_name,
                                                      groom_first_name=groom_first_name,
                                                      bride_last_name=bride_last_name,
                                                      bride_first_name=bride_first_name,
                                                      relationship=relationship,
                                                      purpose=purpose,
                                                      copy_req=copy_req,
                                                      month=month,
                                                      day=day,
                                                      years=years,
                                                      marriage_place=marriage_place,
                                                      borough=borough,
                                                      letter=letter,
                                                      comment=comment,
                                                      sub_order_no=sub_order_no)

            print("Let add this to the marriagecert table")
            db.session.add(insert_marriagecert)
            db.session.commit()

        # Insert into the DeathCert table
        if client_id == '10000182':

            # Get the Certificate No
            certificate_no = clients_data_list[clients_data_list.index("CERTIFICATE_NUMBER") + 1]

            # Pull the Name
            first_name = clients_data_list[
                clients_data_list.index("FIRSTNAME") + 1] if "FIRSTNAME" in clients_data_list else None
            last_name = clients_data_list[
                clients_data_list.index("LASTNAME") + 1] if "LASTNAME" in clients_data_list else None
            mid_name = clients_data_list[
                clients_data_list.index("MIDDLENAME") + 1] if "MIDDLENAME" in clients_data_list else None

            # The relationship && purpose
            relationship = clients_data_list[
                clients_data_list.index("RELATIONSHIP") + 1] if "RELATIONSHIP" in clients_data_list else None
            purpose = clients_data_list[
                clients_data_list.index("PURPOSE") + 1] if "PURPOSE" in clients_data_list else None

            # Amount of copies requested
            copy_req = clients_data_list[clients_data_list.index("COPY_REQ") + 1]

            # Cemetery they are in
            cemetery = clients_data_list[
                clients_data_list.index("CEMETERY") + 1] if "CEMETERY" in clients_data_list else None

            # Get the Date
            month = clients_data_list[
                clients_data_list.index("MONTH") + 1] if "MONTH" in clients_data_list else None
            day = clients_data_list[
                clients_data_list.index("DAY") + 1] if "DAY" in clients_data_list else None
            years = clients_data_list[
                clients_data_list.index("YEAR") + 1] if "YEAR" in clients_data_list else None

            # Death place and Age of Death
            death_place = clients_data_list[
                clients_data_list.index("DEATH_PLACE") + 1] if "DEATH_PLACE" in clients_data_list else None
            age_of_death = clients_data_list[
                clients_data_list.index("AGEOFDEATH") + 1] if "AGEOFDEATH" in clients_data_list else None

            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            # letter Generated
            if clients_data_list[clients_data_list.index("LETTER") + 1] if "LETTER" in clients_data_list else None:
                letter = True
            else:
                letter = False
            # letter = clients_data_list[clients_data_list.find("LETTER") + 1]
            # if "LETTER" in clients_data_list else False

            insert_deathcert = DeathCertificate(certificate_no=certificate_no,
                                                last_name=last_name,
                                                first_name=first_name,
                                                mid_name=mid_name,
                                                relationship=relationship,
                                                purpose=purpose,
                                                copy_req=copy_req,
                                                cemetery=cemetery,
                                                month=month,
                                                day=day,
                                                years=years,
                                                death_place=death_place,
                                                age_of_death=age_of_death,
                                                borough=borough,
                                                letter=letter,
                                                comment=comment,
                                                sub_order_no=sub_order_no)

            print("Let add this to the deathcert table")
            db.session.add(insert_deathcert)
            db.session.commit()

        # Insert into the PropCard table
        if client_id == '10000058':
            # Pull the address of the building
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None
            building_no = clients_data_list[clients_data_list.index("BUILDING_NO") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Get the description
            description = clients_data_list[clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in \
                                                                                           clients_data_list else None

            certified = clients_data_list[clients_data_list.index("CERTIFIED") + 1]

            # mailed/pickup
            if clients_data_list[
                    clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            contact_info = clients_data_list[
                clients_data_list.index("EMAIL") + 1] if "EMAIL" in clients_data_list else None

            insert_propcard = PropertyCard(borough=borough,
                                           block=block,
                                           lot=lot,
                                           building_no=building_no,
                                           street=street,
                                           description=description,
                                           certified=certified,
                                           mail_pickup=mail_pickup,
                                           contact_info=contact_info,
                                           sub_order_no=sub_order_no)

            print("Let add this to the propcard table")
            db.session.add(insert_propcard)
            db.session.commit()

        # Insert into the PhotoTax table
        if client_id == '10000048':

            collection = clients_data_list[clients_data_list.index("Collection") + 1]
            borough = clients_data_list[clients_data_list.index("BOROUGH") + 1]

            roll = clients_data_list[clients_data_list.index("ROLL") + 1] if "ROLL" in clients_data_list else None

            # Pull the address of the building
            block = clients_data_list[clients_data_list.index("BLOCK") + 1] if "BLOCK" in clients_data_list else None
            lot = clients_data_list[clients_data_list.index("LOT") + 1] if "LOT" in clients_data_list else None
            street_no = clients_data_list[clients_data_list.index("STREET_NUMBER") + 1]
            street = clients_data_list[clients_data_list.index("STREET") + 1]

            # Get the description
            description = clients_data_list[
                clients_data_list.index("DESCRIPTION") + 1] if "DESCRIPTION" in clients_data_list else None

            type = clients_data_list[clients_data_list.index("TYPE") + 1]
            size = clients_data_list[clients_data_list.index("SIZE") + 1] if "SIZE" in clients_data_list else None

            copies = clients_data_list[clients_data_list.index("COPIES") + 1]

            # mailed/pickup
            if clients_data_list[
                        clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            contact_no = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            comment = clients_data_list[
                clients_data_list.index("ADD_COMMENT") + 1] if "ADD_COMMENT" in clients_data_list else None

            insert_phototax = PhotoTax(borough=borough,
                                       collection=collection,
                                       roll=roll,
                                       block=block,
                                       lot=lot,
                                       street_no=street_no,
                                       street=street,
                                       description=description,
                                       type=type,
                                       size=size,
                                       copies=copies,
                                       mail_pickup=mail_pickup,
                                       contact_no=contact_no,
                                       comment=comment,
                                       sub_order_no=sub_order_no)

            print("Let add this to the phototax table")
            db.session.add(insert_phototax)
            db.session.commit()

        # Insert into the PhotoGallery table
        if client_id == '10000060':
            # Pull the info for photogallery
            image_id = clients_data_list[clients_data_list.index("IMAGE_IDENTIFIER") + 1]

            # Get the description
            description = clients_data_list[
                clients_data_list.index("IMAGE_DESCRIPTION") + 1]\
                if "IMAGE_DESCRIPTION" in clients_data_list else None
            additional_description = clients_data_list[
                clients_data_list.index("ADDITIONAL_DESCRIPTION") + 1]\
                if "ADDITIONAL_DESCRIPTION" in clients_data_list else None

            size = clients_data_list[clients_data_list.index("SIZE") + 1]
            copy = clients_data_list[clients_data_list.index("COPIES") + 1]

            # mailed/pickup
            if clients_data_list[
                        clients_data_list.index("MAIL_PICKUP") + 1] if "MAIL_PICKUP" in clients_data_list else None:
                mail_pickup = True
            else:
                mail_pickup = False

            contact_no = clients_data_list[
                clients_data_list.index("CONTACT_NUMBER") + 1] if "CONTACT_NUMBER" in clients_data_list else None

            # personal use agreement
            if clients_data_list[
                    clients_data_list.index("PERSONAL_USE_AGREEMENT") + 1] \
                    if "PERSONAL_USE_AGREEMENT" in clients_data_list else None:
                personal_use_agreement = True
            else:
                personal_use_agreement = False

            comment = clients_data_list[
                clients_data_list.index("COMMENTS") + 1] if "COMMENTS" in clients_data_list else None

            insert_photogallery = PhotoGallery(image_id=image_id,
                                               description=description,
                                               additional_description=additional_description,
                                               size=size,
                                               copy=copy,
                                               mail_pickup=mail_pickup,
                                               contact_no=contact_no,
                                               personal_use_agreement=personal_use_agreement,
                                               comment=comment,
                                               sub_order_no=sub_order_no)

            print("Let add this to the photogallery table")
            db.session.add(insert_photogallery)
            db.session.commit()

    return True

