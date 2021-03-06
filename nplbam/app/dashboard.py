"""
This module deals with overview information about animals
within the system.
"""

from datetime import date

from flask import Blueprint, flash, redirect, render_template
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('dashboard', __name__, url_prefix="")


@bp.route("/dashboard")
def dashboard():
    """
    Page URL: /dashboard
    Page with the list of the top 5 animals in each stage
    """
    # Make sure the user is userLVL 0 or 1
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        flash("Not authorized")
        return redirect("/")
    # Open a new DB session
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    # Create a new list
    animals_list = {}
    # Find the newest entries and put it in part 0
    animals_list[0] = db_session.query(db.Animals).\
        order_by(db.Animals.stageDate.desc()).limit(5).all()
    # For parts 1-8 add the oldest of each Stage(1-8)
    for n in range(1, 9, 1):
        animals_list[n] = db_session.query(db.Animals).\
            filter(db.Animals.stage == n).\
            order_by(db.Animals.stageDate.asc()).limit(5).all()

    # Fetch all the user and put them in an easily accessable list
    user_UO_list = db_session.query(db.Users).all()
    user_list = {}
    for x in user_UO_list:
        user_list[x.userID] = x.username

    # Calculate the total amount of days each animal has been in that stage
    # Also grab the breed of the animal
    for x in range(0, 9, 1):
        for animal in animals_list[x]:
            animal.days = (date.today() - animal.stageDate).days
            # Loop through each of our textAnswers for Breed
            animal.creatorName = user_list[animal.creator]
            for q in animal.textAnswers:
                if (q.questionName == "breed"):
                    animal.breed = q.answer
                    break
        # Close the session
    db_session.close()
    return render_template("dashboard.html", role=user_level, title="Dashboard", animals=animals_list)
