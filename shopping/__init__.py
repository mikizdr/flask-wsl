from typing import Union
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from shopping import config

app = Flask(__name__)

# Load the default configuration from the config module
configuration: Union[config.DevelopmentConfig, config.ProductionConfig] = (
    config.DevelopmentConfig
    if config.Config.ENV == "development"
    else config.ProductionConfig
)
app.config.from_object(configuration)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# Set the login view for the login manager
login_manager.login_view = "auth.login"
# Set the login message category for the login manager
login_manager.login_message_category = "gray"

from .routes import auth, dashboard, role, profile, product

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(role.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(product.bp)

# push context manually to app
with app.app_context():
    db.create_all()
    from .database.init_defaults import init_defaults

    init_defaults()
