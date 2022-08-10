from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from app.constants import status, delivery_method, order_types, borough, size
from datetime import datetime


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class SearchOrderForm(FlaskForm):
    order_number = IntegerField('Order Number')
    suborder_number = IntegerField('Suborder Number')
    order_type = SelectField('Order Type', choices=order_types.DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.DROPDOWN)
    status = SelectField('Status', choices=status.DROPDOWN)
    billing_name = StringField('Billing Name')
    email = StringField('Email')
    date_received_start = DateField('Received Start Date', format='%Y-%m-%d', default=datetime.today())
    date_received_end = DateField('Received End Date', format='%Y-%m-%d')
    date_submitted_start = DateField('Submitted Start Date', format='%Y-%m-%d')
    date_submitted_end = DateField('Submitted End Date', format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)


class NewOrderForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    address_line_1 = StringField('Address line 1')
    address_line_2 = StringField('Address line 2')
    city = StringField('City')
    state = StringField('State')
    zip_code = IntegerField('Zip Code')
    phone = IntegerField('Phone')

    def __init__(self, *args, **kwargs):
        super(NewOrderForm, self).__init__(*args, **kwargs)


class NewSuborderForm(FlaskForm):
    num_copies = IntegerField('Number of Copies')
    status = SelectField('Status', choices=status.NEW_ORDER_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewSuborderForm, self).__init__(*args, **kwargs)


class NewBirthCertForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    gender = StringField('Gender')
    last_name = StringField('Last Name')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    add_year = StringField('Additional Years (Separated by comma)')
    birth_place = StringField('Place of Birth')
    borough = RadioField('Borough', choices=borough.RADIO)
    father_name = StringField("Father's Name")
    mother_name = StringField("Mother's Name")
    comment = StringField('Comment')
    exemplification = RadioField('Attach Letter of Exemplification',
                                 choices=[('yes', 'Attach Letter of Exemplification')])
    delivery_method = RadioField('Delivery Method', choices=delivery_method.RADIO)

    def __init__(self, *args, **kwargs):
        super(NewBirthCertForm, self).__init__(*args, **kwargs)


class NewDeathCertForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    gender = StringField('Gender')
    last_name = StringField('Last Name')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    add_year = StringField('Additional Years (Separated by comma)')
    cemetery = StringField('Cemetery')
    death_place = StringField('Place of Death')
    borough = RadioField('Borough', choices=borough.RADIO)
    father_name = StringField("Father's Name")
    mother_name = StringField("Mother's Name")
    comment = StringField('Comment')
    exemplification = RadioField('Attach Letter of Exemplification',
                                 choices=[('yes', 'Attach Letter of Exemplification')])
    delivery_method = RadioField('Delivery Method', choices=delivery_method.RADIO)

    def __init__(self, *args, **kwargs):
        super(NewDeathCertForm, self).__init__(*args, **kwargs)


class NewMarriageCertForm(NewDeathCertForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    bgs_last_name = StringField('Last Name of Bride/Groom/Spouse')
    bgs_first_name = StringField('First Name of Bride/Groom/Spouse')
    bgs_last_name2 = StringField('Last Name of Bride/Groom/Spouse')
    bgs_first_name2 = StringField('First Name of Bride/Groom/Spouse')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    add_year = StringField('Additional Years (Separated by comma)')
    marriage_place = StringField('Place of Marriage')
    borough = RadioField('Borough', choices=borough.RADIO)
    comment = StringField('Comment')
    exemplification = RadioField('Attach Letter of Exemplification',
                                 choices=[('yes', 'Attach Letter of Exemplification')])
    delivery_method = RadioField('Delivery Method', choices=delivery_method.RADIO)

    def __init__(self, *args, **kwargs):
        super(NewMarriageCertForm, self).__init__(*args, **kwargs)


class NewPhotoGalleryForm(FlaskForm):
    image_identifier = StringField('Image Identifier')
    description = StringField('Title/Description of Image')
    add_description = StringField('Additional Description')
    size = RadioField('Size', choices=size.GALLERY_RADIO)
    delivery_method = RadioField('Delivery Method', choices=delivery_method.RADIO)
    comment = StringField('Comment')

    def __init__(self, *args, **kwargs):
        super(NewPhotoGalleryForm, self).__init__(*args, **kwargs)


class NewTaxPhotoForm(FlaskForm):
    collection = RadioField('Collection', choices=[('1940', '1940'), ('1980', '1980'), ('both', 'Both')])
    borough = RadioField('Borough', choices=borough.RADIO)
    image_identifier = StringField('Image Identifier')
    building_num = IntegerField('Building Number')
    street = StringField('Street Name')
    description = StringField('Description')
    block = StringField('Block')
    lot = StringField('Lot')
    order_roll = StringField('Roll # (1940s Only)')
    size = RadioField('Size', choices=size.TAX_RADIO)
    delivery_method = RadioField('Delivery Method', choices=delivery_method.RADIO)

    def __init__(self, *args, **kwargs):
        super(NewTaxPhotoForm, self).__init__(*args, **kwargs)
