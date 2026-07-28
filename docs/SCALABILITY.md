# Analisis Skalabilitas

SQLite dipilih karena aplikasi ini digunakan untuk demonstrasi dan pengembangan lokal. Kelebihannya adalah sederhana, portable, dan tidak membutuhkan database server.

Keterbatasan:
- Tidak ideal untuk banyak transaksi write secara bersamaan.
- Tidak dirancang sebagai database server multi-user skala besar.
- Skalabilitas horizontal terbatas.

Strategi pengembangan:
1. Memindahkan database ke PostgreSQL/MySQL untuk produksi.
2. Menambahkan indexing pada kolom pencarian seperti employee_code, period, dan status.
3. Pagination pada daftar pegawai dan payroll.
4. Memisahkan service layer dan database layer.
5. Menambahkan caching untuk laporan yang sering diakses.
6. Menambahkan background job untuk proses payroll massal.
7. Menambahkan monitoring dan profiling endpoint.

Karena akses database menggunakan SQLAlchemy, migrasi database dapat dilakukan tanpa mengubah seluruh logika bisnis aplikasi.
