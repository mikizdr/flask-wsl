from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Optional

class ProfileForm(FlaskForm):
    
    def validate_genre(self, genre_to_check) -> None:
        if genre_to_check.data not in ['M', 'W']:
            raise ValidationError(
                f"The genre {genre_to_check.data} is not valid. Please select a valid option."
            )
            
    first_name = StringField('First Name', validators=[DataRequired("First name is required.")])
    last_name = StringField('Last Name', validators=[DataRequired("Last name is required.")])
    genre = SelectField(u'Genre', choices=[('', 'Select an option'), ('M', 'Man'), ('W', 'Woman')])
    # about = TextAreaField(label="Short Bio:", validators=[DataRequired("Please enter a short bio.")])
    has_license = RadioField(u'Do You Have A License?', choices=[(1, 'Yes'), (0, 'No')], validators=[DataRequired("Please select an option.")])
    img_url = FileField('Profile Image', validators=[Optional()])
    # phone = StringField('Phone', validators=[DataRequired("Please enter a valid phone number.")])
    # address = StringField('Address', validators=[DataRequired("Please enter a valid address.")])
    # city = StringField('City', validators=[DataRequired("Please enter a valid city name.")])
    # zipcode = StringField('Zipcode', validators=[DataRequired("Please enter a valid zipcode.")])
    # country = StringField('Country', validators=[DataRequired("Please enter a valid country name.")])
    submit = SubmitField('Update Profile')