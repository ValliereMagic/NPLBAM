"""
This module deals with the display of uploaded files for
stored animals, as well as advancing animals through the stages.
"""

import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('gallery', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/gallery")
def gallery():
    """
    Page URL: /gallery
    Page to view images and and limited information associated with animal
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")

    # Check to see if proper Get Parameter
    viewID = request.args.get('viewid', default=None, type=int)
    if viewID is None:
        return redirect("/animals")

    # Open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=viewID).first()

    # Get a dictionary for required information
    info = {}

    info["name"] = animal_entry.name
    info["stage"] = animal_entry.stage
    info["days"] = (date.today() - animal_entry.stageDate).days

    for x in animal_entry.textAnswers:
        info[x.questionName] = x.answer

    # get list of filenames
    images = []
    for x in animal_entry.files:
        images.append(x.fileName)

    # Close the database like a good boy
    db_session.close()

    # Render the page
    return render_template("gallery.html", animalID=viewID, title="View {}".format(animal_entry.name), info=info, images=images)
