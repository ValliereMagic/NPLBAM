from flask import render_template, Blueprint, session as flask_session, redirect

bp = Blueprint('new_animal', __name__, url_prefix="")

@bp.route("/new_animal")
def query():
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    return render_template("add_dog.html", title="Add Dog")
