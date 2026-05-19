#!/usr/bin/env python3
"""Daily Maintenance — Salut Etam Betuah"""
import sys, os, json, datetime, requests

TODAY   = datetime.date.today()
BULAN   = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
           7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
TODAY_ID = f"{TODAY.day} {BULAN[TODAY.month]} {TODAY.year}"
DAY_NAME = TODAY.strftime("%A").replace("Monday","Senin").replace("Tuesday","Selasa")\
    .replace("Wednesday","Rabu").replace("Thursday","Kamis").replace("Friday","Jumat")\
    .replace("Saturday","Sabtu").replace("Sunday","Minggu")

AREA = "Samarinda, Balikpapan, Kutai Kartanegara, Bontang, Berau, dan seluruh Kalimantan Timur"
TEMA = {"Senin":"pendaftaran mahasiswa baru UT","Selasa":"layanan UT dan info Kaltim",
        "Rabu":"RPL untuk ASN dan karyawan","Kamis":"info akademik dan registrasi",
        "Jumat":"cerita sukses mahasiswa","Sabtu":"jam layanan dan konsultasi"
        }.get(DAY_NAME,"info layanan UT")

print(f"Mulai: {DAY_NAME}, {TODAY_ID}")

# STEP 1 — Google Reviews
reviews = []
gkey = os.environ.get("GOOGLE_PLACES_API_KEY","")
gid  = os.environ.get("GOOGLE_PLACE_ID","")
if gkey and gid:
    try:
        r = requests.get("https://maps.googleapis.com/maps/api/place/details/json",
            params={"place_id":gid,"fields":"reviews","language":"id",
                    "reviews_sort":"newest","key":gkey}, timeout=10)
        d = r.json()
        if d.get("status") == "OK":
            GRADS = ["from-blue-500 to-blue-700","from-amber-500 to-orange-600",
                     "from-emerald-500 to-teal-600","from-purple-500 to-indigo-600",
                     "from-rose-500 to-pink-600","from-cyan-500 to-blue-600"]
            for rv in d.get("result",{}).get("reviews",[]):
                if rv.get("rating") != 5: continue
                txt = rv.get("text","").strip()
                if len(txt) < 20: continue
                auth = rv.get("author_name","Anonim")
                pts  = auth.strip().split()
                ini  = (pts[0][0]+(pts[1][0] if len(pts)>1 else pts[0][-1])).upper()
                reviews.append({"author":auth,"initials":ini,
                    "text":txt[:280]+("..." if len(txt)>280 else ""),
                    "time":rv.get("relative_time_description",""),
                    "gradient":GRADS[len(reviews)%len(GRADS)]})
            print(f"Google: {len(reviews)} ulasan bintang 5")
        else:
            print(f"Google API: {d.get('status')}")
    except Exception as ex:
        print(f"Google API skip: {ex}")

# STEP 2 — Update testimoni HTML
if reviews and os.path.exists("index.html"):
    try:
        def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        def card(rv):
            return (f'        <div class="testi-item shadow-card">\n'
                    f'          <div class="flex items-center gap-3 mb-4">\n'
                    f'            <div class="w-10 h-10 rounded-full bg-gradient-to-br {rv["gradient"]} '
                    f'flex items-center justify-center text-sm font-bold text-white flex-shrink-0">'
                    f'{esc(rv["initials"])}</div>\n'
                    f'            <div><div class="text-sm font-bold text-brand-navy">{esc(rv["author"])}</div>'
                    f'<div class="text-[10px] text-slate-400">Google Maps · {esc(rv["time"])}</div></div>\n'
                    f'            <div class="ml-auto flex text-amber-400 text-sm">★★★★★</div>\n'
                    f'          </div>\n'
                    f'          <p class="text-xs text-slate-600 leading-relaxed">"{esc(rv["text"])}"</p>\n'
                    f'        </div>')
        track = '<div class="testi-track" id="testi-track">\n' + \
                "\n".join(card(rv) for rv in reviews[:6]) + '\n      </div>'
        html = open("index.html","r",encoding="utf-8").read()
        si = html.find('<div class="testi-track" id="testi-track">')
        if si != -1:
            pos, depth, ei = si, 0, si
            while pos < len(html):
                if html[pos:pos+4] == "<div": depth += 1
                elif html[pos:pos+6] == "</div>":
                    depth -= 1
                    if depth == 0: ei = pos+6; break
                pos += 1
            open("index.html","w",encoding="utf-8").write(html[:si]+track+html[ei:])
            print(f"Testimoni: {len(reviews[:6])} ulasan diupdate")
    except Exception as ex:
        print(f"Testimoni skip: {ex}")

# STEP 3 — AI GBP Content
akey = os.environ.get("ANTHROPIC_API_KEY","")
if not akey:
    print("ANTHROPIC_API_KEY tidak ada — selesai")
    sys.exit(0)

try:
    import anthropic
    client = anthropic.Anthropic(api_key=akey)

    def ai(prompt, fallback):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001", max_tokens=1000,
                messages=[{"role":"user","content":prompt}])
            raw = resp.content[0].text.strip()
            if "```" in raw:
                for p in raw.split("```"):
                    p = p.strip().lstrip("json").strip()
                    try: return json.loads(p)
                    except: pass
            return json.loads(raw)
        except Exception as ex:
            print(f"AI skip: {ex}")
            return fallback

    posts = ai(
        f"Buat 2 caption GBP untuk Salut Etam Betuah ({AREA}).\n"
        f"ATURAN: Jangan 'tim kami'/'kami siap'. Gaya orang Samarinda share info. "
        f"Max 220 karakter. 1-2 emoji. Hari: {DAY_NAME}. Tema: {TEMA}.\n"
        f'JSON ONLY: {{"post_1":{{"topik":"...","konten":"..."}},"post_2":{{"topik":"...","konten":"..."}}}}',
        {"post_1":{"topik":"Pendaftaran UT","konten":f"🎓 Daftar kuliah UT di Salut Etam Betuah Samarinda. Proses mudah, bisa dari seluruh Kaltim. WA 0822-5063-8289"},
         "post_2":{"topik":"RPL UT","konten":f"💼 Pengalaman kerja bisa jadi SKS via RPL UT. Cocok ASN, karyawan, TNI/Polri. salutetambetuah.id"}}
    )

    tmpl = ai(
        f"Template untuk Salut Etam Betuah ({AREA}).\n"
        f"reply_bintang5: formal+profesional, max 180 karakter.\n"
        f"contoh review: dari sudut pandang mahasiswa, informal, sebut kota.\n"
        f"template_wa: pesan WA singkat + link https://g.page/r/CcXrBsm7Ua8xEAE/review\n"
        f'JSON ONLY: {{"template_wa":"...","contoh_1":"...","contoh_2":"...","contoh_3":"...","reply_bintang5":"...","reply_rendah":"..."}}',
        {"template_wa":"Halo Kak [Nama], boleh minta ulasan di Google Maps? https://g.page/r/CcXrBsm7Ua8xEAE/review 🙏",
         "contoh_1":"Daftar UT di Salut Etam Betuah Samarinda gampang banget. Recommended!",
         "contoh_2":"Dari Balikpapan urus via WA ke Salut Etam Betuah, alhamdulillah lancar.",
         "contoh_3":"ASN pakai RPL di Salut Etam Betuah, hemat waktu dan biaya kuliah.",
         "reply_bintang5":"Terima kasih banyak atas kepercayaan Kakak kepada Salut Etam Betuah! Semoga sukses kuliahnya 🎓",
         "reply_rendah":"Terima kasih masukannya. Hubungi WA 0822-5063-8289 agar segera kami bantu 🙏"}
    )

    def g(obj, *keys):
        for k in keys: obj = (obj or {}).get(k, "")
        return str(obj)

    md = f"""# Konten GBP — Salut Etam Betuah
### {DAY_NAME}, {TODAY_ID}

---

## Google Posts Hari Ini

### Post 1 — {g(posts,"post_1","topik")}
```
{g(posts,"post_1","konten")}
```

### Post 2 — {g(posts,"post_2","topik")}
```
{g(posts,"post_2","konten")}
```

---

## Template Minta Review (WA)
```
{g(tmpl,"template_wa")}
```

## Contoh Review Mahasiswa
**Samarinda:** {g(tmpl,"contoh_1")}
**Luar kota:** {g(tmpl,"contoh_2")}
**ASN/RPL:** {g(tmpl,"contoh_3")}

---

## Reply Google Maps
**★★★★★:** {g(tmpl,"reply_bintang5")}
**Keluhan:** {g(tmpl,"reply_rendah")}

---
*{TODAY_ID} | Auto-generated | salutetambetuah.id | WA: 0822-5063-8289 / 0852-5283-4986*
"""
    open("GBP_KONTEN_SALUT.md","w",encoding="utf-8").write(md)
    print("GBP_KONTEN_SALUT.md selesai")

except ImportError:
    print("anthropic library tidak ada — skip AI")

print("Selesai!")
