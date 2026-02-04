# Intel Notes - Credential Access (SOC Actionable)

## Note 01
Observation: Satu `src_ip` melakukan login gagal ke banyak `user` dalam window waktu sempit.
Why it matters: Pola kuat password spraying.
What to look for in auth logs: `timestamp` rapat, `src_ip` sama, `user` banyak, `status=fail`, `user_agent` relatif konsisten.
Suggested control/mitigation: Rate limiting per IP dan MFA untuk akun target.
Confidence (1–5): 4

## Note 02
Observation: Satu `user` mengalami banyak `status=fail` beruntun.
Why it matters: Indikasi brute force pada akun tunggal.
What to look for in auth logs: `timestamp` rapat, `user` sama, `status=fail` berulang, `src_ip` bisa sama/berbeda, `user_agent` bisa konsisten.
Suggested control/mitigation: Lockout bertahap dan alert per akun.
Confidence (1–5): 4

## Note 03
Observation: Banyak akun gagal lalu ada `status=success` dari `src_ip` dan `user_agent` yang sama.
Why it matters: Pola credential stuffing dengan keberhasilan.
What to look for in auth logs: `timestamp` rapat, `user` banyak, `status=fail` diikuti `status=success`, `src_ip`/`user_agent` sama.
Suggested control/mitigation: Bot detection, throttle login, reset kredensial akun terdampak.
Confidence (1–5): 5

## Note 04
Observation: Lonjakan login gagal pada jam tidak biasa.
Why it matters: Otomasi sering berjalan di luar jam kerja.
What to look for in auth logs: agregasi `timestamp`, lonjakan `status=fail`, banyak `user`, `src_ip` berulang, `user_agent` cenderung seragam.
Suggested control/mitigation: Alerting berbasis baseline jam kerja.
Confidence (1–5): 3

## Note 05
Observation: Banyak `status=fail` dengan `user_agent` kosong atau sangat generik.
Why it matters: Otomasi kadang menghilangkan UA.
What to look for in auth logs: `timestamp` rapat, `user_agent` kosong/seragam, `src_ip` berulang, `user` beragam, `status=fail`.
Suggested control/mitigation: Block UA kosong dan terapkan challenge tambahan.
Confidence (1–5): 3

## Note 06
Observation: `user_agent` sama digunakan oleh banyak akun berbeda dalam waktu singkat.
Why it matters: Tool otomatis atau bot reuse UA.
What to look for in auth logs: `timestamp` rapat, `user_agent` identik, `user` banyak, `src_ip` bisa sama, `status=fail` dominan.
Suggested control/mitigation: Rate limit per UA + IP, enforce MFA.
Confidence (1–5): 3

## Note 07
Observation: `status=success` muncul setelah serangkaian `status=fail` untuk `user` yang sama.
Why it matters: Kemungkinan kredensial akhirnya berhasil.
What to look for in auth logs: `timestamp` rapat, `user` sama, urutan fail → success, `src_ip` dan `user_agent` konsisten.
Suggested control/mitigation: Tandai akun berisiko dan force password reset.
Confidence (1–5): 4

## Note 08
Observation: Akun privileged/service menjadi target login gagal berulang.
Why it matters: Targeting akun bernilai tinggi.
What to look for in auth logs: `user` ada di daftar privileged (eksternal), `status=fail` berulang, `src_ip` sama, `user_agent` seragam, `timestamp` rapat.
Suggested control/mitigation: MFA wajib dan lockout lebih ketat.
Confidence (1–5): 4

## Note 09
Observation: `src_ip` baru menarget banyak akun dalam window singkat.
Why it matters: Sumber baru sering terkait kampanye.
What to look for in auth logs: `timestamp` rapat, `src_ip` baru, `user` banyak, `status=fail` dominan, `user_agent` konsisten.
Suggested control/mitigation: Rate limit, blacklist sementara, dan evaluasi reputasi IP (opsional: geo/asn).
Confidence (1–5): 3

## Note 10
Observation: Rasio `status=fail` jauh lebih tinggi daripada `status=success` untuk satu `src_ip`.
Why it matters: Indikasi brute force atau spraying.
What to look for in auth logs: agregasi per `src_ip`, `status` fail/success, `timestamp` window, `user` beragam, `user_agent` konsisten.
Suggested control/mitigation: Threshold alerting dan throttling per IP.
Confidence (1–5): 4

## Note 11
Observation: Pola login gagal berulang dari `src_ip` yang sama setiap hari.
Why it matters: Otomasi yang terus mencoba.
What to look for in auth logs: `timestamp` periodik, `src_ip` sama, `status=fail` berulang, `user` beragam, `user_agent` konsisten.
Suggested control/mitigation: Blok IP berulang, rate limit adaptif.
Confidence (1–5): 3

## Note 12
Observation: `src_ip` yang sama menunjukkan `user_agent` berubah-ubah saat gagal login.
Why it matters: Evasion untuk menghindari deteksi berbasis UA.
What to look for in auth logs: `timestamp` rapat, `src_ip` sama, `user_agent` banyak variasi, `status=fail` dominan, `user` beragam.
Suggested control/mitigation: Rate limit per IP, deteksi anomali UA.
Confidence (1–5): 3

## Note 13
Observation: Banyak akun gagal dengan `user_agent` yang sama lalu beberapa sukses.
Why it matters: Stuffing dengan sebagian kredensial valid.
What to look for in auth logs: `timestamp` rapat, `user` banyak, `user_agent` identik, `status=fail` dan sebagian `status=success`, `src_ip` sama.
Suggested control/mitigation: Reset kredensial, monitor akun sukses, enable MFA.
Confidence (1–5): 5

## Note 14
Observation: `status=success` dari `src_ip` baru untuk akun yang punya riwayat gagal.
Why it matters: Kompromi setelah percobaan.
What to look for in auth logs: `timestamp` berdekatan, `user` sama, `status=fail` historis, `status=success` dari `src_ip` baru, `user_agent` serupa.
Suggested control/mitigation: Force reset dan review akses awal.
Confidence (1–5): 4

## Note 15
Observation: Perubahan lokasi login yang signifikan untuk akun yang sama.
Why it matters: Kemungkinan penyalahgunaan kredensial.
What to look for in auth logs: `timestamp` rapat, `user` sama, `src_ip` berbeda jauh, `status` sukses, `user_agent` berbeda. Opsional: `geo/asn` untuk konfirmasi.
Suggested control/mitigation: Challenge tambahan atau verifikasi out-of-band.
Confidence (1–5): 3

## Note 16
Observation: Banyak akun dari satu `src_ip` tetapi pola sukses/gagal normal dan konsisten.
Why it matters: Potensi false positive karena proxy/NAT kantor.
What to look for in auth logs: `timestamp` normal, `src_ip` sama, `user` banyak, `status=success` dominan, `user_agent` beragam tapi stabil.
Suggested control/mitigation: Allowlist IP internal dan perlakukan sebagai noise setelah verifikasi.
Confidence (1–5): 2

## Mapping cepat
A) Spraying: Note 01, Note 09, Note 10, Note 11, Note 12
B) Stuffing: Note 03, Note 05, Note 06, Note 13
C) Brute force akun tunggal: Note 02, Note 07, Note 08, Note 14
D) Noise/false positives: Note 04, Note 16
E) Mitigasi prioritas: Note 01, Note 02, Note 03, Note 07, Note 08, Note 14, Note 16
