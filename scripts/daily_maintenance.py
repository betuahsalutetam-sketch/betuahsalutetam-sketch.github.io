#!/usr/bin/env python3
"""Daily Maintenance Script — Salut Etam Betuah"""

import anthropic, requests, datetime, json, os, sys

TODAY    = datetime.date.today()
TODAY_ISO = TODAY.strftime("%Y-%m-%d")
BULAN    = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
            7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
TODAY_ID  = f"{TODAY.day} {BULAN[TODAY.month]} {TODAY.year}"
DAY_NAME  = TODAY.strftime("%A").replace(
    "Monday","Senin").replace("Tuesday","Selasa").replace(
    "Wednesday","Rabu").replace("Thursday","Kamis").replace(
    "Friday","Jumat").replace("Saturday","Sabtu").replace("Sunday","Minggu")

SERVICE_AREA = "Samarinda, Balikpapan, Kutai Kartanegara, Bontang, Berau, dan seluruh Kalimantan Timur, serta seluruh Indonesia"

TEMA = {
    "Senin":  "semangat awal minggu, info pendaftaran, motivasi kuliah sambil kerja",
    "Selasa": "info layanan, cerita dari mahasiswa berbagai kota Kaltim",
    "Rabu":   "tips kuliah UT, info RPL untuk ASN dan karyawan",
    "Kamis":  "info akademik, registrasi, ujian, deadline",
    "Jumat":  "cerita sukses, motivasi akhir pekan",
    "Sabtu":  "reminder jam buka, suasana kantor"
}.get(DAY_NAME, "info layanan UT")

print(f"📅 {DAY_NAME}, {TODAY_ID}")

# ── STEP 1: Fetch 5-star reviews ──────────────────────────────
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
            all_r = data.get("result", {}).get("reviews", [])
            GRADS = ["from-blue-500 to-blue-700","from-amber-500 to-orange-600",
                     "from-emerald-500 to-teal-600","from-purple-500 to-indigo-600",
                     "from-rose-500 to-pink-600","from-cyan-500 to-blue-600"]
            for r in all_r:
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
            print(f"⚠️  Google API status: {data.get('status')} — skip review sync")
    except Exception as e:
        print(f"⚠️  Google API error: {e} — skip review sync")
else:
    print("ℹ️  Google secrets tidak diset — skip review sync")

# ── STEP 2: Update testimoni di index.html ────────────────────
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
                     "\n".join(build(r) for r in reviews[:6]) +
                     '\n      </div>')

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
            html = html[:si] + new_track + html[ei:]
            with open("index.html","w",encoding="utf-8") as f:
                f.write(html)
            print(f"✅ Testimoni diperbarui: {len(reviews[:6])} ulasan")
        else:
            print("⚠️  testi-track tidak ditemukan di index.html")
    except Exception as e:
        print(f"⚠️  Update testimoni error: {e} — lanjut")

# ── STEP 3: Generate GBP content dengan AI ───────────────────
anthropic_key = os.environ.get("ANTHROPIC_API_KEY","")
if not anthropic_key:
    print("⚠️  ANTHROPIC_API_KEY tidak diset — skip GBP generation")
    sys.exit(0)

client = anthropic.Anthropic(api_key=anthropic_key)

def call_ai(prompt, max_tokens=1200, fallback=None):
    """Call AI dengan error handling penuh — tidak pernah crash."""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            messages=[{"role":"user","content":prompt}]
        )
        raw = resp.content[0].text.strip()
        # Bersihkan markdown code block jika ada
        if "```" in raw:
            parts = raw.split("```")
            for p in parts:
                p = p.strip()
                if p.startswith("json"): p = p[4:].strip()
                try:
                    return json.loads(p)
                except:
                    continue
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse error: {e} — pakai fallback")
        return fallback or {}
    except Exception as e:
        print(f"⚠️  AI call error: {e} — pakai fallback")
        return fallback or {}

# Fallback konten jika AI gagal
FALLBACK_POSTS = {
    "post_1": {"topik": "Pendaftaran UT 2026", "konten": f"🎓 Daftar kuliah UT sekarang di Salut Etam Betuah Samarinda. Proses mudah, bisa dari Balikpapan, Bontang, Berau, atau seluruh Kaltim. WA 0822-5063-8289"},
    "post_2": {"topik": "RPL UT Kaltim", "konten": f"💼 Pengalaman kerja bisa jadi SKS kuliah via program RPL UT. Cocok untuk ASN, karyawan, TNI/Polri. Info: salutetambetuah.id"}
}
FALLBACK_REVIEW = {
    "template_wa": "Halo Kak [Nama], boleh minta ulasan di Google Maps? Link: https://g.page/r/CcXrBsm7Ua8xEAE/review 🙏",
    "contoh_1": "Udah daftar kuliah UT lewat Salut Etam Betuah Samarinda, gampang banget prosesnya. Recommended!",
    "contoh_2": "Dari Balikpapan tapi urus semua via WA ke Salut Etam Betuah, alhamdulillah lancar.",
    "contoh_3": "ASN kayak saya cocok banget pakai jalur RPL di Salut Etam Betuah, hemat waktu.",
    "reply_bintang5": "Terima kasih banyak atas ulasan dan kepercayaan Kakak kepada Salut Etam Betuah. Semoga sukses kuliahnya! 🎓",
    "reply_rendah": "Terima kasih atas masukannya. Kami akan terus memperbaiki layanan. Silakan hubungi kami langsung agar kami bisa bantu selesaikan. 🙏"
}

print("🤖 Generating GBP content...")
posts = call_ai(
    f"Buat 2 caption Google Business Profile untuk Salut Etam Betuah "
    f"yang melayani {SERVICE_AREA}.\n\n"
    f"ATURAN KETAT: Jangan sebut 'tim kami'/'admin kami'/'kami siap'. "
    f"Jangan gaya korporat. Tulis seperti orang Samarinda share info ke teman. "
    f"Sesekali sebut kota lain (Balikpapan, Bontang dll). Max 220 karakter per post. "
    f"1-2 emoji saja.\n\nHari ini: {DAY_NAME}, {TODAY_ID}. Tema: {TEMA}\n\n"
    f'Return JSON ONLY (no markdown): {{"post_1":{{"konten":"...","topik":"..."}},"post_2":{{"konten":"...","topik":"..."}}}}',
    fallback=FALLBACK_POSTS
)
print("✅ Google Posts generated")

review_tmpl = call_ai(
    f"Buat template untuk Salut Etam Betuah yang melayani {SERVICE_AREA}.\n\n"
    f"ATURAN REPLY BINTANG 5: Formal dan profesional. Boleh mulai "
    f"'Terima kasih banyak...' atau 'Alhamdulillah...'. Hangat tapi sopan. Max 180 karakter.\n\n"
    f"ATURAN CONTOH REVIEW: Dari sudut pandang MAHASISWA sungguhan. Informal, "
    f"ada pengalaman nyata. Sebut 'Salut Etam Betuah' dan kota secara natural.\n\n"
    f"ATURAN TEMPLATE MINTA REVIEW: Pesan WA singkat personal. "
    f"Sertakan link: https://g.page/r/CcXrBsm7Ua8xEAE/review\n\n"
    f'Return JSON ONLY (no markdown): {{"template_wa":"...","contoh_1":"...","contoh_2":"...","contoh_3":"...","reply_bintang5":"...","reply_rendah":"..."}}',
    fallback=FALLBACK_REVIEW
)
print("✅ Review templates generated")

def s(v, d=""): return str(v) if v else d

md = f"""# Konten GBP — Salut Etam Betuah
### {DAY_NAME}, {TODAY_ID}
*Melayani: {SERVICE_AREA}*

---

## Google Posts Hari Ini

### Post 1 — {s(posts.get("post_1",{}).get("topik",""))}
> GBP → Tambahkan pembaruan → salin teks → tombol "Pelajari selengkapnya" → salutetambetuah.id

```
{s(posts.get("post_1",{}).get("konten",""))}
```
*{len(s(posts.get("post_1",{}).get("konten","")))} karakter*

---

### Post 2 — {s(posts.get("post_2",{}).get("topik",""))}
```
{s(posts.get("post_2",{}).get("konten",""))}
```
*{len(s(posts.get("post_2",{}).get("konten","")))} karakter*

---

## Minta Review dari Mahasiswa

### Pesan WhatsApp
*Ganti [Nama] sebelum kirim.*

```
{s(review_tmpl.get("template_wa",""))}
```

### Contoh Teks Review

**Mahasiswa Samarinda:**
```
{s(review_tmpl.get("contoh_1",""))}
```

**Mahasiswa luar kota (Balikpapan / Bontang / Berau / Kukar):**
```
{s(review_tmpl.get("contoh_2",""))}
```

**ASN / Karyawan / RPL:**
```
{s(review_tmpl.get("contoh_3",""))}
```

---

## Reply Ulasan di Google Maps

**Untuk ulasan ★★★★★:**
```
{s(review_tmpl.get("reply_bintang5",""))}
```

**Untuk ulasan bintang rendah / keluhan:**
```
{s(review_tmpl.get("reply_rendah",""))}
```

---

## Area Layanan
**Samarinda · Balikpapan · Kutai Kartanegara · Bontang · Berau**
dan seluruh Kalimantan Timur, serta **seluruh Indonesia**

Konsultasi: WA 0822-5063-8289 | 0852-5283-4986 | salutetambetuah.id

---
*Update: {TODAY_ID} | Auto-generated by GitHub Actions + Anthropic AI*
"""

with open("GBP_KONTEN_SALUT.md","w",encoding="utf-8") as f:
    f.write(md)
print("✅ GBP_KONTEN_SALUT.md selesai")
print("🎉 Daily maintenance selesai!")
