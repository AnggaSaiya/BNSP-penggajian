from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ..models import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        # Case-insensitive lookup
        user = User.query.filter(
            db.func.lower(User.username) == db.func.lower(username)
        ).first()

        if user and user.check_password(password):
            # Hanya admin dan manager yang boleh login (employee tidak punya akses login)
            if user.role == "employee":
                flash("Akun pegawai tidak memiliki akses login.", "danger")
                return render_template("auth/login.html")
            login_user(user)
            return redirect(url_for("main.dashboard"))

        flash("Username atau password salah.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
