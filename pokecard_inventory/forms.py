from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()


class CardForm(FlaskForm):
    name = StringField('name')
    type = StringField('type')
    series = StringField('series')
    year = IntegerField('year')
    collector_card_number = StringField('collector card number')
    is_graded = StringField('is graded')
    grade = StringField('grade')
    description = StringField('description')
    for_sale = StringField('for sale')
    submit_button = SubmitField()