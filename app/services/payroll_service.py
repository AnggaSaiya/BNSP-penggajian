from datetime import datetime
from sqlalchemy import text
from ..extensions import db
from ..models import Payroll, Employee, Attendance, SalaryComponent

OVERTIME_RATE = 50000
BPJS_RATE = 0.01
TAX_RATE = 0.02


def calculate_payroll(employee, period, bonus=0):
    position = employee.position
    attendance = Attendance.query.filter_by(
        employee_id=employee.id, period=period
    ).first()

    base_salary = position.base_salary if position else 0

    # Prorata gaji berdasarkan hari tidak masuk (absensi)
    if attendance:
        work_days = attendance.work_days or 22
        absent_days = attendance.absent_days or 0
        effective_days = max(work_days - absent_days, 0)
        if work_days > 0:
            base_salary = base_salary * effective_days / work_days

    allowance = sum(
        c.default_amount for c in SalaryComponent.query.filter_by(component_type="ALLOWANCE").all()
    )
    fixed_deduction = sum(
        c.default_amount for c in SalaryComponent.query.filter_by(component_type="DEDUCTION").all()
    )

    overtime_hours = attendance.overtime_hours if attendance else 0
    overtime = overtime_hours * OVERTIME_RATE

    gross_salary = base_salary + allowance + overtime + bonus
    bpjs = gross_salary * BPJS_RATE
    taxable_income = max(gross_salary - bpjs, 0)
    tax = taxable_income * TAX_RATE
    total_deduction = fixed_deduction + bpjs + tax
    net_salary = gross_salary - total_deduction

    return {
        "base_salary": base_salary,
        "allowance": allowance,
        "overtime": overtime,
        "bonus": bonus,
        "fixed_deduction": fixed_deduction,
        "bpjs": bpjs,
        "tax": tax,
        "gross_salary": gross_salary,
        "total_deduction": total_deduction,
        "net_salary": net_salary,
    }


def create_payroll(employee_id, period, bonus=0):
    employee = db.session.get(Employee, employee_id)
    if not employee:
        raise ValueError("Pegawai tidak ditemukan.")
    if employee.status != "ACTIVE":
        raise ValueError(
            f"Pegawai '{employee.full_name}' sudah tidak aktif "
            f"(status: {employee.status}). Tidak bisa dibuat payroll."
        )

    # Validasi periode payroll tidak boleh sebelum join_date
    if employee.join_date:
        join_period = employee.join_date[:7]
        if period < join_period:
            raise ValueError(
                f"Pegawai '{employee.full_name}' bergabung pada {employee.join_date}. "
                f"Tidak bisa membuat payroll untuk periode {period} (sebelum join date)."
            )

    existing = Payroll.query.filter_by(
        employee_id=employee_id,
        period=period
    ).filter(
        Payroll.status != "REJECTED"
    ).first()

    if existing:
        raise ValueError(
            "Payroll untuk pegawai dan periode tersebut sudah ada "
            "dan masih dalam proses atau sudah disetujui."
        )

    result = calculate_payroll(employee, period, bonus)

    payroll = Payroll(
        employee_id=employee_id,
        period=period,
        **result
    )

    db.session.add(payroll)
    db.session.commit()

    return payroll


def get_payroll_summary():
    # Contoh raw SQL untuk demonstrasi kompetensi SQL.
    query = text("""
        SELECT period, status, COUNT(*) AS total_payroll,
               SUM(net_salary) AS total_net_salary
        FROM payroll
        GROUP BY period, status
        ORDER BY period DESC
    """)
    return db.session.execute(query).mappings().all()


def approve_payroll(payroll):
    if payroll.status != "DRAFT":
        raise ValueError(f"Payroll dengan status {payroll.status} tidak bisa di-approve.")
    payroll.status = "APPROVED"
    payroll.approved_at = datetime.utcnow()
    db.session.commit()


def reject_payroll(payroll, notes):
    if payroll.status != "DRAFT":
        raise ValueError(f"Payroll dengan status {payroll.status} tidak bisa di-reject.")
    existing_notes = payroll.notes or ""
    payroll.status = "REJECTED"
    payroll.notes = (existing_notes + "\n[REJECTED] " + notes).strip()
    db.session.commit()
