# Data Dictionary - Pack 01 Auth Logs

## Kolom
- `timestamp`: Waktu event autentikasi dalam ISO 8601. Semua event menggunakan UTC (`Z`).
- `user`: Identifier pengguna (email dummy).
- `src_ip`: IPv4 sumber autentikasi.
- `status`: Hasil autentikasi (`success` atau `fail`).
- `user_agent`: User agent perangkat/klien.

## Pola yang Disimulasikan
- **Password spraying**: 1–2 IP mencoba banyak akun dalam window singkat, mayoritas gagal.
- **Brute force akun tunggal**: 1 akun ditarget dari 1 IP dengan banyak gagal beruntun, ada kemungkinan 1 sukses.
- **Credential stuffing**: Rate tinggi, UA sama, banyak username berbeda, campuran gagal/sukses.
- **Proxy/NAT noise**: Satu IP kantor memunculkan banyak user dengan mayoritas sukses.

## Asumsi Timezone
Semua timestamp berada pada UTC dengan sufiks `Z`.
