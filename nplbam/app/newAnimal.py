from flask import render_template, Blueprint, session as flask_session, redirect

bp = Blueprint('newAnimal', __name__, url_prefix="")

@bp.route("/newAnimal")
def query():
    if flask_session.get("userID", default=None) is None:
        return redirect("/")
    return render_template("addDog.html", title="Add Dog")
