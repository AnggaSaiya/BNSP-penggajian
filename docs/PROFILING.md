# Profiling Program

Profiling digunakan untuk menemukan bagian program yang menggunakan waktu atau resource paling besar.

Contoh demo:
python -m cProfile -s cumtime run.py

Untuk pengujian endpoint, gunakan browser developer tools atau alat benchmarking lokal.

Fokus profiling:
- Waktu query payroll.
- Query laporan dashboard.
- Perhitungan payroll massal.
- Waktu render halaman.

Jika jumlah payroll meningkat, optimasi dapat dilakukan dengan indexing, pagination, mengurangi query berulang, dan memindahkan proses berat ke background job.
