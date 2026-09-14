import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, make_response
from flask_login import login_required, current_user
from ..models import Payroll, Employee
from ..utils import role_required
from ..extensions import db

karyawan_bp = Blueprint("karyawan", __name__)


def _now():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")


@karyawan_bp.route("/")
@login_required
@role_required("karyawan", "employee")
def dashboard():
    # Cari Employee berdasarkan user_id yang login
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee:
        flash("Data pegawai tidak ditemukan untuk akun ini.", "danger")
        return render_template("karyawan/dashboard.html", rows=[], employee=None)

    # Hanya tampilkan payroll yang sudah APPROVED
    rows = Payroll.query.filter_by(
        employee_id=employee.id, status="APPROVED"
    ).order_by(Payroll.period.desc()).all()

    return render_template("karyawan/dashboard.html", rows=rows, employee=employee)


@karyawan_bp.route("/slip-gaji/<int:payroll_id>")
@login_required
@role_required("karyawan", "employee")
def slip_gaji(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        abort(404)

    # Pastikan karyawan hanya bisa lihat slip gaji miliknya sendiri
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee or payroll.employee_id != employee.id:
        abort(403)

    return render_template("karyawan/slip_gaji.html", payroll=payroll, employee=employee, now=_now)


@karyawan_bp.route("/slip-gaji/<int:payroll_id>/download")
@login_required
@role_required("karyawan", "employee")
def download_slip(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        abort(404)

    # Pastikan karyawan hanya bisa download slip gaji miliknya sendiri
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee or payroll.employee_id != employee.id:
        abort(403)

    html = render_template("karyawan/slip_gaji.html", payroll=payroll, employee=employee, now=_now)

    from io import BytesIO
    from xhtml2pdf import pisa

    try:
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(src=html, dest=pdf_buffer)

        if pisa_status.err:
            raise Exception("Gagal mengkonversi HTML ke PDF.")

        pdf_buffer.seek(0)
        filename = f"slip_gaji_{employee.employee_code}_{payroll.period}.pdf"
        response = make_response(pdf_buffer.read())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        flash(f"Gagal generate PDF: {str(e)}", "danger")
        # Fallback: download sebagai HTML
        resp = make_response(html)
        resp.headers["Content-Type"] = "text/html; charset=utf-8"
        fallback_name = f"slip_gaji_{employee.employee_code}_{payroll.period}.html"
        resp.headers["Content-Disposition"] = f'attachment; filename="{fallback_name}"'
        return resp
