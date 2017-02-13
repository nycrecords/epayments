import os
import xml.etree.ElementTree as ET
import datetime
import time
from datetime import date, timedelta
from flask import url_for
from app import db, scheduler
from app.models import Order
from app.file_utils import sftp_ctx


def create_object(obj):
    """
    :param obj: Object class being created in database
    :return: Adding and committing object to database
    """
    try:
        db.session.add(obj)
        db.session.commit()
        return str(obj)
    except Exception as e:
        return None


def import_xml_folder():
    """
    Function is called from scheduler at 3AM everyday.
    Downloads all xml files from a remote folder to local folder.
    Imports xml files from local folder to database.
    """
    with scheduler.app.app_context():
        # Create new folder with date of download and download all files
        filepath = '/Users/btang/Desktop/data/files/DOR/'
        localpath = '/Users/btang/Desktop/all_data/'
        with sftp_ctx() as sftp:
            new_folder = localpath + 'DOR-' + time.strftime("%m-%d-%Y") + '/'
            if not os.path.isdir(new_folder):
                sftp.mkdir(new_folder)
                print("SFTP Created Directory: " + new_folder)
            for file in os.listdir(filepath):
                if os.path.isfile(os.path.join(filepath, file)) and not os.path.exists(os.path.join(new_folder, file)):
                    sftp.get(os.path.join(filepath, file), os.path.join(new_folder, file))
                    print("SFTP Transferred File: " + file)
            sftp.close()

        xml_folder = localpath + 'DOR-' + time.strftime("%m-%d-%Y") + '/'

        # Initalize client_agency_name_dict and ordertypelist
        client_agency_name_dict = {"10000048": "Photo Tax", "10000060": "Photo Gallery", "10000102": "Birth Search",
                                   "10000147": "Birth Cert", "10000104": "Marriage Search", "10000181": "Marriage Cert",
                                   "10000103": "Death Search", "10000182": "Death Cert"}
        ordertypelist = ['tax photo', 'online gallery', 'Birth search', 'Birth cert', 'Marriage search',
                         'Marriage cert', 'Death search', 'Death cert']

        # Parse files in XML folder
        for file in os.listdir(xml_folder):
            tree = ET.parse(xml_folder + file)
            root = tree.getroot()

            # Elements involving ClientsData
            clientsdatalist = (root.find('ClientsData').text).split('|')
            clientid = clientsdatalist[clientsdatalist.index("ClientID") + 1]
            clientagencyname = client_agency_name_dict[clientid]
            customeremail = root.find("EPaymentReq").find("CustomerEmail").text

            orderno = root.find("EPaymentReq").find("OrderNo").text
            if "CPY" in orderno:
                orderno = orderno.strip('CPY')
            suborderno = clientsdatalist[clientsdatalist.index("OrderNo") + 1]
            # suborderno = clientsdatalist[clientsdatalist.index("OrderNo") + 1] + orderno[:5]

            ordertypes = []
            itemdescription = root.findall(".//ItemDescription")
            for item in itemdescription:
                for ordertype in ordertypelist:
                    if ordertype in item.text:
                        ordertypes.append(ordertype)
            ordertypes = ','.join(ordertypes)

            clientsdata = root.find('ClientsData').text
            billingname = root.find("EPaymentRes").find("BillingInfo").find("BillingName").text
            confirmationmessage = root.find('ConfirmationMessage').text
            datereceived = date.today() - timedelta(1)
            datelastmodified = datetime.datetime.fromtimestamp(
                os.path.getmtime(xml_folder + file)).strftime('%Y-%m-%d %H:%M:%S')

            # Elements in ShippingAdd Root
            shipping_add = root.find("EPaymentRes").find("ShippingAdd")
            shiptoname = shipping_add.find("ShipToName").text
            shiptostreetadd = shipping_add.find("ShipToStreetAdd").text
            shiptostreetadd2 = shipping_add.find("ShipToStreetAdd2").text
            shiptocity = shipping_add.find("ShipToCity").text
            shiptostate = shipping_add.find("ShipToState").text
            shiptozipcode = shipping_add.find("ShipToZipCode").text
            shiptocountry = shipping_add.find("ShipToCountry").text
            shiptophone = shipping_add.find("ShipToPhone").text
            shippinginstructions = shipping_add.find("ShippingInstructions").text

            # Check for duplicate in database
            duplicate = Order.query.filter_by(orderno=orderno).first()

            # Insert into database if duplicate doesn't exist, else print message
            if not duplicate:
                insert_order = Order(orderno=orderno, clientagencyname=clientagencyname, shiptoname=shiptoname,
                                     shiptostreetadd=shiptostreetadd, shiptostreetadd2=shiptostreetadd2,
                                     shiptocity=shiptocity, shiptostate=shiptostate, shiptozipcode=shiptozipcode,
                                     shiptocountry=shiptocountry, shiptophone=shiptophone, customeremail=customeremail,
                                     shippinginstructions=shippinginstructions, clientsdata=clientsdata,
                                     confirmationmessage=confirmationmessage, datereceived=datereceived,
                                     billingname=billingname, datelastmodified=datelastmodified, suborderno=suborderno,
                                     clientid=clientid, ordertypes=ordertypes)
                db.session.add(insert_order)
                db.session.commit()

                print("Added order " + str(orderno) + " into database.")

            else:
                print("Order %s already exists in the database." % orderno)


def import_missing_xml():
    """
    Function called to import a missing xml file.
    Variables folder_date and file must be changed according to the missing xml file.

    Downloads a single missing xml file from a remote folder to local dated folder.
    Imports single xml file from local folder to database.
    """
    # Input date of folder and missing xml file name to insert missing xml file into database
    filepath = '/Users/btang/Desktop/data/files/DOR/'
    localpath = '/Users/btang/Desktop/all_data/'
    with sftp_ctx() as sftp:
        folder_date = time.strftime("%m-%d-%Y")  # Change date accordingly
        folder = localpath + 'DOR-' + folder_date + '/'
        file = 'DOR20161103_125347_CPY100017228.xml'  # Change missing xml filename accordingly
        if os.path.isfile(os.path.join(filepath, file)):
            sftp.get(os.path.join(filepath, file), os.path.join(folder, file))
        sftp.close()

    # Initalize client_agency_name_dict and ordertypelist
    clientagencynamedict = {"10000048": "Photo Tax", "10000060": "Photo Gallery", "10000102": "Birth Search",
                            "10000147": "Birth Cert", "10000104": "Marriage Search", "10000181": "Marriage Cert",
                            "10000103": "Death Search", "10000182": "Death Cert"}
    ordertypelist = ['Photo tax', 'Photo gallery', 'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert',
                     'Death search', 'Death cert']

    # Parse XML file
    tree = ET.parse(file)
    root = tree.getroot()

    # Elements involving ClientsData
    clientsdatalist = (root.find('ClientsData').text).split('|')
    clientid = clientsdatalist[clientsdatalist.index("ClientID") + 1]
    clientagencyname = clientagencynamedict[clientid]
    customeremail = root.find("EPaymentReq").find("CustomerEmail").text

    orderno = root.find("EPaymentReq").find("OrderNo").text
    if "CPY" in orderno:
        orderno = orderno.strip('CPY')
    suborderno = clientsdatalist[clientsdatalist.index("OrderNo") + 1]
    # suborderno = clientsdatalist[clientsdatalist.index("OrderNo") + 1] + orderno[:5]

    ordertypes = []
    itemdescription = root.findall(".//ItemDescription")
    for item in itemdescription:
        for ordertype in ordertypelist:
            if ordertype in item.text:
                ordertypes.append(ordertype)
    ordertypes = ','.join(ordertypes)

    clientsdata = root.find('ClientsData').text
    billingname = root.find("EPaymentRes").find("BillingInfo").find("BillingName").text
    confirmationmessage = root.find('ConfirmationMessage').text
    datereceived = date.today()
    datelastmodified = datetime.datetime.fromtimestamp(os.path.getmtime(file))

    # Elements in ShippingAdd Root
    shipping_add = root.find("EPaymentRes").find("ShippingAdd")
    shiptoname = shipping_add.find("ShipToName").text
    shiptostreetadd = shipping_add.find("ShipToStreetAdd").text
    shiptostreetadd2 = shipping_add.find("ShipToStreetAdd2").text
    shiptocity = shipping_add.find("ShipToCity").text
    shiptostate = shipping_add.find("ShipToState").text
    shiptozipcode = shipping_add.find("ShipToZipCode").text
    shiptocountry = shipping_add.find("ShipToCountry").text
    shiptophone = shipping_add.find("ShipToPhone").text
    shippinginstructions = shipping_add.find("ShippingInstructions").text

    # Check for duplicate in database
    duplicate = Order.query.filter_by(orderno=orderno).first()

    # Insert into database if duplicate doesn't exist, else print message
    if not duplicate:
        insert_order = Order(orderno=orderno, clientagencyname=clientagencyname, shiptoname=shiptoname,
                             shiptostreetadd=shiptostreetadd, shiptostreetadd2=shiptostreetadd2, shiptocity=shiptocity,
                             shiptostate=shiptostate, shiptozipcode=shiptozipcode, shiptocountry=shiptocountry,
                             shiptophone=shiptophone, customeremail=customeremail,
                             shippinginstructions=shippinginstructions, clientsdata=clientsdata,
                             confirmationmessage=confirmationmessage, datereceived=datereceived,
                             billingname=billingname, datelastmodified=datelastmodified, suborderno=suborderno,
                             clientid=clientid, ordertypes=ordertypes)
        db.session.add(insert_order)
        db.session.commit()

    else:
        print("Order %s already exists in the database." % orderno)


def make_public_order(order):
    """
    Create a JSON object with URI that references a specific order.

    :param order: order as a JSON object
    :return: JSON object
    """
    new_order = {}
    for field in order:
        if field == 'SubOrderNo':
            new_order['uri'] = url_for(
                'api_1_0.get_order',
                order_id=order['SubOrderNo'],
                _external=True
            )
        else:
            new_order[field] = order[field]

    return new_order
