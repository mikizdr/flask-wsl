from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    HiddenField,
    IntegerField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import ValidationError, Optional, Length, DataRequired

from shopping.models.definitions import Category


class ProductForm(FlaskForm):

    product_id = HiddenField("Product ID")
    name = StringField(
        label="Name",
        validators=[Length(min=3, max=100), DataRequired("Name is required.")],
    )
    description = TextAreaField(
        label="Poduct Description",
        validators=[
            Length(min=10, max=1000),
            DataRequired("Product description is required."),
        ],
    )
    price = IntegerField(
        label="Price",
        validators=[DataRequired("Price is required.")],
        render_kw={"step": "0.01", "min": "0.99"},
    )
    stock = IntegerField(
        label="How many items in the stock?",
        validators=[DataRequired("Stock number is required.")],
    )
    img_url = FileField(
        label="Product Image", validators=[Optional("Select an image for the product.")]
    )
    category = SelectField(
        label="Product Category",
        coerce=int,
        validators=[Optional("Please select an option for the category.")],
    )

    submit = SubmitField("Create Product")

    def __repr__(self) -> str:
        return f"ProductForm('{self.name}')"
