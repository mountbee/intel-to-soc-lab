# Confidence Scale (1–5)

Skala ini dipakai untuk menilai tingkat keyakinan terhadap IOC.
Semakin tinggi nilai, semakin kuat bukti dan konsistensi observasi.

## Definisi Level
1. **Sangat rendah**: Indikasi lemah, data terbatas, belum tervalidasi.
2. **Rendah**: Ada pola awal, tetapi masih banyak noise atau sumber tunggal.
3. **Sedang**: Pola konsisten dan bisa diulang, namun bukti belum lengkap.
4. **Tinggi**: Banyak sinyal mendukung, korelasi kuat, dan konteks jelas.
5. **Sangat tinggi**: Bukti kuat lintas sumber, tervalidasi, dan berdampak.

## Contoh Pemakaian (CTI)
- Level 2: IOC dari satu laporan publik tanpa konfirmasi lapangan.
- Level 3: IOC muncul berulang pada beberapa insiden internal.
- Level 5: IOC terkonfirmasi lewat multiple sources dan memiliki chain-of-evidence.

## Contoh Pemakaian (SOC)
- Level 1–2: Gunakan untuk hunting ringan dan penambahan watchlist.
- Level 3: Naikkan prioritas alert dan lakukan triage terjadwal.
- Level 4–5: Eskalasi cepat, jalankan containment/response bila sesuai.

## Faktor yang Menaikkan Confidence
- Konsistensi pola pada waktu berbeda.
- Korelasi lintas data source (auth logs, endpoint, network).
- Konfirmasi hasil hunting atau investigasi.
- Konteks kuat (TTP, kampanye, dan target yang selaras).

## Faktor yang Menurunkan Confidence
- Sumber tunggal tanpa validasi.
- IOC sudah lama dan tidak muncul lagi.
- Banyak false positive atau konflik dengan data internal.

## Common Mistakes
- Memberi confidence tinggi tanpa bukti lintas sumber atau tanpa verifikasi internal.
- Mencampur penilaian IOC (indikator) dengan TTP (pola), padahal horizon waktunya berbeda.
- Mengabaikan konteks waktu (IOC lama tetap diberi confidence tinggi).
- Tidak membedakan sumber primer vs sekunder.

## Peringatan
IOC cepat basi, sedangkan TTP lebih tahan lama. Prioritaskan pemetaan TTP untuk deteksi jangka panjang.
