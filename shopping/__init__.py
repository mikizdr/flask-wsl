from typing import Union
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import Engine, PoolProxiedConnection, create_engine

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

from .routes import auth, dashboard, role, profile, product, category, home

# Register the blueprints
for bp in (auth, dashboard, role, profile, product, category, home):
    app.register_blueprint(bp.bp)

# push context manually to app
with app.app_context():
    db.create_all()
    from .database.init_defaults import init_defaults

    init_defaults()

# Uncomment the following lines to dump the database to a file, that can serve as a the db backup.
# engine: Engine = create_engine("sqlite:///instance/shopping.db")
# con: PoolProxiedConnection = engine.raw_connection()
# with open("./shopping/database/dump.sql", "w") as f:
#     for line in con.iterdump():
#         f.write("%s\n" % line)


PORT = app.config["PORT"]

# Compare this snippet from shopping/__init__.py:
if __name__ == "__main__":
    """
    If the next error occurs:
    socket.error: [Errno 10013] An attempt was made to access a socket in a way forbidden by its access permissions
    then, put the port number to some other value than 5000, for example 8000. Port can be get from .env file or
    from the configuration file.
    """
    app.run(
        debug=True, port=PORT
    )  # Run the app in debug mode (for development purposes only!)
