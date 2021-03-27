"""
This page deals with editing the entries of animals
previously entered into the system.
"""

import json
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from . import handle_file_operations
from .db import db

bp = Blueprint('edit_animal', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/edit_animal")
def edit_animal():
    """
    Page URL: /edit_animal
    Displays the current information about the animal, and allows
    the user to change it, and submit those changes.
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 3:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Check to see if proper Get Parameter
    editID = request.args.get('editid', default=None, type=int)
    if editID is None:
        flash("Invalid Animal ID")
        return redirect("/animals")

    # Open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Find the animal we are editting
    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=editID).first()

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
        flash("Could not find Animal Type")
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
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("edit_animal.html", animalID=editID, questions=questions,
                           title="Edit {}".format(animal_entry.name), predetermined=predetermined, species=animal_entry.animalType)

# Route to view animal page.


@bp.route("/animal_edited", methods=['POST', 'GET'])
def animal_edited():
    """
    Page URL: /animal_edited
    This is a subpage that receives the updated information from the animal edit page,
    and applies the user's changes to the database.
    It can redirect back to the calling page or to the edit animal page depending on which
    button was clicked.
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 3:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        # Get the species
        given_type = request.form['species']

        # Open Json with the different species
        with open('nplbam/app/jsons/animal_species.json') as json_file:
            species = json.load(json_file)

        # Get the location of the json for the given type of given type from the species json
        json_location = ""
        for entry in species:
            if (entry["name"] == given_type):
                json_location = "nplbam/app/jsons/" + entry["questions"]

        # If location is empty, then it must not be a correct type of species.
        if json_location == "":
            flash("Could not find animal type")
            return redirect("/")

        # Open the JSON with the questions for dog
        with open(json_location) as json_file:
            questions = json.load(json_file)

        # Need to Add Data to database.
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        user_ID = flask_session.get("userID", default=None)
        user_entry = db_session.query(
            db.Users).filter_by(userID=user_ID).first()
        # Update the Animal Entry
        animal = db_session.query(db.Animals).filter(
            db.Animals.animalID == request.form['animalId']).one()
        animal.name = request.form['name']
        # Go through the Json to get out find out which questions we asked
        for group in questions:
            for subgroup in group["subgroups"]:
                for question in subgroup["questions"]:
                    # Save the Question Name here
                    q_name = question["name"]
                    # Check to see what type of question it was since they go into different tables
                    if question["type"] == "text":
                        if q_name != "name":
                            db_session.query(db.IntakeTextAnswers).\
                                filter(db.IntakeTextAnswers.animalID == animal.animalID).\
                                filter(db.IntakeTextAnswers.questionName == q_name).\
                                update({"answer": request.form[q_name]})
                    elif question["type"] == "radio":
                        db_session.query(db.IntakeRadioAnswers).\
                            filter(db.IntakeRadioAnswers.animalID == animal.animalID).\
                            filter(db.IntakeRadioAnswers.questionName == q_name).\
                            update({"answer": request.form[q_name]})
                    elif question["type"] == "checkbox":
                        for answer in question["answers"]:
                            q_name = answer["name"]
                            if q_name in request.form:
                                db_session.query(db.IntakeCheckboxAnswers).\
                                    filter(db.IntakeCheckboxAnswers.animalID == animal.animalID).\
                                    filter(db.IntakeCheckboxAnswers.subQuestionName == q_name).\
                                    update({"answer": True})
                            else:
                                db_session.query(db.IntakeCheckboxAnswers).\
                                    filter(db.IntakeCheckboxAnswers.animalID == animal.animalID).\
                                    filter(db.IntakeCheckboxAnswers.subQuestionName == q_name).\
                                    update({"answer": False})
                    elif question["type"] == "textarea":
                        db_session.query(db.IntakeTextAnswers).\
                            filter(db.IntakeTextAnswers.animalID == animal.animalID).\
                            filter(db.IntakeTextAnswers.questionName == q_name).\
                            update({"answer": request.form[q_name]})
        # Commit changes to the database
        db_session.commit()
        # Handle file uploads
        errors: list = list()
        # Pull the uploaded file list from the form data
        uploaded_files_list: list = request.files.getlist("files[]")
        # Save the uploaded file, and add its metadata to the database
        handle_file_operations.save_uploaded_files(
            animal.animalID, uploaded_files_list, errors)
        # Close the database like a good boy
        db_session.close()
        flash("Animal information modified")
    return redirect("/animals")
