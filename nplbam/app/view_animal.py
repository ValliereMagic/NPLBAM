import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('view_animal', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/view_animal")
def new_animal():
    """
    Page to see all the information filled out
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")

    # Check to see if proper Get Parameter
    viewID = request.args.get('viewid', default=None, type=int)
    if viewID is None:
        return redirect("/animals")

    # Open the JSON with the questions for dog
    with open('nplbam/app/jsons/dog_questions.json') as json_file:
        questions = json.load(json_file)

    # Open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=viewID).first()
    # Get a list of all the predetermined answers stored in the relationship
    predetermined = {}
    predetermined["name"] = animal_entry.name
    for x in animal_entry.radioAnswers:
        predetermined[x.questionName] = x.answer
    for x in animal_entry.checkBoxAnswers:
        predetermined[x.subQuesitonName] = x.answer
    for x in animal_entry.textAnswers:
        predetermined[x.questionName] = x.answer
    # Close the database like a good boy
        db_session.close()
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("view_animal.html", questions=questions, title="View {}".format(animal_entry.name), predetermined=predetermined)

# Route to view animal page.


@bp.route("/animal_viewed", methods=['POST', 'GET'])
def animal_viewed():
    """
    This is a subpage that is used to get the button click from the animal view page.
    Can redirect back to the calling page or to the edit animal page depending on which
    button was clicked.
    """
    return redirect("/animals")
