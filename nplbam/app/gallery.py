import json
from datetime import date

from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import null

from .db import db

bp = Blueprint('gallery', __name__, url_prefix="")


# Route to view animal page.
@bp.route("/gallery")
def gallery():
    """
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

    # get stage info from database
    stage_entry = db_session.query(db.StageInfo).filter_by(
        animalID=viewID).order_by(getattr(db.StageInfo, "stageNum"))

    stage_info = {}
    # go through all the stages and add them to stage_info
    for x in stage_entry:
        stage_info[f"{x.stageNum}:{x.substageNum}"] = (
            x.note, x.completionDate)

    # Close the database like a good boy
    db_session.close()

    # Render the page
    return render_template("gallery.html", animalID=viewID, title="View {}".format(animal_entry.name), info=info, images=images, current_stage=animal_entry.stage, stage_info=stage_info)


@bp.route("/stage_updated", methods=['GET', 'POST'])
def stage_updated():
    """
    Route for adding stage info to database
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
            print("good to go")
            engine = db.get_db_engine()
            db_session = (sessionmaker(bind=engine))()
            # Get animalID
            animalID: int = request.form['animalID']
            # Get stage number
            stageNum: int = request.form['stage']
            # Get substage number
            substages = [int(i) for i in request.form.getlist("substage")]
            # Get notes
            notes = request.form.getlist("notes")
            # Get todays date
            completionDate: date = date.today()
            # If go through each substage in form and if it is new add it otherwise update it
            for substageNum in substages:
                substage = db_session.query(db.StageInfo).filter_by(
                    animalID=animalID, stageNum=stageNum, substageNum=substageNum).first()
                if substage is None:
                    new = db.StageInfo(animalID=animalID, stageNum=stageNum, substageNum=substageNum,
                                       completionDate=completionDate, note=notes[substageNum - 1])
                    db_session.add(new)
                else:
                    substage.note = notes[substageNum - 1]
                    substage.completionDate = completionDate

                db_session.commit()
            db_session.close()

    return redirect(f"/gallery?viewid={animalID}")


@bp.route("/stage_completed", methods=['GET', 'POST'])
def stage_completed():
    """
    Route for incrementing stage number in the Animals table
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
            engine = db.get_db_engine()
            db_session = (sessionmaker(bind=engine))()

            # Get animalID from form
            animalID: int = request.form['animalID']
            # Get todays date
            today: date = date.today()
            # Get the correct animal from the database
            animal = db_session.query(db.Animals).filter_by(
                animalID=animalID).first()

            # Determine and set the new stage number
            if animal.stage < 8:
                animal.stage += 1
            elif animal.stage > 8:
                animal.stage = 8
            # Set the date
            animal.stageDate = today

            # Update the animal
            db_session.commit()
            db_session.close()

    return redirect(f"/gallery?viewid={animalID}")
