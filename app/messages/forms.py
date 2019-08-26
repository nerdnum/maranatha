from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, validators, TextAreaField, BooleanField, HiddenField)


class MessageForm(FlaskForm):
    is_urgent = BooleanField('Send as urgent broadcast')
    user_list = HiddenField('User List')
    subject = StringField('Subject', validators=[validators.DataRequired()])
    content = TextAreaField('Content', validators=[validators.DataRequired()])
    submit = SubmitField('Submit Message')

