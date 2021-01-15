from flask import render_template, Blueprint, session as flask_session, redirect

bp = Blueprint('animals', __name__, url_prefix="")


@bp.route("/animals")
def query():
    """
    Page with the list of all animals, which can be filtered.
    """
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    return render_template("animals.html", title="Animals")
