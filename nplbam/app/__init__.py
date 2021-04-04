"""
Initializes and sets up the flask application.
"""

import logging
import os
from datetime import timedelta

from flask import Flask
from sqlalchemy.sql.expression import true

from . import config

UPLOAD_FOLDER = "/nplbam/files"
# Whether we want to be able to add mock data fast
DEBUG = 0
# Whether we want to be able to delete
DELETION = 1


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
    global DEBUG
    global DELETION
    app = Flask(__name__, instance_relative_config=True)
    # Set up folder for uploaded content
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # Set up logging
    gunicorn_logger: Logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Set debug mode to true CHANGE FOR PROD
    app.debug = False
    # Set testing mode to true CHANGE FOR PROD
    app.testing = False
    # Set the secret key from the config file
    app.secret_key = config.SECRET_KEY
    # Set the session lifetime
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    from . import (accounts, add_organization, animals, dashboard,
                   db_test_data, delete, edit_animal, edit_organization,
                   file_downloads, gallery, main, new_animal, options,
                   organizations, upload, view_animal, visualize)

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
    # Visualization Page
    app.register_blueprint(visualize.bp)
    # CSV page
    app.register_blueprint(upload.bp)
    if (DELETION == 1):
        # Delete Page
        app.register_blueprint(delete.bp)
    if (DEBUG == 1):
        # Test Data Page. Please Delete
        app.register_blueprint(db_test_data.bp)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
