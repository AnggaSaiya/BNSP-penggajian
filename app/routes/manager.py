from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from ..models import Payroll
from ..services.payroll_service import approve_payroll, reject_payroll
from ..utils import role_required
from ..extensions import db

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/")
@login_required
@role_required("manager")
def dashboard():
    rows = Payroll.query.order_by(Payroll.created_at.desc()).all()
    return render_template("manager/dashboard.html", rows=rows)


@manager_bp.route("/payroll/<int:payroll_id>/approve", methods=["POST"])
@login_required
@role_required("manager")
def approve(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    try:
        approve_payroll(payroll)
        flash("Payroll berhasil di-approve.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/payroll/<int:payroll_id>/reject", methods=["POST"])
@login_required
@role_required("manager")
def reject(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    try:
        reject_payroll(payroll, request.form.get("notes", "Perlu diperbaiki."))
        flash("Payroll dikembalikan ke Admin.", "warning")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("manager.dashboard"))
