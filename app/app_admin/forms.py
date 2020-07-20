from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class UploadUsersForm(FlaskForm):
    password = PasswordField('Default password', validators=[DataRequired()], default=False)
    excel_file = FileField(validators=[FileRequired(), FileAllowed(['xlsx'])])
    submit = SubmitField('Upload')