import os

from flask import Flask
from . import config


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Set debug mode to true CHANGE FOR PROD
    app.debug = True
    # Set testing mode to true CHANGE FOR PROD
    app.testing = True
    # Set the secret key from the config file
    app.secret_key = config.SECRET_KEY
    from . import main, animals
    # Index Blueprint
    app.register_blueprint(main.bp)
    # Animals Blueprint
    app.register_blueprint(animals.bp)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
