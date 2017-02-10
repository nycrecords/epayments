import os
import paramiko
import xml.etree.ElementTree as ET
import datetime
from datetime import date
from flask import url_for, current_app
from app import db
from app.models import Order
from contextlib import contextmanager


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


@contextmanager
def sftp_ctx():
    """
    Context manager that provides an SFTP client object
    (an SFTP session across an open SSH Transport)
    """
    transport = paramiko.Transport(('localhost', 22))
    transport.connect(username='btang', pkey=paramiko.RSAKey(filename='/Users/btang/.ssh/id_rsa'))
    # transport = paramiko.Transport((os.environ.get('SFTP_HOSTNAME'), os.environ.get('SFTP_PORT')))
    # transport.connect(username=os.environ.get('SFTP_USERNAME'),
    #               pkey=paramiko.RSAKey(filename=os.environ.get('SFTP_RSA_KEY_FILE')))
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        yield sftp
    except Exception as e:
        current_app.logger.error("Exception occurred with SFTP: {}".format(e))
    finally:
        sftp.close()
        transport.close()


def import_single_xml():
    # with sftp_ctx() as sftp:
    #     sftp.get('/Users/btang/Desktop/test1.pdf', '/Users/btang/Desktop/test1downloaded.pdf')
    #     sftp.close()

    file = 'DOR20161103_125347_CPY100017228.xml'  # Change file path

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


def import_xml_folder():
    xml_folder = '/Users/btang/Downloads/data/files/DOR'  # Change folder path

    # Initalize client_agency_name_dict and ordertypelist
    client_agency_name_dict = {"10000048": "Photo Tax", "10000060": "Photo Gallery", "10000102": "Birth Search",
                               "10000147": "Birth Cert", "10000104": "Marriage Search", "10000181": "Marriage Cert",
                               "10000103": "Death Search", "10000182": "Death Cert"}
    ordertypelist = ['tax photo', 'online gallery', 'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert',
                     'Death search', 'Death cert']

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
        datereceived = date.today()
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
