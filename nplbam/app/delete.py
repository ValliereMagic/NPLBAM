"""
This module deals with the pages/routes for deleting entries from the database. 
"""

import os

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)
from flask import session as flask_session
from sqlalchemy.orm import Query, relationship, sessionmaker

from .db import db

bp = Blueprint('delete', __name__, url_prefix="")


@bp.route("/delete")
def delete_page():
    """
    This is a landing page which will give the user choices on what
    they want to delete.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    return render_template("delete.html", role=user_level, title="Delete")


@bp.route("/delete_file")
def delete_file():
    """
    If they want to delete a single file, they come to this page to enter info
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    return render_template("delete_file.html", role=user_level, title="Delete File")


@bp.route("/delete_animal")
def delete_animal():
    """
    If they want to delete an animal, they come to this page to enter info
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    return render_template("delete_animal.html", role=user_level, title="Delete Animal")


@bp.route("/delete_files")
def delete_files():
    """
    If they want to delete multiple files associated with an animal, they come to this 
    page to enter info
    """

    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    return render_template("delete_files.html", role=user_level, title="Delete Files")


@bp.route("confirm_delete_animal", methods=['POST', 'GET'])
def confirm_delete_animal():
    """
    A page to confirm which animal they are deleting before doing so.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':

        # Get post Param
        given_animal_id = int(request.form['animal_id'])

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        animal_entry = db_session.query(db.Animals).filter(
            db.Animals.animalID == given_animal_id).first()

        # Check if we found something
        if (animal_entry == None):
            flash("ID {} does not exist.".format(given_animal_id))
            return redirect("/delete")

        # Get a list of files
        files = []
        for x in animal_entry.files:
            files.append(x)

        # Close the session like a good boy
        db_session.close()

        return render_template("delete_animal_confirm.html", role=user_level, title="Delete Animal", animal=animal_entry, files=files)
    return redirect("/")


@bp.route("submit_delete_animal", methods=['POST', 'GET'])
def submit_delete_animal():
    """
    This route will delete an animal given its ID through post
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':
        # Get user ID
        user_ID: int = flask_session.get("userID", default=None)
        if (user_ID is None):
            flash("Not logged in")
            return redirect("/")

        # Get post Param
        given_animal_id = int(request.form['animal_id'])

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        animal_entry = db_session.query(db.Animals).filter(
            db.Animals.animalID == given_animal_id).first()

        # Delete the files off the server
        for x in animal_entry.files:
            os.remove(os.path.join(
                current_app.config["UPLOAD_FOLDER"], x.fileName))

        # Delete entry
        db_session.delete(animal_entry)

        # Commit
        db_session.commit()

        # Close the session like a good boy
        db_session.close()

        # Log it
        current_app.logger.info(
            "Animal ID# {} deleted by User ID: {}".format(given_animal_id, user_ID))

        flash("Deleted animal id# {}".format(given_animal_id))
    return redirect("/")


@bp.route("confirm_delete_file", methods=['POST', 'GET'])
def confirm_delete_file():
    """
    This page will confirm the file they want to delete.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':

        # Get post Param
        given_file_name = request.form['file_name']

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        file_entry = db_session.query(db.Files).filter(
            db.Files.fileName == given_file_name).first()

        # Check if we found something
        if (file_entry == None):
            flash("File {} does not exist.".format(given_file_name))
            return redirect("/delete")

        # Close the session like a good boy
        db_session.close()

        return render_template("delete_file_confirm.html", role=user_level, title="Delete File", file=file_entry)
    return redirect("/")


@bp.route("submit_delete_file", methods=['POST', 'GET'])
def submit_delete_file():
    """
    This route will delete a file given its name through post.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':

        # Get user ID
        user_ID: int = flask_session.get("userID", default=None)
        if (user_ID is None):
            flash("Not logged in")
            return redirect("/")

        # Get post Param
        given_file_name = request.form['file_name']

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        file_entry = db_session.query(db.Files).filter(
            db.Files.fileName == given_file_name).first()

        os.remove(os.path.join(
            current_app.config["UPLOAD_FOLDER"], file_entry.fileName))

        # Delete entry
        db_session.delete(file_entry)

        # Commit
        db_session.commit()

        # Close the session like a good boy
        db_session.close()

        # Log it
        current_app.logger.info(
            "File named {} deleted by User ID: {}".format(given_file_name, user_ID))

        flash("Deleted file named {}".format(given_file_name))
    return redirect("/")


@bp.route("confirm_delete_files", methods=['POST', 'GET'])
def confirm_delete_files():
    """
    This route will confirm if they want to delete the specified files for a given animal.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':

        # Get post Param
        given_animal_id = int(request.form['animal_id'])

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        animal_entry = db_session.query(db.Animals).filter(
            db.Animals.animalID == given_animal_id).first()

        # Get a list of files
        files = []
        for x in animal_entry.files:
            files.append(x)

        # Close the session like a good boy
        db_session.close()

        return render_template("delete_files_confirm.html", role=user_level, title="Delete File", animal=animal_entry, files=files)
    return redirect("/")


@bp.route("submit_delete_files", methods=['POST', 'GET'])
def submit_delete_files():
    """
    This route will delete all files for an animal given its ID.
    """
    # Make sure the user is userLVL 0
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 0:
        # May need to change where we redirect them in the future
        flash("Not authorized")
        return redirect("/")

    # Make sure they got here with post
    if request.method == 'POST':
        # Get user ID
        user_ID: int = flask_session.get("userID", default=None)
        if (user_ID is None):
            flash("Not logged in")
            return redirect("/")

        # Get post Param
        given_animal_id = int(request.form['animal_id'])

        # Create our DB session
        engine = db.get_db_engine()
        db_session = (sessionmaker(bind=engine))()

        # Find animal
        animal_entry = db_session.query(db.Animals).filter(
            db.Animals.animalID == given_animal_id).first()

        # Delete the files off the server
        for x in animal_entry.files:
            os.remove(os.path.join(
                current_app.config["UPLOAD_FOLDER"], x.fileName))
            # Delete the files from the database
            db_session.delete(x)

        # Commit
        db_session.commit()

        # Close the session like a good boy
        db_session.close()

        # Log it
        current_app.logger.info(
            "Files for animal ID# {} deleted by User ID: {}".format(given_animal_id, user_ID))

        flash("Deleted files for animal id# {}".format(given_animal_id))
    return redirect("/")
