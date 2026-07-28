# Strategi Testing

## Unit Test
Menguji fungsi perhitungan payroll secara terisolasi.

Jalankan:
pytest tests/test_payroll_service.py -v

## Integration Test
Menguji alur login dan akses dashboard menggunakan Flask test client.

Jalankan:
pytest tests/test_integration.py -v

## Semua Test
pytest -v
