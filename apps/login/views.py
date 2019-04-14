from flask import Blueprint, render_template
login_app = Blueprint("login_app", __name__, template_folder='templates', static_folder='./static')


@login_app.route("/login", methods=["GET"])
def method_get():
    return render_template("login.html")


@login_app.route("/login", methods=["POST"])
def method_post():
    return render_template("login.html")
