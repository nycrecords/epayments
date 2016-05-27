import xmltodict
from datetime.datetime import now
from app import TYPE


def open_file(filename):
    """
    Opens a file
    :param filename: Name of the file to be opened (Full Path)
    :return: File object
    """

    with open(filename) as fd:
        return fd.read()


def parse_xml(filename):
    """
    Parses a single XML file
    :param filename: Name of XML file to be parsed (Full Path)
    :return: A dictionary of the relevant fields from the XML
    """

    # Convert the XML
    xml_file = open_file(filename)
    parsed = xmltodict.parse(xml_file)

    # Setup order dictionary
    order_info = {}
    order_info['order_number'] = parsed['EPayment']['EPaymentReq']['OrderNo']

    # Get Shipping Information - If Needed
    if parsed['EPayment']['EPaymentReq']['isShippingRequired'].upper() == 'true':
        order_info['shipping_info']['name'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToName'])
        order_info['shipping_info']['address_line_one'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToStreetAdd'])
        order_info['shipping_info']['address_line_two'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToStreetAdd2'])
        order_info['shipping_info']['city'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToCity'])
        order_info['shipping_info']['state'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToState'])
        order_info['shipping_info']['zip'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToZipCode'])
        order_info['shipping_info']['country'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToCountry'])
        order_info['shipping_info']['phone'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShipToPhone'])
        order_info['shipping_info']['customer_email'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['CustomerEmail'])
        order_info['shipping_info']['shipping_instructions'] = str(parsed['EPayment']['EPaymentRes']['ShippingAdd']['ShippingInstructions'])

    # Get Routing Information
    clients_data = parsed['EPayment']['ClientsData'].split('|')

    # Get Division Information
    order_type = clients_data[1]

    order_info['order_type'] = TYPE[order_type]

    # Confirmation Message -> Is this needed?
    order_info['confirmation_message'] = parsed['EPayment']['ConfirmationMessage']

    # Date order inserted into database
    order_info['date_received'] = now()

    # Billing Information
    order_info['billing_name'] = parsed['EPayment']['EPaymentRes']['BillingInfo']['BillingName']

    # Last Modified Date
    order_info['date_modified'] = None  # Look this up in docs
