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
from shopping.models.definitions import Product, Role, User
from shopping.routes.auth import only_admin
from shopping.templates.components.forms.role import RoleForm

bp = Blueprint("product", __name__, url_prefix="/products")

@bp.route("/")
@login_required
def index() -> Response:
    products: List = Product.query.all()

    return render_template("product/index.html", products=products)