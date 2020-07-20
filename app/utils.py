from app import mail, mail_send_grid, celery
from flask import current_app as app
from flask_mail import Message
from twilio.rest import Client
from validate_email import validate_email
import phonenumbers


def is_valid_email(email):
    return validate_email(email)


def is_valid_phone_number(phone_number):
    try:
        phonenumbers.parse(phone_number)
        if phone_number[0] != '+':
            raise Exception()
        if len(phone_number) < 10:
            raise Exception()
        return True
    except (phonenumbers.phonenumberutil.NumberParseException, Exception) as error:
        return False


def send_email(recipient, sender, subject, message_html):
    message = Message(subject=subject, recipients=[recipient],
                      sender=sender)
    message.html = message_html
    send_async_mail.delay(message)


def send_sms(mobile_number, message_body):
    send_async_sms.delay(mobile_number, message_body)


def send_bulk_mail(recipients, sender, subject, message_html):
    send_async_bulk_mail.delay(recipients, sender, subject, message_html)


@celery.task
def send_async_mail(message):
    mail.send(message)


@celery.task
def send_async_sms(mobile_number, message_body):
    account_sid = app.config['TWILIO_ACCOUNT_SID']
    auth_token = app.config['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(body=message_body,
                from_='+12055831447',
                to=mobile_number)


@celery.task
def send_async_bulk_mail(recipients, sender, subject, message_html):
    message = Message(subject, sender=sender, recipients=recipients)
    message.html = message_html
    mail_send_grid.send(message)
