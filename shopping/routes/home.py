from flask import (
    Blueprint,
    render_template,
)

from shopping.models.definitions import Product

bp = Blueprint("home", __name__)


@bp.route("/")
def index() -> str:
    products: list = Product.query.order_by(Product.created_at.desc()).all()

    return render_template("pages/home.html", products=products)
