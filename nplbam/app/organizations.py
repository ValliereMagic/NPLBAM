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
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    rescues_list = db_session.query(db.Rescues).all()
    pounds_list = db_session.query(db.Pounds).all()
    db_session.close()
    return render_template("organizations.html", title="Organizations", pounds=pounds_list, rescues=rescues_list)
