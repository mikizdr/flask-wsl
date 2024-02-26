from flask import (
    Blueprint,
    render_template,
)

from flask_login import login_required

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index() -> str:
    return render_template("welcome.html")

@bp.route("/home")
@login_required
def home() -> str:
    return render_template("dashboard/index.html")
