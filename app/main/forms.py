from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import validators, FieldList, SubmitField, SelectMultipleField, DecimalField, TextAreaField, \
    EmailField
from wtforms.fields import (StringField, IntegerField, SelectField, BooleanField, DateField, FormField)
from wtforms.validators import ValidationError, Email, InputRequired, Optional

from app.constants import status, delivery_method, suborder_form, order_types


class LoginForm(FlaskForm):
    username = StringField("Email Address", validators=[InputRequired(), Email()])
    submit = SubmitField("Log In")


class SearchOrderForm(FlaskForm):
    class Meta:
        csrf = False

    order_number = StringField("Order Number", validators=[validators.Length(max=64)])
    suborder_number = StringField("Suborder Number", validators=[validators.Length(max=32)])
    order_type = SelectField("Order Type", choices=order_types.DROPDOWN)
    delivery_method = SelectField("Delivery Method", choices=delivery_method.DROPDOWN)
    status = SelectField("Status", choices=status.DROPDOWN)
    billing_name = StringField("Billing Name", validators=[validators.Length(max=64)])
    email = EmailField("Email", validators=[Optional(), Email(), validators.Length(max=64)])
    date_received_start = DateField("Received Start Date", format="%Y-%m-%d", default=datetime.today)
    date_received_end = DateField("Received End Date", format="%Y-%m-%d")
    date_submitted_start = DateField("Submitted Start Date", format="%Y-%m-%d")
    date_submitted_end = DateField("Submitted End Date", format="%Y-%m-%d")

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)


def validate_numeric(form, field):
    if field.data:
        try:
            int(field.data)
        except ValueError:
            formatted_field = field.name.replace("_", " ")
            raise ValidationError(f"Invalid {formatted_field}.")


def validate_copies(form, field):
    if field.data:
        copies_type = field.short_name + "_copies"
        if not getattr(form, copies_type).data:
            formatted_field = copies_type.replace("_", " ").title()
            raise ValidationError(f"Number of {formatted_field} is required.")


def validate_certificate_number(form, field):
    if field.data:
        if not any(char.isdigit() for char in field.data):
            raise ValidationError("Certificate Number must have at least 1 numeric character.")


def validate_additional_years(form, field):
    if field.data:
        form_min_year = form.year.flags.min
        form_max_year = form.year.flags.max
        form_year_input = form.year.data
        form_additional_years_input = field.data.replace(" ", "")

        additional_years = form_additional_years_input.split(",")
        all_years = set(additional_years + [form_year_input])

        error_msg = "Invalid value entered for Additional Years."

        for year in additional_years:
            try:
                additional_year = int(year)

                if additional_year == form_year_input:
                    error_msg = f"Duplicate values entered for Additional Year. Additional Year values cannot be equal to {form_year_input}."
                    raise ValueError()

                if not (form_min_year <= additional_year <= form_max_year):
                    error_msg = f"Additional Year values must be between {form_min_year} and {form_max_year}."
                    raise ValueError()

                if len(all_years) != len(additional_years) + 1:
                    error_msg = "Duplicate values entered for Additional Year."
                    raise ValueError()

            except ValueError:
                raise ValidationError(f"{error_msg}")

        form.additional_years.data = form_additional_years_input


def validate_total(form, field):
    total = field.data
    if total < 0 or ("." in str(total) and len(str(total).split(".")[1]) != 2):
        raise ValidationError("Invalid value entered for total.")


class BirthCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[
            InputRequired("Certificate Number is required."),
            validators.Length(max=40),
            validate_certificate_number
        ]
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
            validators.number_range(1847, 1909, "Year must be between 1847 and 1909.")
        ]
    )
    birth_place = StringField("Place of Birth", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    exemplification = BooleanField("Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(BirthCertificateForm, self).__init__(*args, **kwargs)


class BirthSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
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
            validators.number_range(1847, 1909, "Year must be between 1847 and 1909.")
        ]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    birth_place = StringField("Place of Birth", validators=[validators.Length(max=40)])
    boroughs = SelectMultipleField(
        "Borough (Hold down CTRL while clicking an option for multi-select)",
        choices=suborder_form.ADDITIONAL_BOROUGHS,
        validators=[InputRequired("Borough is required.")],
        render_kw={'size': 5}
    )
    exemplification = BooleanField("Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(BirthSearchForm, self).__init__(*args, **kwargs)


class DeathCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[
            InputRequired("Certificate Number is required."),
            validators.Length(max=40),
            validate_certificate_number
        ]
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
        "Year (1795 - 1949)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1795, 1949, "Year must be between 1795 and 1949.")
        ]
    )
    death_place = StringField("Place of Death", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    exemplification = BooleanField("Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(DeathCertificateForm, self).__init__(*args, **kwargs)


class DeathSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
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
        "Year (1795 - 1949)",
        validators=[
            InputRequired("Year is required."),
            validators.number_range(1795, 1949, "Year must be between 1795 and 1949.")
        ]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    death_place = StringField("Place of Death", validators=[validators.Length(max=40)])
    boroughs = SelectMultipleField(
        "Borough (Hold down CTRL while clicking an option for multi-select)",
        choices=suborder_form.ADDITIONAL_BOROUGHS,
        validators=[InputRequired("Borough is required.")],
        render_kw={'size': 5}
    )
    father_name = StringField("Father's Name", validators=[validators.Length(max=105)])
    mother_name = StringField("Mother's Name", validators=[validators.Length(max=105)])
    exemplification = BooleanField("Attach Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(DeathSearchForm, self).__init__(*args, **kwargs)


class MarriageCertificateForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    certificate_num = StringField(
        "Certificate Number",
        validators=[
            InputRequired("Certificate Number is required."),
            validators.Length(max=40),
            validate_certificate_number
        ]
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
            validators.number_range(1790, 1949, message="Year must be between 1790 and 1949.")
        ]
    )
    marriage_place = StringField("Place of Marriage", validators=[validators.Length(max=40)])
    borough = SelectField(
        "Borough",
        choices=suborder_form.BOROUGHS,
        validators=[InputRequired("Borough is required."), validators.Length(max=20)]
    )
    exemplification = BooleanField("Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(MarriageCertificateForm, self).__init__(*args, **kwargs)


class MarriageSearchForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
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
            validators.number_range(1790, 1949, message="Year must be between 1790 and 1949.")
        ]
    )
    additional_years = StringField("Additional Years (Separated by comma)", validators=[validate_additional_years])
    marriage_place = StringField("Place of Marriage", validators=[validators.Length(max=40)])
    boroughs = SelectMultipleField(
        "Borough (Hold down CTRL while clicking an option for multi-select)",
        choices=suborder_form.ADDITIONAL_BOROUGHS,
        validators=[InputRequired("Borough is required.")],
        render_kw={'size': 5}
    )
    exemplification = BooleanField("Letter of Exemplification", validators=[validate_copies])
    exemplification_copies = SelectField(
        "Exemplification Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    raised_seal = BooleanField("Raised Seal", validators=[validate_copies])
    raised_seal_copies = SelectField(
        "Raised Seal Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    no_amends = BooleanField("No Amends", validators=[validate_copies])
    no_amends_copies = SelectField(
        "No Amends Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[validators.length(max=1)]
    )
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(MarriageSearchForm, self).__init__(*args, **kwargs)


class PhotoGalleryForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
    )
    status = SelectField("Status", choices=suborder_form.ORDER_STATUS)
    image_identifier = StringField(
        "Image Identifier",
        validators=[InputRequired("Image Identifier is required."), validators.Length(max=35)]
    )
    description = StringField("Title/Description of Image", validators=[validators.Length(max=500)])
    additional_description = StringField("Additional Description", validators=[validators.Length(max=500)])
    size = SelectField("Size", choices=suborder_form.PHOTO_GALLERY_SIZES)
    contact_num = StringField("Contact Number", validators=[validators.Length(max=64)])
    contact_email = StringField("Contact Email", validators=[Optional(), Email(), validators.Length(max=256)])
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryForm, self).__init__(*args, **kwargs)


class TaxPhotoForm(FlaskForm):
    class Meta:
        csrf = False

    num_copies = SelectField(
        "Number of Copies",
        choices=suborder_form.NUMBER_OF_COPIES,
        validators=[InputRequired("Number of copies is required."), validators.length(max=1)]
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
    building_num = StringField(
        "Building Number",
        validators=[InputRequired("Building Number is required."), validators.Length(min=1, max=10)]
    )
    street = StringField("Street Name", validators=[InputRequired("Street is required."), validators.Length(max=40)])
    block = StringField("Block", validators=[validators.Length(max=9)])
    lot = StringField("Lot", validators=[validators.Length(max=9)])
    description = StringField("Description", validators=[validators.Length(max=35)])
    roll = StringField("Roll #", validators=[validators.Length(max=9)])
    size = SelectField("Size", choices=suborder_form.TAX_PHOTO_SIZES)
    delivery_method = SelectField(
        "Delivery Method",
        choices=suborder_form.DELIVERY_METHODS,
        validators=[InputRequired("Delivery Method is required.")]
    )
    total = DecimalField(
        "Total",
        validators=[InputRequired("Total is required."), validate_total]
    )
    contact_num = StringField("Contact Number", validators=[validators.Length(max=64)])
    contact_email = StringField("Contact Email", validators=[Optional(), Email(), validators.Length(max=256)])
    comment = TextAreaField("Comment", validators=[validators.Length(max=225)])

    def __init__(self, *args, **kwargs):
        super(TaxPhotoForm, self).__init__(*args, **kwargs)


class SuborderForm(FlaskForm):
    # CSRF is disabled because SuborderForm is a FieldList of MainOrderForm
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
    check_mo_number = StringField("Check/Money Order Number", validators=[validators.Length(max=20)])
    country = SelectField(
        "Country",
        choices=suborder_form.COUNTRIES,
        default="United States",
        validators=[validators.Length(max=64)]
    )
    address_line_1 = StringField("Address Line 1", validators=[validators.Length(max=64)])
    address_line_2 = StringField("Address Line 2", validators=[validators.Length(max=64)])
    city = StringField("City", [validators.Length(max=64)])
    state = SelectField("State", choices=suborder_form.STATES, validators=[validators.Length(max=64)])
    zip_code = StringField("Zip Code", validators=[Optional(), validators.Length(min=5, max=10), validate_numeric])
    phone = StringField("Phone", validators=[validators.Length(max=64)])
    email = EmailField("Email", validators=[Optional(), Email(), validators.Length(max=64)])
    suborders = FieldList(FormField(SuborderForm))

    def __init__(self, *args, **kwargs):
        super(MainOrderForm, self).__init__(*args, **kwargs)
