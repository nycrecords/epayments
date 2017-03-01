import os
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import current_app
from app import db, scheduler
from app.models import Order
from app.file_utils import sftp_ctx
from app.constants import (
    ORDER_TYPES,
    CLIENT_AGENCY_NAMES
)


def import_xml_folder(scheduled=False):
    """
    Function is called from scheduler at 3AM everyday.
    Downloads all xml files from a remote folder to local folder.
    Imports xml files from local folder to database.
    :param scheduled: Boolean determines whether this is running as a Cron job or manually
    """

    with scheduler.app.app_context():
        file_path = current_app.config['REMOTE_FILE_PATH']
        local_path = current_app.config['LOCAL_FILE_PATH']

        if scheduled:
            file_path = current_app.config['REMOTE_FILE_PATH']
            local_path = current_app.config['LOCAL_FILE_PATH']
            # Create new folder with date of download and download all files

            import_folder = os.path.join(local_path,
                                         'DOR-{date_time}/'.format(date_time=datetime.datetime.now().strftime('%m-%d-%Y_%H:%M')))

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
                file_ = os.path.join(local_path, file_)
                print("Imported {}".format(file_)) if import_file(file_) else print("Failed to Import {}".format(file_))
        else:
            for file_ in os.listdir(local_path):
                file_ = os.path.join(local_path, file_)
                print("Imported {}".format(file_)) if import_file(file_) else print("Failed to Import {}".format(file_))


def import_file(file_name):
    """
    Inserts a single order from an XML file into the database.
    :param file_name: XML file to import
    :return: Bool
    """
    # Populate XML Parser
    tree = ET.parse(file_name)
    root = tree.getroot()

    # Order Number: Specific order number for this Order
    order_no = root.find("EPaymentReq").find("OrderNo").text

    # Remove CPY header from DOF Payment Processing System
    if "CPY" in order_no:
        order_no = order_no.strip('CPY')

    # Check for duplicate in database
    duplicate = Order.query.filter_by(order_no=order_no).first()

    if duplicate:
        print("Order %s already exists in the database." % order_no)
        return False

    # Extract ClientsData - Information about the Order Type
    clients_data = root.find('ClientsData').text
    clients_data_list = clients_data.split('|')

    # Client ID: Order Type ID
    client_id = clients_data_list[clients_data_list.index("ClientID") + 1]

    # Client Agency Name: Order Type as String
    client_agency_name = CLIENT_AGENCY_NAMES[client_id]

    # Sub Order Number: Used to identify multi-part orders
    sub_order_no = clients_data_list[clients_data_list.index("OrderNo") + 1]

    # Determine if multiple items are requested as part of this order.
    order_types = []
    item_description = root.findall(".//ItemDescription")
    for item in item_description:
        for order_type in ORDER_TYPES:
            if order_type in item.text:
                order_types.append(order_type)
    order_types = ','.join(order_types)

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
    shipping_instructions = shipping_add.find("ShippingInstructions").text

    # Create Order in Database
    insert_order = Order(order_no=order_no,
                         client_agency_name=client_agency_name,
                         ship_to_name=ship_to_name,
                         ship_to_street_add=ship_to_street_add,
                         ship_to_street_add_2=ship_to_street_add_2,
                         ship_to_city=ship_to_city,
                         ship_to_state=ship_to_state,
                         ship_to_zipcode=ship_to_zipcode,
                         ship_to_country=ship_to_country,
                         ship_to_phone=ship_to_phone,
                         customer_email=customer_email,
                         shipping_instructions=shipping_instructions,
                         clients_data=clients_data,
                         confirmation_message=confirmation_message,
                         date_received=date_received,
                         billing_name=billing_name,
                         date_last_modified=date_last_modified,
                         sub_order_no=sub_order_no,
                         client_id=client_id,
                         order_types=order_types
                         )
    db.session.add(insert_order)
    db.session.commit()

    print("Added order " + str(order_no) + " into database.")
    return True
