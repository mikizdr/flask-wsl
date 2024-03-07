"""
Global helper functions, constants and other entities for the app.
"""

import uuid

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
