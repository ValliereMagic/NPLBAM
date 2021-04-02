import csv
import io
import json
import os
import re
from datetime import date

from flask import (Blueprint, Response, current_app, flash, redirect,
                   render_template, request)
from flask import session as flask_session
from sqlalchemy.orm import Query, relationship, sessionmaker
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .db import db

bp = Blueprint('upload', __name__, url_prefix="")


@bp.route("/csv")
def upload():
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
        # Get list of animal types from json
    with open('nplbam/app/jsons/animal_species.json') as json_file:
        animal_types = json.load(json_file)

    return render_template("csv.html", role=user_level, title="CSV", animal_types=animal_types)


@bp.route("/submit_csv", methods=['POST', 'GET'])
def submit_csv():
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        user_ID: int = flask_session.get("userID", default=None)
        if (user_ID is None):
            flash("Not logged in")
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
            flash("Could not find Animal Type")
            return redirect("/")

        # Open the JSON with the questions for dog
        with open(json_location) as json_file:
            questions = json.load(json_file)

        # Get Downloaded File
        file = FileStorage(request.files['csv_file'])
        # Check if file exists
        if file.filename == '':
            flash("No File Given")
            return redirect("/")

        # Save the File

        server_filename: str = secure_filename(file.filename)
        # If the files directory doesn't exist... create it.
        if not os.path.exists(current_app.config["UPLOAD_FOLDER"]):
            os.makedirs(current_app.config["UPLOAD_FOLDER"])
        # save the file to the filesystem
        file.save(os.path.join(
            current_app.config["UPLOAD_FOLDER"], server_filename))

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Read from the file
        with open(os.path.join(current_app.config["UPLOAD_FOLDER"], server_filename), "r") as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)

            for x in csv_data:
                new = db.Animals(creator=user_ID,
                                 stage=1, stageDate=date.today(), animalType=given_type,
                                 name=x["Name"])
                db_session.add(new)
                db_session.flush()
                # Complete Stage 1 - 1
                initial_stage = db.StageInfo(animalID=new.animalID,
                                             stageNum=1,
                                             substageNum=1,
                                             completionDate=date.today(),
                                             note="Completed by CSV")
                db_session.add(initial_stage)
                # Go through the questions
                for group in questions:
                    for subgroup in group["subgroups"]:
                        for question in subgroup["questions"]:
                            # Save the Question Label here
                            q_label = question["label"]
                            # Check to see what type of question it was since they go into different tables
                            if question["type"] == "text":
                                if q_label != "Name":
                                    db_session.add(db.IntakeTextAnswers(
                                        animalID=new.animalID,
                                        questionName=question["name"],
                                        answer=x[q_label]))
                            elif question["type"] == "textarea":
                                db_session.add(db.IntakeTextAnswers(
                                    animalID=new.animalID,
                                    questionName=question["name"],
                                    answer=x[q_label]))
                            elif question["type"] == "radio":
                                i = 0
                                for radios in question["answers"]:
                                    if (radios["label"] == x[q_label]):
                                        db_session.add(db.IntakeRadioAnswers(
                                            animalID=new.animalID,
                                            questionName=question["name"],
                                            answer=i))
                                    else:
                                        i += 1
                            elif question["type"] == "checkbox":
                                check_list = x[q_label].split(", ")
                                for answer in question["answers"]:
                                    check = False
                                    for element in check_list:
                                        if (element == answer["label"]):
                                            check = True
                                    db_session.add(db.IntakeCheckboxAnswers(
                                        animalID=new.animalID,
                                        subQuestionName=answer["name"],
                                        answer=check))
                # Commit the animal to database
                db_session.commit()
            # Close the File
            f.close()
        db_session.close()
        # Delete the file from server. Do I deserve a biscuit?
        os.remove(os.path.join(
            current_app.config["UPLOAD_FOLDER"], server_filename))
        flash("Animals Added by CSV")
        current_app.logger.info("Some animals were added via "
                                "CSV by User ID: {}".format(flask_session["userID"]))
        return redirect("/")
