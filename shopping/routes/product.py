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
    products: List = Product.query.all()

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
