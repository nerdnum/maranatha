from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, validators, BooleanField, HiddenField, TextAreaField, SelectField)


class MessageForm(FlaskForm):
    is_urgent = BooleanField('Notify everyone about the new message by SMS and/or e-mail')
    message_type = HiddenField('Message Type')
    user_list = HiddenField('User List')
    subject = StringField('Subject', validators=[validators.DataRequired()])
    content = TextAreaField('Content', validators=[validators.DataRequired()], )
    submit = SubmitField('Submit Message')

