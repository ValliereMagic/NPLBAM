"""
Initializes and sets up the flask application.
"""

import logging
import os

from flask import Flask

from . import config

UPLOAD_FOLDER = "/nplbam/files"


def create_app():
    """
    Create and configure the Flask application
    in factory style.

    Things that are configured here:
     - The location for uploaded files (UPLOAD_FOLDER constant)
     - The logger for gunicorn
     - Whether the application is in debug mode or in production mode
     - The blueprints for all the pages

    :return: The Flask app configured in this function.
    """
    global UPLOAD_FOLDER
    app = Flask(__name__, instance_relative_config=True)
    # Set up folder for uploaded content
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    from . import (accounts, add_organization, animals, dashboard,
                   db_test_data, edit_animal, edit_organization,
                   file_downloads, gallery, main, new_animal, options,
                   organizations, view_animal)

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
    # Organizations Blueprint
    app.register_blueprint(organizations.bp)
    # Add Organization
    app.register_blueprint(add_organization.bp)
    # Edit Organization
    app.register_blueprint(edit_organization.bp)
    # File Downloads
    app.register_blueprint(file_downloads.bp)
    # Gallery
    app.register_blueprint(gallery.bp)
    # Options
    app.register_blueprint(options.bp)
    # Test Data Page. Please Delete
    app.register_blueprint(db_test_data.bp)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
