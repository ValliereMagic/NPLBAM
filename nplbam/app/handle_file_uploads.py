import os
import re
import uuid
from typing import List

from flask import current_app
from sqlalchemy.orm import sessionmaker
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .db import db

image_mime_regex: re.Pattern = re.compile("^image/")


def save_uploaded_files(animal_id: int,
                        uploaded_files_list: List[FileStorage],
                        errors: list) -> bool:
    """
    Take the uploaded files list extracted from the form data entered by the user
    and save the file in the nplbam/files folder on the server prefixed with _<animal_id>_
    This function returns False whenever a single file in the list is unable to be uploaded
    successfully.
    """
    success: bool = True
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    # Look at each file to be uploaded
    file_type: str = "image"
    for upload in uploaded_files_list:
        if upload.filename == '':
            errors.append("No file was selected")
            db_session.close()
            success = False
            return success
        # Check whether the file is an image
        if re.match(image_mime_regex, upload.mimetype) is None:
            file_type: str = "other"
        # sanitize the filename:
        server_filename: str = secure_filename(upload.filename)
        # Add the animal ID and a random string to the filename
        server_filename = str(uuid.uuid4()) + \
            "_{}_".format(animal_id) + server_filename
        # If the files directory doesn't exist... create it.
        if not os.path.exists(current_app.config["UPLOAD_FOLDER"]):
            os.makedirs(current_app.config["UPLOAD_FOLDER"])
        # save the file to the filesystem
        upload.save(os.path.join(
            current_app.config["UPLOAD_FOLDER"], server_filename))
        # Add the file to the database as uploaded
        new_db_file_entry: db.Files = db.Files(animalID=animal_id,
                                               fileName=server_filename,
                                               fileType=file_type)
        db_session.add(new_db_file_entry)
        db_session.commit()
    db_session.close()
    return success
