from flask import Blueprint, render_template

index_app = Blueprint("index_app", __name__, template_folder='templates', static_folder='./static')


@index_app.route("/", methods=["GET"])
def method_get():
    return render_template("index.html")
