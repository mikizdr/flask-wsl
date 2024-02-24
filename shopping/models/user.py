from shopping import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    email_verified_at = db.Column(db.DateTime(), nullable=True)
    password = db.Column(db.String(length=60), nullable=False)
    remember_token = db.Column(db.String(length=100), nullable=True)

    def __repr__(self):
        return f"User('{self.username}')"
