# Skenario Debugging

Contoh bug:
Payroll menghasilkan gaji lembur 0 walaupun pegawai memiliki jam lembur.

Langkah:
1. Reproduksi bug dengan data attendance periode yang sama.
2. Periksa nilai overtime_hours dari database.
3. Periksa filter employee_id dan period.
4. Periksa rumus overtime = overtime_hours * OVERTIME_RATE.
5. Tambahkan logging sementara.
6. Perbaiki query/filter.
7. Jalankan ulang unit test dan integration test.

Bukti demo:
- Tampilkan kondisi sebelum perbaikan.
- Tampilkan hasil investigasi.
- Tampilkan perubahan kode.
- Tampilkan hasil test setelah perbaikan.
