from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import validators, FieldList, PasswordField, SubmitField
from wtforms.fields import (StringField, IntegerField, SelectField, BooleanField, DateField, FormField)
from wtforms.validators import ValidationError, Email, InputRequired

from app.constants import status, delivery_method, suborder_form, order_types


class SignInForm(FlaskForm):
    username = StringField("Email Address", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Sign In")


class SearchOrderForm(FlaskForm):
    order_number = IntegerField("Order Number")
    suborder_number = IntegerField("Suborder Number")
    order_type = SelectField("Order Type", choices=order_types.DROPDOWN)
    delivery_method = SelectField("Delivery Method", choices=delivery_method.DROPDOWN)
    status = SelectField("Status", choices=status.DROPDOWN)
    billing_name = StringField("Billing Name")
    email = StringField("Email")
    date_received_start = DateField("Received Start Date", format="%Y-%m-%d", default=datetime.today())
    date_received_end = DateField("Received End Date", format="%Y-%m-%d")
    date_submitted_start = DateField("Submitted Start Date", format="%Y-%m-%d")
    date_submitted_end = DateField("Submitted End Date", format="%Y-%m-%d")

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)


def validate_numeric(form, field):
    if field.data != "":
        try:
            int(field.data)
        except ValueError:
            formatted_field = field.name.replace("_", " ")
            raise ValidationError(f"Invalid {formatted_field}.")


def validate_year(form, field):
    if field.data is not None and field.data < 1867:
        if form.day.data is not None and form.month.data != "":
            pass
        else:
            raise ValidationError("If the year entered is before 1867, Month and Day fields are required.")


def validate_additional_years(form, field):
    if field.data is not None and field.data != "":
        min_year = form.year.flags.min
        max_year = form.year.flags.max
        additional_years = field.data.replace(" ", "")
        years = additional_years.split(",")
        error_msg = "Invalid value entered for Additional Years."
        for year in years:
            try:
                form_year = int(year)
                if form_year < min_year:
                    error_msg = f"Additional Year values must be greater than or equal to {min_year}."
                    raise ValidationError()
                if form_year > max_year:
                    error_msg = f"Additional Year values must be less than or equal to {max_year}."
                    raise ValidationError()
            except ValueError:
                raise ValidationError(f"{error_msg}")
        form.additional_years.data = additional_years


class BirthCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1, max=99)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[InputRequired("Certificate Number is required."), validators.Length(max=40)]
    )
    first_name = StringField("First Name", validators=[validators.Length(max=40)])
    last_name = StringField(
        "Last Name",
        validators=[InputRequired("Last Name is required."), validators.Length(max=25)]
    )
    middle_name = StringField("Middle Name", validators=[validators.Length(max=40)])
    gender = SelectField("Gender", choices=suborder_form.GENDERS)
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1847 - 1909)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1847, 1909, "Year must be between 1847 and 1909 "),
            validate_year
        ]
    )
    birth_place = StringField("Place of Birth", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    comment = StringField("Comment", validators=[validators.Length(max=225)])
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(BirthCertificateForm, self).__init__(*args, **kwargs)


class BirthSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1, max=99)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    first_name = StringField("First Name", validators=[validators.Length(max=40)])
    last_name = StringField(
        "Last Name",
        validators=[InputRequired("Last Name is required."), validators.Length(max=25)]
    )
    middle_name = StringField("Middle Name", validators=[validators.Length(max=40)])
    gender = SelectField("Gender", choices=suborder_form.GENDERS)
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1847 - 1909)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1847, 1909, "Year must be between 1847 and 1909 "),
            validate_year]
    )
    birth_place = StringField("Place of Birth", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    comment = StringField("Comment", validators=[validators.Length(max=225)])
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(BirthSearchForm, self).__init__(*args, **kwargs)


class DeathCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[InputRequired("Certificate Number is required."), validators.Length(max=40)]
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired("Last Name is required."), validators.Length(max=25)]
    )
    first_name = StringField("First Name", validators=[validators.Length(max=40)])
    middle_name = StringField("Middle Name", validators=[validators.Length(max=40)])
    cemetery = StringField("Cemetery", validators=[validators.Length(max=40)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1795 - 1948)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1795, 1948, "Year must be between 1795 and 1948 "),
            validate_year
        ]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    death_place = StringField("Place of Death", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    comment = StringField("Comment", validators=[validators.Length(max=225)])
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(DeathCertificateForm, self).__init__(*args, **kwargs)


class DeathSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    last_name = StringField(
        "Last Name",
        validators=[InputRequired("Last Name is required."), validators.Length(max=25)]
    )
    first_name = StringField("First Name", validators=[validators.Length(max=40)])
    middle_name = StringField("Middle Name", validators=[validators.Length(max=40)])
    cemetery = StringField("Cemetery", validators=[validators.Length(max=40)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1795 - 1948)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1795, 1948, "Year must be between 1795 and 1948 "),
            validate_year
        ]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    death_place = StringField("Place of Death", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    comment = StringField("Comment", validators=[validators.Length(max=225)])
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(DeathSearchForm, self).__init__(*args, **kwargs)


class MarriageCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[InputRequired("Certificate Number is required."), validators.Length(max=40)]
    )
    bride_last_name = StringField(
        "Last Name of Bride",
        validators=[InputRequired("Last Name of bride is required."), validators.Length(max=25)]
    )
    bride_first_name = StringField("First Name of Bride", validators=[validators.Length(max=40)])
    groom_last_name = StringField(
        "Last Name of Groom",
        validators=[InputRequired("Last Name of groom is required."), validators.Length(max=25)]
    )
    groom_first_name = StringField("First Name of Groom", validators=[validators.Length(max=40)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1790 - 1949)",
        validators=[
            InputRequired("Year is required"),
            validators.number_range(1790, 1949, message="Year must be between 1790 and 1949 "),
            validate_year]
    )
    marriage_place = StringField("Place of Marriage", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    comment = StringField("Comment", validators=[validators.Length(max=255)])
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(MarriageCertificateForm, self).__init__(*args, **kwargs)


class MarriageSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    bride_last_name = StringField(
        "Last Name of Bride",
        validators=[InputRequired("Last Name of bride is required."), validators.Length(max=25)]
    )
    bride_first_name = StringField("First Name of Bride", validators=[validators.Length(max=40)])
    groom_last_name = StringField(
        "Last Name of Groom",
        validators=[InputRequired("Last Name of groom is required."), validators.Length(max=25)]
    )
    groom_first_name = StringField("First Name of Groom", validators=[validators.Length(max=40)])
    month = SelectField("Month", choices=suborder_form.MONTHS, validators=[validators.Length(max=20)])
    day = IntegerField(
        "Day",
        validators=[validators.optional(), validators.number_range(1, 31, "Day must be between 1 and 31.")]
    )
    year = IntegerField(
        "Year (1790 - 1949)",
        validators=[
            InputRequired("Year is required"),
            validators.number_range(1790, 1949, message="Year must be between 1790 and 1949 "),
            validate_year
        ]
    )
    marriage_place = StringField("Place of Marriage", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    exemplification = BooleanField("Attach Letter of Exemplification")
    raised_seals = BooleanField("Raised Seals")
    no_amends = BooleanField("No Amends")
    comment = StringField("Comment", validators=[validators.Length(max=255)])
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(MarriageSearchForm, self).__init__(*args, **kwargs)


class PhotoGalleryForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1, max=99)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    image_identifier = StringField(
        "Image Identifier",
        validators=[InputRequired("Image Identifier is required."), validators.Length(max=35)]
    )
    description = StringField("Title/Description of Image", validators=[validators.Length(max=500)])
    additional_description = StringField("Additional Description", validators=[validators.Length(max=500)])
    size = SelectField("Size", choices=suborder_form.PHOTO_GALLERY_SIZES)
    contact_email = StringField("Contact Email", validators=[validators.Length(max=256)])
    comment = StringField("Comment", validators=[validators.Length(max=255)])
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryForm, self).__init__(*args, **kwargs)


class TaxPhotoForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = IntegerField(
        "Number of Copies",
        validators=[InputRequired("Number of copies is required."), validators.NumberRange(min=1, max=99)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    collection = SelectField(
        "Collection",
        choices=suborder_form.COLLECTIONS,
        validators=[InputRequired("Collection is required.")]
    )
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required.")]
    )
    image_identifier = StringField("Image Identifier", validators=[validators.Length(max=35)])
    building_num = IntegerField(
        "Building Number",
        validators=[InputRequired("Building Number is required."), validators.NumberRange(min=1)]
    )
    street = StringField("Street Name", validators=[InputRequired("Street is required."), validators.Length(max=40)])
    block = StringField("Block", validators=[validators.Length(max=9)], default=None)
    lot = StringField("Lot", validators=[validators.Length(max=9)], default=None)
    description = StringField("Description", validators=[validators.Length(max=35)])
    roll = StringField("Roll # (1940s Only)", validators=[validators.Length(max=9)])
    size = SelectField("Size", choices=suborder_form.TAX_PHOTO_SIZES)
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    contact_num = StringField("Contact Number", validators=[validators.Length(max=64)])

    def __init__(self, *args, **kwargs):
        super(TaxPhotoForm, self).__init__(*args, **kwargs)


class SuborderForm(FlaskForm):
    class Meta:
        csrf = False

    birth_certificate_form = FieldList(FormField(BirthCertificateForm))
    birth_search_form = FieldList(FormField(BirthSearchForm))
    death_certificate_form = FieldList(FormField(DeathCertificateForm))
    death_search_form = FieldList(FormField(DeathSearchForm))
    marriage_certificate_form = FieldList(FormField(MarriageCertificateForm))
    marriage_search_form = FieldList(FormField(MarriageSearchForm))
    photo_gallery_form = FieldList(FormField(PhotoGalleryForm))
    tax_photo_form = FieldList(FormField(TaxPhotoForm))

    def __init__(self, *args, **kwargs):
        super(SuborderForm, self).__init__(*args, **kwargs)


class MainOrderForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), validators.Length(max=64)])
    email = StringField("Email", validators=[InputRequired(), Email(), validators.Length(max=64)])
    address_line_1 = StringField("Address Line 1", validators=[validators.Length(max=64)])
    address_line_2 = StringField("Address Line 2", validators=[validators.Length(max=64)])
    city = StringField("City", [InputRequired(), validators.Length(max=64)])
    state = StringField("State", validators=[validators.Length(max=64)])
    zip_code = StringField("Zip Code", validators=[InputRequired(), validators.Length(min=5, max=5), validate_numeric])
    phone = StringField("Phone", validators=[validators.Length(max=64), validate_numeric])
    suborders = FieldList(FormField(SuborderForm))

    def __init__(self, *args, **kwargs):
        super(MainOrderForm, self).__init__(*args, **kwargs)
