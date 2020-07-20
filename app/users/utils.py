from app.token_manager import TokenManager
from app.utils import is_valid_email, send_sms, send_bulk_mail
from flask import render_template, url_for
from flask import current_app as app
from app.users.models import User
from sqlalchemy import or_, func


def get_user_by_login(submitted_login):
    user = User.query.filter(or_(
        User.mobile_phone == submitted_login, func.lower(User.email) == func.lower(submitted_login))).first()
    return user


def send_invitation(log_in, is_phone_number, password, invited_user, current_user):
    token_manager = TokenManager(app)
    token = token_manager.generate_token(current_user.id, invited_user.id)
    sender = app.config['USER_EMAIL_SENDER_EMAIL']
    app_name = app.config['USER_APP_NAME']
    next_url = url_for('users.profile')
    accept_invitation_link = url_for('users.login', next=next_url, token=token, _external=True)
    accept_invitation_link = accept_invitation_link.replace('http://127.0.0.1:5000', app.config['NGROK'])
    home_link = url_for('main.home', _external=True)
    if not is_phone_number:
        message_html = render_template('emails/invite_user_message.html',
                                       invited_user=invited_user,
                                       password=password,
                                       user=current_user,
                                       accept_invitation_link=accept_invitation_link,
                                       home_link=home_link,
                                       app_name=app_name)
        send_bulk_mail([invited_user.email], sender, '{} invitation'.format(app_name),
                       message_html=message_html)
    else:
        # accept_invitation_link = url_for('users.login', next=next_url, token=token,
        #                                  _external=True)

        message_body = render_template('sms/invite_user_message.txt',
                                       invited_user=invited_user,
                                       password=password,
                                       user=current_user,
                                       accept_invitation_link=accept_invitation_link,
                                       app_name=app_name)
        send_sms(invited_user.mobile_phone, message_body)


def send_password_reset(login):
    user = get_user_by_login(login)
    reset_token = user.get_reset_token()
    sender = app.config['USER_EMAIL_SENDER_EMAIL']
    app_name = app.config['USER_APP_NAME']
    reset_link = url_for('users.reset_password', token=reset_token, _external=True)
    if is_valid_email(login):
        message_body = render_template('emails/password_reset_message.html',
                                       reset_link=reset_link,
                                       app_name=app_name)
        send_bulk_mail([login], sender, '{} password reset'.format(app_name), message_body)
    else:
        if app.config['DEBUG']:
            reset_link = "{}{}".format(app.config['NGROK'],
                                                   url_for('users.reset_password', token=reset_token))
        else:
            reset_link = url_for('users.reset_password', token=reset_token, _external=True)

        message_body = render_template('sms/password_reset_message.txt',
                                       reset_link=reset_link,
                                       app_name=app_name)
        send_sms(login, message_body)
