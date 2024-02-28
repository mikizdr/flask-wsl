from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RoleForm(FlaskForm):
    name = StringField(label="Role Name:", validators=[DataRequired()])
    description = StringField(label="Description:", validators=[DataRequired()])
    submit = SubmitField(label="Create Role")

    def __repr__(self) -> str:
        return f"RoleForm('{self.name}')"
