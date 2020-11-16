from flask import render_template, Blueprint

bp = Blueprint('index', __name__, url_prefix="")


@bp.route("/")
def index():
    test_str: str = "Banana Bread"
    return render_template("index.html", test=test_str)
