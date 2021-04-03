"""
This module deals with downloading files
that have been previously uploaded to the system.
"""

from werkzeug.http import http_date
from functools import update_wrapper, wraps
from datetime import datetime

from flask import Blueprint, current_app, redirect, send_from_directory, make_response
from flask import session as flask_session

bp = Blueprint('downloads', __name__, url_prefix="")


def nocache(view):
    """
    Wrapper to make it so what it is wrapped around will not be cached.
    """
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = http_date(datetime.now())
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@bp.route('/downloads/<filename>')
def download_file(filename: str):
    """
    Page URL: /downloads/<filename>
    Supplies the requested filename to the user if they are logged
    in, and have the correct permissions.
    """
    # THESE PERMISSIONS WILL LIKELY NEED TO BE UPDATED
    # AND TAKE THINGS INTO ACCOUNT LIKE USER WHO UPLOADED THE FILE
    # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        return redirect("/")
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/cacheless_downloads/<filename>')
@nocache
def cacheless_downloads(filename: str):
    """
    Page URL: /cacheless_downloads/<filename>
    Supplies the requested filename to the user if they are logged
    in, and have the correct permissions. Will send http header to 
    not cache the file.
    """
    # THESE PERMISSIONS WILL LIKELY NEED TO BE UPDATED
    # AND TAKE THINGS INTO ACCOUNT LIKE USER WHO UPLOADED THE FILE
    # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        return redirect("/")
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
