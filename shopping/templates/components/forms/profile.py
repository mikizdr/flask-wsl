from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, ValidationError, Optional, Length


class ProfileForm(FlaskForm):

    def validate_genre(self, genre_to_check) -> None:
        if genre_to_check.data not in ["M", "W"]:
            raise ValidationError(
                f"The genre {genre_to_check.data} is not valid. Please select a valid option."
            )

    first_name = StringField(
        label="First Name",
        validators=[Length(min=3, max=30), DataRequired("First name is required.")],
    )
    last_name = StringField(
        "Last Name",
        validators=[Length(min=3, max=30), DataRequired("Last name is required.")],
    )
    genre = SelectField(
        label="Genre",
        choices=[("", "Select an option"), ("M", "Man"), ("W", "Woman")],
        validators=[Optional("Please select an option for the genre.")],
    )
    about = TextAreaField(
        label="Short Bio:", validators=[Optional("Please enter a short bio.")]
    )
    has_license = RadioField(
        label="Do You Have A License?",
        choices=[(1, "Yes"), (0, "No")],
        validators=[Optional("Please select an option.")],
    )
    profile_img = FileField(
        label="Profile Image", validators=[Optional("Please select a profile image.")]
    )
    phone = StringField(
        label="Phone",
        validators=[
            Length(min=8, max=30),
            Optional("Please enter a valid phone number."),
        ],
    )
    address = StringField(
        label="Address",
        validators=[Length(min=10, max=100), Optional("Please enter a valid address.")],
    )
    city = StringField(
        label="City",
        validators=[Length(min=2, max=30), Optional("Please enter a valid city name.")],
    )
    zipcode = StringField(
        label="Zipcode",
        validators=[Length(min=1, max=10), Optional("Please enter a valid zipcode.")],
    )
    country = StringField(
        label="Country",
        validators=[
            Length(min=3, max=30),
            Optional("Please enter a valid country name."),
        ],
    )
    submit = SubmitField("Update Profile")
