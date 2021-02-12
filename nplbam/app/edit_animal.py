import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker

from .db import db

bp = Blueprint('edit_animal', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/edit_animal")
def edit_animal():
    """
    Page to see all the information filled out
    """
    # Check if they are logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")

    # Check to see if proper Get Parameter
    editID = request.args.get('editid', default=None, type=int)
    if editID is None:
        return redirect("/animals")

    # Open the JSON with the questions for dog
    with open('nplbam/app/jsons/dog_questions.json') as json_file:
        questions = json.load(json_file)

    # Open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=editID).first()
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
    return render_template("edit_animal.html", animalID=editID, questions=questions, title="Edit {}".format(animal_entry.name), predetermined=predetermined)

# Route to view animal page.


@bp.route("/animal_edited", methods=['POST', 'GET'])
def animal_edited():
    """
    This is a subpage that is used to get the button click from the animal view page.
    Can redirect back to the calling page or to the edit animal page depending on which
    button was clicked.
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
        user_entry = db_session.query(db.Users).filter_by(userID=user_ID).first()   
        # Update the Animal Entry 
        animal = db_session.query(db.Animals).filter(db.Animals.animalID == request.form['animalId']).one()
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
                                filter(db.IntakeTextAnswers.animalID ==  animal.animalID).\
                                filter(db.IntakeTextAnswers.questionName == q_name).\
                               update({"answer": request.form[q_name]})                                    
                    elif question["type"] == "radio":
                        db_session.query(db.IntakeRadioAnswers).\
                            filter(db.IntakeRadioAnswers.animalID ==  animal.animalID).\
                            filter(db.IntakeRadioAnswers.questionName == q_name).\
                            update({"answer": request.form[q_name]})                                    
                    elif question["type"] == "checkbox":
                        for answer in question["answers"]:
                            q_name = answer["name"]
                            if q_name in request.form:
                                db_session.query(db.IntakeCheckboxAnswers).\
                                    filter(db.IntakeCheckboxAnswers.animalID ==  animal.animalID).\
                                    filter(db.IntakeCheckboxAnswers.subQuestionName == q_name).\
                                    update({"answer": True})                                    
                            else:
                                db_session.query(db.IntakeCheckboxAnswers).\
                                    filter(db.IntakeCheckboxAnswers.animalID ==  animal.animalID).\
                                    filter(db.IntakeCheckboxAnswers.subQuestionName == q_name).\
                                    update({"answer": False})                                    
                    elif question["type"] == "textarea":
                        db_session.query(db.IntakeTextAnswers).\
                            filter(db.IntakeTextAnswers.animalID ==  animal.animalID).\
                            filter(db.IntakeTextAnswers.questionName == q_name).\
                            update({"answer": request.form[q_name]})        
        # Commit changes to the database
        db_session.commit()
        # Close the database like a good boy
        db_session.close()
    return redirect("/animals")
