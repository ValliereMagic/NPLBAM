"""
This module deals with the creation of Pound and Rescue
Organizations in the system.
"""

import json
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request
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

    return render_template("add_organization.html", title="Add Org")


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
        # Make an object from our ORM
        # Get the name from the
        name: str = request.form['org_name']
        # check if they entered a rescue or a pound
        if (request.form["type"] == "0"):
            new = db.Rescues(rescueName=name)
        else:
            new = db.Pounds(poundName=name)
        # Add to the DB
        db_session.add(new)
        # Commit changes to the database
        db_session.commit()
        # Close the database like a good boy
        db_session.close()
        flash("Organization Added")
    return redirect("/organizations")
