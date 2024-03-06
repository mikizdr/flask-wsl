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
from flask_login import login_required

from shopping import db
from shopping.models.definitions import Category, User
from shopping.templates.components.forms.category import CategoryForm

bp = Blueprint("category", __name__, url_prefix="/category")


@bp.route("/")
@login_required
def index() -> Response:
    categories: List = Category.query.all()

    return render_template("category/index.html", categories=categories)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Response:

    form = CategoryForm()

    if form.validate_on_submit():
        name: str = form.name.data
        description: str = form.description.data

        category: Category = Category(name=name.lower(), description=description)

        db.session.add(category)
        db.session.commit()

        flash("Category created successfully!", category="green")

        return redirect(url_for("category.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a category: {err_msg}",
                category="red",
            )

    return render_template("category/create.html", form=form)


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_role(id: int) -> Response:

    try:
        category: Category = Category.query.get_or_404(id)

        category.name = request.json.get("name")
        category.description = request.json.get("description")

        db.session.add(category)
        db.session.commit()

        return jsonify({"message": "Category updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Category not found!"}), 404


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_role(id: int) -> Response:
    category: Category = Category.query.get_or_404(id)

    user: User = User.query.filter_by(role_id=id).first()

    if user:
        return (
            jsonify({"message": "Category is being used by a user. Cannot delete!"}),
            409,
        )

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully!"})
