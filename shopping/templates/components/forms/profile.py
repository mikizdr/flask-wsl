from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, Optional, Length

class ProfileForm(FlaskForm):
    
    def validate_genre(self, genre_to_check) -> None:
        if genre_to_check.data not in ['M', 'W']:
            raise ValidationError(
                f"The genre {genre_to_check.data} is not valid. Please select a valid option."
            )
            
    first_name = StringField('First Name', validators=[Length(min=3, max=30), Optional("First name is required.")])
    last_name = StringField('Last Name', validators=[Length(min=3, max=30), Optional("Last name is required.")])
    genre = SelectField(u'Genre', choices=[('', 'Select an option'), ('M', 'Man'), ('W', 'Woman')])
    about = TextAreaField(label="Short Bio:", validators=[Optional("Please enter a short bio.")])
    has_license = RadioField(u'Do You Have A License?', choices=[(1, 'Yes'), (0, 'No')], validators=[Optional("Please select an option.")])
    img_url = FileField('Profile Image', validators=[Optional()])
    # phone = StringField('Phone', validators=[Optional("Please enter a valid phone number.")])
    # address = StringField('Address', validators=[Optional("Please enter a valid address.")])
    # city = StringField('City', validators=[Optional("Please enter a valid city name.")])
    # zipcode = StringField('Zipcode', validators=[Optional("Please enter a valid zipcode.")])
    # country = StringField('Country', validators=[Optional("Please enter a valid country name.")])
    submit = SubmitField('Update Profile')