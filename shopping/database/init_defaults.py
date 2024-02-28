from shopping import db
from shopping.models.definitions import Role, User
from werkzeug.security import generate_password_hash


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
        
    """Pre-Populate User Table"""
    if User.query.first() is None:
        user = User(username='admin', email='admin@email.com', password=generate_password_hash('admin'), role_id=1)
        db.session.add(user)
        db.session.commit()
    pass
