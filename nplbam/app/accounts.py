from flask import Blueprint, redirect, render_template
from flask import session as flask_session

from sqlalchemy.orm import sessionmaker, relationship
from .db import db

bp = Blueprint('accounts', __name__, url_prefix="")


@bp.route("/accounts")
def query():
    """
    Page with the list of all accounts, which can be filtered.
    """
    # Make sure visitor is logged in
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Get the list of animals from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    accounts_list = db_session.query(db.Users).all()
    db_session.close()
    return render_template("accounts.html", title="Accounts", accounts=accounts_list)
