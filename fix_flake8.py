import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Fix admin.py - long lines E501
with open('app/routes/admin.py', 'r', newline='') as f:
    content = f.read()

old1 = 'return render_template("admin/attendance.html", employees=employees, rows=Attendance.query.order_by(Attendance.period.desc()).all(), edit_attendance=att)'
new1 = 'rows = Attendance.query.order_by(Attendance.period.desc()).all()\n    return render_template("admin/attendance.html", employees=employees, rows=rows, edit_attendance=att)'
if old1 in content:
    content = content.replace(old1, new1)
    print('Fixed admin.py E501 line 363')

old2 = 'return render_template("admin/payroll.html", employees=Employee.query.filter_by(status="ACTIVE").all(), rows=Payroll.query.order_by(Payroll.created_at.desc()).all(), edit_payroll=payroll)'
new2 = 'employees = Employee.query.filter_by(status="ACTIVE").all()\n    rows = Payroll.query.order_by(Payroll.created_at.desc()).all()\n    return render_template("admin/payroll.html", employees=employees, rows=rows, edit_payroll=payroll)'
if old2 in content:
    content = content.replace(old2, new2)
    print('Fixed admin.py E501 line 434')

with open('app/routes/admin.py', 'w', newline='') as f:
    f.write(content)

print('\nAll fixes applied!')
