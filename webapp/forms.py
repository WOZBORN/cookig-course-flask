from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class EnrollmentForm(FlaskForm):
    fullname = StringField('ФИО', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон')
    submit = SubmitField('Записаться')
