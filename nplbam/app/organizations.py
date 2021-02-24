import nacl.pwhash
from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('organizations', __name__, url_prefix="")

USER_LEVEL_MAX: int = 5


@bp.route("/organizations")
def organizations():
    """
    Page with the list of all organizations, which can be filtered.
    """
     # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        return redirect("/")
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    rescues_list = db_session.query(db.Rescues).all()
    pounds_list = db_session.query(db.Pounds).all()
    db_session.close()
    return render_template("organizations.html", title="Organizations", pounds=pounds_list, rescues=rescues_list)
