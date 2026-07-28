import re

# Fix models.py - blank line at end
with open('app/models.py', 'r') as f:
    content = f.read()
content = content.rstrip('\n') + '\n'
with open('app/models.py', 'w') as f:
    f.write(content)

# Fix manager.py - blank line at end  
with open('app/routes/manager.py', 'r') as f:
    content = f.read()
content = content.rstrip('\n') + '\n'
with open('app/routes/manager.py', 'w') as f:
    f.write(content)

# Fix admin.py F541 - f-string without placeholder
with open('app/routes/admin.py', 'r') as f:
    content = f.read()
content = content.replace('flash(f"Pegawai berhasil ditambahkan!", "success")', 'flash("Pegawai berhasil ditambahkan!", "success")')
with open('app/routes/admin.py', 'w') as f:
    f.write(content)

# Fix test_integration.py - remove unused Employee import
with open('tests/test_integration.py', 'r') as f:
    content = f.read()
content = content.replace('from app.models import User, Employee, Position', 'from app.models import User, Position')
with open('tests/test_integration.py', 'w') as f:
    f.write(content)

# Fix main.py E302 - remove extra blank line
with open('app/routes/main.py', 'r') as f:
    content = f.read()
content = content.replace('main_bp = Blueprint("main", __name__)\n\n\n@main_bp.route("/")', 'main_bp = Blueprint("main", __name__)\n\n@main_bp.route("/")')
with open('app/routes/main.py', 'w') as f:
    f.write(content)

# Fix test_payroll_service.py - blank line at end
with open('tests/test_payroll_service.py', 'r') as f:
    content = f.read()
content = content.rstrip('\n') + '\n'
with open('tests/test_payroll_service.py', 'w') as f:
    f.write(content)

print('All fixes applied')
