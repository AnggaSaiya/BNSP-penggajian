"""Test PDF generation for slip gaji - 1 page only"""
import sys, datetime
sys.path.insert(0, "d:/Kuliah bro/BNSP/Program BNSP/payroll_bns_project")
from app import create_app
app = create_app()
from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template
from app.models import Employee, Payroll, Attendance
from app.services.payroll_service import calculate_payroll, create_payroll
from app.extensions import db

with app.test_request_context():
    def now():
        return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    
    emp = Employee.query.first()
    if not emp:
        print("FAIL: No employees found, run seed.py first")
        sys.exit(1)
    
    payroll = Payroll.query.filter_by(employee_id=emp.id, status="APPROVED").first()
    if not payroll:
        try:
            payroll = create_payroll(employee_id=emp.id, period="2026-07")
            payroll.status = "APPROVED"
            payroll.approved_at = datetime.datetime.utcnow()
            db.session.commit()
        except ValueError as e:
            payroll = Payroll.query.filter_by(employee_id=emp.id, period="2026-07").first()
            if not payroll:
                print(f"FAIL: Cannot create payroll: {e}")
                sys.exit(1)
            payroll.status = "APPROVED"
            payroll.approved_at = datetime.datetime.utcnow()
            db.session.commit()
    
    print(f"Employee: {emp.employee_code} - {emp.full_name}")
    print(f"Payroll ID:{payroll.id}, Period:{payroll.period}, Status:{payroll.status}")
    
    html = render_template("karyawan/slip_gaji.html", payroll=payroll, employee=emp, now=now)
    print(f"HTML length: {len(html)} chars")
    
    buf = BytesIO()
    status = pisa.CreatePDF(src=html, dest=buf)
    print(f"PDF err: {status.err}")
    buf.seek(0)
    data = buf.read()
    print(f"PDF OK: {len(data)} bytes")
    
    with open("test_slip.pdf", "wb") as f:
        f.write(data)
    print("Saved to test_slip.pdf")
