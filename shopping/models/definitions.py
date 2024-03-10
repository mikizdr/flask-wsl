from typing import Union
import uuid
from flask import url_for

from werkzeug.security import check_password_hash
from flask_login import UserMixin, current_user

from shopping import db, login_manager, app
from shopping.templates.components.forms.product import ProductForm


# join table for favorite products
favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


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
    role = db.relationship("Role", back_populates="users")
    profile = db.relationship(
        "Profile", back_populates="user", lazy="select", uselist=False
    )
    products = db.relationship("Product", back_populates="user")
    favorites = db.relationship(
        "Product",
        secondary=favorites,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )
    carts = db.relationship("Cart", back_populates="user")
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

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

    @property
    def list_of_favorites(self) -> list:
        """List of favorite products ids."""
        return [p.id for p in self.favorites]

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
    users = db.relationship("User", back_populates="role")
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    @property
    def get_name(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Role('{self.name}')"


class Cart(db.Model):
    __tablename__: str = "carts"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="carts")
    product_id = db.Column(db.Integer(), db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="carts")
    number_of_products = db.Column(db.Integer(), nullable=False, default=1)
    total = db.Column(db.Float(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    def __repr__(self) -> str:
        return f"Cart('{self.id}')"


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
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    @property
    def get_profile_image(self) -> str:
        """returns the profile image of the user as a url"""
        return url_for(
            "static",
            filename="images/uploads/users/" + self.profile_img,
        )

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
    category_id = db.Column(
        db.Integer(), db.ForeignKey("categories.id"), nullable=False
    )
    category = db.relationship("Category", back_populates="products")
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="products")
    carts = db.relationship("Cart", back_populates="product")
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    @property
    def get_product_image(self) -> str:
        """returns the first image of the product as a url"""
        return url_for(
            "static",
            filename="images/uploads/products/" + self.images.split(",")[0],
        )

    @property
    def get_created_at(self) -> str:
        """returns the date of creation of the product"""
        return self.created_at.strftime("%d %b %Y")

    def create_product(self, form: ProductForm) -> None:
        """Create a new product in the database."""
        product: Product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            images=form.images.data,
            category_id=form.category.data,
            user_id=current_user.id,
        )
        db.session.add(product)
        db.session.commit()

    def __repr__(self) -> str:
        return f"Product('{self.id}')"
