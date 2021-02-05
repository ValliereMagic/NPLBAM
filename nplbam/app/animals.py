from datetime import date

from flask import Blueprint, redirect, render_template
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('animals', __name__, url_prefix="")


@bp.route("/animals")
def query():
    """
    Page with the list of all animals, which can be filtered.
    """
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    animals_list = db_session.query(db.Animals).all()
    # Fetch all the user and put them in an easily accessable list
    user_UO_list = db_session.query(db.Users).all()
    user_list = {}
    for x in user_UO_list:
        user_list[x.userID] = x.username
    # Calculate the total amount of days each animal has been in that stage
    # Also grab the breed of the animal
    for animal in animals_list:
        animal.days = (date.today() - animal.stageDate).days
        # Loop through each of our textAnswers for Breed
        animal.creatorName = user_list[animal.creator]
        for q in animal.textAnswers:    
            if (q.questionName == "breed"):
                animal.breed = q.answer
                break;
    # Close the session
    db_session.close()
    return render_template("animals.html", title="Animals", animals=animals_list)
