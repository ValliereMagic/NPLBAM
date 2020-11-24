from flask import render_template, Blueprint

bp = Blueprint('animals', __name__, url_prefix="")


@bp.route("/animals")
def query():
    return render_template("animals.html", title="Animals")
