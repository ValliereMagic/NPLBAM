"""
This module deals with the page presented to every unauthenticated
user connecting to this application, and presents them the opportunity
to login.
"""

from datetime import datetime

import nacl.exceptions
import nacl.pwhash
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
from flask import session as flask_session
from flask import url_for
from sqlalchemy.orm import Query, Session, relationship, sessionmaker

from .db import db

bp = Blueprint('index', __name__, url_prefix="")


@bp.route("/", methods=("GET", "POST"))
@bp.route("/index", methods=("GET", "POST"))
def index():
    """
    Page URL: /index and /
    Present login page to user, validate input, check login credentials,
    and give user a valid session.
    """
    if flask_session.get("userID", default=None) is not None:
        return redirect("/animals")
    # User is attempting to login
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
        errors: list = []
        # Make sure the user entered a username and
        # password
        data_intact: bool = True
        if username == "":
            errors.append("Username is required.")
            data_intact = False
        if password == "":
            errors.append("Password is required")
            data_intact = False
        # Fail out, and show the user the errors
        # that occurred
        if not data_intact:
            return render_template("index.html", errors=errors)
        # Credentials are possibly good, get the User from the database
        engine = db.get_db_engine()
        db_session: Session = (sessionmaker(bind=engine))()
        user_entry: db.Users = db_session.query(db.Users).filter(
            db.Users.username == username).first()
        db_session.close()
        # Check that the user exists, if not, then
        # user login data is invalid.
        if user_entry is None:
            errors.append("Incorrect Credentials.")
        else:
            # Check if the password entered matches the username
            # being authenticated against.
            try:
                nacl.pwhash.verify(user_entry.password,
                                   bytes(password, 'utf-8'))
            # Tried to login with an incorrect password
            except nacl.exceptions.InvalidkeyError:
                errors.append("Incorrect Credentials.")
                # Get the current time for the log entry:
                time_string: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                # Append an entry to the log stating what happened
                # access_route(0) is the ip address of the actual client
                # (Forwarded through nginx to our flask application)
                current_app.logger.warning("Failed login attempt from: {}"
                                           " using username: {} at: {}".format(
                                               request.access_route[0], username,
                                               time_string))
                # Bail out to make sure the user is NOT logged in.
                return render_template("index.html", errors=errors)
            except Exception as e:
                current_app.logger.error("Exception: {} occurred while"
                                         " attempting a login.".format(
                                             type(e).__name__))
                # Bail out to make sure the user is NOT logged in.
                return redirect("/")
        # If there were no errors, log the user in
        if len(errors) == 0:
            flask_session.clear()
            flask_session.permanent = True
            flask_session["userID"] = user_entry.userID
            flask_session["userLVL"] = user_entry.userLVL
            flash("Login Successful")
            return redirect("animals")
        else:
            return render_template("index.html", errors=errors)
    else:
        return render_template("index.html", errors=[])


@bp.route('/logout')
def logout():
    """
    Page URL: /logout
    Clear the user's session, and send them back to the login
    page.
    """
    flask_session.clear()
    return redirect("/")
