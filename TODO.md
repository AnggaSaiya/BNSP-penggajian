# Bug Fix Progress ✅

- [x] 1. Prorata gaji berdasarkan absent_days di `payroll_service.py`
- [x] 2. Error handling duplicate employee_code di `admin.py`
- [x] 3. Pindahkan import `abort` ke top-level di `employee.py`
- [x] 4. Tambah UniqueConstraint Attendance (employee_id + period) di `models.py`
- [x] 5. Ganti `query.get_or_404` → `db.session.get()` di `manager.py` & `employee.py`
- [x] 6. Validasi format period YYYY-MM di route yang relevan
- [x] 7. Update unit tests + tambah test absent_days
- [x] 8. Tambah 10 jabatan di seed data
- [x] 9. Auto-create User account saat tambah pegawai baru
- [x] 10. Tampilkan username login di tabel data pegawai
- [x] 11. Seed idempoten (tidak hapus data existing)
- [x] 12. EMP002 (Budi Santoso) di-link ke user emp002
- [x] 13. Cek status pegawai non-AKTIF sebelum buat payroll
- [x] 14. Tambah UniqueConstraint Payroll (employee_id + period) di level DB
- [x] 15. Buang dead code `effective_days` yang tidak terpakai
- [x] 16. Pesan error IntegrityError yang lebih informatif (tidak menyesatkan)
- [x] 17. Tambah `check_login.py` ke .gitignore

---

# New Feature: Self-Registration — REMOVED ❌

- [x] 18-23. Fitur register dihapus — hanya role admin & manager dengan login manual

---

# Phase 2: Hapus Role "employee" ✅

- [x] 24. Role default register jadi "manager" (bukan "employee")
- [x] 25. Hapus blueprint `employee.py` dan folder template employee/
- [x] 26. Route `/main/dashboard` fallback semua non-admin ke manager dashboard
- [x] 27. Sidebar base.html: hapus link `employee.dashboard`, ganti dengan manager
- [x] 28. Seed.py: role "employee" → "manager"
- [x] 29. Update integration test: assert role "manager", assert "Review Payroll"
- [x] 30. Semua 10 test passing ✅

---

# Phase 3: Fitur Edit & Hapus Data ✅

- [x] 31. Route edit/delete Employee + form edit dengan data lama
- [x] 32. Route edit/delete Position + inline edit form
- [x] 33. Route edit/delete SalaryComponent + inline edit form
- [x] 34. Route edit/delete Attendance + inline edit form
- [x] 35. Route edit/delete Payroll + edit form detail
- [x] 36. Tombol Edit/Hapus di semua tabel dengan konfirmasi
- [x] 37. Error handling: IntegrityError jika data masih dipakai
- [x] 38. Semua test tetap 10/10 passing ✅

---

# Phase 4: Perbaikan Periode & Payroll ✅

- [x] 39. Validasi period >= join_date di `create_payroll()`
- [x] 40. Blokir edit/delete payroll APPROVED
- [x] 41. Ubah input period manual jadi `<input type="month">`

---

# Phase 5: Full Debug HTML ✅

- [x] 42. Fix HTML `login.html` — tambah 3 `</div>` penutup + hapus demo employee
- [x] 43. Fix HTML `register.html` — perbaiki div nesting (username & password tidak tertutup)
- [x] 44. Fix HTML `base.html` — tambah `</div>` penutup container-fluid/row
- [x] 45. Verifikasi semua test: **10/10 passed** ✅

# Phase 6: Final Bug Squash (13 Bugs Fixed) ✅

- [x] Bug 1: Manager approve/reject guard — hanya bisa DRAFT (`payroll_service.py` + `manager.py`)
- [x] Bug 2: Delete employee jangan hapus manager's User account (`admin.py`)
- [x] Bug 3: Validasi negative values (`admin.py` — komponen + absensi)
- [x] Bug 4: Payroll edit form — tambah `</div>` penutup row (`payroll.html`)
- [x] Bug 5: `base.html` — tambah `</div>` untuk `container-fluid`
- [x] Bug 6: `login.html` — tambah 3 `</div>` penutup
- [x] Bug 7: `register.html` — tutup div username & password
- [x] Bug 8: `attendance.html` — tambah `</div>` untuk row edit form
- [x] Bug 9: `positions.html` — tambah `</div>` untuk row edit form
- [x] Bug 10: `register.html` — "otomatis kapital" → "otomatis lowercase"
- [x] Bug 11: `reject_payroll()` — preserve existing notes (`payroll_service.py`)
- [x] Bug 12: Duplicate `employee_code` check di `new_employee()` (`admin.py`)
- [x] Bug 13: `seed.py` — role "employee" → "manager" (bisa login)
- [x] Verifikasi: **10/10 tests passing** ✅
