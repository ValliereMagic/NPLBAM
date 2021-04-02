"""
This module deals with the display of all the organizations
that currently exist within the system.
"""

import nacl.pwhash
from flask import Blueprint, flash, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('organizations', __name__, url_prefix="")

USER_LEVEL_MAX: int = 5


@bp.route("/organizations", methods=['POST', 'GET'])
def organizations():
    """
    Page URL: /organizations
    Page with the list of all organizations, which can be filtered.
    """
    # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    predetermined = {}
    # Get Post Params
    if request.method == 'POST':
        predetermined["search_by"] = request.form['searchBy']
        predetermined["search"] = request.form['searchText']
        predetermined["display"] = (int)(request.form['display'])
        # If its an ID we're searching for make sure its an int
        if ((predetermined["search_by"] == "animalID") or (predetermined["search_by"] == "stage")) and \
                (predetermined["search"] != ""):
            try:
                predetermined["search"] = int(predetermined["search"])
            except ValueError:
                predetermined["search"] = ""
    # Otherwise make defaults
    else:
        predetermined["search_by"] = str(
            request.args.get('search_by', "name"))
        predetermined["display"] = request.args.get('display', 0, type=int)
        predetermined["search"] = str(request.args.get('search', ""))
    rescues_list = {}
    pounds_list = {}
    # create engine for the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    if (predetermined["search"] != ""):
        search_text = "%{}%".format(predetermined["search"])
        if (predetermined["search_by"] == "name"):
            if (predetermined["display"] != 2):
                rescues_list = db_session.query(db.Rescues).\
                    filter(db.Rescues.rescueName.ilike(search_text)).all()
            if (predetermined["display"] != 1):
                pounds_list = db_session.query(db.Pounds).\
                    filter(db.Pounds.poundName.ilike(search_text)).all()
        else:
            if (predetermined["display"] != 2):
                rescues_list = db_session.query(db.Rescues).\
                    filter(db.Rescues.rescueID.ilike(search_text)).all()
            if (predetermined["display"] != 1):
                pounds_list = db_session.query(db.Pounds).\
                    filter(db.Pounds.poundID.ilike(search_text)).all()
    else:
        if (predetermined["display"] != 2):
            rescues_list = db_session.query(db.Rescues).all()
        if (predetermined["display"] != 1):
            pounds_list = db_session.query(db.Pounds).all()

    db_session.close()
    return render_template("organizations.html", role=user_level, title="Organizations", pounds=pounds_list,
                           rescues=rescues_list, predetermined=predetermined)
