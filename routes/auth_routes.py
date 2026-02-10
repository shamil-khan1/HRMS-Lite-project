from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

# 🔐 Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# 🚪 Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

