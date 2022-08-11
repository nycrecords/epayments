from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from app.constants import status, delivery_method, order_types, borough, size, gender
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
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    last_name = StringField('Last Name')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    additional_years = StringField('Additional Years (Separated by comma)')
    birth_place = StringField('Place of Birth')
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN)
    father_name = StringField("Father's Name")
    mother_name = StringField("Mother's Name")
    comment = StringField('Comment')
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewBirthCertForm, self).__init__(*args, **kwargs)


class NewDeathCertForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    last_name = StringField('Last Name')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    additional_years = StringField('Additional Years (Separated by comma)')
    cemetery = StringField('Cemetery')
    death_place = StringField('Place of Death')
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN)
    father_name = StringField("Father's Name")
    mother_name = StringField("Mother's Name")
    comment = StringField('Comment')
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewDeathCertForm, self).__init__(*args, **kwargs)


class NewMarriageCertForm(NewDeathCertForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    groom_last_name = StringField('Last Name of Groom')
    groom_first_name = StringField('First Name of Groom')
    bride_last_name = StringField('Last Name of Bride')
    bride_first_name = StringField('First Name of Bride')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    additional_years = StringField('Additional Years (Separated by comma)')
    marriage_place = StringField('Place of Marriage')
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN)
    comment = StringField('Comment')
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewMarriageCertForm, self).__init__(*args, **kwargs)


class NewPhotoGalleryForm(FlaskForm):
    image_identifier = StringField('Image Identifier')
    description = StringField('Title/Description of Image')
    additional_description = StringField('Additional Description')
    size = SelectField('Size', choices=size.GALLERY_FORM_DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)
    contact_email = StringField('Contact Email')
    comment = StringField('Comment')

    def __init__(self, *args, **kwargs):
        super(NewPhotoGalleryForm, self).__init__(*args, **kwargs)


class NewTaxPhotoForm(FlaskForm):
    collection = SelectField('Collection', choices=[('1940', '1940'), ('1980', '1980'), ('both', 'Both')])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN)
    image_identifier = StringField('Image Identifier')
    building_num = IntegerField('Building Number')
    street = StringField('Street Name')
    description = StringField('Description')
    block = StringField('Block')
    lot = StringField('Lot')
    roll = StringField('Roll # (1940s Only)')
    size = SelectField('Size', choices=size.TAX_FORM_DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)
    contact_num = StringField('Contact Number')

    def __init__(self, *args, **kwargs):
        super(NewTaxPhotoForm, self).__init__(*args, **kwargs)
