from typing import List
from flask import Blueprint, Response, jsonify, render_template, request
from flask_login import login_required

from shopping import db
from shopping.models.definitions import Role, User

bp = Blueprint("role", __name__, url_prefix="/roles")


@bp.route("/")
@login_required
def index() -> Response:
    roles: List = Role.query.all()

    return render_template("role/index.html", roles=roles)


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def edit_role(id: int) -> Response:

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
@login_required
def delete_role(id: int) -> Response:
    role: Role = Role.query.get_or_404(id)

    user: User = User.query.filter_by(role_id=id).first()

    if user:
        return jsonify({"message": "Role is being used by a user. Cannot delete!"}), 409

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "Role deleted successfully!"})
