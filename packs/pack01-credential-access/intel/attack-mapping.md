# Attack Mapping - Credential Access (Pack 01)

## 1) Scope & Data Reality
Mapping ini berbasis auth logs dengan field minimum: `timestamp`, `user`, `src_ip`, `status`, `user_agent`.
Field ideal (opsional) untuk memperkuat confidence: `geo`, `asn`, `device_id`, `mfa_result`.

## 2) ATT&CK Mapping (High-level)
| Tactic | Technique (nama) | Kenapa relevan | Data source (auth logs) |
|---|---|---|---|
| Credential Access | Brute Force | Upaya mencoba banyak kredensial untuk satu akun atau banyak akun | Auth logs (success/fail, user, src_ip, user_agent) |
| Credential Access | Password Spraying | Upaya 1 sumber mencoba banyak akun dengan sedikit percobaan per akun | Auth logs (user, src_ip, status, timestamp) |
| Credential Access | Credential Stuffing | Pengujian kredensial hasil kebocoran pada banyak akun, sebagian sukses | Auth logs (success/fail, user_agent, src_ip) |
| Initial Access (opsional) | Valid Accounts | Akun valid dipakai untuk akses awal setelah stuffing berhasil | Auth logs (success events) |
| Defense Evasion (opsional) | Modify Authentication Process | Upaya menghindari kontrol autentikasi; sering tidak terlihat di auth logs | Keterbatasan: umumnya tidak terlihat dari auth logs saja |
| Discovery (opsional) | Account Discovery | Pencarian akun biasanya tidak muncul di auth logs | Keterbatasan: butuh data lain (directory logs) |

## 3) Telemetry → Observable → Detection/Hunting
| Observable (dari auth logs) | Sinyal utama | Heuristik deteksi | Parameter tuning | False positives umum | Apa yang memperkuat confidence |
|---|---|---|---|---|---|
| Banyak `user` unik dari 1 `src_ip` dalam window | Pola spraying | Hitung unique users per IP per window | `N_users`, `W_minutes` | NAT/proxy kantor | Konsistensi `user_agent` dan peningkatan fail rate |
| Banyak gagal untuk 1 `user` | Brute force akun tunggal | Hitung failed attempts per user per window | `N_fails`, `W_minutes` | User lupa password | `src_ip`/`user_agent` konsisten dan meningkat tajam |
| Success setelah banyak fail | Kompromi setelah percobaan | Deteksi urutan fail → success untuk user yang sama | `N_fails_before_success`, `W_minutes` | User reset password | Success dari `src_ip`/`user_agent` baru |
| `user_agent` konsisten untuk banyak akun | Bot reuse UA | Hitung jumlah akun per UA per window | `N_users`, `W_minutes` | Aplikasi resmi populer | UA sama + fail dominan |
| Spike gagal pada jam tertentu | Aktivitas otomatis | Bandingkan baseline jam kerja | `fail_rate_delta`, `W_hours` | Maintenance/seasonal | Kenaikan tajam di luar jam kerja |
| Distribusi IP per user tidak normal | Login dari banyak sumber | Hitung unique IP per user per window | `N_ips`, `W_hours` | Mobile/ISP dinamis | IP baru + fail dominan |
| “Impossible travel” [OPTIONAL: `geo`] | Lokasi tidak masuk akal | Selisih jarak/waktu antar login sukses | `max_km_per_hour`, `W_hours` | VPN/roaming | Geo baru + `user_agent` baru |
| Anomali perangkat [OPTIONAL: `device_id`] | Perangkat baru | Login sukses dari device baru setelah banyak fail | `N_fails_before_success`, `W_minutes` | Perangkat baru sah | Device baru + IP baru |
| Rasio fail/success tinggi per IP | Attack yang tidak berhasil | Fail rate per IP > threshold | `fail_rate`, `W_minutes`, `min_attempts` | Testing internal | Fail dominan + banyak user |
| Banyak akun dengan UA kosong/generik | Otomasi | UA kosong/generik + fail dominan | `N_events`, `W_minutes` | Perangkat lama | UA kosong + IP baru |

## 4) Detection Backlog (Roadmap)
- Detector #1: Password spraying (`N`, `W`, `failure_rate_threshold`).
  - Target file: `packs/pack01-credential-access/detections/detector-password-spraying.md`
- Detector #2: Credential stuffing (rate, UA, `unique_users`, `success_mix`).
  - Target file: `packs/pack01-credential-access/detections/detector-credential-stuffing.md`
- Hunt workflow: triage suspicious IP & targeted accounts.
  - Target file: `packs/pack01-credential-access/hunting/hunt-suspicious-ips.md`

## 5) Notes on Limitations
- Auth logs saja tidak cukup untuk memastikan root cause (mis. phishing atau token theft tanpa event login).
- NAT/proxy/SSO gateway dapat membuat banyak user tampak dari 1 IP (false positive).
- Tanpa `geo`/`device_id`/`mfa_result`, confidence dan triage akan lebih rendah.

## Example Thresholds (Starter)
- `N_users`: 10 dalam `W_minutes`: 10 (indikasi spraying).
- `N_fails`: 20 dalam `W_minutes`: 10 (indikasi brute force akun tunggal).
- `fail_rate`: 0.9 dengan `min_attempts`: 30 (indikasi IP agresif).
- `N_fails_before_success`: 10 dalam `W_minutes`: 15 (indikasi kompromi setelah percobaan).
- `N_events`: 50 dalam `W_minutes`: 10 untuk UA kosong/generik.
