from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

from shopping.models.definitions import Category


class CategoryForm(FlaskForm):

    def validate_name(self, name_to_check) -> None:
        category: Category | None = Category.query.filter_by(name=name_to_check.data).first()
        if category:
            raise ValidationError(
                "This category already exists! Please try a different name."
            )

    name = StringField(label="Category Name:", validators=[DataRequired('Category name is required.')])
    description = TextAreaField(label="Description:", validators=[DataRequired('Category description is required.')])
    submit = SubmitField(label="Create category")

    def __repr__(self) -> str:
        return f"CategoryForm('{self.name}')"
