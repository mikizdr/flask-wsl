from typing import Union
from flask import url_for

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
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    role_id = db.Column(
        db.Integer(), db.ForeignKey("roles.id"), nullable=False, default=3
    )
    role = db.relationship("Role", back_populates="users")
    profile = db.relationship(
        "Profile", back_populates="user", lazy="select", uselist=False
    )
    products = db.relationship("Product", back_populates="user")

    def password_is_valid(self, password: str) -> bool:
        """Check the password against the hashed password.

        Args:
            password (str): password entered by the user in the login form

        Returns:
            bool: True if the password is valid, False otherwise
        """
        return check_password_hash(self.password, password)

    @property
    def get_username(self) -> str:
        return self.username.capitalize()

    @property
    def get_full_name(self) -> str:
        return (
            self.profile.first_name + " " + self.profile.last_name
            if self.profile
            else self.username
        )

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
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    users = db.relationship("User", back_populates="role")

    @property
    def get_name(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Role('{self.name}')"


class Profile(db.Model):
    __tablename__: str = "profiles"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=True)
    last_name = db.Column(db.String(length=30), nullable=True)
    genre = db.Column(db.Enum("", "M", "W"), nullable=True)
    about: str = db.Column(db.String(length=1000), nullable=True)
    has_license: bool = db.Column(db.Boolean(), nullable=True, default=True)
    profile_img = db.Column(
        db.String(length=500), nullable=True, default="user-profile.png"
    )
    phone = db.Column(db.String(length=15), nullable=True)
    address = db.Column(db.String(length=100), nullable=True)
    city = db.Column(db.String(length=30), nullable=True)
    zipcode = db.Column(db.String(length=10), nullable=True)
    country = db.Column(db.String(length=30), nullable=True)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    user = db.relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile('{self.first_name} {self.last_name}')"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    products = db.relationship("Product", back_populates="category")

    def __repr__(self) -> str:
        return f"Category('{self.id}')"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=1000), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    images = db.Column(db.String(length=500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    category_id = db.Column(
        db.Integer(), db.ForeignKey("categories.id"), nullable=False
    )
    category = db.relationship("Category", back_populates="products")
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="products")

    @property
    def get_product_image(self) -> str:
        """returns the first image of the product as a url"""
        return url_for(
            "static",
            filename="images/uploads/products/" + self.images.split(",")[0],
        )

    def __repr__(self) -> str:
        return f"Product('{self.id}')"
