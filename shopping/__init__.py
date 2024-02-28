from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shopping.db"
app.config["SECRET_KEY"] = "yziSWR7ZXM4tLeJJIDjjdtMe18OjO3urIl42tgxnW9w"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message_category = "gray"

from .routes import auth
from .routes import dashboard

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)

# @app.before_first_request
# def create_tables():
#     """Create Tables and populate certain ones"""
#     db.create_all()

# push context manually to app
with app.app_context():
    db.create_all()
    from .database.init_defaults import init_defaults
    init_defaults()
