# BNSP Payroll Management System

Aplikasi web Sistem Informasi Penggajian untuk proyek sertifikasi BNSP Skema Analis Program.

## Stack
- Python
- Flask 3.x
- Flask-SQLAlchemy
- SQLite
- Flask-Login
- Bootstrap 5 CDN
- pytest

## Role
1. **Admin**: mengelola pegawai, jabatan, komponen gaji, absensi, dan payroll.
2. **Manager**: review dan approve/reject payroll.
3. **Karyawan**: melihat dan mendownload slip gaji yang sudah di-approve.

## Alur Payroll
```
DRAFT  →  APPROVED (oleh Manager)  →  Karyawan bisa lihat slip gaji
       ↘  REJECTED (oleh Manager)   →  Admin perbaiki, buat ulang
```

## Aturan Perhitungan
- **Gross** = Gaji Pokok + Tunjangan + Lembur + Bonus
- **Total Potongan** = Potongan Tetap + BPJS + Pajak
- **Gaji Bersih** = Gross - Total Potongan

### Prorata Absensi
Jika ada hari tidak masuk (absent), gaji pokok dipotong proporsional:
```
Gaji Pokok Efektif = Gaji Pokok × (Hari Kerja - Hari Absen) / Hari Kerja
```

### Komponen Perhitungan
| Komponen | Keterangan |
|----------|------------|
| Tunjangan Transport | Rp 500.000 (default) |
| Tunjangan Makan | Rp 750.000 (default) |
| Potongan Koperasi | Rp 100.000 (default) |
| Lembur | Rp 50.000 / jam |
| BPJS | 1% dari Gross |
| Pajak | 2% dari (Gross - BPJS) |

## Akun Demo
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| Karyawan | emp001 | emp001123 |
| Karyawan | emp002 | emp002123 |

## Menjalankan

### Windows
```powershell
# 1. Buka folder proyek
cd d:\Kuliah bro\BNSP\Program BNSP\payroll_bns_project

# 2. Buat virtual environment
python -m venv .venv

# 3. Aktifkan
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Seed database
python seed.py

# 6. Jalankan
python run.py

# 7. Buka http://127.0.0.1:5000
```

Database SQLite dibuat di `instance/payroll.db`.

## Fitur Lengkap

### Admin (`/admin`)
- Dashboard ringkasan data
- CRUD Pegawai (dengan auto-create User + password default)
- CRUD Jabatan & Gaji Pokok
- CRUD Tunjangan & Potongan
- CRUD Absensi & Lembur
- CRUD Payroll (dengan proteksi status APPROVED)

### Manager (`/manager`)
- Review daftar payroll
- Approve (DRAFT → APPROVED)
- Reject (DRAFT → REJECTED, dengan catatan)

### Karyawan (`/karyawan`)
- Lihat daftar slip gaji yang sudah APPROVED
- Detail slip gaji (lengkap dengan perhitungan)
- Download slip gaji sebagai file HTML

### Keamanan & Validasi
- Role-based access control (`@role_required`)
- Validasi periode >= join_date
- Cegah edit/delete payroll APPROVED
- Cegah approve/reject payroll non-DRAFT
- Cek status pegawai ACTIVE sebelum buat payroll
- Unique constraint (employee + period) untuk absensi & payroll
- Case-insensitive username lookup
- Validasi nilai negatif pada komponen gaji
- Proteksi akun Manager saat hapus pegawai

## Kompetensi BNSP yang Dipetakan
- **SQL**: query SQLAlchemy dan SQL mentah (`text()`) pada `payroll_service.py`
- **Akses basis data**: Flask-SQLAlchemy ORM
- **Algoritma**: `app/services/payroll_service.py` — perhitungan gaji prorata
- **Dokumentasi**: `docs/`
- **Debugging**: `docs/DEBUGGING.md`
- **Profiling**: `docs/PROFILING.md`
- **Code review**: `docs/CODE_REVIEW.md`
- **Unit testing**: `tests/test_payroll_service.py` (3 tests)
- **Integration testing**: `tests/test_integration.py` (2 tests)
- **Skalabilitas**: `docs/SCALABILITY.md`

## Struktur Proyek
```
payroll_bns_project/
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── extensions.py         # db, login_manager
│   ├── models.py             # User, Employee, Position, SalaryComponent, Attendance, Payroll
│   ├── utils.py              # @role_required decorator
│   ├── routes/
│   │   ├── auth.py           # Login/logout
│   │   ├── main.py           # Dashboard redirect
│   │   ├── admin.py          # Admin CRUD
│   │   ├── manager.py        # Manager approve/reject
│   │   └── karyawan.py       # Karyawan slip gaji
│   ├── services/
│   │   └── payroll_service.py  # Payroll calculation engine
│   └── templates/
│       ├── base.html
│       ├── auth/             # login.html, register.html
│       ├── admin/            # dashboard, employees, positions, components, attendance, payroll
│       └── karyawan/         # dashboard, slip_gaji
├── tests/
│   ├── test_integration.py
│   └── test_payroll_service.py
├── docs/                     # Dokumentasi BNSP
├── run.py                    # Entry point
├── seed.py                   # Database seeder
├── requirements.txt
└── README.md
```

## Catatan
Konfigurasi pajak/BPJS pada aplikasi ini adalah simulasi edukasi untuk kebutuhan asesmen, bukan kalkulator payroll/legal compliance untuk produksi.
