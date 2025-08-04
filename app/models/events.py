from datetime import datetime
from pytz import timezone
from sqlalchemy.dialects.postgresql import JSONB
from app import db
from app.constants import event_type


class Events(db.Model):
    """
    Define the Events class with the following columns and relationships:
    Events are any type of action that happened to a request after it was submitted

    id - an integer that is the primary key of an Events
    order_number - a string containing the order number for the event that occurred
    suborder_number - a foreign key that links to a suborder's primary key
    user_id - a foreign key that links to the user_id of the person who performed the event
    type - a string containing the type of event that occurred
    timestamp - a datetime that keeps track of what time an event was performed
    previous_value - a string containing the old value of the event
    new_value - a string containing the new value of the event
    """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), db.ForeignKey('orders.id'), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id', ondelete='CASCADE'))
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))  # who did the action
    type = db.Column(db.Enum(
        event_type.UPDATE_STATUS,
        event_type.UPDATE_TAX_PHOTO,
        event_type.INITIAL_IMPORT,
        event_type.UPDATE_CHECK_MO_NUMBER,
        name='event_type'), nullable=False
    )
    timestamp = db.Column(db.DateTime)
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)
    suborder = db.relationship("Suborders", backref="events")
    user = db.relationship(
        "Users",
        backref="events"
    )

    def __init__(self,
                 suborder_number,
                 type_,
                 user_email=None,
                 previous_value=None,
                 new_value=None,
                 timestamp=None,
                 order_number=None):
        self.suborder_number = suborder_number
        self.type = type_
        self.user_email = user_email
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))
        self.order_number = order_number

    @property
    def status_history(self):
        # previous_value = ''
        # new_value = ''
        # TODO: Show history for event_type.UPDATE_TAX_PHOTO
        # if self.type in (event_type.UPDATE_STATUS, event_type.INITIAL_IMPORT):
        #     previous_value = self.previous_value.get('status', '') if self.previous_value else ''
        #     new_value = self.new_value.get('status', '')
        # elif self.type == event_type.UPDATE_TAX_PHOTO:
        #     for name, value, in [
        #         ('block: ', self.previous_value.get('block')),
        #         ('lot: ', self.previous_value.get('lot')),
        #         ('roll: ', self.previous_value.get('roll'))
        #     ]:
        #         if value:
        #             previous_value += ''.join((name, value, ' '))
        #     for name, value, in [
        #         ('block: ', self.new_value.get('block')),
        #         ('lot: ', self.new_value.get('lot')),
        #         ('roll: ', self.new_value.get('roll'))
        #     ]:
        #         if value:
        #             new_value += ''.join((name, value, ' '))
        return {
            'id': self.id,
            'user': self.user_email,
            'suborder_number': self.suborder_number,
            'previous_status': self.previous_value.get('status', '') if self.previous_value else '',
            'new_status': self.new_value.get('status', '') if self.new_value else '',
            'comment': self.new_value.get('comment', ''),
            'timestamp': self.timestamp.strftime("%x %I:%M %p")
        }

    def __repr__(self):
        return '<Events %r>' % self.id
