from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import validators, FieldList
from wtforms.fields import (StringField, IntegerField, SelectField, BooleanField, DateField, FormField)
from wtforms.validators import ValidationError, Email, InputRequired

from app.constants import status, delivery_method, order_type, borough, size, gender


class SearchOrderForm(FlaskForm):
    order_number = IntegerField('Order Number')
    suborder_number = IntegerField('Suborder Number')
    order_type = SelectField('Order Type', choices=order_type.DROPDOWN)
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


class SuborderForm(FlaskForm):
    order_types = SelectField("Order Type", choices=order_type.ORDER_TYPES_LIST, validators=[InputRequired()])
    num_copies = IntegerField('Number of Copies', validators=[InputRequired(), validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)

    def __init__(self, *args, **kwargs):
        super(SuborderForm, self).__init__(*args, **kwargs)


class MainOrderForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), validators.Length(max=64)])
    email = StringField('Email', validators=[InputRequired(), Email(), validators.Length(max=64)])
    address_line_1 = StringField('Address Line 1', validators=[validators.Length(max=64)])
    address_line_2 = StringField('Address Line 2', validators=[validators.Length(max=64)])
    city = StringField('City', [InputRequired(), validators.Length(max=64)])
    state = StringField('State', validators=[validators.Length(max=64)])
    zip_code = StringField('Zip Code', validators=[InputRequired(), validators.Length(min=5, max=5), validate_numeric])
    phone = StringField('Phone', validators=[validators.Length(max=64), validate_numeric])
    suborders = FieldList(FormField(SuborderForm))

    def __init__(self, *args, **kwargs):
        super(MainOrderForm, self).__init__(*args, **kwargs)


class BirthCertificateOrderForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)', validators=[validators.Length(max=40)])
    first_name = StringField('First Name', validators=[validators.Length(max=40)])
    last_name = StringField('Last Name', validators=[InputRequired(), validators.Length(max=25)])
    middle_name = StringField('Middle Name', validators=[validators.Length(max=40)])
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year', validators=[validators.Length(max=4)])
    birth_place = StringField('Place of Birth', validators.Length(max=40))
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[validators.Length(max=20)])
    additional_years = StringField('Additional Years (Separated by comma)')
    comment = StringField('Comment', validators=[validators.Length(max=225)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals', validators=[InputRequired()])
    no_amends = BooleanField('No Amends', validators=[InputRequired()])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(BirthCertificateOrderForm, self).__init__(*args, **kwargs)


class DeathCertificateOrderForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)', validators.Length(max=40))
    last_name = StringField('Last Name', validators=[InputRequired(), validators.Length(max=25)])
    first_name = StringField('First Name', validators=[validators.Length(max=40)])
    middle_name = StringField('Middle Name', validators=[validators.Length(max=40)])
    cemetery = StringField('Cemetery', validators=[validators.Length(max=40)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year', validators=[InputRequired(), validators.Length(max=4)])
    additional_years = StringField('Additional Years (Separated by comma)')
    death_place = StringField('Place of Death', validators=[validators.Length(max=40)])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN,
                          validators=[InputRequired(), validators.Length(max=20)])
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    comment = StringField('Comment', validators=[validators.Length(max=225)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals', validators=[InputRequired()])
    no_amends = BooleanField('No Amends', validators=[InputRequired()])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(DeathCertificateOrderForm, self).__init__(*args, **kwargs)


class MarriageCertificateOrderForm(FlaskForm):
    certificate_num = IntegerField('Certificate Number (If Known)', validators.Length(max=40))
    bride_last_name = StringField('Last Name of Bride', validators=[InputRequired(), validators.Length(max=25)])
    bride_first_name = StringField('First Name of Bride', validators=[validators.Length(max=40)])
    groom_last_name = StringField('Last Name of Groom', validators=[InputRequired(), validators.Length(max=25)])
    groom_first_name = StringField('First Name of Groom', validators=[validators.Length(max=40)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year', validators=[validators.Length(max=4)])
    marriage_place = StringField('Place of Marriage', validators=[validators.Length(max=40)])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN,
                          validators=[InputRequired(), validators.Length(max=20)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals', validators=[InputRequired()])
    no_amends = BooleanField('No Amends', validators=[InputRequired()])
    comment = StringField('Comment', validators=[validators.Length(max=255)])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(MarriageCertificateOrderForm, self).__init__(*args, **kwargs)


class PhotoGalleryOrderForm(FlaskForm):
    image_identifier = StringField('Image Identifier', validators=[InputRequired(), validators.Length(max=35)])
    description = StringField('Title/Description of Image', validators=[validators.Length(max=500)])
    additional_description = StringField('Additional Description', validators=[validators.Length(max=500)])
    size = SelectField('Size', choices=size.GALLERY_FORM_DROPDOWN)
    contact_email = StringField('Contact Email', validators=[validators.Length(max=256)])
    comment = StringField('Comment', validators=[validators.Length(max=255)])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryOrderForm, self).__init__(*args, **kwargs)


class TaxPhotoOrderForm(FlaskForm):
    collection = SelectField('Collection', choices=[('1940', '1940'), ('1980', '1980'), ('both', 'Both')],
                             validators=[InputRequired()])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[InputRequired()])
    image_identifier = StringField('Image Identifier', validators.Length(max=35))
    building_num = IntegerField('Building Number', validators=[InputRequired(), validators.Length(max=10)])
    street = StringField('Street Name', validators=[InputRequired(), validators.Length(max=40)])
    block = StringField('Block', validators=[validators.Length(max=9)])
    lot = StringField('Lot', validators=[validators.Length(max=9)])
    description = StringField('Description', validators=[validators.Length(max=35)])
    roll = StringField('Roll # (1940s Only)', validators=[validators.Length(max=9)])
    size = SelectField('Size', choices=size.TAX_FORM_DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)
    contact_num = StringField('Contact Number', validators=[validators.Length(max=64)])

    def __init__(self, *args, **kwargs):
        super(TaxPhotoOrderForm, self).__init__(*args, **kwargs)
