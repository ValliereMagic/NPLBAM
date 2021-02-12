import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('new_animal', __name__, url_prefix="")


# Route for the new animal page.
@bp.route("/new_animal")
def new_animal():
    """
    Form page for adding a new animal to the system.
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Open the JSON with the questions for dog
    with open('nplbam/app/jsons/dog_questions.json') as json_file:
        questions = json.load(json_file)
    # Create the form page dynamically using the add_animal template and the questions
    return render_template("add_animal.html", questions=questions,  title="Add Dog")


@bp.route("/animal_added", methods=['GET', 'POST'])
def animal_added():
    """
    Route for getting the data from the form to put in the database
    """
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        # Open the JSON with the questions for dog
        with open('nplbam/app/jsons/dog_questions.json') as json_file:
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
        new = db.Animals(poundID=user_entry.poundID, stage=1, creator=user_ID,
                         stageDate=date.today(), animalType="Dog", name=name)
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
        # Close the database like a good boy
        db_session.close()
    return redirect("/animals")
