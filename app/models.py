from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    employee = db.relationship("Employee", back_populates="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    base_salary = db.Column(db.Float, nullable=False, default=0)
    description = db.Column(db.Text)

    employees = db.relationship("Employee", back_populates="position")


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=True)
    employee_code = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"), nullable=False)
    join_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="ACTIVE")

    user = db.relationship("User", back_populates="employee")
    position = db.relationship("Position", back_populates="employees")
    attendances = db.relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    payrolls = db.relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")


class SalaryComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    component_type = db.Column(db.String(20), nullable=False)  # ALLOWANCE / DEDUCTION
    default_amount = db.Column(db.Float, nullable=False, default=0)
    description = db.Column(db.Text)


class Attendance(db.Model):
    __table_args__ = (
        db.UniqueConstraint("employee_id", "period", name="uq_attendance_employee_period"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    period = db.Column(db.String(7), nullable=False)
    work_days = db.Column(db.Integer, default=22)
    absent_days = db.Column(db.Integer, default=0)
    overtime_hours = db.Column(db.Float, default=0)

    employee = db.relationship("Employee", back_populates="attendances")


class Payroll(db.Model):
    __table_args__ = (
        db.UniqueConstraint("employee_id", "period", name="uq_payroll_employee_period"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    period = db.Column(db.String(7), nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    allowance = db.Column(db.Float, default=0)
    overtime = db.Column(db.Float, default=0)
    bonus = db.Column(db.Float, default=0)
    fixed_deduction = db.Column(db.Float, default=0)
    bpjs = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    gross_salary = db.Column(db.Float, default=0)
    total_deduction = db.Column(db.Float, default=0)
    net_salary = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="DRAFT")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    employee = db.relationship("Employee", back_populates="payrolls")
