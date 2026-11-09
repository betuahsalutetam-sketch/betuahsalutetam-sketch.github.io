#!/usr/bin/env python3
"""Perbarui lastmod sitemap, dateModified JSON-LD, dan tanggal terlihat memakai tanggal perubahan isi
yang sebenarnya (riwayat git), bukan tanggal hari ini. Commit otomatis (chore: daily/weekly) diabaikan.
Berkas dengan perubahan yang belum di-commit dihitung berubah hari ini."""
import re, subprocess, datetime, os, sys
BOT = r'^chore: (daily|weekly)'
BULAN = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember']
def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()
dirty = {l[3:].strip().strip('"') for l in sh('git', 'status', '--porcelain').splitlines()}
def last_change(path):
    if path in dirty: return datetime.date.today().isoformat()
    d = sh('git', 'log', '-1', '--format=%cs', '--invert-grep', f'--grep={BOT}', '--', path)
    return d or datetime.date.today().isoformat()
def tgl(iso):
    y, m, d = map(int, iso.split('-')); return f'{d} {BULAN[m-1]} {y}'
def url_to_file(loc):
    p = loc.replace('https://salutetambetuah.id', '').lstrip('/')
    if p == '': return 'index.html'
    if p.endswith('/'): return p + 'index.html'
    return p
changed = 0
sm = open('sitemap.xml', encoding='utf-8').read()
def fix_url(m):
    blk = m.group(0); loc = re.search(r'<loc>([^<]+)</loc>', blk).group(1)
    f = url_to_file(loc)
    if not os.path.exists(f): return blk
    return re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{last_change(f)}</lastmod>', blk)
new = re.sub(r'<url>.*?</url>', fix_url, sm, flags=re.S)
if new != sm: open('sitemap.xml', 'w', encoding='utf-8').write(new); changed += 1
for f in sorted(os.popen("git ls-files '*.html'").read().split()):
    if f.startswith('google') or 'section' in f: continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    d = last_change(f); o = t
    t = re.sub(r'("dateModified"\s*:\s*")[0-9-]+(")', lambda m: m.group(1) + d + m.group(2), t)
    t = re.sub(r'(<time[^>]*data-lastmod[^>]*datetime=")[0-9-]+(")([^>]*>)[^<]*(</time>)',
               lambda m: f'{m.group(1)}{d}{m.group(2)}{m.group(3)}Terakhir diperbarui: {tgl(d)}{m.group(4)}', t)
    if t != o: open(f, 'w', encoding='utf-8').write(t); changed += 1
print('berkas diperbarui:', changed)
