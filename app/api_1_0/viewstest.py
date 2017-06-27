import datetime
from datetime import date, timedelta
from app.constants.client_agency_names import CLIENT_AGENCY_NAMES

from app.models import StatusTracker, Orders
from app import db

comment = "The Record is Done."
new_status = 'Done'
sub_order_no = 9128144811


def update_status(sub_order_no, comment, new_status):
    """
        POST: {sub_order_no, new_status, comment};
        returns: {status_id, sub_order_no, status, comment}, 201

    Take in the info, this function only gets called if the form is filled
     - access the db to get the status_id for this particular order
     - now create a new row in the db in the status table with
     - this row should have a status_id + 1 then the highest status row
     - 1) it will have the same sub_order_no
     - 2) it will have the comment that was passed in or None
     - 3) it will have the new status that was passed from the user
    """

    # session = StatusTracker.query.filter_by(sub_order_no=sub_order_no).first_or_404()

    insert_status = StatusTracker(sub_order_no=sub_order_no)

    db.session.add(insert_status)
    db.session.commit()





# update_status(sub_order_no, comment, new_status)


# def get_orders_by_fields_dict(order_number, suborder_number, order_type, billing_name, user, date_received,
#                               date_submitted):
#     """
#     TEST FUNCTION - manually put in a few orders
#     Filter orders by fields received
#     :return:
#     """
#
#     orders = [
#
#
#         {
#             "billingname": "Jeffrey Kobacker",
#             "clientagencyname": "Death Search",
#             "clientdata": "ClientID|10000103|ClientAgencyName|Department of Record|OrderNo|9127848504|LASTNAME|Bloch|FIRSTNAME|Isaac|MIDDLENAME|S|RELATIONSHIP|Great Grandson|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|7|DEATH_PLACE|Manhattan, New York|AGEOFDEATH|78|YEAR_|1918,|BOROUGH|MANHATTAN,|",
#             "clientid": 10000103,
#             "confirmationmessage": "\nLast name:               Bloch\nFirst name:              Isaac\nMiddle name:             S\n\nMonth:                   December\nDay:                     7\nYear:                    1918\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          Manhattan, New York\nAge at Death:            78\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Great Grandson\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "jkobacker@gmail.com",
#             "datereceived": "2017-04-04 04:06:15",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592000",
#             "suborderno": 9127848504
#         },
#         {
#             "billingname": "Christina Rubino",
#             "clientagencyname": "Marriage Cert",
#             "clientdata": "ClientID|10000181|ClientAgencyName|Department of Record|OrderNo|9128144811|LASTNAME_G|O'toole|FIRSTNAME_G|Joseph|LASTNAME_B|Burke|FIRSTNAME_B|Mary|RELATIONSHIP|Grand Daughter|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|November|DAY|13|YEAR|1926|MARRIAGE_PLACE|Brooklyn|CERTIFICATE_NUMBER|16581|BOROUGH|BROOKLYN|",
#             "clientid": 10000181,
#             "confirmationmessage": "\nGroom's last name:       O'toole\nGroom's first name:      Joseph\nBride's last name:       Burke\nBride's first name:      Mary\n\nMonth:                   November\nDay:                     13\nYear:                    1926\n\nPlace of Marriage:       Brooklyn\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand Daughter\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      16581\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "pettycoat4@aol.com",
#             "datereceived": "2017-04-04 04:54:15",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592026",
#             "suborderno": 9128144811
#         },
#         {
#             "billingname": "Jeremy Kamen",
#             "clientagencyname": "Marriage Cert",
#             "clientdata": "ClientID|10000181|ClientAgencyName|Department of Record|OrderNo|9128113134|LASTNAME_G|Squillante|FIRSTNAME_G|Sabato|LASTNAME_B|Donnadio|FIRSTNAME_B|Madelina|RELATIONSHIP|Great, Great Grandson|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|January|DAY|10|YEAR|1898|MARRIAGE_PLACE|New York|CERTIFICATE_NUMBER|800|BOROUGH|MANHATTAN|",
#             "clientid": 10000181,
#             "confirmationmessage": "\nGroom's last name:       Squillante\nGroom's first name:      Sabato\nBride's last name:       Donnadio\nBride's first name:      Madelina\n\nMonth:                   January\nDay:                     10\nYear:                    1898\n\nPlace of Marriage:       New York\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Great, Great Grandson\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      800\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "jeremykamen@gmail.com",
#             "datereceived": "2017-04-04 05:05:15",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592023",
#             "suborderno": 9128113134
#         },
#         {
#             "billingname": "Megan Carver",
#             "clientagencyname": "Death Cert",
#             "clientdata": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9128624422|LASTNAME|Meurtz (Meury)|FIRSTNAME|Rosa|RELATIONSHIP|great-great-grandchild|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|November|DAY|18|YEAR|1899|DEATH_PLACE|Brooklyn, Kings, NY, USA|AGEOFDEATH|59|CERTIFICATE_NUMBER|19381|BOROUGH|BROOKLYN|",
#             "clientid": 10000182,
#             "confirmationmessage": "\nLast name:               Meurtz (Meury)\nFirst name:              Rosa\nMiddle name:             (Left Blank)\n\nMonth:                   November\nDay:                     18\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          Brooklyn, Kings, NY, USA\n\nAge at Death:            59\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  great-great-grandchild\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      19381\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "mbrucecarver@gmail.com",
#             "datereceived": "2017-04-04 06:15:15",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592055",
#             "suborderno": 9128624422
#         },
#         {
#             "billingname": "Francine  Hardin ",
#             "clientagencyname": "Marriage Cert",
#             "clientdata": "ClientID|10000181|ClientAgencyName|Department of Record|OrderNo|9128776248|LASTNAME_G|Benedict |FIRSTNAME_G|Charles|LASTNAME_B|Kline|FIRSTNAME_B|Julia|RELATIONSHIP|Great Grandparents |PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|August|DAY|3|YEAR|1898|CERTIFICATE_NUMBER|12418|BOROUGH|MANHATTAN|",
#             "clientid": 10000181,
#             "confirmationmessage": "\nGroom's last name:       Benedict \nGroom's first name:      Charles\nBride's last name:       Kline\nBride's first name:      Julia\n\nMonth:                   August\nDay:                     3\nYear:                    1898\n\nPlace of Marriage:       (Left Blank)\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Great Grandparents \nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      12418\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "fabfran63@yahoo.com",
#             "datereceived": "2017-04-04 06:43:14",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592058",
#             "suborderno": 9128776248
#         },
#         {
#             "billingname": "Michael Rafter",
#             "clientagencyname": "Marriage Cert",
#             "clientdata": "ClientID|10000181|ClientAgencyName|Department of Record|OrderNo|9130050681|LASTNAME_G|Rafter|FIRSTNAME_G|William|LASTNAME_B|Whalen|FIRSTNAME_B|Catherine|RELATIONSHIP|gt nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|August|DAY|12|YEAR|1929|CERTIFICATE_NUMBER|21296|BOROUGH|MANHATTAN|",
#             "clientid": 10000181,
#             "confirmationmessage": "\nGroom's last name:       Rafter\nGroom's first name:      William\nBride's last name:       Whalen\nBride's first name:      Catherine\n\nMonth:                   August\nDay:                     12\nYear:                    1929\n\nPlace of Marriage:       (Left Blank)\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  gt nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      21296\n\n--------------------------------------------------------------------------------\n\n",
#             "customeremail": "mrafter719@aol.com",
#             "datereceived": "2017-04-04 10:15:14",
#             "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
#             "orderno": "000592086",
#             "suborderno": 9130050681
#         }
#
#     ]
#
#     yesterday = date.today() - timedelta(1)
#     if len(date_received) < 1:
#         date_received = yesterday
#     else:
#         date_received = datetime.datetime.strptime(date_received, "%Y-%m-%d %H:%M:%S").date()
#     if len(date_submitted) < 1:
#         date_submitted = yesterday
#     else:
#         date_submitted = datetime.datetime.strptime(date_submitted, "%Y-%m-%d %H:%M:%S").date()
#     orders = [order for order in orders if date_received <= datetime.datetime.strptime(order['datereceived'],
#               "%Y-%m-%d %H:%M:%S").date() <= date_submitted]
#     if len(order_number) != 0:
#         orders = [order for order in orders if order['clientid'] == int(order_type)]
#     if len(suborder_number) != 0:
#         orders = [order for order in orders if order['suborderno'] == int(suborder_number)]
#     if len(order_type) != 4 and order_type != 'All' and order_type != 'multitems':
#         # orders = [order for order in orders if order['clientagencyname'] == order_type]
#         orders = [order for order in orders if order['clientagencyname'] == CLIENT_AGENCY_NAMES[order_type]]
#     if len(billing_name) != 0:
#         orders = [order for order in orders if billing_name.lower() in order['billingname'].lower()]
#
#     print ("Hello")
#     print (date_received)
#     print (date_submitted)
#     print (orders)
#     return orders
#
#
# get_orders_by_fields_dict("000592086", '9130050681', '10000181', "Michael Rafter", 0, "2017-04-04 10:15:14",
#                           "2017-06-13 00:00:00")
