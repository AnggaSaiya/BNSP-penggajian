# Code Review Checklist

Checklist:
- Penamaan variabel jelas.
- Function memiliki satu tanggung jawab utama.
- Business logic tidak ditempatkan langsung di template.
- Query database tidak dibuat berulang tanpa kebutuhan.
- Validasi input dilakukan.
- Password disimpan dalam bentuk hash.
- Role access diperiksa di server.
- Error handling tersedia.
- Tidak ada credential hardcoded untuk production.
- Test tersedia untuk business logic penting.

Contoh hasil review:
Sebelum: logika perhitungan gaji berada di route.
Sesudah: logika dipindahkan ke payroll_service.py.
Alasan: separation of concerns, testability, dan maintainability meningkat.
