"""
Global helper functions, constants and other entities for the app.
"""

import uuid

from flask_sqlalchemy.pagination import Pagination

from shopping import app


def allowed_file(filename) -> bool:
    """True if the file extension is allowed, False otherwise."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def make_unique_image_name(filename) -> str:
    """Return a unique image name."""
    extension: str = filename.rsplit(".", 1)[1]

    return str(uuid.uuid4()) + "." + extension


def paginator(model: object, page: int) -> Pagination:
    """Return a paginator object."""
    per_page = app.config["PER_PAGE"]
    max_per_page = app.config["MAX_PER_PAGE"]

    return model.query.paginate(
        page=page, per_page=per_page, max_per_page=max_per_page, error_out=False
    )
