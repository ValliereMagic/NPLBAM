"""
This module deals with the creation of Pound and Rescue
Organizations in the system.
"""

import json
from datetime import date

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('add_organization', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/add_organization")
def add_organization():
    """
    Page URL: /add_organization
    Form page for adding a new organization to the system.
    """
    # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    return render_template("add_organization.html", role=user_level, title="Add Org")


@bp.route("/organization_added", methods=['GET', 'POST'])
def organization_added():
    """
    Page URL: /organization_added
    Route for getting the data from the form to put in the database
    """
    # Make sure the user's userLVL is in (0, 1)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect("/organizations")
        # Need to Add Data to database.
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Import tools for adding to meta table
        from .metatable_tools import (get_metainformation_record)

        # Get the most recent record (even if it needs to be created)
        meta_info = get_metainformation_record(db_session)

        # Make an object from our ORM
        # Get the name from the
        name: str = request.form['org_name']
        # check if they entered a rescue or a pound
        if (request.form["type"] == "0"):
            new = db.Rescues(rescueName=name)
            meta_info.rescues += 1
        else:
            new = db.Pounds(poundName=name)
            meta_info.pounds += 1
        # Add to the DB
        db_session.add(new)
        # Commit changes to the database
        db_session.commit()
        # Close the database like a good boy
        db_session.close()
        flash("Organization Added")
        current_app.logger.info("Organization: {} Added by UserID: {}".format(
            name, flask_session["userID"]))
    return redirect("/organizations")
