from datetime import datetime
from pytz import timezone
from sqlalchemy.dialects.postgresql import JSONB
from app import db
from app.constants import event_type
from app.models import Suborder


class Event(db.Model):
    """
    Define the Event class with the following columns and relationships:
    Events are any type of action that happened to a request after it was submitted

    id - an integer that is the primary key of an Events
    suborder_number - a foreign key that links to a suborder's primary key
    user_id - a foreign key that links to the user_id of the person who performed the event
    type - a string containing the type of event that occurred
    timestamp - a datetime that keeps track of what time an event was performed
    previous_value - a string containing the old value of the event
    new_value - a string containing the new value of the event
    """
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborder.id', ondelete='CASCADE'))
    # user_guid = db.Column(db.String(64))  # who did the action
    type = db.Column(db.Enum(
        event_type.UPDATE_STATUS,
        event_type.UPDATE_PHOTO_TAX,
        event_type.INITIAL_IMPORT,
        name='event_type')
    )
    timestamp = db.Column(db.DateTime)
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)
    suborder = db.relationship("Suborder", backref="event")
    # user = db.relationship(
    #     "Users",
    #     primaryjoin="and_(Event.user_guid == Users.guid, "
    #                 "Event.auth_user_type == Users.auth_user_type)",
    #     backref="events"
    # )

    def __init__(self,
                 suborder_number,
                 # user_guid,
                 type_,
                 previous_value=None,
                 new_value=None,
                 timestamp=None):
        self.suborder_number = suborder_number
        # self.user_guid = user_guid
        self.type = type_
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))

    @property
    def status_history(self):
            return {
                'id': self.id,
                'suborder_number': self.suborder_number,
                'previous_status': self.previous_value.get('status', '') if self.previous_value else '',
                'new_status': self.new_value.get('status', ''),
                'comment': self.new_value.get('comment', ''),
                'timestamp': self.timestamp.strftime("%x %I:%M %p")
            }

    def __repr__(self):
        return '<Events %r>' % self.id
