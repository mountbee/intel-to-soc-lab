# Intel Requirements - Credential Access (Auth Logs)

Dokumen ini menjadi kontrak kerja antara CTI/Hunter dan SOC untuk kasus credential access berbasis auth logs.

## 1) Scope & Objective
**In scope:**
- Aktivitas credential access pada auth logs: brute force, password spraying, dan credential stuffing.
- Aplikasi/layanan yang menghasilkan event autentikasi (VPN, SSO, email, portal aplikasi).

**Out of scope:**
- Akses awal via malware atau phishing tanpa jejak autentikasi.
- Pengambilalihan akun yang tidak meninggalkan pola login (token reuse tanpa event login).

**Outcome yang diharapkan:**
- Alerting yang bisa ditindak (triage → response).
- Hunting yang dapat diulang dengan hipotesis jelas.
- Playbook respons untuk kasus terverifikasi.

## 2) Threat Questions (Intel Requirements)
1. Apakah ada password spraying (1 IP → banyak akun dalam window waktu tertentu)?
2. Apakah ada brute force (1 akun → banyak attempt gagal beruntun)?
3. Apakah ada credential stuffing (rate tinggi, UA sama, beberapa sukses)?
4. Akun mana yang paling sering ditarget (top target by failed attempts)?
5. Apakah ada lonjakan login gagal pada jam tertentu atau di luar jam kerja?
6. Apakah ada pola “success after many failures” yang mencurigakan?
7. Apakah ada perubahan lokasi login yang signifikan untuk akun tertentu (berdasarkan geo/asn)?
8. Apakah ada sumber IP dengan rasio fail/success yang abnormal?
9. Apakah ada akun service/privileged yang mengalami spike gagal?
10. Apakah ada kombinasi IP + UA yang berulang pada banyak akun?

## 3) Data Sources & Minimum Fields
**Wajib (minimum):**
- `timestamp`
- `username`
- `src_ip`
- `auth_result` (success/fail)
- `user_agent`

**Ideal (nice to have):**
- `geo` / `asn`
- `device_id`
- `auth_method` (password/OAuth/token)
- `mfa_result`
- `failure_reason`
- `target_app`
- `tenant_org_id`

**Format waktu:** ISO 8601 (contoh: `2026-02-04T12:34:56Z`).
**Timezone assumption:** semua event dinormalisasi ke UTC.

**Example log row (CSV, 1 baris):**
```csv
2026-02-04T12:34:56Z,user@example.com,203.0.113.10,fail,"Mozilla/5.0",device-12345,password,none,invalid_password,portal-app,tenant-001
```

## 4) Collection Plan
- Frekuensi: harian (minimum), dengan batch tambahan jika ada lonjakan event.
- Retensi: minimum 14–30 hari untuk baseline dan korelasi pola.
- Normalisasi: dedup event duplikat, parsing timestamp ke UTC, dan standarisasi field.
- Catatan dataset simulasi: pola dapat bias dan tidak mewakili kondisi produksi.

## 5) Detection Coverage Goals
**Minimal detector yang dibuat:**
- Password spraying detector.
- Credential stuffing detector.

**Hunting workflow:**
- Hipotesis: “sumber IP/UA yang sama menyerang banyak akun dengan sebagian sukses.”

**Metrik sederhana:**
- False positive handling: pengecualian untuk IP kantor/proxy/NAT internal.
- Tuning knobs: threshold jumlah akun (`N`) dan window waktu (`W`).

## Escalation Criteria (SOC → IR)
- Terdeteksi login sukses setelah >`N` kegagalan dari sumber IP/UA baru.
- Terjadi kompromi pada akun privileged atau akun service kritikal.
- Pola stuffing/spraying terkonfirmasi pada banyak akun dalam window singkat.
- Ada indikasi persistensi (login sukses berulang dari sumber yang sama).

## 6) Confidence Model (1–5)
1. **Sangat rendah:** pola lemah, data minim, contoh: 3 gagal dalam 1 hari tanpa konteks.
2. **Rendah:** pola sebagian cocok, contoh: 1 IP → 5 akun tetapi hanya 1 sumber data.
3. **Sedang:** pola konsisten, contoh: 1 akun → >30 gagal dalam 10 menit.
4. **Tinggi:** multi-sinyal, contoh: fail spike + success after many failures + UA sama.
5. **Sangat tinggi:** multi-sumber terverifikasi dan dapat diulang, contoh: pola sama pada beberapa hari dengan bukti respons.

**Menaikkan confidence:**
- Korelasi event lintas sumber.
- Konsistensi pola pada waktu berbeda.
- Konfirmasi dari hasil hunting atau response.

## 7) Assumptions, Limitations, & Risks
- Tanpa geo/MFA logs, beberapa skenario tidak terdeteksi.
- Proxy kantor, NAT, atau SSO gateway bisa memicu false positive.
- Tidak semua aplikasi menghasilkan user_agent yang konsisten.
- Dataset simulasi membatasi akurasi baseline.

## 8) Deliverables (Target 2 Minggu)
- `packs/pack01-credential-access/intel/` berisi kebutuhan intel final dan catatan asumsi.
- `packs/pack01-credential-access/detections/` minimal 2 detector (spraying + stuffing).
- `packs/pack01-credential-access/hunting/` hasil hunting dan query yang digunakan.
- `packs/pack01-credential-access/playbook/` playbook respons ringkas.
- `packs/pack01-credential-access/data/` contoh input/log anonim untuk uji lokal.
