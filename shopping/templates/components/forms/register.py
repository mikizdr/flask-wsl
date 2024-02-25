from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from shopping.models.user import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check) -> None:
        user: User | None = User.query.filter_by(
            username=username_to_check.data
        ).first()
        if user:
            raise ValidationError(
                "Username already exists! Please try a different username"
            )

    def validate_email(self, email_to_check) -> None:
        email: User | None = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError(
                "Email Address already exists! Please try a different email address"
            )

    username = StringField(
        label="Username:", validators=[Length(min=3, max=30), DataRequired()]
    )
    email = StringField(label="Your email:", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="Password:", validators=[Length(min=8), DataRequired()]
    )
    confirm_password = PasswordField(
        label="Confirm Password:", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")

    def __repr__(self) -> str:
        return f"RegisterForm('{self.username}', '{self.email}')"
