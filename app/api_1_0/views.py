from flask import jsonify, abort, request
import datetime
from datetime import date, datetime, timedelta
from sqlalchemy import func
from . import api_1_0 as api
from ..models import Order
from ..utils import make_public_order


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['POST', 'GET'])
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with the previous day's date.
    """
    # orders = [
    #     {
    #         "OrderNo": 9046420448,
    #         "ClientAgencyName": "Death Cert",
    #         "ShipToName": "Mark Reichard",
    #         "ShipToStreetAdd": "23307 Los Codona Ave.",
    #         "ShipToStreetAdd2": "",
    #         "ShipToCity": "Torrance",
    #         "ShipToState": "CA",
    #         "ShipToZipCode": "90505",
    #         "ShipToCountry": "USA",
    #         "ShipToPhone": "310-710-0413",
    #         "CustomerEmail": "mreichard@socal.rr.com",
    #         "ShippingInstructions": "",
    #         "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046401977|LASTNAME|Reichard|FIRSTNAME|Sarah|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|September|DAY|16|YEAR|1899|ADD_COMMENT| Born abt. 1899.  Trying to establish relationship|CERTIFICATE_NUMBER|26473|BOROUGH|MANHATTAN,",
    #         "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    #         "DateReceived": "2016-12-24 00:00:00",
    #         "BillingName": "Mark Reichard",
    #         "DateLastModified": "12/25/2016 3:10:21 AM",
    #         "SubOrderNo": 9046401977,
    #         "ClientID": "10000182"
    #     },
    #     {
    #         "OrderNo": 9046420448,
    #         "ClientAgencyName": "Death Cert",
    #         "ShipToName": "Mark Reichard",
    #         "ShipToStreetAdd": "23307 Los Codona Ave.",
    #         "ShipToStreetAdd2": "",
    #         "ShipToCity": "Torrance",
    #         "ShipToState": "CA",
    #         "ShipToZipCode": "90505",
    #         "ShipToCountry": "USA",
    #         "ShipToPhone": "310-710-0413",
    #         "CustomerEmail": "mreichard@socal.rr.com",
    #         "ShippingInstructions": "",
    #         "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046401977|LASTNAME|Reichard|FIRSTNAME|Sarah|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|September|DAY|16|YEAR|1899|ADD_COMMENT| Born abt. 1899.  Trying to establish relationship|CERTIFICATE_NUMBER|26473|BOROUGH|MANHATTAN,",
    #         "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    #         "DateReceived": "2017-01-03 00:00:00",
    #         "BillingName": "Michael Reichard",
    #         "DateLastModified": "12/25/2016 3:10:21 AM",
    #         "SubOrderNo": 9046401973,
    #         "ClientID": "10000182"
    #     },
    #     {
    #         "OrderNo": 9046420447,
    #         "ClientAgencyName": "Death Search",
    #         "ShipToName": "Mark Reichard",
    #         "ShipToStreetAdd": "23307 Los Codona Ave.",
    #         "ShipToStreetAdd2": "",
    #         "ShipToCity": "Torrance",
    #         "ShipToState": "CA",
    #         "ShipToZipCode": "90505",
    #         "ShipToCountry": "USA",
    #         "ShipToPhone": "310-710-0413",
    #         "CustomerEmail": "mreichard@socal.rr.com",
    #         "ShippingInstructions": "",
    #         "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046401977|LASTNAME|Reichard|FIRSTNAME|Sarah|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|September|DAY|16|YEAR|1899|ADD_COMMENT| Born abt. 1899.  Trying to establish relationship|CERTIFICATE_NUMBER|26473|BOROUGH|MANHATTAN,",
    #         "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    #         "DateReceived": "2016-12-09 00:00:00",
    #         "BillingName": "Mark Reichard",
    #         "DateLastModified": "11/23/2016 3:10:21 AM",
    #         "SubOrderNo": 9046401974,
    #         "ClientID": "10000182"
    #     },
    #     {
    #         "OrderNo": 9046420447,
    #         "ClientAgencyName": "Birth Search",
    #         "ShipToName": "Mark Reichard",
    #         "ShipToStreetAdd": "23307 Los Codona Ave.",
    #         "ShipToStreetAdd2": "",
    #         "ShipToCity": "Torrance",
    #         "ShipToState": "CA",
    #         "ShipToZipCode": "90505",
    #         "ShipToCountry": "USA",
    #         "ShipToPhone": "310-710-0413",
    #         "CustomerEmail": "mreichard@socal.rr.com",
    #         "ShippingInstructions": "",
    #         "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046415827|LASTNAME|Reichard|FIRSTNAME|Hugo|MIDDLENAME|G.|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|31|YEAR|1898|ADD_COMMENT| born abt. 1898.  Trying to establish relationship.|CERTIFICATE_NUMBER|25|BOROUGH|BROOKLYN,|",
    #         "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    #         "DateReceived": "2016-12-09 00:00:00",
    #         "BillingName": "Matt Bomer",
    #         "DateLastModified": "12/25/2016 3:10:21 AM",
    #         "SubOrderNo": 9046415563,
    #         "ClientID": "10000182"
    #     },
    #     {
    #         "OrderNo": 9046420447,
    #         "ClientAgencyName": "Birth Search",
    #         "ShipToName": "Mark Reichard",
    #         "ShipToStreetAdd": "23307 Los Codona Ave.",
    #         "ShipToStreetAdd2": "",
    #         "ShipToCity": "Torrance",
    #         "ShipToState": "CA",
    #         "ShipToZipCode": "90505",
    #         "ShipToCountry": "USA",
    #         "ShipToPhone": "310-710-0413",
    #         "CustomerEmail": "mreichard@socal.rr.com",
    #         "ShippingInstructions": "",
    #         "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046415827|LASTNAME|Reichard|FIRSTNAME|Hugo|MIDDLENAME|G.|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|31|YEAR|1898|ADD_COMMENT| born abt. 1898.  Trying to establish relationship.|CERTIFICATE_NUMBER|25|BOROUGH|BROOKLYN,|",
    #         "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    #         "DateReceived": "2016-12-09 00:00:00",
    #         "BillingName": "Bob Stewart",
    #         "DateLastModified": "12/25/2016 3:10:21 AM",
    #         "SubOrderNo": 9046415827,
    #         "ClientID": "10000182"
    #     }
    # ]
    if request.form:
        order_number = str(request.form["order_number"])
        suborder_number = str(request.form["suborder_number"])
        order_type = request.form["order_type"]
        billing_name = str(request.form["billing_name"])
        date_received_start = request.form["date_received_start"]
        date_received_end = request.form["date_received_end"]
        # orders = get_orders_by_fields_dict(orders, order_number, suborder_number, order_type, billing_name,
        #                                    date_received_start, date_received_end)
        orders = get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start,
                                      date_received_end)
        return jsonify(orders=orders)
    else:
        yesterday = datetime.strptime(date.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") - timedelta(4)
        orders = [order.serialize for order in Order.query.filter_by(datereceived=yesterday).all()]
        return jsonify(orders=orders)


def get_orders_by_fields_dict(orders, order_number, suborder_number, order_type, billing_name, date_received_start,
                              date_received_end):
    """Filters orders by fields received."""
    yesterday = date.today() - timedelta(1)
    if len(date_received_start) < 1:
        date_received_start = yesterday
    else:
        date_received_start = datetime.datetime.strptime(date_received_start, "%m/%d/%Y").date()
    if len(date_received_end) < 1:
        date_received_end = yesterday
    else:
        date_received_end = datetime.datetime.strptime(date_received_end, "%m/%d/%Y").date()
    orders = [order for order in orders if date_received_start <= datetime.datetime.strptime(order['DateReceived'],
                                                                                             "%Y-%m-%d %H:%M:%S").date() <= date_received_end]
    if len(order_number) != 0:
        orders = [order for order in orders if order['ClientID'] == order_number]
    if len(suborder_number) != 0:
        orders = [order for order in orders if order['SubOrderNo'] == int(suborder_number)]
    if len(order_type) != 4 and order_type != 'All' and order_type != 'multitems':
        orders = [order for order in orders if order['ClientAgencyName'] == order_type]
    if len(billing_name) != 0:
        orders = [order for order in orders if billing_name.lower() in order['BillingName'].lower()]
    return orders


def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start,
                         date_received_end):
    """Filters orders by fields received."""
    vitalrecordslist = {'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert', 'Death search', 'Death cert'}
    photolist = {'tax photo', 'online gallery'}
    yesterday = datetime.strptime(date.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") - timedelta(4)
    if len(date_received_start) < 1:
        date_received_start = yesterday
    if len(date_received_end) < 1:
        date_received_end = yesterday
    orders = Order.query.filter(Order.datereceived >= date_received_start, Order.datereceived <= date_received_end)
    if len(order_number) != 0:
        orders = orders.filter(Order.clientid == order_number)
    if len(suborder_number) != 0:
        orders = orders.filter(Order.suborderno == suborder_number)
    if len(billing_name) != 0:
        orders = orders.filter(func.lower(Order.billingname).contains(func.lower(billing_name)))
    if len(order_type) != 4 and order_type not in ['All', 'multipleitems', 'vitalrecordsphotos']:
        orders = orders.filter(Order.clientagencyname == order_type)
    elif order_type == 'multipleitems':
        orders = [order for order in orders if len(order.ordertypes.split(',')) > 1]
    elif order_type == 'vitalrecordsphotos':
        orders = [order for order in orders if
                  not set(order.ordertypes.split(',')).isdisjoint(vitalrecordslist) and not set(order.ordertypes.split(
                      ',')).isdisjoint(photolist)]
    order_list = [order.serialize for order in orders]
    return order_list


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    orders = [order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    if len(orders) == 0:
        abort(404)
    return jsonify(orders)
