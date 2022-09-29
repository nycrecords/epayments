import xlsxwriter
from datetime import date, datetime
from typing import Dict, List, Union

from flask import render_template, current_app, url_for
from flask_login import current_user
from os.path import join
from xhtml2pdf.pisa import CreatePDF

from app import db
from app.constants import (
    collection,
    event_type,
    printing
)
from app.constants import order_type
from app.constants.customer import EMPTY_CUSTOMER
from app.constants.search import ELASTICSEARCH_MAX_SIZE
from app.db_utils import create_object, update_object
from app.models import (
    BirthCertificate,
    BirthSearch,
    DeathCertificate,
    DeathSearch,
    MarriageCertificate,
    MarriageSearch,
    Orders,
    OrderNumberCounter,
    Suborders,
    Customers,
    TaxPhoto,
    Events,
    PhotoGallery
)
from app.search.searchfunctions import SearchFunctions
from app.search.utils import search_queries


def update_status(suborder: Suborders, comment: str, new_status: str):
    """Updates the status of a row from the Suborders table.

    Args:
        suborder: A Suborders instance.
        comment: Any additional information about the updating of the status.
        new_status: The value of the status to be updated to.
    """
    prev_event = Events.query.filter(Events.suborder_number == suborder.id,
                                     Events.new_value['status'].astext == suborder.status).order_by(
        Events.timestamp.desc()).first()

    previous_value = {}
    new_value = {}

    previous_value['status'] = suborder.status
    if prev_event is not None and 'comment' in prev_event.new_value:
        previous_value['comment'] = prev_event.new_value['comment']

    update_object({'status': new_status}, Suborders, suborder.id)

    new_value['status'] = new_status
    if comment:
        new_value['comment'] = comment

    event = Events(suborder.id,
                   event_type.UPDATE_STATUS,
                   current_user.email,
                   previous_value,
                   new_value)
    create_object(event)
    suborder.es_update()


def update_tax_photo(suborder_number: str, block_no: str, lot_no: str, roll_no: str) -> str:
    """
    This function is used for the Tax Photo API POST method,
    will update these fields from JSON sent back

    :param suborder_number:
    :param block_no:
    :param lot_no:
    :param roll_no:
    :return: {}
    """
    tax_photo = TaxPhoto.query.filter_by(suborder_number=suborder_number).one()

    message = 'No changes were made'
    new_value = {}
    previous_value = {}

    for name, value, col_value in [
        ('block', block_no, tax_photo.block),
        ('lot', lot_no, tax_photo.lot),
        ('roll', roll_no, tax_photo.roll)
    ]:
        if value and value != col_value:
            setattr(tax_photo, name, value)
            new_value[name] = value
            previous_value[name] = col_value

    if new_value:
        db.session.add(tax_photo)

        event = Events(suborder_number,
                       event_type.UPDATE_TAX_PHOTO,
                       current_user.email,
                       previous_value,
                       new_value)

        db.session.add(event)
        db.session.commit()
        message = 'Tax Photo Info Updated'
    return message


def _print_orders(search_params: Dict[str, str]) -> str:
    """
    Generates a PDF of order sheets.

    Args:
        search_params: Dictionary of attributes to search by.

    Returns:
        URL string of the PDF.
    """
    order_number = search_params.get('order_number')
    suborder_number = search_params.get('suborder_number')
    order_type = search_params.get('order_type')
    delivery_method = search_params.get('delivery_method')
    status = search_params.get('status')
    billing_name = search_params.get('billing_name')
    email = search_params.get('email')
    date_received_start = search_params.get('date_received_start')
    date_received_end = search_params.get('date_received_end')
    date_submitted_start = search_params.get('date_submitted_start')
    date_submitted_end = search_params.get('date_submitted_end')

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborders = search_queries(order_number,
                               suborder_number,
                               order_type,
                               delivery_method,
                               status,
                               billing_name,
                               email,
                               date_received_start,
                               date_received_end,
                               date_submitted_start,
                               date_submitted_end,
                               multiple_items,
                               0,
                               ELASTICSEARCH_MAX_SIZE,
                               'print')

    suborder = SearchFunctions.format_results(suborders)

    order_type_template_handler = {
        'Birth Search': 'birth_search.html',
        'Birth Cert': 'birth_cert.html',
        'Marriage Search': 'marriage_search.html',
        'Marriage Cert': 'marriage_cert.html',
        'Death Search': 'death_search.html',
        'Death Cert': 'death_cert.html',
        'Tax Photo': 'tax_photo.html',
        'Photo Gallery': 'photo_gallery.html',
        'Property Card': 'property_card.html',
        "OCME": "ocme.html",
        'HVR': 'hvr.html',
        'No Amends': 'no_amends.html'
    }

    html = ''

    for item in suborder:
        html += render_template('orders/{}'.format(order_type_template_handler[item['order_type']]),
                                order_info=item,
                                customer_info=item['customer'])

    filename = 'order_sheets_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime('%Y%m%d-%H%M%S'))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_small_labels(search_params: Dict[str, str]) -> str:
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get('order_number')
    suborder_number = search_params.get('suborder_number')
    order_type = search_params.get('order_type')
    delivery_method = search_params.get('delivery_method')
    status = search_params.get('status')
    billing_name = search_params.get('billing_name')
    email = search_params.get('email')
    date_received_start = search_params.get('date_received_start')
    date_received_end = search_params.get('date_received_end')
    date_submitted_start = search_params.get('date_submitted_start')
    date_submitted_end = search_params.get('date_submitted_end')

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborder_results = search_queries(order_number,
                                      suborder_number,
                                      order_type,
                                      delivery_method,
                                      status,
                                      billing_name,
                                      email,
                                      date_received_start,
                                      date_received_end,
                                      date_submitted_start,
                                      date_submitted_end,
                                      multiple_items,
                                      0,
                                      ELASTICSEARCH_MAX_SIZE,
                                      'search')

    # Only want suborder_number, and order type
    suborders = SearchFunctions.format_results(suborder_results)

    customers = []

    for item in suborders:
        customers.append(item['customer'])

    labels = [customers[i:i + printing.SMALL_LABEL_COUNT] for i in range(0, len(customers), printing.SMALL_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.SMALL_LABEL_COUNT:
            for i in range(printing.SMALL_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/small_labels.html', labels=page)

    filename = 'small_labels_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime('%Y%m%d-%H%M%S'))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_large_labels(search_params: Dict[str, str]) -> str:
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get('order_number')
    suborder_number = search_params.get('suborder_number')
    order_type = search_params.get('order_type')
    delivery_method = search_params.get('delivery_method')
    status = search_params.get('status')
    billing_name = search_params.get('billing_name')
    email = search_params.get('email')
    date_received_start = search_params.get('date_received_start')
    date_received_end = search_params.get('date_received_end')
    date_submitted_start = search_params.get('date_submitted_start')
    date_submitted_end = search_params.get('date_submitted_end')

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborder_results = search_queries(order_number,
                                      suborder_number,
                                      order_type,
                                      delivery_method,
                                      status,
                                      billing_name,
                                      email,
                                      date_received_start,
                                      date_received_end,
                                      date_submitted_start,
                                      date_submitted_end,
                                      multiple_items,
                                      0,
                                      ELASTICSEARCH_MAX_SIZE,
                                      'search')

    # Only want suborder_number, and order type
    suborders = SearchFunctions.format_results(suborder_results)

    customers = []

    for item in suborders:
        customers.append(item['customer'])

    customers = sorted(customers, key=lambda customer: customer['billing_name'])

    labels = [customers[i:i + printing.LARGE_LABEL_COUNT] for i in range(0, len(customers), printing.LARGE_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.LARGE_LABEL_COUNT:
            for i in range(printing.LARGE_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/large_labels.html', labels=page)

    filename = 'large_labels_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime('%Y%m%d-%H%M%S'))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def generate_csv(search_params: Dict[str, str]) -> str:
    """Generates CSV from search result.

    Args:
        search_params: Dictionary of attributes to search by.

    Returns:
        URL string of the CSV.
    """
    order_type = search_params.get('order_type')

    suborder_results = search_queries(
        order_number=search_params.get('order_number'),
        suborder_number=search_params.get('suborder_number'),
        order_type=order_type,
        delivery_method=search_params.get('delivery_method'),
        status=search_params.get('status'),
        billing_name=search_params.get('billing_name'),
        email=search_params.get('email'),
        date_received_start=search_params.get('date_received_start'),
        date_received_end=search_params.get('date_received_end'),
        date_submitted_start=search_params.get('date_submitted_start'),
        date_submitted_end=search_params.get('date_submitted_end'),
        search_type='csv',
    )

    filename = 'orders_{}_{}.xlsx'.format(order_type, datetime.now().strftime('%m_%d_%Y_at_%I_%M_%p'))
    path = join(current_app.config["PRINT_FILE_PATH"], filename)
    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet()

    # header formats
    header_format = wb.add_format({'bold': 1})
    header_format.set_bg_color('#FFFF00')

    header_init = ['Order Number',
                   'Suborder Number',
                   'Date Received',
                   'Order Type',
                   'Status',
                   'Phone',
                   'Email',
                   'Billing Name',
                   'Address line 1',
                   'Address line 2',
                   'City',
                   'State',
                   'Zip Code',
                   'Country',
                   ]
    header_last = ['Number of Copies',
                   'Exemplification',
                   'Exemplification Copies',
                   'Raised Seal',
                   'Raised Seal Copies',
                   'No Amends',
                   'No Amends Copies',
                   'Comment',
                   'Delivery Method'
                   ]

    contents = []
    header_data = []
    if order_type in (order_types.BIRTH_SEARCH, order_types.BIRTH_CERT):
        add_header = [
            'Gender',
            'First Name',
            'Middle Name',
            'Last Name',
            'Father Name',
            'Mother Name',
            'Alt First Name',
            'Alt Middle Name',
            'Alt Last Name',
            'Month',
            'Day',
            'Year',
            'Birth Place',
            'Borough'
        ]
        if order_type == order_types.BIRTH_CERT:
            add_header.insert(0, 'Certificate Number')

        header_data = header_init + add_header + header_last

        # get all row content and put into contents
        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('gender'),
                suborder['_source'].get('metadata').get('first_name'),
                suborder['_source'].get('metadata').get('middle_name', ''),
                suborder['_source'].get('metadata').get('last_name'),
                suborder['_source'].get('metadata').get('father_name', ''),
                suborder['_source'].get('metadata').get('mother_name', ''),
                suborder['_source'].get('metadata').get('alt_first_name', ''),
                suborder['_source'].get('metadata').get('alt_middle_name', ''),
                suborder['_source'].get('metadata').get('alt_last_name', ''),
                suborder['_source'].get('metadata').get('month'),
                suborder['_source'].get('metadata').get('day'),
                suborder['_source'].get('metadata').get('year'),
                suborder['_source'].get('metadata').get('birth_place', ''),
                suborder['_source'].get('metadata').get('borough', ''),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('exemplification'),
                suborder['_source'].get('metadata').get('exemplification_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('no_amends'),
                suborder['_source'].get('metadata').get('no_amends_copies'),
                'Yes' if suborder['_source'].get('metadata').get('comment') else '',
                suborder['_source'].get('metadata').get('delivery_method'),
            ]
            if order_type == order_types.BIRTH_CERT:
                row_content.insert(14, suborder['_source'].get('metadata').get('certificate_number'))

            contents.append(row_content)

    elif order_type in (order_types.MARRIAGE_SEARCH, order_types.MARRIAGE_CERT):
        # only difference between the two is a certificate column
        add_header = [
            'Groom First Name',
            'Groom Middle Name',
            'Groom Last Name',
            'Bride First Name',
            'Bride Middle Name',
            'Bride Last Name',
            'Alt Groom First Name',
            'Alt Groom Middle Name',
            'Alt Groom Last Name',
            'Alt Bride First Name',
            'Alt Bride Middle Name',
            'Alt Bride Last Name',
            'Month',
            'Day',
            'Year',
            'Marriage Place',
            'Borough',
        ]
        if order_type == order_types.MARRIAGE_CERT:
            add_header.insert(0, 'Certificate Number')

        header_data = header_init + add_header + header_last

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('groom_first_name'),
                suborder['_source'].get('metadata').get('groom_middle_name', ''),
                suborder['_source'].get('metadata').get('groom_last_name'),
                suborder['_source'].get('metadata').get('bride_first_name'),
                suborder['_source'].get('metadata').get('bride_middle_name', ''),
                suborder['_source'].get('metadata').get('bride_last_name'),
                suborder['_source'].get('metadata').get('alt_groom_first_name', ''),
                suborder['_source'].get('metadata').get('alt_groom_middle_name', ''),
                suborder['_source'].get('metadata').get('alt_groom_last_name', ''),
                suborder['_source'].get('metadata').get('alt_bride_first_name', ''),
                suborder['_source'].get('metadata').get('alt_bride_middle_name', ''),
                suborder['_source'].get('metadata').get('alt_bride_last_name', ''),
                suborder['_source'].get('metadata').get('month'),
                suborder['_source'].get('metadata').get('day'),
                suborder['_source'].get('metadata').get('year'),
                suborder['_source'].get('metadata').get('marriage_place', ''),
                suborder['_source'].get('metadata').get('borough', ''),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('exemplification'),
                suborder['_source'].get('metadata').get('exemplification_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('no_amends'),
                suborder['_source'].get('metadata').get('no_amends_copies'),
                'Yes' if suborder['_source'].get('metadata').get('comment') else '',
                suborder['_source'].get('metadata').get('delivery_method'),
            ]
            if order_type == order_types.MARRIAGE_CERT:
                row_content.insert(14, suborder['_source'].get('metadata').get('certificate_number'))

            contents.append(row_content)

    elif order_type in (order_types.DEATH_SEARCH, order_types.DEATH_CERT):
        # only difference between the two is a certificate column
        add_header = [
            'First Name',
            'Middle Name',
            'Last Name',
            'Father Name',
            'Mother Name',
            'Alt First Name',
            'Alt Middle Name',
            'Alt Last Name',
            'Cemetery',
            'Age at Death',
            'Month',
            'Day',
            'Year',
            'Death Place',
            'Borough',
        ]
        if order_type == order_types.DEATH_CERT:
            add_header.insert(0, 'Certificate Number')

        header_data = header_init + add_header + header_last

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('first_name'),
                suborder['_source'].get('metadata').get('middle_name', ''),
                suborder['_source'].get('metadata').get('last_name'),
                suborder['_source'].get('metadata').get('father_name', ''),
                suborder['_source'].get('metadata').get('mother_name', ''),
                suborder['_source'].get('metadata').get('alt_first_name', ''),
                suborder['_source'].get('metadata').get('alt_middle_name', ''),
                suborder['_source'].get('metadata').get('alt_last_name', ''),
                suborder['_source'].get('metadata').get('cemetery', ''),
                suborder['_source'].get('metadata').get('age_at_death', ''),
                suborder['_source'].get('metadata').get('month'),
                suborder['_source'].get('metadata').get('day'),
                suborder['_source'].get('metadata').get('year'),
                suborder['_source'].get('metadata').get('death_place', ''),
                suborder['_source'].get('metadata').get('borough', ''),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('exemplification'),
                suborder['_source'].get('metadata').get('exemplification_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('no_amends'),
                suborder['_source'].get('metadata').get('no_amends_copies'),
                'Yes' if suborder['_source'].get('metadata').get('comment') else '',
                suborder['_source'].get('metadata').get('delivery_method'),
            ]
            if order_type == order_types.DEATH_CERT:
                row_content.insert(14, suborder['_source'].get('metadata').get('certificate_number'))

            contents.append(row_content)

    elif order_type == order_types.NO_AMENDS:
        add_header = [
            'Number of Copies',
            'Filename',
            'Delivery Method'
        ]

        header_data = header_init + add_header

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('filename'),
                suborder['_source'].get('metadata').get('delivery_method'),
            ]

            contents.append(row_content)

    elif order_type == order_types.PROPERTY_CARD:
        add_header = [
            'Borough',
            'Block',
            'Lot',
            'Building Name',
            'Street',
            'Number of Copies',
            'Raised Seal',
            'Raised Seal Copies',
            'Delivery Method',
            'Contact Number',
            'Contact Email'
        ]

        header_data = header_init + add_header

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('borough'),
                suborder['_source'].get('metadata').get('block'),
                suborder['_source'].get('metadata').get('lot'),
                suborder['_source'].get('metadata').get('building_name'),
                suborder['_source'].get('metadata').get('street'),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('delivery_method'),
                suborder['_source'].get('metadata').get('contact_number'),
                suborder['_source'].get('metadata').get('contact_email'),
            ]

            contents.append(row_content)

    elif order_type == order_types.OCME:
        add_header = [
            'Certificate',
            'Borough',
            'Date',
            'First Name',
            'Middle Name',
            'Last Name',
            'Age',
            'Number of Copies',
            'Raised Seal',
            'Raised Seal Copies',
            'Delivery Method',
            'Contact Number',
            'Contact Email'
        ]

        header_data = header_init + add_header

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('metadata').get('certificate_number'),
                suborder['_source'].get('metadata').get('borough'),
                suborder['_source'].get('metadata').get('date'),
                suborder['_source'].get('metadata').get('first_name'),
                suborder['_source'].get('metadata').get('middle_name'),
                suborder['_source'].get('metadata').get('last_name'),
                suborder['_source'].get('metadata').get('age'),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('delivery_method'),
                suborder['_source'].get('metadata').get('contact_number'),
                suborder['_source'].get('metadata').get('contact_email'),
            ]

            conent.append(row_content)

    elif order_type == order_types.HVR:
        add_header = [
            'Link',
            'Record ID',
            'Type'
        ]

        header_data = header_init + add_header + header_last

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source']['order_type'],
                suborder['_source']['current_status'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('address_line_one'),
                suborder['_source'].get('customer').get('address_line_two'),
                suborder['_source'].get('customer').get('city'),
                suborder['_source'].get('customer').get('state'),
                suborder['_source'].get('customer').get('zip_code'),
                suborder['_source'].get('customer').get('country'),
                suborder['_source'].get('customer').get('link'),
                suborder['_source'].get('customer').get('record_id'),
                suborder['_source'].get('customer').get('type'),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('exemplification'),
                suborder['_source'].get('metadata').get('exemplification_copies'),
                suborder['_source'].get('metadata').get('raised_seal'),
                suborder['_source'].get('metadata').get('raised_seal_copies'),
                suborder['_source'].get('metadata').get('no_amends'),
                suborder['_source'].get('metadata').get('no_amends_copies'),
                'Yes' if suborder['_source'].get('metadata').get('comment') else '',
                suborder['_source'].get('metadata').get('delivery_method'),
            ]

            contents.append(row_content)

    elif order_type == order_types.PHOTOS:
        add_header = [
            'Order Number',
            'Suborder Number',
            'Date Received',
            'Customer Name',
            'Phone',
            'Email',
            'Customer Address',
            'Delivery Method',
            'Size',
            'Copy',
            'Image Identifier',
            'Building Number',
            'Street',
            'Collection',
            'Borough',
            'Block',
            'Lot',
            'Comment',
            'Description',
        ]

        header_data = add_header

        for suborder in suborder_results['hits']['hits']:
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('phone'),
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('customer').get('address'),
                suborder['_source'].get('metadata').get('delivery_method'),
                suborder['_source'].get('metadata').get('size'),
                suborder['_source'].get('metadata').get('num_copies'),
                suborder['_source'].get('metadata').get('image_id', ''),
                suborder['_source'].get('metadata').get('building_number', ''),
                suborder['_source'].get('metadata').get('street', ''),
                suborder['_source'].get('metadata').get('collection', ''),
                suborder['_source'].get('metadata').get('borough', ''),
                suborder['_source'].get('metadata').get('block', ''),
                suborder['_source'].get('metadata').get('lot', ''),
                'Yes' if suborder['_source'].get('metadata').get('comment') else '',
                suborder['_source'].get('metadata').get('description', ''),
            ]

            contents.append(row_content)

    elif order_type == order_types.VITAL_RECORDS:
        add_header = [
            'Order Number',
            'Suborder Number',
            'Date Received',
            'Customer Name',
            'Email',
            'Delivery Method',
            'Certificate Type',
            'Certificate Number',
            'Borough',
            'Years',
        ]

        header_data = add_header

        for suborder in suborder_results['hits']['hits']:
            if suborder['_source'].get('metadata') is None:
                print(suborder)
            row_content = [
                suborder['_source']['order_number'],
                suborder['_source']['suborder_number'],
                suborder['_source'].get('date_received')[:8],  # Remove time from string
                suborder['_source'].get('customer')['billing_name'],
                suborder['_source'].get('customer').get('email'),
                suborder['_source'].get('metadata').get('delivery_method'),
                suborder['_source'].get('order_type'),
                suborder['_source'].get('metadata').get('certificate_number'),
                suborder['_source'].get('metadata').get('borough'),
                suborder['_source'].get('metadata').get('years'),
            ]
            contents.append(row_content)

    # populate worksheet after header_data and contents is filled
    # write headers
    for col, data in enumerate(header_data):
        ws.write(0, col, data, header_format)

    # write in the worksheet
    row = 1  # row starts after header
    for row_content in contents:
        for col, data in enumerate(row_content):
            ws.write(row, col, data)
        row += 1

    wb.close()

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def create_new_order(order_info_dict: Dict[str, str], suborder_list: List[Dict]):
    """

    :param order_info_dict:
    :param suborder_list:
    :return:
    """
    order_types_list = [suborder['order_type'] for suborder in suborder_list]

    year = str(date.today().year)
    next_order_number = OrderNumberCounter.query.filter_by(year=year).one().next_order_number
    order_id = 'EPAY-{0:s}-{1:03d}'.format(year, next_order_number)

    order = Orders(_id=order_id,
                   date_submitted=date.today(),
                   date_received=date.today(),
                   _order_types=order_types_list,
                   multiple_items=True if len(suborder_list) > 1 else False)
    db.session.add(order)

    customer = Customers(billing_name=order_info_dict['name'],
                         shipping_name=order_info_dict['name'],
                         email=order_info_dict.get('email'),
                         address_line_1=order_info_dict.get('address_line_1'),
                         address_line_2=order_info_dict.get('address_line_2'),
                         city=order_info_dict.get('city'),
                         state=order_info_dict.get('state'),
                         zip_code=order_info_dict.get('zip_code'),
                         phone=order_info_dict.get('phone'),
                         order_number=order.id)
    db.session.add(customer)
    db.session.commit()
    print('made customer')

    for suborder in suborder_list:
        next_suborder_number = order.next_suborder_number
        suborder_id = '{} - {}'.format(order_id, next_suborder_number)

        order_type = suborder['order_type']
        if not suborder.get('certificate_num'):
            if order_type == order_types.BIRTH_CERT:
                order_type = order_types.BIRTH_SEARCH
            elif order_type == order_types.DEATH_CERT:
                order_type = order_types.DEATH_SEARCH
            elif order_type == order_types.MARRIAGE_CERT:
                order_type = order_types.MARRIAGE_SEARCH

        new_suborder = Suborders(id=suborder_id,
                                 order_type=order_type,
                                 order_number=order.id,
                                 _status=suborder['status'])
        db.session.add(new_suborder)
        db.session.commit()

        new_suborder.es_create()

        event = Events(suborder_number=new_suborder.id,
                       type_=event_type.INITIAL_IMPORT,
                       user_email=current_user.email,
                       previous_value=None,
                       new_value={
                           'status': new_suborder.status,
                       })

        db.session.add(event)
        db.session.commit()

        handler_for_order_type = {
            order_types.BIRTH_CERT: _create_new_birth_object,
            order_types.DEATH_CERT: _create_new_death_object,
            order_types.MARRIAGE_CERT: _create_new_marriage_object,
            order_types.TAX_PHOTO: _create_new_tax_photo,
            order_types.PHOTO_GALLERY: _create_new_photo_gallery
        }

        handler_for_order_type[suborder['order_type']](suborder, new_suborder)


def _create_new_birth_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificate_num')
    years = [suborder.get('year')] + suborder.get('additional_years').split(',')
    exemplification = True if 'exemplification' in suborder else False
    raised_seals = True if 'raised_seals' in suborder else False
    no_amends = True if 'no_amends' in suborder else False

    if certificate_number:
        birth_object = BirthCertificate(certificate_number=certificate_number,
                                        first_name=suborder.get('first_name'),
                                        last_name=suborder['last_name'],
                                        middle_name=suborder.get('middle_name'),
                                        gender=suborder['gender'],
                                        father_name=suborder.get('father_name'),
                                        mother_name=suborder.get('mother_name'),
                                        num_copies=suborder['num_copies'],
                                        month=suborder.get('month'),
                                        day=suborder.get('day'),
                                        years=years,
                                        birth_place=suborder.get('birth_place'),
                                        borough=[suborder['borough']],
                                        # letter=suborder.get('exemplification'),
                                        comment=suborder.get('comment'),
                                        _delivery_method=suborder['delivery_method'],
                                        suborder_number=new_suborder_obj.id,
                                        exemplification=exemplification,
                                        raised_seal=raised_seals,
                                        no_amends=no_amends)
    else:
        birth_object = BirthSearch(first_name=suborder.get('first_name'),
                                   last_name=suborder['last_name'],
                                   middle_name=suborder.get('middle_name'),
                                   gender=suborder['gender'],
                                   father_name=suborder.get('father_name'),
                                   mother_name=suborder.get('mother_name'),
                                   num_copies=suborder['num_copies'],
                                   month=suborder.get('month'),
                                   day=suborder.get('day'),
                                   years=years,
                                   birth_place=suborder.get('birth_place'),
                                   borough=[suborder['borough']],
                                   # letter=suborder.get('letter'),
                                   comment=suborder.get('comment'),
                                   _delivery_method=suborder['delivery_method'],
                                   suborder_number=new_suborder_obj.id,
                                   exemplification=exemplification,
                                   raised_seal=raised_seals,
                                   no_amends=no_amends)
    db.session.add(birth_object)
    db.session.commit()

    new_suborder_obj.es_update(birth_object.serialize)


def _create_new_death_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificate_num')
    years = [suborder.get('year')] + suborder.get('additional_years').split(',')
    exemplification = True if 'exemplification' in suborder else False
    raised_seals = True if 'raised_seals' in suborder else False
    no_amends = True if 'no_amends' in suborder else False

    if certificate_number:
        death_object = DeathCertificate(certificate_number=certificate_number,
                                        last_name=suborder['last_name'],
                                        first_name=suborder.get('first_name'),
                                        middle_name=suborder.get('middle_name'),
                                        num_copies=suborder['num_copies'],
                                        cemetery=suborder.get('cemetery'),
                                        month=suborder.get('month'),
                                        day=suborder.get('day'),
                                        years=years,
                                        death_place=suborder.get('death_place'),
                                        borough=suborder['borough'],
                                        father_name=suborder.get('father_name'),
                                        mother_name=suborder.get('mother_name'),
                                        # letter=suborder.get('letter'),
                                        comment=suborder.get('comment'),
                                        _delivery_method=suborder['delivery_method'],
                                        suborder_number=new_suborder_obj.id,
                                        exemplification=exemplification,
                                        raised_seal=raised_seals,
                                        no_amends=no_amends)
    else:
        death_object = DeathSearch(last_name=suborder['last_name'],
                                   first_name=suborder.get('first_name'),
                                   middle_name=suborder.get('middle_name'),
                                   num_copies=suborder['num_copies'],
                                   cemetery=suborder.get('cemetery'),
                                   month=suborder.get('month'),
                                   day=suborder.get('day'),
                                   years=years,
                                   death_place=suborder.get('death_place'),
                                   borough=suborder['borough'],
                                   father_name=suborder.get('father_name'),
                                   mother_name=suborder.get('mother_name'),
                                   # letter=suborder.get('letter'),
                                   comment=suborder.get('comment'),
                                   _delivery_method=suborder['delivery_method'],
                                   suborder_number=new_suborder_obj.id,
                                   exemplification=exemplification,
                                   raised_seal=raised_seals,
                                   no_amends=no_amends)
    db.session.add(death_object)
    db.session.commit()

    new_suborder_obj.es_update(death_object.serialize)


def _create_new_marriage_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificate_num')
    years = [suborder.get('year')] + suborder.get('additional_years').split(',')
    exemplification = True if 'exemplification' in suborder else False
    raised_seals = True if 'raised_seals' in suborder else False
    no_amends = True if 'no_amends' in suborder else False

    if certificate_number:
        marriage_object = MarriageCertificate(certificate_number=certificate_number,
                                              groom_last_name=suborder['groom_last_name'],
                                              groom_first_name=suborder.get('groom_first_name'),
                                              bride_last_name=suborder['bride_last_name'],
                                              bride_first_name=suborder.get('bride_first_name'),
                                              num_copies=suborder['num_copies'],
                                              month=suborder.get('month'),
                                              day=suborder.get('day'),
                                              years=years,
                                              marriage_place=suborder.get('marriage_place'),
                                              borough=suborder['borough'],
                                              # letter=suborder.get('letter'),
                                              comment=suborder.get('comment'),
                                              _delivery_method=suborder['delivery_method'],
                                              suborder_number=new_suborder_obj.id,
                                              exemplification=exemplification,
                                              raised_seal=raised_seals,
                                              no_amends=no_amends)
    else:
        marriage_object = MarriageSearch(groom_last_name=suborder['groom_last_name'],
                                         groom_first_name=suborder.get('groom_first_name'),
                                         bride_last_name=suborder['bride_last_name'],
                                         bride_first_name=suborder.get('bride_first_name'),
                                         num_copies=suborder['num_copies'],
                                         month=suborder.get('month'),
                                         day=suborder.get('day'),
                                         years=years,
                                         marriage_place=suborder.get('marriage_place'),
                                         borough=suborder['borough'],
                                         # letter=suborder.get('letter'),
                                         comment=suborder.get('comment'),
                                         _delivery_method=suborder['delivery_method'],
                                         suborder_number=new_suborder_obj.id,
                                         exemplification=exemplification,
                                         raised_seal=raised_seals,
                                         no_amends=no_amends)
    db.session.add(marriage_object)
    db.session.commit()

    new_suborder_obj.es_update(marriage_object.serialize)


def _create_new_tax_photo(suborder: Dict[str, str], new_suborder_obj: Suborders):
    new_collection = suborder['collection']

    if new_collection in [collection.YEAR_1940, collection.BOTH]:
        tax_photo_1940 = TaxPhoto(collection=collection.YEAR_1940,
                                  borough=suborder['borough'],
                                  image_id=suborder.get('image_identifier'),
                                  roll=suborder.get('roll'),
                                  block=suborder.get('block'),
                                  lot=suborder.get('lot'),
                                  building_number=suborder['building_num'],
                                  street=suborder['street'],
                                  description=suborder.get('description'),
                                  size=suborder['size'],
                                  num_copies=suborder['num_copies'],
                                  _delivery_method=suborder['delivery_method'],
                                  contact_number=suborder.get('contact_num'),
                                  suborder_number=new_suborder_obj.id)
        db.session.add(tax_photo_1940)
        db.session.commit()

        new_suborder_obj.es_update(tax_photo_1940.serialize)

    if new_collection in [collection.YEAR_1980, collection.BOTH]:
        tax_photo_1980 = TaxPhoto(collection=collection.YEAR_1980,
                                  borough=suborder['borough'],
                                  image_id=suborder.get('image_identifier'),
                                  block=suborder.get('block'),
                                  lot=suborder.get('lot'),
                                  building_number=suborder['building_num'],
                                  street=suborder['street'],
                                  description=suborder.get('description'),
                                  size=suborder['size'],
                                  num_copies=suborder['num_copies'],
                                  _delivery_method=suborder['delivery_method'],
                                  contact_number=suborder.get('contact_num'),
                                  suborder_number=new_suborder_obj.id)
        db.session.add(tax_photo_1980)
        db.session.commit()

        new_suborder_obj.es_update(tax_photo_1980.serialize)


def _create_new_photo_gallery(suborder: Dict[str, str], new_suborder_obj: Suborders):
    photo_gallery = PhotoGallery(image_id=suborder['image_identifier'],
                                 description=suborder.get('description'),
                                 additional_description=suborder.get('additional_description'),
                                 size=suborder['size'],
                                 num_copies=suborder.get('num_copies'),
                                 _delivery_method=suborder['delivery_method'],
                                 contact_number=suborder.get('contact_num'),
                                 comment=suborder.get('comment'),
                                 suborder_number=new_suborder_obj.id,
                                 contact_email=suborder['contact_email'])
    db.session.add(photo_gallery)
    db.session.commit()

    new_suborder_obj.es_update(photo_gallery.serialize)
