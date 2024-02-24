from typing import Union
from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash,
    g
)
from werkzeug.security import check_password_hash, generate_password_hash

from shopping import db
from shopping.templates.components.forms.register import RegisterForm
from shopping.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

@bp.route("/register", methods=["POST", "GET"])
def register() -> Union[Response, str]:
    if request.method == "POST":
        username: str = request.form["username"]
        email: str = request.form["email"]
        password: str = request.form["password"]
        confirm_password: str = request.form["confirm_password"]

        error = None

        if not username:
            error = "Username is required"
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif not confirm_password:
            error = "Password confirmation is required"
        elif password != confirm_password:
            error = "Passwords do not match"
        elif User.query.filter_by(email=email).first() is not None:
            error = f"Email address {email} is already registered"
        elif User.query.filter_by(username=username).first() is not None:
            error = f"Username {username} is already registered"

        print(username, email, password, confirm_password)

        if error is None:
            try:
                hashed_password: str = generate_password_hash(password)
                user = User(username=username, email=email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                error: Exception = e
            else:
                return redirect(url_for("auth.login"))

        print(error)

    return render_template("auth/register.html", form=RegisterForm())


@bp.route("/login", methods=["POST", "GET"])
def login() -> str:
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]

        error = None

        user: User | None = User.query.filter_by(username=username).first()

        if user is None:
            error = "Invalid username"
        elif not check_password_hash(user.password, password):
            error = "Invalid password"
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for("dashboard.home"))

        flash(error)

    return render_template("auth/login.html", form=RegisterForm())

@bp.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('dashboard.index'))
