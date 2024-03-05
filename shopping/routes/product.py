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
from flask_login import current_user, login_required

from shopping import db
from shopping.models.definitions import Category, Product
from shopping.routes.auth import only_admin
from shopping.templates.components.forms.product import ProductForm

bp = Blueprint("product", __name__, url_prefix="/products")


@bp.route("/", methods=["GET"])
@login_required
def index() -> Response:
    products: List = Product.query.filter_by(user_id=current_user.id).all()

    return render_template("product/index.html", products=products)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Response:
    form = ProductForm()

    categories: List = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit():
        name: str = form.name.data
        description: str = form.description.data
        price: float = form.price.data
        stock: int = form.stock.data
        img_url: str = form.img_url.data
        category_id: int = form.category.data

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            img_url=img_url,
            category_id=category_id,
            user_id=current_user.id,
        )
        db.session.add(product)
        db.session.commit()

        flash("Product created successfully!", category="green")

        return redirect(url_for("product.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a product: {err_msg}", category="red"
            )

    return render_template("product/create.html", form=form, categories=categories)


@bp.route("/<int:id>", methods=["PUT"])
@only_admin
def update_product(id: int) -> Response:

    try:
        product: Product = Product.query.get_or_404(id)

        product.name = request.json.get("name")
        product.description = request.json.get("description")

        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Product not found!"}), 404


@bp.route("/<int:id>", methods=["DELETE"])
@only_admin
def delete_product(id: int) -> Response:
    product: Product = Product.query.get_or_404(id)

    # TODO: Check if product is being associated with an order
    order = False

    if order:
        return (
            jsonify({"message": "Product is being used by a user. Cannot delete!"}),
            409,
        )

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully!"})
