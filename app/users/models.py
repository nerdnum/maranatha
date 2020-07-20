from flask import current_app as app

from app import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.utils import is_valid_phone_number, is_valid_email
from sqlalchemy import and_


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Unicode(255), unique=True)
    mobile_phone = db.Column(db.String(15),  nullable=True)

    first_name = db.Column(db.Unicode(50))
    last_name = db.Column(db.Unicode(50))

    user_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False)

    # User information
    is_active = db.Column('is_active', db.Boolean(), nullable=False, default=False)
    invited_by = db.Column(db.Integer(), db.ForeignKey('users.id'))
    invited_at = db.Column(db.DateTime())
    is_bulk_invite = db.Column(db.Boolean(), default=False, nullable=False)
    inviter = db.relationship('User', remote_side=[id])

    prayer_requests_by_email = db.Column(db.Boolean(), default=False, nullable=False)
    prayer_requests_by_sms = db.Column(db.Boolean(), default=False, nullable=False)
    private_messages_by_email = db.Column(db.Boolean(), default=False, nullable=False)
    private_messages_by_sms = db.Column(db.Boolean(), default=False, nullable=False)

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    # Geographical information
    country_id = db.Column(db.Integer(), db.ForeignKey('countries.id'))                 # 154
    country = db.relationship('Country')
    subdivision_id = db.Column(db.Integer(), db.ForeignKey('subdivisions.id'))
    subdivision = db.relationship('Subdivision')
    populated_area_id = db.Column(db.Integer(), db.ForeignKey('populated_areas.id'))
    populated_area = db.relationship('PopulatedArea')

    last_login = db.Column(db.DateTime())
    login_count = db.Column(db.Integer())

    def get_reset_token(self, expires_seconds=60*60*48):
        serializer = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return user_id

    def has_any_role(self, roles):
        role_list = [role.name for role in self.roles]
        has_role = False
        if isinstance(roles, list):
            for role in roles:
                if role in role_list:
                    has_role = True
        else:
            if roles in role_list:
                has_role = True
        return has_role

    def has_role(self, role):
        has_role = False
        role_list = [role.name for role in self.roles]
        if role in role_list:
            has_role = True
        return has_role

    def __repr__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default='', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default='')  # for display purposes

    def __repr__(self):
        return f"{self.label}"


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class UserInvitation(db.Model):
    __tablename__ = 'user_invitations'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.Unicode(50))
    last_name = db.Column(db.Unicode(50))
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.Unicode(255), nullable=True)
    mobile_phone = db.Column(db.String(15), nullable=True)
    is_bulk_invite = db.Column(db.Boolean(), default=False, nullable=False)
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    invited_by = db.relationship('User')
    invitation_sent = db.Column(db.DateTime())
    user_responded = db.Column(db.DateTime())
    invite_count = db.Column(db.Integer, default=0)
    errors = []
    is_duplicate_invite = False

    def __repr__(self):
        return f"{self.first_name} {self.last_name}, {self.mobile_phone}, {self.email}" \
               f", {self.is_bulk_invite}, {self.invited_by_user_id}"

    def is_ok(self):
        is_ok = True

        self.errors = []

        if self.first_name == '-':
            self.errors.append('No first name provided')
            is_ok = False

        if self.last_name == '-':
            self.errors.append('No last name provided')
            is_ok = False

        if not is_valid_phone_number(self.mobile_phone):
            if not is_valid_email(self.email):
                self.errors.append('No valid login provided, please provide valid '
                                   'e-mail address of mobile phone number')
                is_ok = False

        if self.mobile_phone:

            if self.mobile_phone != '-':
                user = User.query.filter_by(mobile_phone=self.mobile_phone).first()
                if user:
                    is_ok = False
                    self.errors.append('A user with that mobile phone number already exists in the Maranatha database.')
                else:
                    user_invite = UserInvitation.query.filter_by(mobile_phone=self.mobile_phone).first()
                    if user_invite:
                        is_ok = False
                        self.is_duplicate_invite = True
                        self.errors.append(f"An invite for user with mobile phone '{self.mobile_phone}' "
                                           f"already exists.")

        if self.email:
            if self.email != '-':
                user = User.query.filter_by(email=self.email).first()
                if user:
                    is_ok = False
                    self.errors.append('A user with that e-mail address already exists in the Maranatha database.')
                else:
                    user_invite = UserInvitation.query.filter_by(email=self.email).first()
                    if user_invite:
                        is_ok = False
                        self.is_duplicate_invite = True
                        self.errors.append(f"An invite for user with e-mail '{self.email}' already exists.")

        return is_ok

    def get_errors_in_html(self):
        html_list = [f"<p>{error}</p>" for error in self.errors]
        return ''.join(html_list)

    def merge(self, user_invite, populate_empty_fields=True, over_write_existing_fields=True):
        if self.mobile_phone != '-':
            if self.mobile_phone != user_invite.mobile_phone and over_write_existing_fields:
                self.mobile_phone = user_invite.mobile_phone
        else:
            if user_invite.mobile_phone != '-' and populate_empty_fields:
                self.mobile_phone = user_invite.mobile_phone

        if self.email != '-':
            if self.email != user_invite.email and over_write_existing_fields:
                self.email = user_invite.email
        else:
            if user_invite.email != '-' and populate_empty_fields:
                self.email = user_invite.email

