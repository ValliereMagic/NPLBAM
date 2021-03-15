import csv
import json
import random
import time
from datetime import date, timedelta

import nacl.pwhash
from flask import Blueprint, redirect, render_template, request
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean, String

from .db import db

bp = Blueprint('db_test_data', __name__, url_prefix="")

# Can be deleted in production


@bp.route("/test_data")
def test_data():
    random.seed(int(round(time.time()*10000)))
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    # Definately not an initial user
    # Hide this from Adam
    # new = db.Users(username="thors",
    #    password=nacl.pwhash.str(bytes("hammer", "utf-8")),
    #    userLVL=0)
    # db_session.add(new)
    # db_session.flush()
    # db_session.commit()
    # Create some pounds
    names = ["Peterborough Pound", "Oshawa Pound", "Toronto Pound", "Pounds r Us", "One Pound Two Pounds",
             "Sunday Pound", "A Pound a Day", "Free Range Pound", "The New Pound", "Why Pound Us", "The Pound 2",
             "Great Bear Pound", "Alphabet Pound", "Amazing Pound", "Terrific Pound", "Queen Street Pound"]
    p_uids = []
    for x in names:
        new = db.Pounds(poundName=x)
        db_session.add(new)
        db_session.flush()
        p_uids.append(new.poundID)
        db_session.commit()

    # Create some rescues
    names = ["The Dog House", "Loki", "New Rescue",
             "The Perfect Rescue", "Extra Home", "Paradise"]
    r_uids = []
    for x in names:
        new = db.Rescues(rescueName=x)
        db_session.add(new)
        db_session.flush()
        r_uids.append(new.rescueID)
        db_session.commit()

    # Create some users all with impossible passwords
    names = ["Mike", "Ted", "Loki", "Gintama",
             "User1", "User2", "Extra_Account"]
    u_uids = []
    for x in names:
        new = db.Users(username=x,
                       password=nacl.pwhash.str(bytes("", "utf-8")),
                       userLVL=1)
        if (random.randint(0, 5) == 4):
            new.poundID = p_uids[random.randint(0, len(p_uids)-1)]
        if (random.randint(0, 5) == 3):
            new.roundID = r_uids[random.randint(0, len(r_uids)-1)]
        db_session.add(new)
        db_session.flush()
        u_uids.append(new.userID)
        db_session.commit()

    with open('nplbam/app/jsons/dog_questions.json') as json_file:
        questions = json.load(json_file)

    # Create Animals using previous and
    with open("nplbam/app/db/test.csv", "r") as f:
        reader = csv.DictReader(f)
        test_data = list(reader)
        for x in test_data:
            new = db.Animals(creator=u_uids[random.randint(0, len(u_uids)-1)],
                             poundID=p_uids[random.randint(0, len(p_uids)-1)],
                             stage=x["Stage"], stageDate=date.today()-timedelta(int(x["stageDate"])), animalType="Dog",
                             name=x["Name"], notes=x["Notes"])
            db_session.add(new)
            db_session.flush()
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
            db_session.commit()
            # Add stages for animal
            if (x["Stage1A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=1, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage1A"]))
                ))
            if (x["Stage1B"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=1, substageNum=2,
                    completionDate=date.today()-timedelta(int(x["Stage1B"]))
                ))
            if (x["Stage1C"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=1, substageNum=3,
                    completionDate=date.today()-timedelta(int(x["Stage1C"]))
                ))
            if (x["Stage2A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=2, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage2A"]))
                ))
            if (x["Stage3A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=3, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage3A"]))
                ))
            if (x["Stage3B"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=3, substageNum=2,
                    completionDate=date.today()-timedelta(int(x["Stage3B"]))
                ))
            if (x["Stage3C"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=3, substageNum=3,
                    completionDate=date.today()-timedelta(int(x["Stage3C"]))
                ))
            if (x["Stage4A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=4, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage4A"]))
                ))
            if (x["Stage4B"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=4, substageNum=2,
                    completionDate=date.today()-timedelta(int(x["Stage4B"]))
                ))
            if (x["Stage4C"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=4, substageNum=3,
                    completionDate=date.today()-timedelta(int(x["Stage4C"]))
                ))
            if (x["Stage4D"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=4, substageNum=4,
                    completionDate=date.today()-timedelta(int(x["Stage4D"]))
                ))
            if (x["Stage5A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=5, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage5A"]))
                ))
            if (x["Stage5B"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=5, substageNum=2,
                    completionDate=date.today()-timedelta(int(x["Stage5B"]))
                ))
            if (x["Stage6A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=6, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage6A"]))
                ))
            if (x["Stage7A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=7, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage7A"]))
                ))
            if (x["Stage8A"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=8, substageNum=1,
                    completionDate=date.today()-timedelta(int(x["Stage8A"]))
                ))
            if (x["Stage8B"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=8, substageNum=2,
                    completionDate=date.today()-timedelta(int(x["Stage8B"]))
                ))
            if (x["Stage8C"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=8, substageNum=3,
                    completionDate=date.today()-timedelta(int(x["Stage8C"]))
                ))
            if (x["Stage8D"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=8, substageNum=4,
                    completionDate=date.today()-timedelta(int(x["Stage8D"]))
                ))
            if (x["Stage8E"] != '0'):
                db_session.add(db.StageInfo(
                    animalID=new.animalID, stageNum=8, substageNum=5,
                    completionDate=date.today()-timedelta(int(x["Stage8E"]))
                ))
            db_session.commit()
    # Close the database like a good boy
    db_session.close()
    return redirect("/")


@bp.route("/test_data2")
def test_data2():
    random.seed(int(round(time.time()*10000)))
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    month = 3
    year = 2021
    for x in range(0, 10, 1):
        new = db.MetaInformation()
        new.month = month
        new.year = year
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        new.users = random.randint(1, 50)
        new.rescues = random.randint(1, 50)
        new.pounds = random.randint(1, 50)

        new.totalAnimalsInSystem = random.randint(15, 130)
        c = random.randint(1, 20)
        new.animalsCompStage1 = c
        new.totalDaysCompStage1 = c * random.randint(1, 20)
        c = random.randint(1, 20)
        new.animalsCompStage2 = c
        new.totalDaysCompStage2 = c * random.randint(1, 21)
        c = random.randint(1, 20)
        new.animalsCompStage3 = c
        new.totalDaysCompStage3 = c * random.randint(1, 10)
        c = random.randint(1, 20)
        new.animalsCompStage4 = c
        new.totalDaysCompStage4 = c * random.randint(1, 25)
        c = random.randint(1, 20)
        new.animalsCompStage5 = c
        new.totalDaysCompStage5 = c * random.randint(1, 30)
        c = random.randint(1, 20)
        new.animalsCompStage6 = c
        new.totalDaysCompStage6 = c * random.randint(1, 29)
        c = random.randint(1, 20)
        new.animalsCompStage7 = c
        new.totalDaysCompStage7 = c * random.randint(1, 30)
        new.totalStagesLength = c * random.randint(100, 170)
        new.totalStagesAmount = c
        new.totalOutcome1 = random.randint(1, c)
        new.totalOutcome2 = random.randint(1, c)
        new.totalOutcome3 = random.randint(1, c)
        new.totalOutcome4 = random.randint(1, c)
        new.totalOutcome5 = random.randint(1, c)
        db_session.add(new)
        db_session.commit()

    db_session.close()
    return redirect("/")
