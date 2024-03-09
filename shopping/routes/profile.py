import os
from cgi import FieldStorage
from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from shopping import db, app
from shopping.models.definitions import Profile
from shopping.templates.components.forms.profile import ProfileForm
from shopping.utils.helper import allowed_file, make_unique_image_name

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index() -> str:
    form = ProfileForm()
    profile: Union[Profile, None] = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    if form.validate_on_submit():
        if "profile_img" not in request.files:
            flash("No profile_img part", category="red")
            return redirect(request.url)

        file: FieldStorage = request.files["profile_img"]
        # if user does not select file, uploading will be skipped
        if file.filename != "":
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == "":
                flash("No selected file", category="red")
                return redirect(request.url)

            if not allowed_file(file.filename):
                flash(
                    f"Extension of the file {file.filename} not allowed. Allowed extensions: {app.config['ALLOWED_EXTENSIONS']}",
                    category="red",
                )
                return redirect(request.url)

            profile_unique_image_name = None
            if file:
                file_filename: str = secure_filename(file.filename)
                profile_unique_image_name: str = make_unique_image_name(file_filename)
                file.save(
                    os.path.join(
                        os.getcwd() + app.config["UPLOAD_FOLDER"] + "users/",
                        profile_unique_image_name,
                    )
                )

        first_name: str | None = form.first_name.data
        last_name: str | None = form.last_name.data
        genre: str | None = form.genre.data
        has_license: bool = False if form.has_license.data == "0" else True
        about: str | None = form.about.data
        phone: str | None = form.phone.data
        address: str | None = form.address.data
        city: str | None = form.city.data
        zipcode: str | None = form.zipcode.data
        country: str | None = form.country.data

        if profile:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.genre = genre
            profile.has_license = has_license
            profile.about = about
            profile.phone = phone
            profile.address = address
            profile.city = city
            profile.zipcode = zipcode
            profile.country = country

        else:
            profile = Profile(
                user_id=current_user.id,
                first_name=first_name,
                last_name=last_name,
                genre=genre,
                has_license=has_license,
                about=about,
                phone=phone,
                address=address,
                city=city,
                zipcode=zipcode,
                country=country,
            )

        if file.filename != "":
            if profile_unique_image_name:
                profile.profile_img = profile_unique_image_name

        db.session.add(profile)
        db.session.commit()

        flash("Profile updated successfully!", category="green")
        return redirect(url_for("home.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a role: {err_msg}", category="red")

    form.about.data = profile.about if profile else ""

    return render_template("profile/index.html", form=form, profile=profile)
