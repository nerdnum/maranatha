from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class CountryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    iso_alpha_2_code = StringField('Alpha 2 Code',
                                   validators=[DataRequired(), Length(min=2, max=2)])
    iso_alpha_3_code = StringField('Alpha 3 Code',
                                   validators=[DataRequired(), Length(min=3, max=3)])
    iso_number_code = StringField('Iso Number',
                                  validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Save')


class SubdivisionTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')


class PopulatedAreaTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')


class SubdivisionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    country_id = SelectField('Country', choices=[], coerce=int)
    sub_division_type_id = SelectField('Subdivision Type', choices=[], coerce=int)
    iso_3166_2_code = StringField('ISO Code')
    submit = SubmitField('Save')


class PopulatedAreaForm(FlaskForm):
    country_id = SelectField('Country', choices=[], coerce=int)
    subdivision_id = SelectField('Subdivision', choices=[], coerce=int)
    area_type_id = SelectField('Type', choices=[], coerce=int)
    name = StringField('City/Town/Settlement Name', validators=[DataRequired()])
    submit = SubmitField('Save')



