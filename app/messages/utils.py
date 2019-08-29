from app import db
from app.utils import send_bulk_mail, send_sms
from app.messages.models import Message, UserMessage
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


def create_welcome_message(user_id):

    user = User.query.get(user_id)

    message_html = render_template('welcome_message.html',
                              church_image=url_for('static', filename='images/dutch_reformed_church.jpg',
                                                   _external=True),
                                   user=user)

    subject = 'Welcome to Maranatha Namibia'

    message = Message(created_by=7, subject=subject,
                      content=message_html, is_private=True,
                      is_urgent=False)

    db.session.add(message)
    db.session.commit()

    user_message = UserMessage(user_id=user_id, message_id=message.id,
                               sent=False, read=False)

    db.session.add(user_message)
    db.session.commit()

    return message.id

