import datetime as dt

from flask_login import UserMixin

from app import db, login_manager


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    guid = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(32), nullable=True)
    middle_initial = db.Column(db.String(1), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email_validated = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    last_sign_in_at = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.String(254), nullable=True, default=None)
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.password = password
        else:
            self.password = None

    @property
    def id(self):
        return str(self.guid)

    @property
    def role(self):
        return self.roles[0].name if self.roles else None

    @property
    def agency_user(self):
        return self.is_active and self.roles

    @property
    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.guid', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


@login_manager.user_loader
def load_user(username):
    return Users.query.get(username)
