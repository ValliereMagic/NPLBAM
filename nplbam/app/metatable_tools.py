"""
This module Contains functionality to create a new metainformation 
record in the metainformation table
"""
import datetime

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from .db import db


def new_metainformation_record(db_session) -> (db.MetaInformation):
    """
    This method will create a new record in the metainformation table.
    """
    # Get today's date
    today = datetime.date.today()
    
    # create a new record
    new = db.MetaInformation()

    # Set the date
    new.month = today.strftime("%m")
    new.year = today.strftime("%Y")

    # Get counts from the database
    new.rescues = db_session.query(db.Rescues).count()
    new.pounds = db_session.query(db.Pounds).count()
    new.users = db_session.query(db.Users).count()
    new.totalAnimalsInSystem = db_session.query(db.Animals).count()

    # Set these to 0
    new.totalStagesAmount = 0
    new.totalStagesLength = 0
    new.animalsCompStage1 = 0
    new.animalsCompStage2 = 0
    new.animalsCompStage3 = 0
    new.animalsCompStage4 = 0
    new.animalsCompStage5 = 0
    new.animalsCompStage6 = 0
    new.animalsCompStage7 = 0
    new.totalDaysCompStage1 = 0
    new.totalDaysCompStage2 = 0
    new.totalDaysCompStage3 = 0
    new.totalDaysCompStage4 = 0
    new.totalDaysCompStage5 = 0
    new.totalDaysCompStage6 = 0
    new.totalDaysCompStage7 = 0
    new.totalOutcome1 = 0
    new.totalOutcome2 = 0
    new.totalOutcome3 = 0
    new.totalOutcome4 = 0
    new.totalOutcome5 = 0

    # Add the record to the table
    db_session.add(new)
    return new


def get_metainformation_record(db_session) -> (db.MetaInformation):
    """
    This method will get the latest record of the metainformation table.
    If it does not exit it will make one.
    """

    # Get the latest record
    meta_record = db_session.query(db.MetaInformation).\
        order_by(db.MetaInformation.year.desc(), db.MetaInformation.month.desc()).\
        first()

    # Get today's date
    today = datetime.date.today()

    # Check if our meta record is for this month
    if (meta_record.month != int(today.strftime("%m"))):
        # If not correct month, make a new one
        meta_record = new_metainformation_record(db_session)

    # Return db.Metatable class
    return meta_record
