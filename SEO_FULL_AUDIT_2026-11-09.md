# Audit SEO Penuh dan Perbaikan, 9 November 2026

Cakupan: 60 berkas HTML, sitemap, robots.txt, llms.txt, workflow GitHub Actions. Data Google (GSC, GA4, CrUX) dan DataForSEO tidak tersambung di sesi ini, jadi skor performa dan indeks tidak diukur.

## Temuan dan perbaikan
| Area | Temuan | Perbaikan |
| --- | --- | --- |
| Teknis | lastmod sitemap dan dateModified dinaikkan otomatis tiap hari walau isi tidak berubah | `scripts/update_lastmod.py` memakai tanggal perubahan isi dari riwayat git; kedua workflow memakainya |
| On-page | 9 meta description di bawah 110 karakter | Ditulis ulang 130 sampai 160 karakter |
| Sosial | 32 halaman tanpa kartu Twitter, 5 tanpa og:image | Ditambahkan dari og:title, og:description, dan og-image |
| Gambar | 226 tag img masih jpg/png padahal ada webp; 178 tanpa width/height; logo 254 KB | Diganti webp, ukuran ditambahkan, 73 gambar di bawah lipatan dibuat lazy; logo kini 45 KB |
| Schema | HowTo (rich result dihentikan Sept 2023) di 5 halaman; alumni.html tanpa BreadcrumbList; profil Samarinda tanpa Article; 3 artikel tanpa dateModified | HowTo dihapus, sisanya ditambahkan |
| Konten | 3 halaman kota tipis dan mirip satu sama lain | Ditambah daftar layanan dan konteks pekerja per kota |
| Tautan internal | 5 artikel hanya punya 1 tautan masuk | Blok "Baca juga" di 50 halaman, dipilih menurut kemiripan topik |
| Kesegaran | 46 artikel tanpa tanggal terlihat | Tanggal "Terakhir diperbarui" di 50 halaman, disinkronkan dengan dateModified |
| AI search | Belum ada ringkasan harga yang mudah dibaca agen AI | `pricing.md`, dirujuk dari llms.txt |
| Konsistensi | llms.txt menulis arti "Etam Betuah" sebagai bahasa Banjar "Kita Bersungguh-sungguh"; semua halaman lain dan BRAND_GUIDELINES menulis bahasa Kutai "Kita Beruntung/Sejahtera" | llms.txt dan llms-full.txt disamakan |

## Belum bisa diperbaiki dari repo
- `_headers` dan `_redirects` memakai sintaks Netlify, jadi header keamanan (HSTS, CSP) tidak berlaku di GitHub Pages. Jalan keluarnya: Cloudflare di depan domain.
- Angka biaya per semester (selesai): kedua angka benar karena UT punya dua sistem. SIPAS (paket) sekitar Rp 1,5 sampai 3,5 juta per semester, Non-SIPAS per SKS sekitar Rp 900.000 sampai 1.500.000 untuk 15 SKS. Seluruh situs kini menyebut keduanya
- Penulis artikel masih Organization. Byline orang dengan profil penulis akan memperkuat E-E-A-T.
- Halaman tips lulus UT masih memuat `cdn.tailwindcss.com`. Ganti dengan `assets/css/tailwind.min.css` seperti halaman lain agar render lebih cepat.

## Langkah manual
1. Search Console: kirim ulang sitemap, minta indeks untuk beranda dan 3 halaman kota.
2. Tambah peristiwa GA4 untuk klik WhatsApp.
3. Cek Google Business Profile: kategori, jam, foto, balasan ulasan.
4. Cari sumber luar (media, direktori pendidikan, Wikipedia bila memenuhi syarat) karena AI lebih sering mengutip pihak ketiga daripada situs sendiri.
