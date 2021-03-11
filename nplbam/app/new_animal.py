"""
This module deals with adding a new animal to the system.
"""

import json
from datetime import date

from flask import Blueprint, current_app, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from . import handle_file_operations
from .db import db

bp = Blueprint('new_animal', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/new_animal", methods=['GET', 'POST'])
def new_animal():
    """
    Page URL: /new_animal
    Form page for adding a new animal to the system.
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 3:
        # May need to change where we redirect them in the future
        return redirect("/")
    # Make sure they got here through post
    if request.method != 'POST':
        return redirect("/")
    # Get post Param
    given_type = request.form['type']

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
        return redirect("/")

    # Open the JSON with the questions for dog
    with open(json_location) as json_file:
        questions = json.load(json_file)
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("add_animal.html", questions=questions,  title="Add Animal", species=given_type)


@bp.route("/animal_added", methods=['GET', 'POST'])
def animal_added():
    """
    Page URL: /animal_added
    Receives the data from the new_animal page and adds it to the database.
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 3:
        # May need to change where we redirect them in the future
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        if 'cancel' in request.form:
            redirect("/animals")
        else:
            if ('save' in request.form):
                animal_stage = 0
            else:
                animal_stage = 1

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
            # Add the Animal Entry
            # Make an object from our ORM
            name: str = request.form['name']
            new = db.Animals(poundID=user_entry.poundID, stage=animal_stage, creator=user_ID,
                             stageDate=date.today(), animalType=given_type, name=name)
            db_session.add(new)
            # Flush the session so we can get the autoincremented ID in new.animalID
            db_session.flush()
            db_session.add(db.StageInfo(animalID=new.animalID,
                                        stageNum=1,
                                        substageNum=0,
                                        completionDate=date.today(),
                                        note="Created by user # {}".format(user_entry.userID)))
            # Go through the Json to get out find out which questions we asked
            for group in questions:
                for subgroup in group["subgroups"]:
                    for question in subgroup["questions"]:
                        # Save the Question Name here
                        q_name = question["name"]
                        # Check to see what type of question it was since they go into different tables
                        if question["type"] == "text":
                            if q_name != "name":
                                db_session.add(db.IntakeTextAnswers(
                                    animalID=new.animalID,
                                    questionName=q_name,
                                    answer=request.form[q_name]))
                        elif question["type"] == "radio":
                            db_session.add(db.IntakeRadioAnswers(
                                animalID=new.animalID,
                                questionName=q_name,
                                answer=request.form[q_name]))
                        elif question["type"] == "checkbox":
                            for answer in question["answers"]:
                                q_name = answer["name"]
                                if q_name in request.form:
                                    db_session.add(db.IntakeCheckboxAnswers(
                                        animalID=new.animalID,
                                        subQuestionName=q_name,
                                        answer=True))
                                else:
                                    db_session.add(db.IntakeCheckboxAnswers(
                                        animalID=new.animalID,
                                        subQuestionName=q_name,
                                        answer=False))
                        elif question["type"] == "textarea":
                            db_session.add(db.IntakeTextAnswers(
                                animalID=new.animalID,
                                questionName=q_name,
                                answer=request.form[q_name]))
            # Commit changes to the database
            db_session.commit()
            # Handle file uploads
            errors: list = list()
            # Pull the uploaded file list from the form data
            uploaded_files_list: list = request.files.getlist("files[]")
            # Save the uploaded file, and add its metadata to the database
            handle_file_operations.save_uploaded_files(
                new.animalID, uploaded_files_list, errors)
            # Close the database like a good boy
            db_session.close()
    return redirect("/animals")
