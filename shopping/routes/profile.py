from flask import (
    Blueprint,
    render_template,
)

from flask_login import login_required

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/")
@login_required
def index() -> str:
    return render_template("profile/index.html")
