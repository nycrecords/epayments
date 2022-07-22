from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from app.constants import status, delivery_method, order_types


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
    date_received_start = DateField('Received Start Date', format='%m/%d/%y')
    date_received_end = DateField('Received End Date', format='%m/%d/%y')
    date_submitted_start = DateField('Submitted Start Date', format='%m/%d/%y')
    date_submitted_end = DateField('Submitted End Date', format='%m/%d/%y')

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)
