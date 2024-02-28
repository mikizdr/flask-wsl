from typing import List
from flask import (
    Blueprint,
    Response,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from shopping import db
from shopping.models.definitions import Role, User
from shopping.routes.auth import only_admin
from shopping.templates.components.forms.role import RoleForm

bp = Blueprint("role", __name__, url_prefix="/roles")


@bp.route("/")
@only_admin
def index() -> Response:
    roles: List = Role.query.all()

    return render_template("role/index.html", roles=roles)


@bp.route("/create", methods=["GET", "POST"])
@only_admin
def create() -> Response:

    form = RoleForm()

    if form.validate_on_submit():
        name: str = form.name.data
        description: str = form.description.data

        role: Role = Role(name=name.lower(), description=description)

        db.session.add(role)
        db.session.commit()

        return redirect(url_for("role.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a role: {err_msg}", category="red")

    return render_template("role/create.html", form=form)


@bp.route("/<int:id>", methods=["PUT"])
@only_admin
def update_role(id: int) -> Response:

    try:
        role: Role = Role.query.get_or_404(id)

        role.name = request.json.get("name")
        role.description = request.json.get("description")

        db.session.add(role)
        db.session.commit()

        return jsonify({"message": "Role updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Role not found!"}), 404


@bp.route("/<int:id>", methods=["DELETE"])
@only_admin
def delete_role(id: int) -> Response:
    role: Role = Role.query.get_or_404(id)

    user: User = User.query.filter_by(role_id=id).first()

    if user:
        return jsonify({"message": "Role is being used by a user. Cannot delete!"}), 409

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "Role deleted successfully!"})
