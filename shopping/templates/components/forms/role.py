from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

from shopping.models.definitions import Role


class RoleForm(FlaskForm):

    def validate_name(self, name_to_check) -> None:
        role: Role | None = Role.query.filter_by(name=name_to_check.data).first()
        if role:
            raise ValidationError(
                "This role already exists! Please try a different name."
            )

    name = StringField(label="Role Name:", validators=[DataRequired()])
    description = TextAreaField(label="Description:", validators=[DataRequired()])
    submit = SubmitField(label="Create Role")

    def __repr__(self) -> str:
        return f"RoleForm('{self.name}')"
