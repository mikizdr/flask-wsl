from shopping import db
from shopping.models.definitions import Role


def init_defaults():
    """Pre-Populate Role Table"""
    if Role.query.first() is None:
        roles: list[dict[str, str]] = [
            {"name": "Admin", "description": "Administrator"},
            {"name": "Seller", "description": "Customer who sells product"},
            {"name": "Buyer", "description": "Customer who buys products"},
        ]
        for role in roles:
            user_role = Role(name=role['name'], description=role['description'])
            db.session.add(user_role)
        db.session.commit()
    pass
