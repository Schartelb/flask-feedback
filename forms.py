from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, DataRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[
                        Optional(), DataRequired()])
    first_name = StringField("First Name", validators=[
                             Optional(), DataRequired()])
    last_name = StringField("Last Name", validators=[
                            Optional(), DataRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
