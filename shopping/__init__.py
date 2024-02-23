from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shopping.db"
app.config['SECRET_KEY'] = 'yziSWR7ZXM4tLeJJIDjjdtMe18OjO3urIl42tgxnW9w'

db = SQLAlchemy(app)

from .models import user

from .routes import auth

app.register_blueprint(auth.bp)

# push context manually to app
with app.app_context():
    db.create_all()
