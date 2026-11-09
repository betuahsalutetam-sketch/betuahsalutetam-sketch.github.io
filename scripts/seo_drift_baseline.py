#!/usr/bin/env python3
"""Buat snapshot baseline SEO (title, description, canonical, robots, H1, schema, jumlah kata, hash isi).
Pemakaian: python3 scripts/seo_drift_baseline.py [YYYY-MM-DD]"""
import glob, hashlib, json, re, sys, datetime
tgl = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
def types(node, out):
    if isinstance(node, dict):
        t = node.get('@type')
        for x in (t if isinstance(t, list) else [t] if t else []): out.add(x)
        for v in node.values(): types(v, out)
    elif isinstance(node, list):
        for v in node: types(v, out)
data = {}
for f in sorted(glob.glob('**/*.html', recursive=True)):
    if f.startswith('google'): continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    g = lambda p: (re.search(p, t, re.S | re.I) or [None, ''])[1].strip()
    title = g(r'<title>(.*?)</title>')
    desc = g(r'<meta name="description" content="(.*?)"')
    st = set()
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: types(json.loads(j), st)
        except Exception: pass
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', t, flags=re.S)
    text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)).strip()
    data[f] = {'title': title, 'title_len': len(title), 'description': desc, 'desc_len': len(desc),
        'canonical': g(r'rel="canonical" href="(.*?)"'), 'robots': g(r'<meta name="robots" content="(.*?)"'),
        'h1_count': len(re.findall(r'<h1[ >]', t)), 'schema_types': sorted(st),
        'approx_word_count': len(text.split()), 'content_hash': hashlib.md5(text.encode()).hexdigest()[:12]}
out = f'.seo-drift/baseline-{tgl}.json'
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(out, len(data))
