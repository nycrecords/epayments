from sqlalchemy.dialects.postgresql import JSONB
from app import db


class Event(db.Model):
    """
    Define the Event class with the following columns and relationships:
    Events are any type of action that happened to a request after it was submitted

    id - an integer that is the primary key of an Events
    suborder_no - a foreign key that links to a suborder's primary key
    user_id - a foreign key that links to the user_id of the person who performed the event
    type - a string containing the type of event that occurred
    timestamp - a datetime that keeps track of what time an event was performed
    previous_value - a string containing the old value of the event
    new_value - a string containing the new value of the event
    """
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'))
    user_guid = db.Column(db.String(64))  # who did the action
    type = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
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
                 suborder_no,
                 user_guid,
                 type_,
                 previous_value=None,
                 new_value=None,
                 timestamp=None):
        self.suborder_no = suborder_no
        self.user_guid = user_guid
        self.type = type_
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        return '<Events %r>' % self.id
