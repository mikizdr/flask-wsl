import enum
from typing import Union
from werkzeug.security import check_password_hash

from flask_login import UserMixin

from shopping import db, login_manager


class User(db.Model, UserMixin):
    __tablename__: str = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    email_verified_at = db.Column(db.DateTime(), nullable=True)
    password = db.Column(db.String(length=60), nullable=False)
    remember_token = db.Column(db.String(length=100), nullable=True)
    role_id = db.Column(
        db.Integer(), db.ForeignKey("roles.id"), nullable=False, default=3
    )

    def password_is_valid(self, password: str) -> bool:
        """Check the password against the hashed password.

        Args:
            password (str): password entered by the user in the login form

        Returns:
            bool: True if the password is valid, False otherwise
        """
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"User('{self.username}')"


@login_manager.user_loader
def load_user(user_id) -> Union[User, None]:
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__: str = "roles"

    ADMIN = 1

    id: int = db.Column(db.Integer(), primary_key=True)
    name: str = db.Column(db.String(length=20), nullable=False, unique=True)
    description: str = db.Column(db.String(length=1000), nullable=True)

    @property
    def get_name(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Role('{self.name}')"


class Genre(enum.Enum):
    MAN: str = "M"
    WOMAN: str = "W"


class Profile(db.Model):
    __tablename__: str = "profiles"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=True)
    last_name = db.Column(db.String(length=30), nullable=True)
    address = db.Column(db.String(length=100), nullable=True)
    img_url = db.Column(db.String(length=300), nullable=True)
    about: str = db.Column(db.String(length=1000), nullable=True)
    has_license: bool = db.Column(db.Boolean(), nullable=False, default=False)
    genre = db.Column(db.Enum(Genre), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
