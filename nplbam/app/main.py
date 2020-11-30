from flask import render_template, Blueprint, request, \
    redirect, url_for, session as flask_session
from sqlalchemy.orm import sessionmaker, relationship
import nacl.pwhash
import nacl.exceptions
from .db import db

bp = Blueprint('index', __name__, url_prefix="")


@bp.route("/", methods=("GET", "POST"))
@bp.route("/index", methods=("GET", "POST"))
def index():

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
        # Get the User from the database
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        user_entries = db_session.query(db.Users)
        user_entry: db.Users = user_entries.filter(
            db.Users.userID == username).first()
        db_session.close()
        # Check that the user exists
        if user_entry is None:
            errors.append("Incorrect Username.")
        else:
            # Verify the user password is correct
            try:
                nacl.pwhash.verify(user_entry.password,
                                   bytes(password, 'utf-8'))
            except nacl.exceptions.InvalidkeyError:
                errors.append("Incorrect Password.")
            except:
                print("Send it to the blog")
        # If there were no errors, log the user in
        if len(errors) == 0:
            flask_session.clear()
            flask_session["userID"] = user_entry.userID
            flask_session["userLVL"] = user_entry.userLVL
            return redirect("animals")
        else:
            return render_template("index.html", errors=errors)
    else:
        return render_template("index.html", errors=[])


@bp.route('/logout')
def logout():
    flask_session.clear()
    return redirect("/")
