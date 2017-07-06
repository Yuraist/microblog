"""forms.py
"""

from flask_wtf import FlaskForm
from app import app
from app.models import user_datastore
from wtforms.validators import DataRequired, Length
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, FileField
from flask_security import LoginForm, RegisterForm, Security

class MyLoginForm(FlaskForm):
    """LoginForm is a class for user's authorization.
    StringField is a simple textfield. DataRequiered is a validator
    checks the user's input isn't empty.
    """
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember', default=False)


class MyRegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password_confirm', validators=[DataRequired()])


class ExtendedLoginForm(LoginForm):
    email = StringField('Username', validators=[DataRequired()])


class ExtendedRegisterForm(RegisterForm):
    email = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])


class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    avatar = FileField('avatar', validators=[])


class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])


security = Security(app, user_datastore,
                    login_form=ExtendedLoginForm,
                    register_form=ExtendedRegisterForm)
