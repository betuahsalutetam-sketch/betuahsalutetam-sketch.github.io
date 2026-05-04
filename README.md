# Salut Etam Betuah — Website Resmi

Website Sentra Layanan Universitas Terbuka **Salut Etam Betuah** di Samarinda, Kalimantan Timur.

## ✅ Data yang sudah terpasang

- **Email**: bestuahsalutetam@gmail.com
- **WhatsApp Admin 1**: 0822-5063-8289 (utama, terpasang di semua tombol & form)
- **WhatsApp Admin 2**: 0852-5283-4986 (di section kontak)
- **Alamat**: Jl. Kadrie Oening No. 66A, Kel. Air Hitam, Kec. Samarinda Ulu, Samarinda, Kaltim
- **Logo SALUT** (asli, di navbar, hero, footer, audit BDO, tentang)
- **Logo BDO** (asli & sudah dibersihkan, di section Audit BDO)
- **15 foto kegiatan asli** dengan kategori akurat: Wisuda, Salut Talks, Sosprom, Tutorial, Ujian, Kunjungan

## 📸 Mapping Foto Galeri (sudah sesuai konten)

| Kategori | Jumlah | Konten |
|---|---|---|
| 🎓 **Wisuda** | 3 | Pak Husaini di banner wisuda 2026, tim wisudawan jas kuning, panggung penghargaan |
| 🎤 **Salut Talks** | 4 | Podcast 2 orang, diskusi 4 orang banner SALUT, workshop praktisi, sharing session |
| 📣 **Sosprom** | 2 | Sosialisasi siswa SMA, presentasi "Kenapa UT" dengan TV |
| 📚 **Tutorial** | 2 | Mahasiswa jas kuning + dosen, mahasiswa + presenter |
| 📝 **Ujian** | 3 | Lab komputer + pengawas, lab penuh, lab presenter |
| 🤝 **Kunjungan** | 1 | Pak Husaini bersama tokoh + bendera |

Plus 2 foto kantor (`kantor-resepsionis.jpg`, `kantor-luar.jpg`) tersedia untuk kebutuhan masa depan jika ingin section "Lokasi Kami".

## 🟡 Yang perlu Anda isi nanti

1. **Link sosial media** — buka `index.html`, cari `aria-label="Instagram"`, `aria-label="YouTube"`, `aria-label="Facebook"`. Ganti `href="#"` dengan URL akun Anda.
2. **Domain final** — saat sudah punya domain (mis. `salutetambetuah.co.id`), update di `sitemap.xml` dan tag `<link rel="canonical">` di `index.html`.

## 🚀 Cara Deploy (Pilih Salah Satu)

### Opsi 1: Netlify (Paling Mudah, Gratis) ⭐ Direkomendasikan

1. Buka https://app.netlify.com/drop
2. Drag-and-drop folder `salut-etam-betuah/` (atau extract ZIP dulu)
3. Tunggu 30 detik — selesai! Anda dapat URL gratis seperti `xxxxx.netlify.app`
4. Untuk pasang domain custom: Site settings → Domain management → Add custom domain

### Opsi 2: Vercel

1. Buka https://vercel.com/new
2. Login, pilih "Browse" lalu upload folder
3. Klik Deploy

### Opsi 3: GitHub Pages (Gratis selamanya)

```bash
cd salut-etam-betuah
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/salut-etam-betuah.git
git push -u origin main
```

Lalu di GitHub: Settings → Pages → Source: `main` branch → Save.

### Opsi 4: cPanel / Hosting Tradisional

1. Login ke cPanel hosting Anda
2. Buka File Manager → masuk ke `public_html`
3. Upload semua file dalam folder `salut-etam-betuah/`
4. Selesai!

## 📁 Struktur File

```
salut-etam-betuah/
├-- index.html             # Halaman utama
├-- robots.txt             # Untuk SEO
├-- sitemap.xml            # Untuk Google Search
├-- netlify.toml           # Config Netlify
├-- vercel.json            # Config Vercel
├-- README.md              # File ini
└-- assets/
    └-- images/
        ├-- logo.png                      # Logo SALUT (bulat, untuk navbar)
        ├-- logo-landscape.png            # Logo SALUT landscape
        ├-- logo-bdo.png                  # Logo BDO (sudah bersih)
        ├-- favicon.png                   # Icon tab browser
        ├-- og-image.jpg                  # Untuk preview saat di-share
        ├-- wisuda-1/2/3.jpg              # 3 foto wisuda
        ├-- salut-talks-1/2/3/4.jpg       # 4 foto Salut Talks
        ├-- sosprom-1/2.jpg               # 2 foto sosialisasi
        ├-- tutorial-1/2.jpg              # 2 foto tutorial
        ├-- ujian-1/2/3.jpg               # 3 foto ujian
        ├-- kunjungan-1.jpg               # 1 foto kunjungan
        ├-- kantor-resepsionis.jpg        # Foto kantor (tersedia)
        └-- kantor-luar.jpg               # Foto luar gedung (tersedia)
```

## 🎨 Fitur Website

- ✅ Responsif (mobile, tablet, desktop)
- ✅ SEO optimized (meta tags, Open Graph, JSON-LD, sitemap)
- ✅ Section Audit BDO yang prominen
- ✅ Galeri dengan **filter kategori** & **lightbox** (klik foto untuk perbesar)
- ✅ Form kontak otomatis kirim ke WhatsApp
- ✅ Floating WhatsApp button
- ✅ Smooth scroll & animasi modern
- ✅ Performance: gambar dioptimasi (~150 KB rata-rata)

## 🔗 Tautan Penting

- **Audit BDO Article**: https://infokaltim.id/lolos-audit-independen-bdo-salut-etam-betuah-buktikan-tata-kelola-layanan-pendidikan-berstandar-internasional/
- **Google Maps**: https://maps.app.goo.gl/FkwAV4UnkdAcQD5UA

---

© 2026 Salut Etam Betuah. Mitra layanan independen — bukan bagian resmi dari Universitas Terbuka.
