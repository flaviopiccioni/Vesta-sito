#!/usr/bin/env python3
"""Controllo completo di vestadomus.it prima di pubblicare.
Uso, dalla radice del repository:   python3 tools/verifica.py [cartella-sito]
Cartella predefinita: la radice del repository (il sito è lì). Esce con codice 1 se trova errori.
Regole: vedi CLAUDE.md, sezione "Regole tecniche"."""
import re, json, glob, html, os, sys
from collections import defaultdict

SITE = sys.argv[1] if len(sys.argv) > 1 else '.'
if not os.path.isdir(SITE): sys.exit(f'Cartella "{SITE}" non trovata: lancia lo script dalla radice del repository.')
os.chdir(SITE)
BASE = 'https://vestadomus.it'
HUBS = {'lombardia','lombardy','valle-d-aosta','aosta-valley','sardegna','sardinia','sicilia','sicily'}
LEGAL = {'privacy','cookie-policy'}
pages = sorted(glob.glob('*/*/index.html')) + [p for p in ('it/index.html','en/index.html') if os.path.exists(p)]
existing = {'/' + p.rsplit('index.html',1)[0] for p in pages}
sitemap = open('sitemap.xml', encoding='utf-8').read() if os.path.exists('sitemap.xml') else ''
errs = defaultdict(list); warns = defaultdict(list)

def bal(t): return len(re.findall(r'<div\b', t)) - len(re.findall(r'</div>', t))
def clean(x): return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', x))).strip()

for p in pages:
    s = open(p, encoding='utf-8').read()
    lang = p.split('/')[0]; slug = p.split('/')[1] if p.count('/') == 2 else ''
    key = f'{lang}/{slug or "(home)"}'; E = errs[key]; W = warns[key]
    url = f'{BASE}/{lang}/' + (f'{slug}/' if slug else '')
    # URL e lingua
    can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not can or can.group(1) != url: E.append(f'canonical: {can.group(1) if can else "assente"}')
    og = re.search(r'<meta property="og:url" content="([^"]+)"', s)
    if not og or og.group(1) != url: E.append('og:url diverso dal canonical')
    hl = dict(re.findall(r'hreflang="([^"]+)"[^>]*href="([^"]+)"', s))
    if len(hl) != 3: E.append(f'hreflang: {len(hl)} invece di 3')
    other = hl.get('en-US' if lang == 'it' else 'it-IT', '').replace(BASE, '')
    lg = re.search(r'<a class="lang" href="([^"]*)"', s)
    if other and (not lg or lg.group(1) != other): E.append('selettore lingua non coerente con hreflang')
    if url not in sitemap: E.append('non presente in sitemap')
    # meta
    t = clean(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    d = re.search(r'<meta name="description" content="([^"]*)"', s); d = html.unescape(d.group(1)) if d else ''
    if len(t) > 60: E.append(f'title {len(t)} caratteri (max 60)')
    if not 115 <= len(d) <= 165: W.append(f'description {len(d)} caratteri (consigliato 120-160)')
    if slug not in LEGAL and len(re.findall(r'<h1[\s>]', s)) != 1: E.append('H1 non unico')
    if 'Vesta Domus' in s: E.append('"Vesta Domus" presente')
    if re.search(r'deduzion', s, re.I): E.append('parola "deduzione" (usare "rimborso di parte delle spese")')
    # JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if len(blocks) != 1: E.append(f'{len(blocks)} blocchi JSON-LD (deve essere 1)')
    else:
        try:
            g = json.loads(blocks[0])['@graph']; ids = {n.get('@id') for n in g}
            miss = set(re.findall(r'\{"@id":\s*"([^"]+)"\}', blocks[0])) - ids
            if miss: E.append(f'@id non risolti: {sorted(miss)}')
            wp = [n for n in g if n.get('@type') == 'WebPage']
            if wp and (wp[0].get('name') != t or wp[0].get('description') != d): E.append('WebPage nello schema diverso da title/description')
            fq = [n for n in g if n.get('@type') == 'FAQPage']
            vis = [clean(a) for q, a in re.findall(r'<div class="faq-item"><h3>(.*?)</h3><p>(.*?)</p></div>', s, re.S)]
            if fq and [x['acceptedAnswer']['text'] for x in fq[0]['mainEntity']] != vis: E.append('FAQ dello schema diverse da quelle visibili')
        except Exception as ex: E.append(f'JSON-LD non valido: {ex}')
    # struttura
    if bal(s[s.find('<body'):]) != 0: E.append('div non bilanciate nella pagina')
    b0, b1 = s.find('</header>'), s.find('<footer')
    for m in re.finditer(r'<section\b', s[b0:b1]):
        st = b0 + m.start(); en = s.find('</section>', st) + 10; sec = s[st:en]
        h = re.search(r'<h2[^>]*>(.*?)</h2>', sec, re.S); name = clean(h.group(1))[:40] if h else '?'
        if bal(sec) != 0: E.append(f'div sbilanciate nella sezione "{name}"')
        if sec[8:].count('<section'): E.append(f'sezione annidata in "{name}"')
        if 'wrap split' in sec and re.search(r'class="(dcard|feat[^"]*|apts|svc-grid)"', sec): E.append(f'griglia dentro sezione con foto: "{name}"')
    # link, foto, form
    for h in set(re.findall(r'href="(/(?:it|en)/[a-z-]*/?)"', s)):
        if h not in existing: E.append(f'link interno rotto: {h}')
    for a in re.findall(r'href="#([a-z]+)"', s):
        if f'id="{a}"' not in s: W.append(f'ancora #{a} senza destinazione')
    ids_img = re.findall(r'images\.unsplash\.com/(photo-[a-z0-9-]+)', s)
    dup = sorted({i for i in ids_img if ids_img.count(i) > 1})
    if dup: E.append(f'foto ripetuta nella pagina: {dup}')
    for tag in re.findall(r'<img\b[^>]*>', s[s.find('<body'):]):
        if 'alt=""' in tag or 'alt=' not in tag: W.append('immagine senza alt'); break
    if 'formspree.io' in s:
        subj = re.findall(r'name="_subject" value="([^"]*)"', s)
        page = re.findall(r'name="(?:pagina|page)" value="([^"]*)"', s)
        if len(subj) != 1: E.append('oggetto del form (_subject) assente o doppio')
        if page != [url]: E.append(f'campo pagina del form: {page}')
    if slug and slug not in LEGAL and 'class="updated"' not in s: W.append('manca la riga "Aggiornato a"')
    if slug and slug not in LEGAL | HUBS and 'class="bcn"' not in s and slug != 'cortina': W.append('manca il breadcrumb visibile')

# duplicazione (shingle di 8 parole, solo pagine IT località/hub)
def txt(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<(script|style|nav|footer|header)\b.*?</\1>', '', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))
def sh(t, k=8):
    w = re.findall(r'\w+', t.lower()); return {' '.join(w[i:i+k]) for i in range(max(0, len(w)-k))}
loc = {p: sh(txt(p)) for p in glob.glob('it/*/index.html') if p.split('/')[1] not in LEGAL}

n_err = sum(len(v) for v in errs.values()); n_warn = sum(len(v) for v in warns.values())
print(f'\nControllate {len(pages)} pagine — errori: {n_err}, avvisi: {n_warn}\n')
for k in sorted(set(errs) | set(warns)):
    if errs[k] or warns[k]:
        print(f'■ {k}')
        for x in errs[k]: print(f'    ERRORE  {x}')
        for x in warns[k]: print(f'    avviso  {x}')
print('\nDuplicazione pagine IT (obiettivo < 30%):')
vals = []
for a in sorted(loc):
    if not loc[a]: continue
    v, b = max((len(loc[a] & sb) / len(loc[a]), bb) for bb, sb in loc.items() if bb != a)
    vals.append(v); print(f'  {a.split("/")[1]:16} {v:4.0%}  con {b.split("/")[1]}{"  ← sopra il 30%" if v > .30 else ""}')
if vals: print(f'  media: {sum(vals)/len(vals):.0%}')
sys.exit(1 if n_err else 0)
