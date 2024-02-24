from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index() -> str:
    return render_template("welcome.html")

@bp.route("/home")
def home() -> str:
    return render_template("dashboard/index.html")
