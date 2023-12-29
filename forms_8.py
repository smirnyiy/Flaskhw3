from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SingUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4)])
    last_name = StringField(
        'Last name', validators=[DataRequired(), Length(min=2)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8)]
    )