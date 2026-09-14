from app import create_app
from app.extensions import db
from app.models import User, Employee, Position, SalaryComponent, Attendance

app = create_app()

with app.app_context():
    # ===================== USERS =====================
    seed_users = [
        ("admin", "admin123", "admin"),
        ("manager", "manager123", "manager"),
        ("employee", "employee123", "manager"),
    ]
    for username, password, role in seed_users:
        if not User.query.filter_by(username=username).first():
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            print(f"  [OK] User '{username}' ditambahkan.")
        else:
            print(f"  [--] User '{username}' sudah ada, skip.")

    db.session.flush()

    user_map = {}
    for u in User.query.all():
        user_map[u.username] = u

    # ===================== POSITIONS =====================
    positions_data = [
        ("Direktur", 25000000, "Direktur utama perusahaan"),
        ("Manager", 10000000, "Pimpinan unit/bagian"),
        ("Supervisor", 8000000, "Pengawas tim operasional"),
        ("Staff Senior", 7000000, "Staff dengan pengalaman lebih dari 3 tahun"),
        ("Staff", 6000000, "Staff operasional"),
        ("Staff Junior", 4500000, "Staff pemula / fresh graduate"),
        ("Admin", 5000000, "Administrasi perkantoran"),
        ("Finance", 6500000, "Staff keuangan & akuntansi"),
        ("HRD", 6500000, "Human resource development"),
        ("Teknisi", 5500000, "Teknisi lapangan / IT support"),
    ]
    pos_map = {}
    for name, salary, desc in positions_data:
        pos = Position.query.filter_by(name=name).first()
        if not pos:
            pos = Position(name=name, base_salary=salary, description=desc)
            db.session.add(pos)
            db.session.flush()
            print(f"  [OK] Jabatan '{name}' ditambahkan.")
        else:
            print(f"  [--] Jabatan '{name}' sudah ada, skip.")
        pos_map[name] = pos

    # ===================== EMPLOYEES =====================
    employees_data = [
        {"username": "employee", "code": "EMP001", "name": "Andi Pratama", "email": "andi@example.com", "phone": "08123456789", "address": "Jakarta", "position": "Staff", "join_date": "2025-01-10"},
        {"username": "emp002", "code": "EMP002", "name": "Budi Santoso", "email": "budi@example.com", "phone": "08129876543", "address": "Bekasi", "position": "Manager", "join_date": "2023-05-12"},
        {"username": "emp003", "code": "EMP003", "name": "Citra Dewi", "email": "citra@example.com", "phone": "08131122334", "address": "Bandung", "position": "Supervisor", "join_date": "2024-03-01"},
        {"username": "emp004", "code": "EMP004", "name": "Dodi Firmansyah", "email": "dodi@example.com", "phone": "08145566778", "address": "Tangerang", "position": "Staff Senior", "join_date": "2022-07-15"},
        {"username": "emp005", "code": "EMP005", "name": "Eka Wulandari", "email": "eka@example.com", "phone": "08159900112", "address": "Depok", "position": "Finance", "join_date": "2024-06-20"},
        {"username": "emp006", "code": "EMP006", "name": "Fajar Nugroho", "email": "fajar@example.com", "phone": "08162233445", "address": "Bogor", "position": "Teknisi", "join_date": "2025-02-10"},
        {"username": "emp007", "code": "EMP007", "name": "Gita Permata Sari", "email": "gita@example.com", "phone": "08173344556", "address": "Jakarta", "position": "HRD", "join_date": "2024-09-01"},
        {"username": "emp008", "code": "EMP008", "name": "Hendra Gunawan", "email": "hendra@example.com", "phone": "08184455667", "address": "Bekasi", "position": "Staff Junior", "join_date": "2026-01-05"},
        {"username": "emp009", "code": "EMP009", "name": "Intan Ayu R.", "email": "intan@example.com", "phone": "08195566778", "address": "Bandung", "position": "Admin", "join_date": "2025-05-19"},
        {"username": "emp010", "code": "EMP010", "name": "Joko Susilo", "email": "joko@example.com", "phone": "08216677889", "address": "Tangerang", "position": "Staff", "join_date": "2026-03-12"},
        {"username": "emp011", "code": "EMP011", "name": "Kartika Sari Dewi", "email": "kartika@example.com", "phone": "08227788990", "address": "Jakarta", "position": "Staff", "join_date": "2025-08-01"},
        {"username": "emp012", "code": "EMP012", "name": "Lukman Hakim", "email": "lukman@example.com", "phone": "08238899001", "address": "Bekasi", "position": "Teknisi", "join_date": "2024-11-15"},
        {"username": "emp013", "code": "EMP013", "name": "Maya Anggraini", "email": "maya@example.com", "phone": "08249900112", "address": "Bandung", "position": "Finance", "join_date": "2025-04-20"},
        {"username": "emp014", "code": "EMP014", "name": "Nanda Pratama Putra", "email": "nanda@example.com", "phone": "08250011223", "address": "Tangerang", "position": "Staff Senior", "join_date": "2023-09-10"},
        {"username": "emp015", "code": "EMP015", "name": "Olivia Rahmawati", "email": "olivia@example.com", "phone": "08261122334", "address": "Depok", "position": "HRD", "join_date": "2025-06-01"},
        {"username": "emp016", "code": "EMP016", "name": "Pramono Adi Wibowo", "email": "pramono@example.com", "phone": "08272233445", "address": "Bogor", "position": "Supervisor", "join_date": "2024-01-20"},
        {"username": "emp017", "code": "EMP017", "name": "Qori Amalia", "email": "qori@example.com", "phone": "08283344556", "address": "Jakarta", "position": "Staff", "join_date": "2026-02-14"},
        {"username": "emp018", "code": "EMP018", "name": "Rizky Fadhilah", "email": "rizky@example.com", "phone": "08294455667", "address": "Bekasi", "position": "Staff Junior", "join_date": "2026-04-01"},
        {"username": "emp019", "code": "EMP019", "name": "Sari Puspita Dewi", "email": "sari@example.com", "phone": "08305566778", "address": "Bandung", "position": "Admin", "join_date": "2025-07-15"},
        {"username": "emp020", "code": "EMP020", "name": "Teguh Santoso", "email": "teguh@example.com", "phone": "08316677889", "address": "Tangerang", "position": "Staff", "join_date": "2025-10-05"},
        {"username": "emp021", "code": "EMP021", "name": "Umi Kalsum", "email": "umi@example.com", "phone": "08327788990", "address": "Depok", "position": "Staff Senior", "join_date": "2024-05-18"},
        {"username": "emp022", "code": "EMP022", "name": "Vino Bastian", "email": "vino@example.com", "phone": "08338899001", "address": "Bogor", "position": "Teknisi", "join_date": "2025-11-22"},
        {"username": "emp023", "code": "EMP023", "name": "Winda Lestari", "email": "winda@example.com", "phone": "08349900112", "address": "Jakarta", "position": "Finance", "join_date": "2025-03-10"},
        {"username": "emp024", "code": "EMP024", "name": "Xaverius Rudi", "email": "xaverius@example.com", "phone": "08350011223", "address": "Bekasi", "position": "Staff", "join_date": "2026-05-01"},
        {"username": "emp025", "code": "EMP025", "name": "Yuniarti Kusuma", "email": "yuni@example.com", "phone": "08361122334", "address": "Bandung", "position": "HRD", "join_date": "2024-08-25"},
        {"username": "emp026", "code": "EMP026", "name": "Zainal Arifin", "email": "zainal@example.com", "phone": "08372233445", "address": "Tangerang", "position": "Supervisor", "join_date": "2023-12-01"},
        {"username": "emp027", "code": "EMP027", "name": "Ayu Pratiwi", "email": "ayu@example.com", "phone": "08383344556", "address": "Depok", "position": "Staff", "join_date": "2026-06-15"},
        {"username": "emp028", "code": "EMP028", "name": "Bagas Putra", "email": "bagas@example.com", "phone": "08394455667", "address": "Bogor", "position": "Staff Junior", "join_date": "2026-07-01"},
        {"username": "emp029", "code": "EMP029", "name": "Cindy Permata", "email": "cindy@example.com", "phone": "08405566778", "address": "Jakarta", "position": "Admin", "join_date": "2025-09-12"},
        {"username": "emp030", "code": "EMP030", "name": "Dimas Ardiansyah", "email": "dimas@example.com", "phone": "08416677889", "address": "Bekasi", "position": "Staff", "join_date": "2026-08-01"},
    ]

    for ed in employees_data:
        user = User.query.filter_by(username=ed["username"]).first()
        if not user:
            user = User(username=ed["username"], role="karyawan")
            user.set_password(ed["code"].lower() + "123")
            db.session.add(user)
            db.session.flush()
            print(f"  [OK] User '{ed['username']}' dibuat untuk {ed['code']}.")
        user_map[ed["username"]] = user

        emp = Employee.query.filter_by(employee_code=ed["code"]).first()
        if not emp:
            emp = Employee(
                user_id=user.id, employee_code=ed["code"],
                full_name=ed["name"], email=ed["email"],
                phone=ed["phone"], address=ed["address"],
                position_id=pos_map[ed["position"]].id,
                join_date=ed["join_date"], status="ACTIVE",
            )
            db.session.add(emp)
            db.session.flush()
            print(f"  [OK] Pegawai '{ed['code']} - {ed['name']}' ditambahkan.")
        else:
            if not emp.user_id:
                emp.user_id = user.id
                print(f"  [OK] Pegawai '{ed['code']}' di-link ke user '{ed['username']}'.")
            else:
                print(f"  [--] Pegawai '{ed['code']}' sudah ada & sudah punya user, skip.")

    # ===================== SALARY COMPONENTS =====================
    components_data = [
        ("Tunjangan Transport", "ALLOWANCE", 500000, "Tunjangan transport bulanan"),
        ("Tunjangan Makan", "ALLOWANCE", 750000, "Tunjangan makan bulanan"),
        ("Potongan Koperasi", "DEDUCTION", 100000, "Potongan koperasi"),
    ]
    for name, ctype, amount, desc in components_data:
        if not SalaryComponent.query.filter_by(name=name).first():
            sc = SalaryComponent(name=name, component_type=ctype, default_amount=amount, description=desc)
            db.session.add(sc)
            db.session.flush()
            print(f"  [OK] Komponen '{name}' ditambahkan.")
        else:
            print(f"  [--] Komponen '{name}' sudah ada, skip.")

    # ===================== ATTENDANCES =====================
    all_emps = Employee.query.order_by(Employee.id).all()
    attendance_data = [
        (all_emps[0], "2026-07", 22, 0, 5),
        (all_emps[1], "2026-07", 22, 1, 3),
        (all_emps[2], "2026-07", 22, 2, 4),
        (all_emps[3], "2026-07", 22, 0, 2),
        (all_emps[4], "2026-07", 22, 1, 0),
        (all_emps[5], "2026-07", 22, 0, 3),
        (all_emps[6], "2026-07", 22, 1, 1),
        (all_emps[7], "2026-07", 22, 3, 0),
        (all_emps[8], "2026-07", 22, 0, 0),
        (all_emps[9], "2026-07", 22, 2, 2),
        (all_emps[10], "2026-07", 22, 0, 4),
        (all_emps[11], "2026-07", 22, 1, 2),
        (all_emps[12], "2026-07", 22, 0, 0),
        (all_emps[13], "2026-07", 22, 2, 3),
        (all_emps[14], "2026-07", 22, 0, 1),
    ]
    for emp, period, work, absent, overtime in attendance_data:
        if emp and not Attendance.query.filter_by(employee_id=emp.id, period=period).first():
            att = Attendance(employee_id=emp.id, period=period, work_days=work, absent_days=absent, overtime_hours=overtime)
            db.session.add(att)
            print(f"  [OK] Absensi {emp.employee_code} periode {period} ditambahkan.")
        elif emp:
            print(f"  [--] Absensi {emp.employee_code} periode {period} sudah ada, skip.")

    db.session.commit()
    print("\n✅ Seed selesai. Data baru ditambahkan tanpa menghapus data existing.")
