from app.users.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
import phonenumbers
from sqlalchemy import func, or_
from wtforms import ValidationError, StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import Email, DataRequired, EqualTo


def phonenumber_validator(form, field):
    try:
        phone_number = phonenumbers.parse(field.data)
        if field.data[0] != '+':
            raise ValidationError("The submitted phone number should start with a '+'")
        if len(field.data) < 10:
            raise ValidationError("The submitted phone number is to short to be a valid mobile phone number")
    except phonenumbers.phonenumberutil.NumberParseException as error:
        raise ValidationError('That is not a valid phone number.\n'
                              'Please use format +264811234567')


def user_exists_validator(form, field):
    user = User.query.filter(or_(
        User.mobile_phone == form.login.data,
        func.lower(User.email) == func.lower(form.login.data))).first()
    if user:
        raise ValidationError('A user with that login already exists.')


def login_validator(form, field):
    is_valid_email = True
    email = Email()

    if "@" in field.data:
        try:
            email(form, field)
        except ValidationError as error:
            raise ValidationError(error)
    else:
        try:
            phonenumber_validator(form, field)
        except ValidationError as error:
            raise ValidationError(error)


class RegisterForm(FlaskForm):
    login = StringField('Email or Mobile Phone Number', validators=[DataRequired(),
                                                                    login_validator])
    password = PasswordField('Password', validators=[DataRequired()], default=False)
    password_confirm = PasswordField('Confirm Password',
                                     validators=[EqualTo('password',
                                                         'Password and Confirm Password did not match')])
    submit = SubmitField('Submit')


class UserProfileForm(FlaskForm):
    email = StringField('Email')
    mobile_phone = StringField('Mobile Phone')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

    prayer_requests_by_email = BooleanField('Email')
    prayer_requests_by_sms = BooleanField('Sms')
    private_messages_by_email = BooleanField('Email')
    private_messages_by_sms = BooleanField('Sms')

    country_id = SelectField('Country', choices=[], coerce=int)
    subdivision_id = SelectField('Subdivision', choices=[], coerce=int)
    populated_area_id = SelectField('City/Town', choices=[], coerce=int)

    submit = SubmitField('Save Profile')

    def validate(self):
        if not super(UserProfileForm, self).validate():
            return False
        if not self.email.data and not self.mobile_phone.data:
            message = 'You must provide at least an email or a phone number. Both is best.'
            self.email.errors.append(message)
            return False
        return True


class LoginForm(FlaskForm):
    login = StringField('Email or Mobile Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', default=False)
    submit = StringField('Login')


class InviteUserForm(FlaskForm):
    login = StringField('Email or Mobile Number', validators=[DataRequired(), user_exists_validator, login_validator])
    submit = StringField('Invite')


class ForgotPasswordForm(FlaskForm):
    login = StringField('Email or Mobile Number', validators=[DataRequired(),
                                                              login_validator])
    submit = StringField('Send Reset')


class ForgotPasswordFormWithReset(ForgotPasswordForm):
    reactivate_account = BooleanField('Reactivate Account', default=True)


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], default=False)
    password_confirm = PasswordField('Confirm Password',
                                     validators=[EqualTo('password',
                                                         'Password and Confirm Password did not match')])
    submit = SubmitField('Reset password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()], default=False)
    new_password = PasswordField('New Password', validators=[DataRequired()], default=False)
    new_password_confirm = PasswordField('Confirm New Password',
                                         validators=[EqualTo('new_password',
                                                         'Password and Confirm Password did not match')])
    submit = SubmitField('Reset password')


class UploadUsersForm(FlaskForm):
    password = PasswordField('Default password', validators=[DataRequired()], default=False)
    excel_file = FileField(validators=[FileRequired(), FileAllowed(['xlsx'])])
    submit = SubmitField('Upload')


