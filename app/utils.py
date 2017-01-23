import os
import psycopg2
import xml.etree.ElementTree as ET
import datetime
from datetime import date
from flask import url_for


def import_single_xml(file):
    # file = 'DOR20161103_125347_CPY100017228.xml'

    # Connect to database
    conn = psycopg2.connect(host='localhost', port=5432, database='epayments', user='btang')
    # conn = psycopg2.connect(host='ec2-184-72-252-69.compute-1.amazonaws.com', port=5432, database='dabs0ok19r3gri',
    #                         user='zxyjbtckhwfmtr',
    #                         password='4d7038760d0279aa2a7f172852076da1a670f8ed8b088b303bf4781e3f23fd08')
    cursor = conn.cursor()

    # Parse XML file
    clientagencynamedict = {"10000048": "Photo Tax", "10000060": "Photo Gallery", "10000102": "Birth Search",
                            "10000147": "Birth Cert", "10000104": "Marriage Search", "10000181": "Marriage Cert",
                            "10000103": "Death Search", "10000182": "Death Cert"}
    ordertypelist = ['Photo tax', 'Photo gallery', 'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert',
                     'Death search', 'Death cert']

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
    datelastmodified = datetime.datetime.fromtimestamp(
        os.path.getmtime('/Users/btang/Downloads/data/files/DOR/' + file))

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
    check_duplicate = 'SELECT "orderno" FROM "order" WHERE orderno = %s'
    cursor.execute(check_duplicate, (orderno,))
    duplicate = cursor.fetchone()

    # Insert into database if duplicate doesn't exist, else print message
    if not duplicate:
        insert_order = 'INSERT INTO "order" (orderno, clientagencyname, shiptoname, shiptostreetadd, ' \
                       'shiptostreetadd2, shiptocity, shiptostate, shiptozipcode, shiptocountry, shiptophone, ' \
                       'customeremail, shippinginstructions, clientsdata, confirmationmessage, datereceived, ' \
                       'billingname, datelastmodified, suborderno, clientid, ordertypes) VALUES (%s, %s, %s, %s, ' \
                       '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(insert_order, (
            orderno, clientagencyname, shiptoname, shiptostreetadd, shiptostreetadd2, shiptocity, shiptostate,
            shiptozipcode, shiptocountry, shiptophone, customeremail, shippinginstructions, clientsdata,
            confirmationmessage, datereceived, billingname, datelastmodified, suborderno, clientid, ordertypes))
    else:
        print("Order %s already exists in the database." % orderno)

    conn.commit()
    cursor.close()


def import_xml_folder(xml_folder):
    # xml_folder = '/Users/btang/Downloads/data/files/DOR'

    # Connect to database
    # conn = psycopg2.connect(host='localhost', port=5432, database='epayments', user='btang')
    conn = psycopg2.connect(host='ec2-184-72-252-69.compute-1.amazonaws.com', port=5432, database='dabs0ok19r3gri',
                            user='zxyjbtckhwfmtr',
                            password='4d7038760d0279aa2a7f172852076da1a670f8ed8b088b303bf4781e3f23fd08')
    cursor = conn.cursor()

    # Initalize xml folder and client_agency_name_dict
    client_agency_name_dict = {"10000048": "Photo Tax", "10000060": "Photo Gallery", "10000102": "Birth Search",
                               "10000147": "Birth Cert", "10000104": "Marriage Search", "10000181": "Marriage Cert",
                               "10000103": "Death Search", "10000182": "Death Cert"}
    ordertypelist = ['tax photo', 'online gallery', 'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert',
                     'Death search', 'Death cert']

    # Parse files in XML folder
    for file in os.listdir(xml_folder):
        tree = ET.parse('/Users/btang/Downloads/data/files/DOR/' + file)
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
            os.path.getmtime('/Users/btang/Downloads/data/files/DOR/' + file)).strftime('%Y-%m-%d %H:%M:%S')

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
        check_duplicate = 'SELECT "orderno" FROM "order" WHERE orderno = %s'
        cursor.execute(check_duplicate, (orderno,))
        duplicate = cursor.fetchone()

        # Insert into database if duplicate doesn't exist, else print message
        if not duplicate:
            insert_order = 'INSERT INTO "order" (orderno, clientagencyname, shiptoname, shiptostreetadd, ' \
                           'shiptostreetadd2, shiptocity, shiptostate, shiptozipcode, shiptocountry, shiptophone, ' \
                           'customeremail, shippinginstructions, clientsdata, confirmationmessage, datereceived, ' \
                           'billingname, datelastmodified, suborderno, clientid, ordertypes) VALUES (%s, %s, %s, ' \
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(insert_order, (
                orderno, clientagencyname, shiptoname, shiptostreetadd, shiptostreetadd2, shiptocity, shiptostate,
                shiptozipcode, shiptocountry, shiptophone, customeremail, shippinginstructions, clientsdata,
                confirmationmessage, datereceived, billingname, datelastmodified, suborderno, clientid, ordertypes))
        else:
            print("Order %s already exists in the database." % orderno)

    conn.commit()
    cursor.close()


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
