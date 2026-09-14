from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    if current_user.role == "manager":
        return redirect(url_for("manager.dashboard"))
    # Karyawan/employee role diarahkan ke karyawan dashboard (slip gaji)
    return redirect(url_for("karyawan.dashboard"))
