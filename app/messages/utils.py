from app.utils import send_bulk_mail, send_sms
from app.messages.models import Message
from app.users.models import User
from flask import render_template, url_for
from sqlalchemy import and_


def send_broadcast_messages(message_id):

    message = Message.query.get(message_id)
    email_users = User.query.filter(and_(User.is_active, User.prayer_requests_by_email)).all()
    for user in email_users:
        message_html = render_template('emails/new_message.html', user=user, message=message)
        send_bulk_mail([user.email], 'no-reply@marantha-namibia.org',
                       message.subject,  message_html=message_html)

    sms_users = User.query.filter(and_(User.is_active, User.prayer_requests_by_sms)).all()
    link = url_for('messages.view_message', id=message_id, _external=True)
    for user in sms_users:
        message_text = render_template('sms/sms_message.txt', user=user, link=link)
        send_sms(user.mobile_phone, message_text)


