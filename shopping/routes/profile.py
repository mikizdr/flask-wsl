from typing import Union
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_required

from shopping import db
from shopping.models.definitions import Profile
from shopping.templates.components.forms.profile import ProfileForm

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index() -> str:
    form = ProfileForm()
    profile: Union[Profile, None] = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    if form.validate_on_submit():
        first_name: str | None = form.first_name.data
        last_name: str | None = form.last_name.data
        genre: str | None = form.genre.data
        has_license: bool = False if form.has_license.data == "0" else True
        if form.img_url.data:
            img_url: str | None = form.img_url.data
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
            if form.img_url.data:
                profile.img_url = img_url
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
            if form.img_url.data:
                profile.img_url = form.img_url.data

            db.session.add(profile)

        db.session.commit()

        flash("Profile created successfully!", category="green")
        return redirect(url_for("dashboard.index"))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a role: {err_msg}", category="red")

    form.about.data = profile.about if profile else ""

    return render_template("profile/index.html", form=form, profile=profile)
