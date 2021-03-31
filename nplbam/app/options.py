"""
This module deals with a user's self-serve options for their
account, such as the ability for them to change their own
password.
"""

from datetime import date
from logging import error

import nacl.exceptions
import nacl.pwhash
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
from flask import session as flask_session
from sqlalchemy.orm import Query, relationship, sessionmaker

from .db import db

bp = Blueprint('options', __name__, url_prefix="")


@bp.route("/options")
def options():
    """
    Page URL: /options
    Page with options for the users. Such as changing their password
    """
    # Make sure the user exists
    user_level: int = flask_session.get("userLVL", default=None)
    if (user_level is None):
        flash("Not authorized")
        return redirect("/")
    errors: list = []
    return render_template("options.html", title="Options", errors=errors)


@bp.route("/change_password", methods=("GET", "POST"))
def change_password():
    """
    Page URL: /change_password
    This will change the password of the user with the information
    entered from the /options page.
    """
    # Make sure the user exists
    user_level: int = flask_session.get("userLVL", default=None)
    if (user_level is None):
        flash("Not authorized")
        return redirect("/")
    if request.method == 'POST':
        errors: list = []
        old_password: str = request.form['oldpassword']
        new_password1: str = request.form['password']
        new_password2: str = request.form['passwordVerify']

        # Get User from database
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        user_ID = flask_session.get("userID", default=None)
        user_entry = db_session.query(
            db.Users).filter_by(userID=user_ID).first()

        # Make sure old password match database's
        if user_entry is None:
            errors.append("Incorrect Credentials.")
        else:
            # Check if the password entered matches the username
            # being authenticated against.
            try:
                nacl.pwhash.verify(user_entry.password,
                                   bytes(old_password, 'utf-8'))
            # Tried to login with an incorrect password
            except nacl.exceptions.InvalidkeyError:
                errors.append("Incorrect Credentials.")

        # Check if new Passwords match
        if (new_password1 != new_password2):
            errors.append("Passwords Do not Match")

        from .account_tools import (MIN_PASSWORD_ENTROPY_BITS,
                                    verify_password_strength)

        # Check if new Password is strong enough
        if (new_password1 == ""):
            errors.append("Password is not set")
        else:
            entropy_bits, valid = verify_password_strength(new_password1)
            if not valid:
                errors.append(
                    "Password does not meet minimum strength requirement of {} bits. ".format(
                        MIN_PASSWORD_ENTROPY_BITS) +
                    "It contains {} bits of entropy. ".format(entropy_bits) +
                    "Please either increase its length, " +
                    "or add characters from different character sets. " +
                    "(For example: Add some numbers, or a maybe a symbol.)")

        if (len(errors) > 0):
            # Close the session like a good boy
            db_session.close()
            return render_template("options.html", title="Options", errors=errors)
        else:
            # Add to Database
            user_entry.password = nacl.pwhash.str(
                bytes(new_password1, "utf-8"))
            # Commit the changes
            db_session.commit()
            # Close the session like a good boy
            db_session.close()
            flash("Password Changed")
            current_app.logger.info(
                "User ID: {} changed their password.".format(flask_session["userID"]))
            return redirect("/")
