from flask import Blueprint, redirect, render_template
from flask import session as flask_session
from datetime import date
from sqlalchemy.orm import sessionmaker, relationship
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
    db_session.close()
    # Calculate the total amount of days each animal has been in that stage
    for animal in animals_list:
        animal.days = (date.today() - animal.stageDate).days 
    return render_template("animals.html", title="Animals", animals=animals_list)
