import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('add_organization', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/add_organization")
def add_organization():
    """
    Form page for adding a new organization to the system.
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    
    return render_template("add_organization.html", title="Add Org")


@bp.route("/organization_added", methods=['GET', 'POST'])
def organization_added():
    """
    Route for getting the data from the form to put in the database
    """
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
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
    return redirect("/organizations")
