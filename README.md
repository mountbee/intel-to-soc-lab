# intel-to-soc-lab

Repo ini mendukung alur kerja **Intel → Detection → Hunting → Playbook** dengan struktur konsisten dan tooling ringan.

## Quick Setup
```bash
./scripts/bootstrap.sh
```

Atau manual:
```bash
make venv
make install
```

## Make Targets
- `make venv` membuat virtual environment `.venv` bila belum ada.
- `make install` memasang dependensi dari `requirements.txt`.
- `make test` menjalankan `pytest`.
- `make tree` menampilkan struktur folder.
- `make help` menampilkan daftar target.

## Menjalankan Test
```bash
make test
```

## Pack 01: Credential Access
- TODO: Tambahkan deskripsi pack, scope, dan referensi utama.

## Pack 02: Phishing to Endpoint
- TODO: Tambahkan deskripsi pack, scope, dan referensi utama.
