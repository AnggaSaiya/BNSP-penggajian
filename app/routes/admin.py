import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from sqlalchemy import exc
from ..models import User, Employee, Position, SalaryComponent, Attendance, Payroll
from ..services.payroll_service import create_payroll, get_payroll_summary
from ..utils import role_required
from ..extensions import db

admin_bp = Blueprint("admin", __name__)


def _validate_period(period):
    """Validasi format periode YYYY-MM"""
    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", period):
        raise ValueError("Format periode harus YYYY-MM (contoh: 2025-07).")


def _validate_required(form, fields):
    """Validasi field wajib diisi"""
    missing = [f for f in fields if not form.get(f, "").strip()]
    if missing:
        raise ValueError(f"Field wajib diisi: {', '.join(missing)}")


# ===================== DASHBOARD =====================

@admin_bp.route("/")
@login_required
@role_required("admin")
def dashboard():
    return render_template(
        "admin/dashboard.html",
        employees=Employee.query.count(),
        positions=Position.query.count(),
        payrolls=Payroll.query.count(),
        summaries=get_payroll_summary()
    )


# ===================== EMPLOYEES =====================

@admin_bp.route("/employees")
@login_required
@role_required("admin")
def employees():
    return render_template(
        "admin/employees.html",
        employees=Employee.query.order_by(Employee.id.desc()).all()
    )


@admin_bp.route("/employees/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def new_employee():
    positions = Position.query.order_by(Position.name).all()
    if request.method == "POST":
        try:
            _validate_required(
                request.form,
                ["employee_code", "full_name", "email", "position_id"]
            )
            employee_code = request.form["employee_code"].strip()
            password_default = employee_code.lower() + "123"

            # Cek apakah username atau employee_code sudah dipakai
            if User.query.filter_by(username=employee_code).first():
                flash(f"Username '{employee_code}' sudah digunakan.", "danger")
                return render_template("admin/employee_form.html", positions=positions, employee=None)
            if Employee.query.filter_by(employee_code=employee_code).first():
                flash(f"Kode pegawai '{employee_code}' sudah digunakan.", "danger")
                return render_template("admin/employee_form.html", positions=positions, employee=None)

            user = User(username=employee_code, role="employee")
            user.set_password(password_default)
            db.session.add(user)
            db.session.flush()

            employee = Employee(
                user_id=user.id,
                employee_code=employee_code,
                full_name=request.form["full_name"].strip(),
                email=request.form["email"].strip(),
                phone=request.form.get("phone", "").strip(),
                address=request.form.get("address", "").strip(),
                position_id=int(request.form["position_id"]),
                join_date=request.form.get("join_date", "").strip(),
                status=request.form.get("status", "ACTIVE"),
            )
            db.session.add(employee)
            db.session.commit()
            flash("Pegawai berhasil ditambahkan!", "success")
            return redirect(url_for("admin.employees"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Data gagal disimpan. Periksa kemungkinan kode pegawai atau username sudah digunakan.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template("admin/employee_form.html", positions=positions, employee=None)


@admin_bp.route("/employees/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_employee(id):
    employee = db.session.get(Employee, id)
    if not employee:
        abort(404)
    positions = Position.query.order_by(Position.name).all()
    if request.method == "POST":
        try:
            _validate_required(request.form, ["full_name", "email", "position_id"])
            employee.full_name = request.form["full_name"].strip()
            employee.email = request.form["email"].strip()
            employee.phone = request.form.get("phone", "").strip()
            employee.address = request.form.get("address", "").strip()
            employee.position_id = int(request.form["position_id"])
            employee.join_date = request.form.get("join_date", "").strip()
            employee.status = request.form.get("status", "ACTIVE")
            db.session.commit()
            flash("Data pegawai berhasil diperbarui.", "success")
            return redirect(url_for("admin.employees"))
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template("admin/employee_form.html", positions=positions, employee=employee)


@admin_bp.route("/employees/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_employee(id):
    employee = db.session.get(Employee, id)
    if not employee:
        abort(404)
    try:
        # Hapus juga User terkait jika ada (hanya jika role-nya employee)
        if employee.user and employee.user.role == "employee":
            db.session.delete(employee.user)
        elif employee.user:
            # Unlink manager user (jangan hapus karena akun manager self-register)
            employee.user_id = None
            employee.user.employee = None
        db.session.delete(employee)
        db.session.commit()
        flash("Pegawai berhasil dihapus.", "success")
    except exc.IntegrityError:
        db.session.rollback()
        flash("Tidak dapat menghapus pegawai karena masih memiliki data terkait (payroll/absensi).", "danger")
    return redirect(url_for("admin.employees"))


# ===================== POSITIONS =====================

@admin_bp.route("/positions", methods=["GET", "POST"])
@login_required
@role_required("admin")
def positions():
    if request.method == "POST":
        try:
            _validate_required(request.form, ["name", "base_salary"])
            position = Position(
                name=request.form["name"].strip(),
                base_salary=float(request.form["base_salary"]),
                description=request.form.get("description", "").strip()
            )
            db.session.add(position)
            db.session.commit()
            flash("Jabatan berhasil ditambahkan.", "success")
            return redirect(url_for("admin.positions"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Data gagal disimpan. Periksa kemungkinan nama jabatan sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template(
        "admin/positions.html",
        positions=Position.query.all()
    )


@admin_bp.route("/positions/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_position(id):
    position = db.session.get(Position, id)
    if not position:
        abort(404)
    if request.method == "POST":
        try:
            _validate_required(request.form, ["name", "base_salary"])
            position.name = request.form["name"].strip()
            position.base_salary = float(request.form["base_salary"])
            position.description = request.form.get("description", "").strip()
            db.session.commit()
            flash("Jabatan berhasil diperbarui.", "success")
            return redirect(url_for("admin.positions"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Nama jabatan sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template("admin/positions.html", positions=Position.query.all(), edit_position=position)


@admin_bp.route("/positions/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_position(id):
    position = db.session.get(Position, id)
    if not position:
        abort(404)
    try:
        db.session.delete(position)
        db.session.commit()
        flash("Jabatan berhasil dihapus.", "success")
    except exc.IntegrityError:
        db.session.rollback()
        flash("Tidak dapat menghapus jabatan karena masih ada pegawai dengan jabatan ini.", "danger")
    return redirect(url_for("admin.positions"))


# ===================== COMPONENTS =====================

@admin_bp.route("/components", methods=["GET", "POST"])
@login_required
@role_required("admin")
def components():
    if request.method == "POST":
        try:
            _validate_required(
                request.form,
                ["name", "component_type", "default_amount"]
            )
            amount = float(request.form["default_amount"])
            if amount < 0:
                raise ValueError("Nominal komponen tidak boleh negatif.")
            component = SalaryComponent(
                name=request.form["name"].strip(),
                component_type=request.form["component_type"],
                default_amount=float(request.form["default_amount"]),
                description=request.form.get("description", "").strip()
            )
            db.session.add(component)
            db.session.commit()
            flash("Komponen gaji berhasil ditambahkan.", "success")
            return redirect(url_for("admin.components"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Data gagal disimpan. Periksa kemungkinan nama komponen sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template(
        "admin/components.html",
        components=SalaryComponent.query.all()
    )


@admin_bp.route("/components/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_component(id):
    component = db.session.get(SalaryComponent, id)
    if not component:
        abort(404)
    if request.method == "POST":
        try:
            _validate_required(request.form, ["name", "component_type", "default_amount"])
            component.name = request.form["name"].strip()
            component.component_type = request.form["component_type"]
            component.default_amount = float(request.form["default_amount"])
            component.description = request.form.get("description", "").strip()
            db.session.commit()
            flash("Komponen gaji berhasil diperbarui.", "success")
            return redirect(url_for("admin.components"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Nama komponen sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    return render_template("admin/components.html", components=SalaryComponent.query.all(), edit_component=component)


@admin_bp.route("/components/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_component(id):
    component = db.session.get(SalaryComponent, id)
    if not component:
        abort(404)
    db.session.delete(component)
    db.session.commit()
    flash("Komponen gaji berhasil dihapus.", "success")
    return redirect(url_for("admin.components"))


# ===================== ATTENDANCE =====================

@admin_bp.route("/attendance", methods=["GET", "POST"])
@login_required
@role_required("admin")
def attendance():
    employees = Employee.query.filter_by(status="ACTIVE").all()
    if request.method == "POST":
        try:
            period = request.form["period"]
            _validate_period(period)
            _validate_required(request.form, ["employee_id", "period"])
            item = Attendance(
                employee_id=int(request.form["employee_id"]),
                period=period,
                work_days=int(request.form.get("work_days", 22)),
                absent_days=int(request.form.get("absent_days", 0)),
                overtime_hours=float(request.form.get("overtime_hours", 0)),
            )
            db.session.add(item)
            db.session.commit()
            flash("Data absensi berhasil disimpan.", "success")
            return redirect(url_for("admin.attendance"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Data absensi untuk pegawai dan periode tersebut sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    rows = Attendance.query.order_by(Attendance.period.desc()).all()
    return render_template("admin/attendance.html", employees=employees, rows=rows)


@admin_bp.route("/attendance/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_attendance(id):
    att = db.session.get(Attendance, id)
    if not att:
        abort(404)
    employees = Employee.query.filter_by(status="ACTIVE").all()
    if request.method == "POST":
        try:
            period = request.form["period"]
            _validate_period(period)
            _validate_required(request.form, ["employee_id", "period"])
            att.employee_id = int(request.form["employee_id"])
            att.period = period
            att.work_days = int(request.form.get("work_days", 22))
            att.absent_days = int(request.form.get("absent_days", 0))
            att.overtime_hours = float(request.form.get("overtime_hours", 0))
            db.session.commit()
            flash("Data absensi berhasil diperbarui.", "success")
            return redirect(url_for("admin.attendance"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Data absensi untuk pegawai dan periode tersebut sudah ada.", "danger")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    rows = Attendance.query.order_by(Attendance.period.desc()).all()
    return render_template("admin/attendance.html", employees=employees, rows=rows, edit_attendance=att)


@admin_bp.route("/attendance/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_attendance(id):
    att = db.session.get(Attendance, id)
    if not att:
        abort(404)
    db.session.delete(att)
    db.session.commit()
    flash("Data absensi berhasil dihapus.", "success")
    return redirect(url_for("admin.attendance"))


# ===================== PAYROLL =====================

@admin_bp.route("/payroll", methods=["GET", "POST"])
@login_required
@role_required("admin")
def payroll():
    employees = Employee.query.filter_by(status="ACTIVE").all()
    if request.method == "POST":
        try:
            period = request.form["period"]
            _validate_period(period)
            _validate_required(request.form, ["employee_id", "period"])
            create_payroll(
                employee_id=int(request.form["employee_id"]),
                period=period,
                bonus=float(request.form.get("bonus", 0))
            )
            flash("Payroll berhasil dibuat sebagai DRAFT.", "success")
        except ValueError as exc:
            flash(str(exc), "danger")
        return redirect(url_for("admin.payroll"))
    rows = Payroll.query.order_by(Payroll.created_at.desc()).all()
    return render_template("admin/payroll.html", employees=employees, rows=rows)


@admin_bp.route("/payroll/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_payroll(id):
    payroll = db.session.get(Payroll, id)
    if not payroll:
        abort(404)
    # Cegah edit jika status sudah APPROVED
    if payroll.status == "APPROVED":
        flash("Payroll dengan status APPROVED tidak dapat diedit.", "danger")
        return redirect(url_for("admin.payroll"))
    if request.method == "POST":
        try:
            payroll.base_salary = float(request.form.get("base_salary", payroll.base_salary))
            payroll.allowance = float(request.form.get("allowance", payroll.allowance))
            payroll.overtime = float(request.form.get("overtime", payroll.overtime))
            payroll.bonus = float(request.form.get("bonus", payroll.bonus))
            payroll.fixed_deduction = float(request.form.get("fixed_deduction", payroll.fixed_deduction))
            payroll.bpjs = float(request.form.get("bpjs", payroll.bpjs))
            payroll.tax = float(request.form.get("tax", payroll.tax))
            payroll.gross_salary = float(request.form.get("gross_salary", payroll.gross_salary))
            payroll.net_salary = float(request.form.get("net_salary", payroll.net_salary))
            # Hanya manager yang boleh mengubah status (via approve/reject di manager.py)
            payroll.notes = request.form.get("notes", payroll.notes)
            db.session.commit()
            flash("Payroll berhasil diperbarui.", "success")
            return redirect(url_for("admin.payroll"))
        except (ValueError, KeyError) as e:
            db.session.rollback()
            flash(str(e), "danger")
    employees = Employee.query.filter_by(status="ACTIVE").all()
    rows = Payroll.query.order_by(Payroll.created_at.desc()).all()
    return render_template("admin/payroll.html", employees=employees, rows=rows, edit_payroll=payroll)


@admin_bp.route("/payroll/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_payroll(id):
    payroll = db.session.get(Payroll, id)
    if not payroll:
        abort(404)
    # Cegah hapus jika status sudah APPROVED
    if payroll.status == "APPROVED":
        flash("Payroll dengan status APPROVED tidak dapat dihapus.", "danger")
        return redirect(url_for("admin.payroll"))
    db.session.delete(payroll)
    db.session.commit()
    flash("Payroll berhasil dihapus.", "success")
    return redirect(url_for("admin.payroll"))
