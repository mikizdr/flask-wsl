from shopping import db
from shopping.models.definitions import Category, Role, User
from werkzeug.security import generate_password_hash


def init_defaults() -> None:
    """Pre-Populate Role Table"""
    if Role.query.first() is None:
        roles: list[dict[str, str]] = [
            {"name": "Admin", "description": "Administrator"},
            {"name": "Seller", "description": "Customer who sells product"},
            {"name": "Buyer", "description": "Customer who buys products"},
        ]
        for role in roles:
            user_role = Role(name=role["name"], description=role["description"])
            db.session.add(user_role)
        db.session.commit()

    """Pre-Populate User Table"""
    if User.query.first() is None:
        user = User(
            username="admin",
            email="admin@email.com",
            password=generate_password_hash("admin"),
            role_id=1,
        )
        db.session.add(user)
        db.session.commit()

    """Pre-Populate Product Category Table"""
    if Category.query.first() is None:
        catogories: list[dict[str, str]] = [
            {"name": "Vegetable", "description": "Different types of vegetables"},
            {"name": "Fruit", "description": "Different types of fruits"},
            {"name": "Cereals", "description": "Different types of cereals"},
        ]
        for category in catogories:
            product_catogory = Category(
                name=category["name"], description=category["description"]
            )
            db.session.add(product_catogory)
        db.session.commit()

    pass
