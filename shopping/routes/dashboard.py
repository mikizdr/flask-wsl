from flask import (
    Blueprint,
    render_template,
)

from flask_login import login_required

from shopping.models.definitions import Product

bp = Blueprint("dashboard", __name__)


@bp.route("/home")
@login_required
def home() -> str:
    return render_template("dashboard/index.html")
