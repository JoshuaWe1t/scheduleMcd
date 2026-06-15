import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

class TimeValidator:
    def __init__(self, message=None):
        self.message = message or "Invalid data: Your timeshift is invalid. Please, check your data"

    def __call__(self, form, field):
        if not field.data or field.data.strip() == '':
            return
        
        pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        if field.data and not re.match(pattern, field.data):
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class LogoutBtn(FlaskForm):
    submit = SubmitField('Log out')

class ScheduleForm(FlaskForm):
    mon = StringField('Monday', validators=[TimeValidator()])
    tue = StringField('Tuesday', validators=[TimeValidator()])
    wed = StringField('Wednesday ', validators=[TimeValidator()])
    thu = StringField('Thursday', validators=[TimeValidator()])
    fri = StringField('Friday', validators=[TimeValidator()])
    sat = StringField('Saturday', validators=[TimeValidator()])
    sun = StringField('Sunday', validators=[TimeValidator()])
    send_btn = SubmitField('Send')

class ScheduleMng(FlaskForm):
    code_user = HiddenField("", validators=[DataRequired()])
    approved = SubmitField("Approved")
    reject = SubmitField("Reject")