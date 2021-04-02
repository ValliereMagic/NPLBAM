"""
This module deals with the main page of the application that is
presented to the user right after login.
"""

import json
import math
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request
from flask import session as flask_session
from flask import url_for
from sqlalchemy import or_
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean, String

from .db import db

bp = Blueprint('animals', __name__, url_prefix="")

# Pagination constant, signifying how many animals are to be shown on
# each page.
PER_PAGE = 20.0


@bp.route("/animals", methods=['POST', 'GET'])
def animals():
    """
    Page URL: /animals
    Page with the filterable table of all animals that have
    been entered into the system.
    """
    global PER_PAGE
    # Make sure visitor is logged in
    user_id: int = flask_session.get("userID", default=None)
    if user_id is None:
        flash('Not logged in')
        return redirect("/")

    # get user level
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None):
        # May need to change where we redirect them in the future
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
        if 'hide_stuff' in request.form:
            predetermined["hide_stuff"] = 1
        else:
            predetermined["hide_stuff"] = 0
        # If its an ID we're searching for make sure its an int
        if ((predetermined["search_by"] == "animalID") or (predetermined["search_by"] == "stage")) and \
                (predetermined["search"] != ""):
            try:
                predetermined["search"] = int(predetermined["search"])
            except ValueError:
                predetermined["search"] = ""
    # Otherwise make defaults
    else:
        predetermined["search_by"] = str(
            request.args.get('search_by', "name"))
        predetermined["search"] = str(request.args.get('search', ""))
        predetermined["sort_by"] = str(request.args.get('sort_by', "animalID"))
        predetermined["order"] = str(request.args.get('order', "asc"))
        # If user is not a pound/rescue. Default to hide info
        if (user_level < 2):
            predetermined["hide_stuff"] = request.args.get(
                'hide_stuff', 1, type=int)
        else:
            predetermined["hide_stuff"] = 0

    # create engine for the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Query animal list based on dynamaic variables
    _search = getattr(db.Animals, predetermined["search_by"])
    _sort = getattr(db.Animals, predetermined["sort_by"])
    _sort = getattr(_sort, predetermined["order"])
    # If user is level 0  or 1
    if (user_level < 2):
        # If search is blank don't filter
        if (predetermined["search"] != ""):
            search_text = "%{}%".format(predetermined["search"])
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(_search.ilike(search_text)).\
                    filter(db.Animals.stage != 0).filter(
                        db.Animals.stage != 8).order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    filter(_search.ilike(search_text)).\
                    order_by(_sort())
        else:
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(db.Animals.stage != 0).filter(db.Animals.stage != 8).\
                    order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    order_by(_sort())
    # User is 2 or 3. (Pounds)
    elif (user_level < 4):
        user_info = db_session.query(db.Users).filter(
            db.Users.userID == user_id).first()
        # If search is blank don't filter
        if (predetermined["search"] != ""):
            search_text = "%{}%".format(predetermined["search"])
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(or_(db.Animals.creator == user_id, db.Animals.poundID == user_info.poundID)).\
                    filter(db.Animals.stage < 4).\
                    filter(_search.ilike(search_text)).\
                    filter(db.Animals.stage != 0).filter(
                        db.Animals.stage != 8).order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    filter(_search.ilike(search_text)).\
                    filter(db.Animals.stage < 4).\
                    filter(or_(db.Animals.creator == user_id, db.Animals.poundID == user_info.poundID)).\
                    order_by(_sort())
        else:
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(or_(db.Animals.creator == user_id, db.Animals.poundID == user_info.poundID)).\
                    filter(db.Animals.stage < 4).\
                    filter(db.Animals.stage != 0).filter(db.Animals.stage != 8).\
                    order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    filter(db.Animals.stage < 4).\
                    filter(or_(db.Animals.creator == user_id, db.Animals.poundID == user_info.poundID)).\
                    order_by(_sort())
    # User level is 4/5 (Rescues)
    else:
        user_info = db_session.query(db.Users).filter(
            db.Users.userID == user_id).first()
        # If search is blank don't filter
        if (predetermined["search"] != ""):
            search_text = "%{}%".format(predetermined["search"])
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(db.Animals.rescueID == user_info.rescueID).\
                    filter(_search.ilike(search_text)).\
                    filter(db.Animals.stage != 0).filter(
                        db.Animals.stage != 8).order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    filter(_search.ilike(search_text)).\
                    filter(db.Animals.rescueID == user_info.rescueID).\
                    order_by(_sort())
        else:
            # check if we should hide stage 0 and 8
            if predetermined["hide_stuff"] == 1:
                animals_list = db_session.query(db.Animals).\
                    filter(db.Animals.rescueID == user_info.rescueID).\
                    filter(db.Animals.stage != 0).filter(db.Animals.stage != 8).\
                    order_by(_sort())
            else:
                animals_list = db_session.query(db.Animals).\
                    filter(db.Animals.rescueID == user_info.rescueID).\
                    order_by(_sort())

    count = animals_list.count()
    total_pages = math.ceil(count / PER_PAGE)
    # Check if we have a page with info on it.
    if (total_pages >= page):
        # Slice our section it off by PER_PAGE and page#
        animals_list = animals_list[(int)(
            (page-1) * PER_PAGE): (int)(page * PER_PAGE)]
        # Fetch all the user and put them in an easily accessable list
        user_UO_list = db_session.query(db.Users).all()
        user_list = {}
        for x in user_UO_list:
            user_list[x.userID] = x.username
        # Calculate the total amount of days each animal has been in that stage
        # Also grab the breed of the animal
        for animal in animals_list:
            animal.days = (date.today() - animal.stageDate).days
            # Loop through each of our textAnswers for Breed
            animal.creatorName = user_list[animal.creator]
            for q in animal.textAnswers:
                if (q.questionName == "breed"):
                    animal.breed = q.answer
                    break
    # Close the session
    db_session.close()

    # Creates the urls for the pagination
    next_url = None
    prev_url = None
    if (total_pages > page):
        next_page = page + 1
        next_url = url_for('animals.animals', page=next_page, search_by=predetermined["search_by"],
                           search=predetermined["search"], sort_by=predetermined["sort_by"], order=predetermined["order"],
                           hide_stuff=predetermined["hide_stuff"])
    if (page > 1):
        prev_url = url_for('animals.animals', page=page-1, search_by=predetermined["search_by"],
                           search=predetermined["search"], sort_by=predetermined["sort_by"], order=predetermined["order"],
                           hide_stuff=predetermined["hide_stuff"])

    # Get list of animal types from json
    with open('nplbam/app/jsons/animal_species.json') as json_file:
        animal_types = json.load(json_file)

    return render_template("animals.html", title="Animals", role=user_level, animals=animals_list,
                           next_url=next_url, prev_url=prev_url, page=page, total_pages=total_pages,
                           count=count, predetermined=predetermined, animal_types=animal_types)
