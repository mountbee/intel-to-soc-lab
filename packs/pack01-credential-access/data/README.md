# Data Pack 01

## iocs_raw.txt
Daftar IOC dummy untuk latihan normalisasi dan pengujian dedup.
Isinya campuran IP, domain, URL, hash, dan email dengan beberapa duplikat.

## Cara menghasilkan iocs.json
Gunakan CLI normalizer berikut (copy-paste):
```bash
python tools/ioc_normalizer/ioc_normalizer.py \
  --input packs/pack01-credential-access/data/iocs_raw.txt \
  --output packs/pack01-credential-access/data/iocs.json \
  --source pack01-osint \
  --confidence 3 \
  --pack pack01 \
  --tag credential-access
```

## Aturan
Semua data di folder ini bersifat dummy untuk latihan dan pengujian.
