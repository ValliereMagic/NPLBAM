"""
This module deals with the display of uploaded files for
stored animals, as well as advancing animals through the stages.
"""

import json
from datetime import date

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
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
    Page URL: /gallery
    Page to view images and and limited information associated with animal
    """
    # Check if they are logged in
    user_level: int = flask_session.get("userLVL", default=None)
    if (user_level is None) or user_level > 1:
        flash("Not authorized")
        return redirect("/")

    # Check to see if proper Get Parameter
    viewID = request.args.get('viewid', default=None, type=int)
    if viewID is None:
        flash("Incorrect animal ID")
        return redirect("/animals")

    # Open the database.
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    animal_entry = db_session.query(
        db.Animals).filter_by(animalID=viewID).first()

    # Get a dictionary for required information
    info = {}

    info["name"] = animal_entry.name
    info["species"] = animal_entry.animalType
    info["stage"] = animal_entry.stage
    info["creator"] = db_session.query(db.Users).filter_by(
        userID=animal_entry.creator).first().username
    if animal_entry.supervisor is None:
        info["supervisor"] = -1
    else:
        info["supervisor"] = animal_entry.supervisor

    if animal_entry.poundID is None:
        info["pound"] = -1
    else:
        info["pound"] = animal_entry.poundID

    if animal_entry.rescueID is None:
        info["rescue"] = -1
    else:
        info["rescue"] = animal_entry.rescueID

    info["notes"] = animal_entry.notes
    info["days"] = (date.today() - animal_entry.stageDate).days

    rescues_list = db_session.query(db.Rescues).all()
    pounds_list = db_session.query(db.Pounds).all()
    supervisor_list = db_session.query(
        db.Users).filter(db.Users.userLVL < 2).all()

    # get list of filenames
    images = {}
    for x in animal_entry.files:
        images[x.fileName] = x.fileType

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
    return render_template("gallery.html", animalID=viewID, role=user_level, title="View {}".format(animal_entry.name), info=info,
                           images=images, current_stage=animal_entry.stage, stage_info=stage_info, rescues=rescues_list, pounds=pounds_list, supervisors=supervisor_list)


@bp.route("/stage_updated", methods=['GET', 'POST'])
def stage_updated():
    """
    Route for adding stage info to database
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        # Get animalID
        animalID: int = request.form['animalID']
        # Get stage number
        stageNum: int = int(request.form['stage'])
        # Get substage number
        substages = [int(i) for i in request.form.getlist("substage")]
        # Get notes
        notes = request.form.getlist("notes")
        # Get todays date
        completionDate: date = date.today()

        # Meta table only needs for stage 8
        if (stageNum == 8):
            # Import tools for adding to meta table
            from .metatable_tools import (get_metainformation_record)

            # Get the most recent record (even if it needs to be created)
            meta_info = get_metainformation_record(db_session)

        # If go through each substage in form and if it is new add it otherwise update it
        for substageNum in substages:
            substage = db_session.query(db.StageInfo).filter_by(
                animalID=animalID, stageNum=stageNum, substageNum=substageNum).first()
            if substage is None:
                new = db.StageInfo(animalID=animalID, stageNum=stageNum, substageNum=substageNum,
                                   completionDate=completionDate, note=notes[substageNum - 1])
                # Add a stage to the record
                db_session.add(new)
                # If stage 8, Set the meta table for outcomes
                if (stageNum == 8):
                    if (substageNum == 1):
                        meta_info.totalOutcome1 += 1
                    elif (substageNum == 2):
                        meta_info.totalOutcome2 += 1
                    elif (substageNum == 3):
                        meta_info.totalOutcome3 += 1
                    elif (substageNum == 4):
                        meta_info.totalOutcome4 += 1
                    elif (substageNum == 5):
                        meta_info.totalOutcome5 += 1
            else:
                # Only update if new and old notes are different
                if str(notes[substageNum - 1]) != str(substage.note):
                    substage.note = notes[substageNum - 1]
                    substage.completionDate = completionDate

            db_session.commit()

        flash("Substages Updated")
        current_app.logger.info("Substages of animal ID: {} "
                                "edited by user ID: {}".format(
                                    animalID, flask_session["userID"]))

        # Also run this if "Complete Stage" button was pressed
        if 'complete' in request.form:
            # Get todays date
            today: date = date.today()
            animal = db_session.query(db.Animals).filter_by(
                animalID=animalID).first()
            # Import tools for adding to meta table
            from .metatable_tools import (get_metainformation_record)

            # Get the most recent record (even if it needs to be created)
            meta_info = get_metainformation_record(db_session)

            # Check which animal stage is currently is and put the meta info in
            if animal.stage == 1:
                meta_info.animalsCompStage1 += 1
                meta_info.totalDaysCompStage1 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 2:
                meta_info.animalsCompStage2 += 1
                meta_info.totalDaysCompStage2 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 3:
                meta_info.animalsCompStage3 += 1
                meta_info.totalDaysCompStage3 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 4:
                meta_info.animalsCompStage4 += 1
                meta_info.totalDaysCompStage4 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 5:
                meta_info.animalsCompStage5 += 1
                meta_info.totalDaysCompStage5 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 6:
                meta_info.animalsCompStage6 += 1
                meta_info.totalDaysCompStage6 += (date.today() -
                                                animal.stageDate).days
            elif animal.stage == 7:
                meta_info.animalsCompStage7 += 1
                meta_info.totalDaysCompStage7 += (date.today() -
                                                animal.stageDate).days

            # Determine and set the new stage number
            if animal.stage < 8:
                animal.stage += 1
            elif animal.stage > 8:
                animal.stage = 8
            animal_stage: int = animal.stage
            # Set the date
            animal.stageDate = today

            # Update the animal
            db_session.commit()

            flash("Stage Updated")
            current_app.logger.info("Animal ID: {} Updated to Stage: {} "
                                    "by user ID: {}".format(animalID, animal_stage, flask_session["userID"]))

        db_session.close()
    return redirect(f"/gallery?viewid={animalID}")


@bp.route("/gallery_info_updated", methods=['GET', 'POST'])
def gallery_info_updated():
    """
    Update animal information within the gallery page
    """
    # Make sure the user's userLVL is in (0, 1, 2, 3)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")
    # Make sure they got here with post
    if request.method == 'POST':
        # Get our params
        animalID: int = (int)(request.form['animalID'])
        pound: int = (int)(request.form['pound'])
        rescue: int = (int)(request.form['rescue'])
        supervisor: int = (int)(request.form['supervisor'])

        # Get the database engine and create a session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Get our animal from the database
        animal: db.Animals = db_session.query(db.Animals).filter_by(
            animalID=animalID).first()
        animal_name: str = animal.name
        # Update values
        animal.notes = request.form['notes']
        if (pound != -1):
            animal.poundID = pound
        # Check if rescue was set
        if (rescue != -1):
            animal.rescueID = rescue
        # Check if supervisor was set
        if (supervisor != -1):
            animal.supervisor = supervisor
        db_session.commit()
        db_session.close()
    flash("Info updated")
    current_app.logger.info("Information for animal: {} "
                            "updated by user ID: {}".format(animal_name, flask_session["userID"]))
    return redirect(f"/gallery?viewid={animalID}")
