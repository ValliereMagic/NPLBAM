from flask import render_template, Blueprint, session as flask_session, redirect
import json
bp = Blueprint('new_animal', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/new_animal")
def new_animal():
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Open the JSON with the questions for dog
    with open('nplbam/app/jsons/dog_questions.json') as json_file:
        questions = json.load(json_file)
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("add_animal.html", questions=questions,  title="Add Dog")


""" Route for getting the data from the form to put in the database """
@bp.route("/animal_added", methods=['GET', 'POST'])
def animal_added():
    # Need to Add Data to database.
    return redirect("/animals")
