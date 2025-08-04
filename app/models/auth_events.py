from datetime import datetime

from pytz import timezone
from sqlalchemy.dialects.postgresql import JSONB

from app import db
from app.constants import auth_event_type
from app.models.users import Users


class AuthEvents(db.Model):
    """
    Define the Auth Events class with the following columns and relationships:

    id - an integer that is the primary key of an Events
    user_guid - a foreign key that links to the user_guid of the person who performed the event
    type - a string containing the type of event that occurred
    timestamp - a datetime that keeps track of what time an event was performed
    previous_value - a string containing the old value of the event
    new_value - a string containing the new value of the event
    """

    __tablename__ = 'auth_events'
    id = db.Column(db.Integer, primary_key=True)
    user_guid = db.Column(db.String(64), db.ForeignKey('users.guid'))
    type = db.Column(db.Enum(
        auth_event_type.USER_CREATED,
        auth_event_type.USER_LOGIN,
        auth_event_type.USER_FAILED_LOG_IN,
        auth_event_type.USER_LOGGED_OUT,
        auth_event_type.USER_ROLE_CHANGED,
        auth_event_type.AGENCY_USER_ACTIVATED,
        auth_event_type.AGENCY_USER_DEACTIVATED,
        name='auth_event_type'), nullable=False
    )
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    __table_args__ = (
        db.ForeignKeyConstraint([user_guid], [Users.guid], onupdate="CASCADE"),
    )

    user = db.relationship(
        "Users",
        backref="auth_events"
    )

    def __init__(self, user_guid, type_, previous_value=None, new_value=None, timestamp=None):
        self.user_guid = user_guid
        self.type = type_
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))
