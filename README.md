# BNSP Payroll Management System

Aplikasi web Sistem Informasi Penggajian untuk proyek sertifikasi BNSP Skema Analis Program.

## Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-Login
- Bootstrap 5 CDN
- pytest

## Role
1. Admin: mengelola pegawai, jabatan, komponen gaji, absensi, dan payroll.
2. Manager: review dan approve/reject payroll.

## Alur Payroll
DRAFT -> APPROVED atau REJECTED.
Jika rejected, Admin dapat memperbaiki/membuat ulang payroll.
Slip gaji hanya dapat dilihat setelah payroll APPROVED.

## Aturan Perhitungan
Gross = Gaji Pokok + Tunjangan + Lembur + Bonus
Total Potongan = Potongan Tetap + BPJS + Pajak
Gaji Bersih = Gross - Total Potongan

Lembur:
Jam lembur x tarif lembur per jam.

BPJS dan pajak pada proyek demo ini menggunakan persentase yang dapat dikonfigurasi per payroll.

## Akun Demo
- Admin: admin / admin123
- Manager: manager / manager123

## Menjalankan
Windows:
1. Buka folder proyek.
2. Buat virtual environment:
   python -m venv .venv
3. Aktifkan:
   .venv\Scripts\activate
4. Install:
   pip install -r requirements.txt
5. Seed database:
   python seed.py
6. Jalankan:
   python run.py
7. Buka:
   http://127.0.0.1:5000

Database SQLite dibuat di instance/payroll.db.

## Kompetensi BNSP yang dipetakan
- SQL: query SQLAlchemy dan SQL mentah pada service/report.
- Akses basis data: Flask-SQLAlchemy.
- Algoritma: app/services/payroll_service.py.
- Dokumentasi: docs/.
- Debugging: docs/DEBUGGING.md.
- Profiling: docs/PROFILING.md.
- Code review: docs/CODE_REVIEW.md.
- Unit testing: tests/test_payroll_service.py.
- Integration testing: tests/test_integration.py.
- Skalabilitas: docs/SCALABILITY.md.

Catatan: konfigurasi pajak/BPJS pada aplikasi adalah simulasi edukasi untuk kebutuhan asesmen, bukan kalkulator payroll/legal compliance produksi.