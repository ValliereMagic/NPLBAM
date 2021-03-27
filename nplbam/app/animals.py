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
    if flask_session.get("userID", default=None) is None:
        flash('Not logged in')
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
        predetermined["hide_stuff"] = request.args.get(
            'hide_stuff', 1, type=int)

    # create engine for the database
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()

    # Query animal list based on dynamaic variables
    _search = getattr(db.Animals, predetermined["search_by"])
    _sort = getattr(db.Animals, predetermined["sort_by"])
    _sort = getattr(_sort, predetermined["order"])
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

    count = animals_list.count()
    total_pages = math.ceil(count / PER_PAGE)
    # Check if we have a page with info on it.
    if (total_pages >= page):
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

    return render_template("animals.html", title="Animals", animals=animals_list,
                           next_url=next_url, prev_url=prev_url, page=page, total_pages=total_pages,
                           count=count, predetermined=predetermined, animal_types=animal_types)
