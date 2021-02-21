from flask import Blueprint, current_app, redirect, send_from_directory
from flask import session as flask_session

bp = Blueprint('downloads', __name__, url_prefix="")


@bp.route('/downloads/<filename>')
def download_file(filename: str):
    # THESE PERMISSIONS WILL LIKELY NEED TO BE UPDATED
    # AND TAKE THINGS INTO ACCOUNT LIKE USER WHO UPLOADED FILE
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 3:
        return redirect("/")
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
