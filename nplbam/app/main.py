from flask import render_template, Blueprint

bp = Blueprint('index', __name__, url_prefix="")


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")
