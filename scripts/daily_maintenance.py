#!/usr/bin/env python3
"""Daily Maintenance Script — Salut Etam Betuah (No API required)"""

import requests, datetime, json, os, random

TODAY    = datetime.date.today()
BULAN    = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
            7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
TODAY_ID  = f"{TODAY.day} {BULAN[TODAY.month]} {TODAY.year}"
DAY_NAME  = TODAY.strftime("%A").replace(
    "Monday","Senin").replace("Tuesday","Selasa").replace(
    "Wednesday","Rabu").replace("Thursday","Kamis").replace(
    "Friday","Jumat").replace("Saturday","Sabtu").replace("Sunday","Minggu")

print(f"📅 {DAY_NAME}, {TODAY_ID}")

# ── STEP 1: Fetch Google Reviews ───────────────────────────────
api_key  = os.environ.get("GOOGLE_PLACES_API_KEY", "")
place_id = os.environ.get("GOOGLE_PLACE_ID", "")
reviews  = []

if api_key and place_id:
    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/place/details/json",
            params={"place_id": place_id, "fields": "reviews",
                    "language": "id", "reviews_sort": "newest", "key": api_key},
            timeout=10
        )
        data = resp.json()
        if data.get("status") == "OK":
            GRADS = ["from-blue-500 to-blue-700","from-amber-500 to-orange-600",
                     "from-emerald-500 to-teal-600","from-purple-500 to-indigo-600",
                     "from-rose-500 to-pink-600","from-cyan-500 to-blue-600"]
            for r in data.get("result", {}).get("reviews", []):
                if r.get("rating") != 5: continue
                text = r.get("text","").strip()
                if len(text) < 20: continue
                author = r.get("author_name","Anonim")
                parts  = author.strip().split()
                initials = (parts[0][0] + (parts[1][0] if len(parts)>1 else parts[0][-1])).upper()
                reviews.append({
                    "author":   author,
                    "initials": initials,
                    "text":     text[:280]+("..." if len(text)>280 else ""),
                    "time":     r.get("relative_time_description",""),
                    "gradient": GRADS[len(reviews) % len(GRADS)]
                })
            print(f"✅ {len(reviews)} ulasan bintang 5 diambil")
        else:
            print(f"ℹ️  Google API: {data.get('status')} — skip review sync")
    except Exception as e:
        print(f"ℹ️  Google API tidak tersedia: {e}")
else:
    print("ℹ️  Google secrets belum diset — skip review sync")

# ── STEP 2: Update testimoni di index.html ─────────────────────
if reviews and os.path.exists("index.html"):
    try:
        def esc(t):
            return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        def build(r):
            return (f'        <div class="testi-item shadow-card">\n'
                    f'          <div class="flex items-center gap-3 mb-4">\n'
                    f'            <div class="w-10 h-10 rounded-full bg-gradient-to-br {r["gradient"]} '
                    f'flex items-center justify-center text-sm font-bold text-white flex-shrink-0">'
                    f'{esc(r["initials"])}</div>\n'
                    f'            <div><div class="text-sm font-bold text-brand-navy">{esc(r["author"])}</div>'
                    f'<div class="text-[10px] text-slate-400">Google Maps · {esc(r["time"])}</div></div>\n'
                    f'            <div class="ml-auto flex text-amber-400 text-sm">★★★★★</div>\n'
                    f'          </div>\n'
                    f'          <p class="text-xs text-slate-600 leading-relaxed">"{esc(r["text"])}"</p>\n'
                    f'        </div>')
        new_track = ('<div class="testi-track" id="testi-track">\n' +
                     "\n".join(build(r) for r in reviews[:6]) + '\n      </div>')
        with open("index.html","r",encoding="utf-8") as f:
            html = f.read()
        si = html.find('<div class="testi-track" id="testi-track">')
        if si != -1:
            pos, depth, ei = si, 0, si
            while pos < len(html):
                if html[pos:pos+4] == "<div": depth += 1
                elif html[pos:pos+6] == "</div>":
                    depth -= 1
                    if depth == 0: ei = pos+6; break
                pos += 1
            with open("index.html","w",encoding="utf-8") as f:
                f.write(html[:si] + new_track + html[ei:])
            print(f"✅ Testimoni diperbarui: {len(reviews[:6])} ulasan")
    except Exception as e:
        print(f"ℹ️  Update testimoni: {e}")

# ── STEP 3: Generate GBP content dari template ────────────────
# Template konten per hari — tanpa AI, selalu berhasil
KONTEN = {
    "Senin": [
        ("Pendaftaran UT 2026",
         "🎓 Awal minggu yang produktif! Masih buka pendaftaran mahasiswa baru UT 2026 di Salut Etam Betuah Samarinda. Non-RPL & RPL tersedia. WA 0822-5063-8289"),
        ("Kuliah Sambil Kerja",
         "📚 Kuliah di UT bisa sambil kerja, dari Balikpapan, Bontang, Berau, atau Kukar — semua bisa. Info lengkap: salutetambetuah.id"),
    ],
    "Selasa": [
        ("Layanan Lengkap UT",
         "✅ Di Salut Etam Betuah, satu tempat untuk semua urusan UT: daftar, registrasi, modul, ujian, wisuda. Samarinda & seluruh Kaltim. WA 0822-5063-8289"),
        ("Konsultasi Gratis",
         "💬 Bingung soal kuliah UT? Konsultasi dulu, gratis, tanpa komitmen. Balas WA ini atau kunjungi salutetambetuah.id 🙏"),
    ],
    "Rabu": [
        ("RPL untuk ASN & Karyawan",
         "💼 Pengalaman kerja bisa jadi SKS! Program RPL UT cocok untuk ASN, PNS, TNI, Polri & karyawan berpengalaman. Info: salutetambetuah.id"),
        ("Tips Kuliah UT",
         "📖 Kuliah di UT itu fleksibel — bisa belajar kapan saja, dari mana saja. Banyak mahasiswa dari Bontang & Berau sudah buktikan. WA 0852-5283-4986"),
    ],
    "Kamis": [
        ("Deadline Registrasi",
         "⏰ Jangan sampai terlewat! Cek deadline registrasi semester ini. Hubungi Salut Etam Betuah Samarinda sekarang: 0822-5063-8289"),
        ("Info Ujian UT",
         "📝 Mau ujian UT? Persiapan bisa dibantu di Salut Etam Betuah. Dari Kukar, Balikpapan, Bontang semua bisa koordinasi via WA 🙏"),
    ],
    "Jumat": [
        ("Cerita Sukses Mahasiswa",
         "🌟 Alhamdulillah, satu lagi mahasiswa UT dari Samarinda berhasil wisuda! Bergabung dan raih gelar S1 Anda bersama Salut Etam Betuah 🎓"),
        ("Akhir Pekan Produktif",
         "🙌 Akhir pekan bukan halangan untuk daftar kuliah UT! Salut Etam Betuah tetap siap dikontak via WA. salutetambetuah.id"),
    ],
    "Sabtu": [
        ("Jam Buka Sabtu",
         "🏢 Sabtu tetap buka! Salut Etam Betuah Samarinda siap membantu urusan UT Anda hari ini. WA: 0822-5063-8289 | 0852-5283-4986"),
        ("Layanan Online",
         "💻 Tidak sempat ke kantor? Semua urusan UT bisa via WhatsApp. Mahasiswa dari Berau & Kukar juga bisa urus online 🙏"),
    ],
    "Minggu": [
        ("Info UT Minggu",
         "📱 WA Salut Etam Betuah aktif setiap hari. Tanya soal kuliah UT, RPL, atau registrasi — langsung chat: 0822-5063-8289"),
        ("Persiapan Pekan Ini",
         "✅ Siapkan dokumen untuk daftar UT: KTP, ijazah, foto 3x4, email aktif. Proses mudah, dibantu sampai NIM aktif! salutetambetuah.id"),
    ],
}

hari_posts = KONTEN.get(DAY_NAME, KONTEN["Minggu"])
# Pilih berdasarkan tanggal agar variatif tiap minggu
idx = TODAY.day % 2
post1_topik, post1_konten = hari_posts[0]
post2_topik, post2_konten = hari_posts[idx]

TEMPLATE_WA = (
    "Halo Kak [Nama] 😊\n\n"
    "Makasih ya sudah mempercayakan urusan kuliah UT ke Salut Etam Betuah!\n\n"
    "Boleh minta tolong kasih ulasan di Google Maps kami? Sangat membantu calon mahasiswa lain 🙏\n\n"
    "Klik di sini: https://g.page/r/CcXrBsm7Ua8xEAE/review\n\n"
    "Ceritakan pengalaman Kakak singkat saja sudah cukup. Terima kasih banyak! 🎓"
)

CONTOH_REVIEWS = [
    "Daftar kuliah UT di Salut Etam Betuah Samarinda, prosesnya gampang banget. Admin responsif, semua dijelasin dengan sabar. Recommended! ⭐⭐⭐⭐⭐",
    "Dari Balikpapan urus administrasi UT via WA ke Salut Etam Betuah, alhamdulillah lancar. Tidak perlu ke Samarinda, semua bisa online 🙏",
    "Sebagai ASN, pilih jalur RPL di Salut Etam Betuah sangat tepat. Pengalaman kerja saya diakui jadi SKS, hemat waktu & biaya kuliah.",
]

md = f"""# Konten GBP — Salut Etam Betuah
### {DAY_NAME}, {TODAY_ID}
*Samarinda · Balikpapan · Kutai Kartanegara · Bontang · Berau · Seluruh Kaltim*

---

## Google Posts Hari Ini

### Post 1 — {post1_topik}
> GBP → Tambahkan pembaruan → salin teks → tombol "Pelajari selengkapnya" → salutetambetuah.id

```
{post1_konten}
```
*{len(post1_konten)} karakter*

---

### Post 2 — {post2_topik}
```
{post2_konten}
```
*{len(post2_konten)} karakter*

---

## Minta Review dari Mahasiswa (Kirim via WA)
*Ganti [Nama] sebelum kirim. Kirim ke 2-3 mahasiswa yang baru selesai urusan.*

```
{TEMPLATE_WA}
```

---

## Contoh Teks Review untuk Mahasiswa

**Mahasiswa Samarinda:**
```
{CONTOH_REVIEWS[0]}
```

**Mahasiswa luar kota (Balikpapan / Bontang / Berau / Kukar):**
```
{CONTOH_REVIEWS[1]}
```

**ASN / Karyawan / RPL:**
```
{CONTOH_REVIEWS[2]}
```

---

## Reply Ulasan ★★★★★ di Google Maps
```
Terima kasih banyak atas ulasan dan kepercayaan Kakak kepada Salut Etam Betuah! 🙏 Semoga sukses kuliahnya dan sampai jumpa di wisuda! 🎓
```

## Reply Ulasan Bintang Rendah
```
Terima kasih atas masukannya. Kami mohon maaf atas ketidaknyamanan ini. Silakan hubungi kami langsung di WA 0822-5063-8289 agar bisa segera kami bantu selesaikan. 🙏
```

---

## Kontak
WA Admin 1: 0822-5063-8289
WA Admin 2: 0852-5283-4986
Website: salutetambetuah.id

---
*Update: {TODAY_ID} | Auto-generated oleh GitHub Actions*
"""

with open("GBP_KONTEN_SALUT.md","w",encoding="utf-8") as f:
    f.write(md)

print("✅ GBP_KONTEN_SALUT.md selesai")
print("🎉 Daily maintenance selesai — exit code 0")
