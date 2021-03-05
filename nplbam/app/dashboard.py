from datetime import date

from flask import Blueprint, redirect, render_template
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('dashboard', __name__, url_prefix="")


@bp.route("/dashboard")
def dashboard():
    """
    Page with the list of top 5 of each stage
    """
    # Make sure the user is userLVL 0 or 1
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        return redirect("/")
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    animals_list = {}
    for n in range(1, 9, 1):
        animals_list[n] = db_session.query(db.Animals).\
          filter(db.Animals.stage==n).\
          order_by(db.Animals.stageDate.asc()).limit(5).all()
    
    # Fetch all the user and put them in an easily accessable list
    user_UO_list = db_session.query(db.Users).all()
    user_list = {}
    for x in user_UO_list:
        user_list[x.userID] = x.username

    # Calculate the total amount of days each animal has been in that stage
    # Also grab the breed of the animal
    for x in range(1,9,1):
        for animal in animals_list[x]:
            animal.days = (date.today() - animal.stageDate).days
            # Loop through each of our textAnswers for Breed
            animal.creatorName = user_list[animal.creator]
            for q in animal.textAnswers:    
                if (q.questionName == "breed"):
                    animal.breed = q.answer
                    break;
        # Close the session
    db_session.close()
    return render_template("dashboard.html", title="Dashboard", animals=animals_list)

@bp.route("/add_test")
def add_test():
    """ Temporary function please delete in production """
    from .db_test_data import create_test_data
    create_test_data()
    return redirect("/")