from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, SelectField, BooleanField, DateField, FormField, \
    FieldList
from wtforms.validators import DataRequired, ValidationError, Email
from wtforms import validators
from app.constants import status, delivery_method, order_types, borough, size, gender
from datetime import datetime


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


def validate_numeric(form, field):
    if field.data != "":
        try:
            int(field.data)
        except ValueError:
            formatted_field = field.name.replace("_", " ")
            raise ValidationError(f"Invalid {formatted_field}.")


class NewSuborderForm(FlaskForm):
    order_types = SelectField("Order Type", choices=order_types.ORDER_TYPES_LIST)
    num_copies = IntegerField('Number of Copies')
    status = SelectField('Status', choices=status.NEW_ORDER_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewSuborderForm, self).__init__(*args, **kwargs)


class NewOrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), validators.Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), validators.length(max=64)])
    address_line_1 = StringField('Address Line 1', validators=[validators.length(max=64)])
    address_line_2 = StringField('Address Line 2', validators=[validators.length(max=64)])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[validators.length(max=64)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), validators.length(min=5, max=5), validate_numeric])
    phone = StringField('Phone', validators=[validators.length(max=64), validate_numeric])
    suborder = FieldList(FormField(NewSuborderForm), min_entries=1)

    def __init__(self, *args, **kwargs):
        super(NewOrderForm, self).__init__(*args, **kwargs)


# class NewSuborderForm(FlaskForm):
#     num_copies = IntegerField('Number of Copies')
#     status = SelectField('Status', choices=status.NEW_ORDER_DROPDOWN)
#
#     def __init__(self, *args, **kwargs):
#         super(NewSuborderForm, self).__init__(*args, **kwargs)


class NewBirthCertForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    last_name = StringField('Last Name', validators=[DataRequired()])
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
    raised_seals = BooleanField('Raised Seals', validators=[DataRequired()])
    no_amends = BooleanField('No Amends', validators=[DataRequired()])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewBirthCertForm, self).__init__(*args, **kwargs)


class NewDeathCertForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    last_name = StringField('Last Name', validators=[DataRequired()])
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
    raised_seals = BooleanField('Raised Seals', validators=[DataRequired()])
    no_amends = BooleanField('No Amends', validators=[DataRequired()])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(NewDeathCertForm, self).__init__(*args, **kwargs)


class NewMarriageCertForm(NewDeathCertForm):
    certificate_num = IntegerField('Certificate Number (If Known)')
    groom_last_name = StringField('Last Name of Groom', validators=[DataRequired()])
    groom_first_name = StringField('First Name of Groom')
    bride_last_name = StringField('Last Name of Bride', validators=[DataRequired()])
    bride_first_name = StringField('First Name of Bride')
    month = StringField('Month')
    day = StringField('Day')
    year = StringField('Year')
    additional_years = StringField('Additional Years (Separated by comma)')
    marriage_place = StringField('Place of Marriage')
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[DataRequired()])
    comment = StringField('Comment')
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends', validators=[DataRequired()])
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
    collection = SelectField('Collection', choices=[('1940', '1940'), ('1980', '1980'), ('both', 'Both')],
                             validators=[DataRequired()])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[DataRequired()])
    image_identifier = StringField('Image Identifier')
    building_num = IntegerField('Building Number', validators=[DataRequired()])
    street = StringField('Street Name', validators=[DataRequired()])
    description = StringField('Description')
    block = StringField('Block')
    lot = StringField('Lot')
    roll = StringField('Roll # (1940s Only)')
    size = SelectField('Size', choices=size.TAX_FORM_DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)
    contact_num = StringField('Contact Number')

    def __init__(self, *args, **kwargs):
        super(NewTaxPhotoForm, self).__init__(*args, **kwargs)
