from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean, String

from .db import db


def create_test_data():
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    # Create some pounds
    names = ["Peterborough Pound", "Oshawa Pound", "Toronto Pound", "Pounds r Us", "One Pound Two Pounds",\
        "Sunday Pound", "A Pound a Day", "Free Range Pound", "The New Pound", "Why Pound Us", "The Pound 2",\
            "Great Bear Pound", "Alphabet Pound", "Amazing Pound", "Terrific Pound", "Queen Street Pound"]
    p_uids = []
    for x in names:
        new = db.Pounds(poundName=x)
        db_session.add(new)
        db_session.flush()
        p_uids.append(new.poundID)

    # Create some rescues
    names = ["The Dog House", "Loki", "New Rescue", "The Perfect Rescue", "Extra Home", "Paradise"]
    r_uids = []
    for x in names:
        new = db.Rescues(rescueName=x)
        db_session.add(new)
        db_session.flush()
        r_uids.append(new.poundID)

    

    # Close the database like a good boy
    db_session.close()
