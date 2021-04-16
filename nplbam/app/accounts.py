"""
This module Deals with he pages that create, and edit accounts.
"""
import math

import nacl.pwhash
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
from flask import session as flask_session
from flask import url_for
from sqlalchemy import cast
from sqlalchemy.orm import Query, relationship, sessionmaker
from sqlalchemy.sql.sqltypes import String

from . import account_tools
from .db import db

bp = Blueprint('accounts', __name__, url_prefix="")

# Pagination constant, signifying how many animals are to be shown on
# each page.
PER_PAGE = 10.0


@bp.route("/accounts", methods=['POST', 'GET'])
def accounts():
    """
    Page URL: /accounts
    This page shows the Admin user a list of all the accounts
    that currently exist in the system.
    """
    global PER_PAGE

    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        flash("Not authorized")
        return redirect("/")

    # Get the page # of the page.
    page = request.args.get('page', 1, type=int)

    predetermined = {}
    # Get Post Params
    if request.method == 'POST':
        predetermined["search_by"] = request.form['searchBy']
        predetermined["search"] = request.form['searchText']
        predetermined["sort_by"] = request.form['sortBy']
        predetermined["order"] = request.form['order']
        # If its an ID we're searching for make sure its an int
        if ((predetermined["search_by"] != "username") and
                (predetermined["search"] != "")):
            try:
                predetermined["search"] = int(predetermined["search"])
            except ValueError:
                predetermined["search"] = ""
    # Otherwise make defaults
    else:
        predetermined["search_by"] = str(
            request.args.get('search_by', "username"))
        predetermined["search"] = str(request.args.get('search', ""))
        predetermined["sort_by"] = str(request.args.get('sort_by', "userID"))
        predetermined["order"] = str(request.args.get('order', "asc"))

    # Get the list of user accounts from the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Query account list based on dynamic variables
    _search = cast(getattr(db.Users, predetermined["search_by"]), String)
    _sort = getattr(db.Users, predetermined["sort_by"])
    _sort = getattr(_sort, predetermined["order"])

    # If search is blank don't filter
    if (predetermined["search"] != ""):
        search_text = "%{}%".format(predetermined["search"])
        accounts_list = db_session.query(db.Users).\
            filter(_search.ilike(search_text)).\
            order_by(_sort())
    else:
        accounts_list = db_session.query(db.Users)

    count = accounts_list.count()
    total_pages = math.ceil(count / PER_PAGE)
    # Check if we have a page with info on it.
    if (total_pages >= page):
        accounts_list = accounts_list[(int)(
            (page-1) * PER_PAGE): (int)(page * PER_PAGE)]

    # Close the session like a good boy.
    db_session.close()

    # Creates the urls for the pagination
    next_url = None
    prev_url = None
    if (total_pages > page):
        next_page = page + 1
        next_url = url_for('accounts.accounts', page=next_page, search_by=predetermined["search_by"],
                           search=predetermined["search"], sort_by=predetermined["sort_by"], order=predetermined["order"])
    if (page > 1):
        prev_url = url_for('accounts.accounts', page=page-1, search_by=predetermined["search_by"],
                           search=predetermined["search"], sort_by=predetermined["sort_by"], order=predetermined["order"])

    return render_template("accounts.html", title="Accounts", role=user_level, accounts=accounts_list,
                           next_url=next_url, prev_url=prev_url, page=page, total_pages=total_pages,
                           count=count, predetermined=predetermined)


def pull_pounds_and_rescue_info() -> dict:
    """
    Simple helper function to pull the pounds and rescue information
    from the database, then format it into a format good for iterating
    on the Jinja2 template. 

    This function creates the information used to populate the drop down boxes
    for Rescues and Pounds on the Create and Edit account pages.

    :return: dictionary containing 2 lists. keys: ["rescues"], ["pounds"]
    """
    # db session
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    # Pull the Rescues and Pounds Tables
    rescues_list = db_session.query(db.Rescues).all()
    pounds_list = db_session.query(db.Pounds).all()
    db_session.close()
    # Populate the dict and return
    rescue_pound_info = dict()
    rescue_pound_info["rescues"] = rescues_list
    rescue_pound_info["pounds"] = pounds_list
    return rescue_pound_info


@bp.route("/new_account", methods=("GET", "POST"))
def new_account():
    """
    Page URL: /new_account
    Form for creating new accounts for the NPLBAM system.
    """
    # Make sure the user is userLVL 0 (FOR NOW)
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        flash("Not authorized")
        return redirect("/")
    # Pull the rescue and pound info to populate the form with
    rescue_pound_info: dict = pull_pounds_and_rescue_info()
    # User is requesting the form to make a user page:
    if request.method == "GET":
        return render_template("new_account.html",
                               role=user_level,
                               title="New Account",
                               rescue_pound_info=rescue_pound_info,
                               errors=[])
    # User is submitting the form to make a new user
    elif request.method == "POST":
        # Any errors that accumulate:
        errors: list = []
        # Verify the entered form data
        account: account_tools.AccountInfo = account_tools.validate_form_input(
            request, errors)
        # Check whether the user entered valid account data
        if not account.valid:
            return render_template("new_account.html",
                                   role=user_level,
                                   title="New Account",
                                   rescue_pound_info=rescue_pound_info,
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

        # Import tools for adding to meta table
        from .metatable_tools import (get_metainformation_record)

        # Get the most recent record (even if it needs to be created)
        meta_info = get_metainformation_record(db_session)
        # Add an users to the record
        meta_info.users += 1

        # Add the new account
        db_session.add(new_db_account)

 
        # Commit the changes and close
        db_session.commit()
        db_session.close()
        flash("Account id# {} Created".format(account.username))
        current_app.logger.info("New user with username: {} "
                                "created by ID: {}".format(
                                    account.username, flask_session["userID"]))
        return redirect("/accounts")
    else:
        return redirect("/")


@bp.route("/edit_account", methods=("GET", "POST"))
def edit_account():
    """
    Page URL: /edit_account
    Form for editing an existing account.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level != 0:
        flash("Not authorized")
        return redirect("/")
    # User is requesting the form to edit their user account:
    if request.method == "GET":
        # Check to see if the account ID has been set properly
        account_id: int = request.args.get(
            'account_id', default=None, type=int)
        # Otherwise redirect them to the accounts page. We have nothing to edit.
        if account_id is None:
            flash("Incorrect account")
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
        return render_template("edit_account.html",
                               role=user_level,
                               title="Edit Account",
                               rescue_pound_info=pull_pounds_and_rescue_info(),
                               info=info,
                               errors=[])
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
                                   role=user_level,
                                   title="Account Error",
                                   redirect="/accounts",
                                   errors=errors)
        # Validate the rest of the data
        account: account_tools.AccountInfo = account_tools.validate_form_input(
            request, errors, True)
        # Check whether the user entered valid account data
        if not account.valid:
            flask_session["actively_editing"] = None
            return render_template("error_page.html",
                                   role=user_level,
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
        flash("Account Modified")
        current_app.logger.info("Account ID: {} Edited by ID: {}".format(
            account_id, flask_session["userID"]))
        return redirect("/accounts")
    else:
        flask_session["actively_editing"] = None
        return redirect("/accounts")
