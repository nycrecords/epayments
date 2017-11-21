import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.password = password
        else:
            self.password = None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Creates and stores password hash.
        :param password: String to hash.
        :return: None.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Checks user-entered passwords against hashes stored in the database.
        :param password: The user-entered password.
        :return: True if user has entered the correct password, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.email)


@login_manager.user_loader
def load_user(username):
    return Users.query.get(username).first()
