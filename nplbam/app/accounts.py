import nacl.pwhash
from flask import Blueprint, redirect, render_template, request
from flask import session as flask_session
from sqlalchemy.orm import Query, relationship, sessionmaker

from . import account_tools
from .db import db

bp = Blueprint('accounts', __name__, url_prefix="")


@bp.route("/accounts")
def query():
    """
    Page with the list of all accounts, which can be filtered.
    """
    # Make sure the user is userLVL 0 (FOR NOW)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        # May need to change where we redirect them in the future
        return redirect("/")
    # Get the list of user accounts from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    accounts_list = db_session.query(db.Users).all()
    db_session.close()
    return render_template("accounts.html", title="Accounts", accounts=accounts_list)


@bp.route("/new_account", methods=("GET", "POST"))
def new_account():
    """
    Create a new account for the system.
    """
    # Make sure the user is userLVL 0 (FOR NOW)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        # May need to change where we redirect them in the future
        return redirect("/")
    # User is requesting the form to make a user page:
    if request.method == "GET":
        return render_template("new_account.html", title="New Account", errors=[])
    # User is submitting the form to make a new user
    elif request.method == "POST":
        # Any errors that accumulate:
        errors: list = []
        # Verify the entered form data
        account: NewAccount = account_tools.validate_form_input(
            request, errors)
        # Check whether the user entered valid account data
        if not account.valid:
            return render_template("new_account.html",
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


@bp.route("/edit_account", methods=("GET", "POST"))
def edit_account():
    """
    Edit an existing account
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        # May need to change where we redirect them in the future
        return redirect("/")
    # User is requesting the form to edit their user account:
    if request.method == "GET":
        # Check to see if the account ID has been set properly
        account_id: int = request.args.get(
            'account_id', default=None, type=int)
        # Otherwise redirect them to the accounts page. We have nothing to edit.
        if account_id is None:
            return redirect("/accounts")
        # Set the actively_editing id in the session
        flask_session["actively_editing"] = account_id
        # Information to display on the page
        info = dict()
        # Get the existing account information from the database
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        user_to_edit: db.Users = db_session.query(db.Users).filter(
            db.Users.userID == account_id).first()
        db_session.close()
        # Populate the dictionary to display the current values to the user
        info["user_id"] = user_to_edit.userID
        info["username"] = user_to_edit.username
        info["user_lvl"] = user_to_edit.userLVL
        info["rescue_id"] = user_to_edit.rescueID
        info["pound_id"] = user_to_edit.poundID
        # Show the form, displaying all the editable fields
        return render_template("edit_account.html", title="Edit Account", info=info, errors=[])
    # User is submitting the updated account information
    elif request.method == "POST":
        # Any errors that accumulate:
        errors: list = []
        try:
            account_id: int = int(flask_session["actively_editing"])
        except:
            # Cannot continue, account id is bogus
            errors.append(
                "Error. Account ID not passed correctly in hidden form field.")
            flask_session["actively_editing"] = None
            return render_template("error_page.html",
                                   title="Account Error",
                                   redirect="/accounts",
                                   errors=errors)
        # Validate the rest of the data
        account: account_tools.NewAccount = account_tools.validate_form_input(
            request, errors, True)
        # Check whether the user entered valid account data
        if not account.valid:
            flask_session["actively_editing"] = None
            return render_template("error_page.html",
                                   title="Account Error",
                                   redirect="/accounts",
                                   errors=errors)
        # Modify the account object
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()
        user_to_edit: Query = db_session.query(db.Users).filter(
            db.Users.userID == account_id)
        # Add what will always be added
        user_to_edit.update({"username": account.username,
                             "userLVL": account.user_lvl})
        # Add the optional ones if set
        if account.password_set:
            user_to_edit.update(
                {"password": nacl.pwhash.str(bytes(account.password, "utf-8"))})
        if account.rescue_set:
            user_to_edit.update({"rescueID": account.rescue_id})
        if account.pound_set:
            user_to_edit.update({"poundID": account.pound_id})
        # Commit the changes and close
        db_session.commit()
        db_session.close()
        flask_session["actively_editing"] = None
        return redirect("/accounts")
    else:
        flask_session["actively_editing"] = None
        return redirect("/accounts")
