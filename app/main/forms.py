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


def validate_numeric_suborder(form, field):
    if field.data != "":
        try:
            int(field.data)
        except ValueError:
            field_name = field.name[field.name.rindex("-") + 1:].title()
            formatted_field = field.name.replace("_", " ")
            raise ValidationError(f"Invalid {field_name}.")


class BirthCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField('Number of Copies *', validators=[InputRequired("Number of copies is required."),
                                                                validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)
    certificate_num = StringField('Certificate Number (If Known)', validators=[validators.Length(max=40)])
    first_name = StringField('First Name', validators=[validators.Length(max=40)])
    last_name = StringField('Last Name *',
                            validators=[InputRequired("Last Name is required."), validators.Length(max=25)])
    middle_name = StringField('Middle Name', validators=[validators.Length(max=40)])
    gender = SelectField('Gender', choices=gender.FORM_DROPDOWN)
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year', validators=[validators.Length(max=4)])
    birth_place = StringField('Place of Birth', validators=[validators.Length(max=40)])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[validators.Length(max=20)])
    additional_years = StringField('Additional Years (Separated by comma)')
    comment = StringField('Comment', validators=[validators.Length(max=225)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(BirthCertificateForm, self).__init__(*args, **kwargs)


class DeathCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField('Number of Copies *', validators=[InputRequired("Number of copies is required."),
                                                                validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)
    last_name = StringField('Last Name *',
                            validators=[InputRequired("Last Name is required."), validators.Length(max=25)])
    first_name = StringField('First Name', validators=[validators.Length(max=40)])
    middle_name = StringField('Middle Name', validators=[validators.Length(max=40)])
    cemetery = StringField('Cemetery', validators=[validators.Length(max=40)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year *', validators=[InputRequired("Year is required."), validators.Length(max=4)])
    additional_years = StringField('Additional Years (Separated by comma)')
    death_place = StringField('Place of Death', validators=[validators.Length(max=40)])
    borough = SelectField('Borough *', choices=borough.FORM_DROPDOWN,
                          validators=[InputRequired("Borough is required."), validators.Length(max=20)])
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    comment = StringField('Comment', validators=[validators.Length(max=225)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(DeathCertificateForm, self).__init__(*args, **kwargs)


class MarriageCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField('Number of Copies *', validators=[InputRequired("Number of copies is required."),
                                                                validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)
    bride_last_name = StringField('Last Name of Bride *', validators=[InputRequired("Last Name of bride is required."),
                                                                      validators.Length(max=25)])
    bride_first_name = StringField('First Name of Bride', validators=[validators.Length(max=40)])
    groom_last_name = StringField('Last Name of Groom *', validators=[InputRequired("Last Name of groom is required."),
                                                                      validators.Length(max=25)])
    groom_first_name = StringField('First Name of Groom', validators=[validators.Length(max=40)])
    month = StringField('Month', validators=[validators.Length(max=20)])
    day = StringField('Day', validators=[validators.Length(max=2)])
    year = StringField('Year', validators=[validators.Length(max=4)])
    marriage_place = StringField('Place of Marriage', validators=[validators.Length(max=40)])
    borough = SelectField('Borough *', choices=borough.FORM_DROPDOWN,
                          validators=[InputRequired("Borough is required."), validators.Length(max=20)])
    exemplification = BooleanField('Attach Letter of Exemplification')
    raised_seals = BooleanField('Raised Seals')
    no_amends = BooleanField('No Amends')
    comment = StringField('Comment', validators=[validators.Length(max=255)])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(MarriageCertificateForm, self).__init__(*args, **kwargs)


class PhotoGalleryForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField('Number of Copies *', validators=[InputRequired("Number of copies is required."),
                                                                validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)
    image_identifier = StringField('Image Identifier *', validators=[InputRequired("Image Identifier is required."),
                                                                     validators.Length(max=35)])
    description = StringField('Title/Description of Image', validators=[validators.Length(max=500)])
    additional_description = StringField('Additional Description', validators=[validators.Length(max=500)])
    size = SelectField('Size', choices=size.GALLERY_FORM_DROPDOWN)
    contact_email = StringField('Contact Email', validators=[validators.Length(max=256)])
    comment = StringField('Comment', validators=[validators.Length(max=255)])
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryForm, self).__init__(*args, **kwargs)


class TaxPhotoForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField('Number of Copies *', validators=[InputRequired("Number of copies is required."),
                                                                validators.NumberRange(min=1)])
    status = SelectField('Status', choices=status.ORDER_STATUS_LIST)
    collection = SelectField('Collection *',
                             choices=[("", "-- Select Collection --"), ('1940', '1940'), ('1980', '1980'),
                                      ('both', 'Both')],
                             validators=[InputRequired("Collection is required.")])
    borough = SelectField('Borough', choices=borough.FORM_DROPDOWN, validators=[InputRequired("Borough is required.")])
    image_identifier = StringField('Image Identifier', validators=[validators.Length(max=35)])
    building_num = IntegerField('Building Number *',
                                validators=[InputRequired("Building Number is required."), validators.Length(max=10)])
    street = StringField('Street Name', validators=[InputRequired("Street is required."), validators.Length(max=40)])
    block = StringField('Block', validators=[validators.Length(max=9)])
    lot = StringField('Lot', validators=[validators.Length(max=9)])
    description = StringField('Description', validators=[validators.Length(max=35)])
    roll = StringField('Roll # (1940s Only)', validators=[validators.Length(max=9)])
    size = SelectField('Size', choices=size.TAX_FORM_DROPDOWN)
    delivery_method = SelectField('Delivery Method', choices=delivery_method.FORM_DROPDOWN)
    contact_num = StringField('Contact Number', validators=[validators.Length(max=64)])

    def __init__(self, *args, **kwargs):
        super(TaxPhotoForm, self).__init__(*args, **kwargs)


class SuborderForm(FlaskForm):
    class Meta:
        csrf = False

    birth_certificate_form = FieldList(FormField(BirthCertificateForm))
    death_certificate_form = FieldList(FormField(DeathCertificateForm))
    marriage_certificate_form = FieldList(FormField(MarriageCertificateForm))
    photo_gallery_form = FieldList(FormField(PhotoGalleryForm))
    tax_photo_form = FieldList(FormField(TaxPhotoForm))

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
