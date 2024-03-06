from cgi import FieldStorage
import os
import uuid
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
import requests

from shopping import db, app
from shopping.models.definitions import Category, Product
from shopping.templates.components.forms.product import ProductForm
from werkzeug.utils import secure_filename

bp = Blueprint("product", __name__, url_prefix="/product")


def get_img_url() -> str:
    """Get random image url from picsum.photos."""
    return requests.get("https://picsum.photos/400/400").url


def allowed_file(filename) -> bool:
    """True if the file extension is allowed, False otherwise."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def make_unique_image_name(filename) -> str:
    """Return a unique image name."""
    extension = filename.rsplit(".", 1)[1]

    return str(uuid.uuid4()) + "." + extension


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

    if form.validate_on_submit():
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

            name: str = form.name.data
            description: str = form.description.data
            price: float = form.price.data
            stock: int = form.stock.data
            category_id: int = form.category.data

            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                images=images,
                category_id=category_id,
                user_id=current_user.id,
            )
            db.session.add(product)
            db.session.commit()

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


@bp.route("/<int:id>", methods=["PUT"])
@login_required
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
@login_required
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
