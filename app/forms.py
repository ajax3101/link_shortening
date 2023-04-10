from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired


class ShortenForm(FlaskForm):
    url = StringField('Enter URL', validators=[DataRequired(), URL(message="Invalid URL format")])
    custom_code = StringField('Custom short code', validators=[URL(message="Invalid URL format")])
    submit = SubmitField('Shorten')


class EditForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(message="Invalid URL format")])
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
