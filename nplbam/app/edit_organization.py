import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('edit_organization', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/edit_organization")
def edit_organization():
    """
    Form page for adding a new organization to the system.
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    
    # Check to see if proper Get Parameter
    editID = request.args.get('editid', default=None, type=int)
    orgType = request.args.get('type', default=None, type=int)
    # Make sure both are there
    if editID is None or orgType is None:
        return redirect("/organizations")

    # Need open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Get the information on the org
    predetermined = {}
    if (orgType == 0):
        predetermined["type"] = "rescue"
        organization = db_session.query(db.Rescues).filter(db.Rescues.rescueID == editID).one()
        predetermined["name"] = organization.rescueName
    else:
        predetermined["type"] = "pound"
        organization = db_session.query(db.Pounds).filter(db.Pounds.poundID == editID).one()
        predetermined["name"] = organization.poundName

    # Close the database like a good boy
    db_session.close()    

    # Make the page using said information
    return render_template("edit_organization.html", title="Edit Org", orgID=editID, predetermined=predetermined)


@bp.route("/organization_edited", methods=['GET', 'POST'])
def organization_edited():
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
        elif 'delete' in request.form:
            # Still need to do
            return redirect("/organizations")    
        
        # Need open the database.
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        # Make an object from our ORM
        # Get the name from the
        name: str = request.form['org_name']
        # check if they entered a rescue or a pound
        if (request.form["orgType"] == "rescue"):
            organization = db_session.query(db.Rescues).filter(db.Rescues.rescueID == request.form['orgID']).one()
            organization.rescueName = name
        else:
            organization = db_session.query(db.Pounds).filter(db.Pounds.poundID == request.form['orgID']).one()
            organization.poundName = name
        # Commit changes to the database
        db_session.commit()
        # Close the database like a good boy
        db_session.close()
    return redirect("/organizations")
