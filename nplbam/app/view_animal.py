"""
This module deals with displaying all of the animals in the system
to the user in a highly detailed way, and in a form that the user
cannot edit.
"""

import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('view_animal', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/view_animal")
def view_animal():
    """
    Page URL: /view_animal
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
        predetermined[x.subQuestionName] = x.answer
    for x in animal_entry.textAnswers:
        predetermined[x.questionName] = x.answer
    # Close the database like a good boy
    db_session.close()
    # Create a view string of the animal for easy copying and pasting.
    # Create a list of strings and add to the back of the list
    string_list = []
    string_list.append('Name: "{}", Species: "{}"'.format(
        animal_entry.name, animal_entry.animalType))
    # Go through each of the steps of the questions
    for step in questions:
        # Go through each of the subgroups of each step
        for subgroup in step["subgroups"]:
            # Display the subgroup
            string_list.append("  {} [".format(subgroup["name"]))
            check = True
            # Go through each question
            for question in subgroup["questions"]:
                # If its first in the list, don't put a ,
                if (check == True):
                    check = False
                else:
                    string_list.append(",")
                # Check each type of question
                if question["type"] == "radio":
                    i = 0
                    # Go through each of the answers
                    for answer in question["answers"]:
                        # Check if this is what they answered
                        if (predetermined[question["name"]] == i):
                            string_list.append(' {}: "{}"'.format(
                                question["label"], answer["label"]))
                        i += 1
                # Go through text types
                elif question["type"] == "text":
                    # Name was already displayed
                    if (question["label"] != "Name"):
                        # Don't display empty areas.
                        if (predetermined[question["name"]] != ""):
                            string_list.append(' {}: "{}"'.format(
                                question["label"], predetermined[question["name"]]))
                        else:
                            string_list.pop(-1)
                    # Since name was taken out, we don't need next comma
                    else:
                        check = True
                # Go through each textarea
                elif question["type"] == "textarea":
                    string_list.append(' {}: "{}"'.format(
                        question["label"], predetermined[question["name"]]))
                # Type if checkbox
                elif question["type"] == "checkbox":
                    string_list.append(' {}:"'.format(question["label"]))
                    check = True
                    # Only display the boxes that were checked
                    for answer in question["answers"]:
                        if (predetermined[answer["name"]] == True):
                            if check == True:
                                check = False
                            else:
                                string_list.append(" ")
                            string_list.append('{}'.format(answer["label"]))
                    string_list.append('"')
            # Add a ] to end the subgroup
            string_list.append("]")
    # Compile into single string.
    view_string = ''.join(string_list)
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("view_animal.html", animalID=viewID,
                           questions=questions,
                           title="View {}".format(animal_entry.name),
                           predetermined=predetermined,
                           view_string=view_string)

# Route to view animal page.


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
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        if 'edit' in request.form:
            id: str = request.form['animalId']
            redir = "/edit_animal?editid={}".format(id)
            return redirect(redir)
        else:
            redirect("/animals")
    return redirect("/animals")
