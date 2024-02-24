from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='Username:')
    email = StringField(label='Your email:')
    password = PasswordField(label='Password:')
    confirm_password = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')
    
    def __repr__(self) -> str:
        return super().__repr__()