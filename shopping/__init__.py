from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shopping.db"
app.config["SECRET_KEY"] = "yziSWR7ZXM4tLeJJIDjjdtMe18OjO3urIl42tgxnW9w"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from .models import definitions

from .routes import auth
from .routes import dashboard

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)

# push context manually to app
with app.app_context():
    db.create_all()
