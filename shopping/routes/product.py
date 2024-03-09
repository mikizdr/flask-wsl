import os
import requests
from cgi import FieldStorage

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
from werkzeug.utils import secure_filename

from shopping import db, app
from shopping.models.definitions import Category, Product
from shopping.templates.components.forms.product import ProductForm
from shopping.utils.helper import allowed_file, make_unique_image_name


bp = Blueprint("product", __name__, url_prefix="/product")


def get_img_url() -> str:
    """Get random image url from picsum.photos."""
    return requests.get("https://picsum.photos/400/400").url


@bp.route("/", methods=["GET"])
@login_required
def index() -> Response:
    products: list = Product.query.filter_by(user_id=current_user.id).all()

    return render_template("product/index.html", products=products)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Response:
    form = ProductForm()

    categories: list = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if request.method == "POST" and form.validate_on_submit():
        try:
            if "images" not in request.files:
                flash("No images part", category="red")
                return redirect(request.url)

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            file: FieldStorage = request.files["images"]
            if file.filename == "":
                flash("No selected file", category="red")
                return redirect(request.url)

            files_filenames: list = []
            # product = Product()
            for file in form.images.data:
                if not allowed_file(file.filename):
                    flash(
                        f"Extension of the file {file.filename} not allowed. Allowed extensions: {app.config['ALLOWED_EXTENSIONS']}",
                        category="red",
                    )
                    return redirect(request.url)

            for file in form.images.data:
                file_filename: str = secure_filename(file.filename)
                unique_image_name: str = make_unique_image_name(file_filename)
                file.save(
                    os.path.join(
                        os.getcwd() + app.config["UPLOAD_FOLDER"] + "products/",
                        unique_image_name,
                    )
                )
                files_filenames.append(unique_image_name)

            images: str = ",".join(files_filenames)
            form.images.data = images
            Product().create_product(form)

            flash("Product created successfully!", category="green")
            return redirect(url_for("product.index"))
        except Exception as e:
            flash(f"Error: {e}", category="red")
            return redirect(url_for("product.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a product: {err_msg}", category="red"
            )

    return render_template("product/create.html", form=form, categories=categories)


@bp.route("/<int:id>", methods=["GET"])
def show(id: int) -> Response:
    product: Product = Product.query.get_or_404(id)

    return render_template("product/show.html", product=product)


@bp.route("/favorites", methods=["GET"])
def favorites() -> Response:
    """Show user's favorite products."""
    favorites: list[Product] = current_user.favorites

    return render_template("pages/home.html", products=favorites)


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update(id: int) -> Response:

    try:
        product: Product = Product.query.get_or_404(id)

        product.name = request.json.get("name")
        product.description = request.json.get("description")

        db.session.commit()

        return jsonify({"message": "Product updated successfully!"})
    except Exception as e:
        return jsonify({"message": "Product not found!", "status": 404})


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete(id: int) -> Response:
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


@bp.route("/favorite/<int:id>", methods=["POST"])
@login_required
def add_product_to_favorite(id: int) -> Response:
    """Add/remove product to/from favorite products."""
    try:
        product: Product = Product.query.get_or_404(id)

        if id in current_user.list_of_favorites:
            current_user.favorites.remove(product)
            db.session.commit()

            return jsonify(
                {"message": "Product removed from favorite products.", "status": 204}
            )

        current_user.favorites.append(product)
        db.session.commit()

        return jsonify(
            {
                "message": "Product added to favorite products successfully!",
                "status": 200,
            }
        )
    except Exception as e:
        return jsonify({"message": e, "status": 404})
