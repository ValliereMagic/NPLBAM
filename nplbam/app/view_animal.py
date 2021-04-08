"""
This module deals with displaying all of the animals in the system
to the user in a highly detailed way, and in a form that the user
cannot edit.
"""

import json
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('view_animal', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/view_animal")
def view_animal():
    """
    Page URL: /view_animal
    Page to see all the information filled out in the form
    """
    # Check if they are logged in
    user_level: int = flask_session.get("userLVL", default=None)
    if (user_level is None):
        flash("Not authorized")
        return redirect("/")

    # Get User ID
    user_id: int = flask_session.get("userID", default=None)
    # Make sure user ID is valid
    if user_id is None:
        flash('Not logged in')
        return redirect("/")

    # Check to see if proper Get Parameter
    viewID = request.args.get('viewid', default=None, type=int)
    if viewID is None:
        flash("No animal selected")
        return redirect("/animals")

    # Open the database session
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Find the entry matching the ID
    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=viewID).first()

    # Check if user is a rescue
    if (user_level > 3):
        # Find the user
        user_entry = db_session.query(
            db.Users).filter_by(userID=user_id).first()
        # Check if they should have access
        if (animal_entry.rescueID != user_entry.rescueID):
            flash("Not Authorized")
            return redirect("/animals")
    # Check if user is a pound
    elif (user_level > 1):
        # Find the user
        user_entry = db_session.query(
            db.Users).filter_by(userID=user_id).first()
        # Check if they should have access
        if ((animal_entry.poundID != user_entry.poundID) and (animal_entry.creator != user_id)) or (animal_entry.stage > 3):
            flash("Not Authorized")
            return redirect("/animals")

    # Open Json with the different species
    with open('nplbam/app/jsons/animal_species.json') as json_file:
        species = json.load(json_file)

    # Get the location of the json for the given type of given type from the species json
    json_location = ""
    for entry in species:
        if (entry["name"] == animal_entry.animalType):
            json_location = "nplbam/app/jsons/" + entry["questions"]

    # If location is empty, then it must not be a correct type of species.
    if json_location == "":
        flash("Animal type not found")
        return redirect("/")

    # Open the JSON with the questions for dog
    with open(json_location) as json_file:
        questions = json.load(json_file)

    # Get a list of all the predetermined answers stored in the relationship
    predetermined = {}
    predetermined["name"] = animal_entry.name
    for x in animal_entry.radioAnswers:
        predetermined[x.questionName] = x.answer
    for x in animal_entry.checkBoxAnswers:
        predetermined[x.subQuestionName] = x.answer
    for x in animal_entry.textAnswers:
        predetermined[x.questionName] = x.answer
    # Close the database like a good boy
    db_session.close()
    # Create a view string of the animal for easy copying and pasting.
    # Create a list of strings and add to the back of the list
    string_list = []
    string_list.append('Name: "{}"\nSpecies: "{}"\n'.format(
        animal_entry.name, animal_entry.animalType))
    # Go through each of the steps of the questions
    for step in questions:
        # Go through each of the subgroups of each step
        for subgroup in step["subgroups"]:
            # Display the subgroup
            string_list.append("\n{}".format(subgroup["name"]))
            # Go through each question
            for question in subgroup["questions"]:
                # If its first in the list, don't put a ,
                string_list.append("\n")
                # Check each type of question
                if question["type"] == "radio":
                    i = 0
                    # Go through each of the answers
                    for answer in question["answers"]:
                        # Check if this is what they answered
                        if (predetermined[question["name"]] == i):
                            string_list.append(' {}: {}'.format(
                                question["label"], answer["label"]))
                        i += 1
                # Go through text types
                elif question["type"] == "text":
                    # Name was already displayed
                    if (question["label"] != "Name"):
                        # Don't display empty areas.
                        if (predetermined[question["name"]] != ""):
                            string_list.append(' {}: {}'.format(
                                question["label"], predetermined[question["name"]]))
                        else:
                            string_list.pop(-1)
                    # Since name was taken out, we don't need next new line
                    else:
                        string_list.pop(-1)
                # Go through each textarea
                elif question["type"] == "textarea":
                    string_list.append(' {}: {}'.format(
                        question["label"], predetermined[question["name"]]))
                # Type if checkbox
                elif question["type"] == "checkbox":
                    string_list.append(' {}: '.format(question["label"]))
                    # Check variable to see if we need a comma before
                    check = True
                    # Only display the boxes that were checked
                    for answer in question["answers"]:
                        if (predetermined[answer["name"]] == True):
                            if check == True:
                                check = False
                            else:
                                string_list.append(", ")
                            string_list.append('{}'.format(answer["label"]))
                    string_list.append('')
            # Add a \n to end the subgroup
            string_list.append("\n")
    # Compile into single string.
    view_string = ''.join(string_list)
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("view_animal.html", animalID=viewID,
                           role=user_level,
                           questions=questions,
                           title="View {}".format(animal_entry.name),
                           predetermined=predetermined,
                           view_string=view_string,
                           species=animal_entry.animalType)


@bp.route("/animal_viewed", methods=['POST', 'GET'])
def animal_viewed():
    """
    Page URL: /animal_viewed
    This is a subpage that is used to get the button click from the animal view page.
    Can redirect back to the calling page or to the edit animal page depending on which
    button was clicked.
    """
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        # If they clicked edit, redirect to edit page
        if 'edit' in request.form:
            id: str = request.form['animalId']
            redir = "/edit_animal?editid={}".format(id)
            return redirect(redir)
        # Else return to main page
        else:
            redirect("/animals")
    return redirect("/animals")
