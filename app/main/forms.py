from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
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
    submit_field = SubmitField('Apply')
    clear_field = SubmitField('Clear')

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)
