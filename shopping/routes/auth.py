from typing import Union
from flask import (
    Blueprint,
    Response,
    render_template,
    session,
    url_for,
    redirect,
    flash,
    g,
)
from werkzeug.security import check_password_hash, generate_password_hash

from shopping import db
from shopping.templates.components.forms.auth import LoginForm, RegisterForm
from shopping.models.definitions import User
from flask_login import login_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route("/register", methods=["GET", "POST"])
def register() -> Union[Response, str]:

    form = RegisterForm()

    if form.validate_on_submit():
        username: str = form.username.data
        email: str = form.email.data
        password: str = form.password.data

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
        )

        db.session.add(user)
        db.session.commit()

        session.clear()
        session["user_id"] = user.id

        return redirect(url_for("dashboard.home"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}")

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:

    form = LoginForm()

    if form.validate_on_submit():
        user: User | None = User.query.filter_by(username=form.username.data).first()

        if user and user.password_is_valid(password=form.password.data):
            login_user(user)  # Fix: Call the login_user function with the user object
            flash(
                f"Success! You are logged in as: {user.username}",
                category="success",
            )

            session.clear()
            session["user_id"] = user.id

            return redirect(url_for("dashboard.home"))
        else:
            flash(
                "Username and password are not match! Please try again",
                category="danger",
            )

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    session.clear()
    flash("You have been logged out!", category="info")

    return redirect(url_for("dashboard.index"))
