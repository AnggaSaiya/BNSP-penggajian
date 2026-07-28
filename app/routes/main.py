from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    # Manager role diarahkan ke manager dashboard
    return redirect(url_for("manager.dashboard"))
