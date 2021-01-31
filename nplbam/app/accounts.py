import nacl.pwhash
from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import relationship, sessionmaker

from .db import db

bp = Blueprint('accounts', __name__, url_prefix="")

USER_LEVEL_MAX: int = 5


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


class NewAccount:
    # Whether this account creation is valid
    valid: bool = True
    username: str = ""
    password: str = ""
    user_lvl: int = 0
    # The sets signal whether these optional
    # values are present
    rescue_set: bool = False
    rescue_id: int = 0
    pound_set: bool = False
    pound_id: int = 0


def validate_form_input(username: str, password: str,
                        password_verify: str, user_lvl: str,
                        rescue_id: str, pound_id: str,
                        errors: list) -> NewAccount:
    """
    Validate the form input for the new_account page.
    """
    global USER_LEVEL_MAX
    account: NewAccount = NewAccount()
    # Validate username and password:
    if username == "":
        errors.append("A username is required.")
        account.valid = False
        return account
    if password == "":
        errors.append("A password is required.")
        account.valid = False
        return account
    if (password_verify == "") or (password != password_verify):
        errors.append("The passwords entered do not match.")
        account.valid = False
        return account
    #
    # Will need to verify password strength right here
    # Probably a new function or external library for that
    #
    # They are good, add them to the structure.
    account.username = username
    account.password = password
    # Validate against our user level:
    try:
        user_lvl: int = int(user_lvl)
        if (user_lvl < 0) or (user_lvl > USER_LEVEL_MAX):
            errors.append("User level is out of bounds")
            account.valid = False
            return account
    except:
        errors.append("user level wasn't entered or was not a number.")
        account.valid = False
        return account
    account.user_lvl = user_lvl
    # Validate our optional fields:
    if rescue_id != "":
        try:
            rescue_id: int = int(rescue_id)
        except:
            errors.append("Rescue ID field filled out, and is not a number.")
            account.valid = False
            return account
        account.rescue_id = rescue_id
        account.rescue_set = True
    if pound_id != "":
        try:
            pound_id: int = int(pound_id)
        except:
            errors.append("Pound ID field is filled out, and is not a number.")
            account.valid = False
            return account
        account.pound_id = pound_id
        account.pound_set = True
    return account


@bp.route("/new_account", methods=("GET", "POST"))
def new_account():
    """
    Create a new account for the system.
    """
    # Make sure that the user is logged in.
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    # Make sure the user is userLVL 0 (FOR NOW)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        # May need to change where we redirect them in the future
        return redirect("/")
    # User is requesting the form to make a user page:
    if request.method == "GET":
        return render_template("add_account.html", title="New Account", errors=[])
    # User is submitting the form to make a new user
    elif request.method == "POST":
        # Any errors that accumulate:
        errors: list = []
        # Pull and validate the fields:
        username: str = request.form["username"]
        password: str = request.form["password"]
        password_verify: str = request.form["passwordVerify"]
        user_lvl: str = request.form["userLVL"]
        rescue_id: str = request.form["rescueID"]
        pound_id: str = request.form["poundID"]
        # Verify the entered form data
        account: NewAccount = validate_form_input(
            username, password, password_verify, user_lvl,
            rescue_id, pound_id, errors)
        # Check whether the user entered valid account data
        if not account.valid:
            return render_template("add_account.html",
                                   title="New Account",
                                   errors=errors)
        # Create the new user object for the database:
        new_db_account: db.Users = db.Users(username=account.username,
                                            password=nacl.pwhash.str(
                                                bytes(account.password, "utf-8")),
                                            userLVL=account.user_lvl)
        if account.rescue_set:
            new_db_account.rescueID = account.rescue_id
        if account.pound_set:
            new_db_account.poundID = account.pound_id
        # Create a db session:
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        # Add the new account
        db_session.add(new_db_account)
        # Commit the changes and close
        db_session.commit()
        db_session.close()
        return redirect("/accounts")
    else:
        return redirect("/")
