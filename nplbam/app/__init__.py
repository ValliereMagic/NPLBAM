import logging
import os

from flask import Flask

from . import config


def create_app():
    """
    Create and configure the Flask application
    in factory style.
    """
    app = Flask(__name__, instance_relative_config=True)
    # Set up logging
    gunicorn_logger: Logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Set debug mode to true CHANGE FOR PROD
    app.debug = True
    # Set testing mode to true CHANGE FOR PROD
    app.testing = True
    # Set the secret key from the config file
    app.secret_key = config.SECRET_KEY
    from . import accounts, animals, main, new_animal, view_animal, edit_animal, dashboard

    # Index Blueprint
    app.register_blueprint(main.bp)
    # Animals Blueprint
    app.register_blueprint(animals.bp)
    # New Animal Blueprint
    app.register_blueprint(new_animal.bp)
    # Edit Animal Blueprint
    app.register_blueprint(edit_animal.bp)
    # View Animal Blueprint
    app.register_blueprint(view_animal.bp)
    # Accounts Blueprint
    app.register_blueprint(accounts.bp)
    # Dashboard Blueprint
    app.register_blueprint(dashboard.bp)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
