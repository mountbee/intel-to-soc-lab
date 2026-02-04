# IOC Normalizer

CLI sederhana untuk menormalkan IOC dari input teks/CSV menjadi format JSON yang konsisten.

## Cara Install
Gunakan dependensi dari root repo:
```bash
make venv
make install
```

## Contoh Run
```bash
python tools/ioc_normalizer/ioc_normalizer.py \
  --input data/ioc.txt \
  --output out/ioc_normalized.json \
  --source pack01-osint \
  --confidence 3 \
  --pack pack01 \
  --tag credential-access
```

## Data Contract
- Schema: lihat `tools/ioc_normalizer/schema.json`.
- Dedup rules:
  - Domain dan email didedup secara case-insensitive.
  - Domain/host di-normalisasi ke lowercase.
  - Whitespace di-trim sebelum klasifikasi.
- Normalisasi URL/domain:
  - URL: scheme + host di-lowercase, path/query dipertahankan.
  - Domain: selalu lowercase.
- Tags vs context:
  - `tags` untuk label kategorikal (mis. `spraying`, `phishing`).
  - `context` untuk penjelasan singkat kenapa IOC relevan.
