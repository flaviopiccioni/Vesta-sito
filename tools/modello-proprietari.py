#!/usr/bin/env python3
"""Porta una pagina località alla struttura "pagina proprietari" nata su Milano (novembre 2026).

Uso (dalla radice del repo):
    python3 tools/modello-proprietari.py it/cervinia/index.html docs/modelli/cervinia-it.json
    python3 tools/modello-proprietari.py it/cervinia/index.html docs/modelli/cervinia-it.json --prova

Con --prova scrive il risultato in _anteprima/MODELLO-<slug>-<lingua>.html e non tocca la pagina.
Senza --prova sovrascrive la pagina e aggiorna il lastmod in sitemap.xml. Poi lanciare sempre
python3 tools/verifica.py e guardare la pagina prima di pubblicare.

Cosa fa:
  - hero: lead, riga 80 immobili / 6.100 ospiti, tre punti, pulsanti valutazione + WhatsApp;
  - sezioni nuove: servizi, costi (barre a confronto), portale proprietario,
    casa gestita (solo se il file di testi la prevede), poi "Come si comincia" esistente;
  - tutte le altre sezioni esistenti diventano FAQ compatte (testo e fonti restano uguali);
  - schema FAQ rigenerato dal testo visibile, dateModified e "Aggiornato a" aggiornati;
  - stile da /css/proprietari.css.
I testi nuovi vanno scritti per ogni località nel file JSON (vedi docs/modelli/milano-it.json):
non copiarli da un'altra pagina. Richiede beautifulsoup4 (pip install beautifulsoup4).
"""
import json, re, sys, html as H, datetime
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

class Fmt(HTMLFormatter):
    """Lascia gli attributi nell'ordine originale e i tag vuoti senza barra, come nel resto del sito."""
    def attributes(self, tag):
        return list(tag.attrs.items())
FMT = Fmt(void_element_close_prefix=None)

if len(sys.argv) < 3:
    sys.exit(__doc__)
PAGE, TEXTS = Path(sys.argv[1]), Path(sys.argv[2])
PROVA = '--prova' in sys.argv
ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads(TEXTS.read_text(encoding='utf-8'))
L = cfg.get('lingua', 'it')

FIX = {
    'it': dict(
        stats='Oltre 80 immobili gestiti in Italia · 6.100 ospiti accolti da gennaio a ottobre 2026',
        cta='Richiedi una valutazione gratuita', wa='Scrivici su WhatsApp', anchor='#valutazione',
        services='<p class="svc-more" style="margin:22px 0 0">Cosa è incluso, cosa è su richiesta e cosa resta a te lo trovi, voce per voce, nella pagina dei <a href="/it/servizi/">servizi di gestione affitti brevi</a>.</p>',
        us='Con Vesta', us_sub='Commissione e cedolare calcolate sul netto', lo='Calcolo sul lordo',
        lo_sub='Commissione più bassa, ma cedolare su tutto il prezzo', keep='Ti resta',
        leg=['Portale', 'Pulizie', 'Commissione di gestione', 'Cedolare secca 21%', 'Ti resta'],
        seg=['Portale', 'Pulizie', 'Commissione', 'Cedolare', 'Ti resta'],
        group='Confronto su una prenotazione da 600 euro',
        gain='<b>+36,44 €</b> a te su ogni prenotazione da 600 €, con la stessa casa e lo stesso prezzo.',
        why='La nostra commissione in euro è più alta, ma la cedolare la paghi su una base molto più bassa: è lì che si recuperano i soldi. <small style="display:block;margin-top:6px;font-size:12.5px;color:#5f7d78">Esempio indicativo su una prenotazione da 600 € con pulizie da 67,90 €: la stima per la tua casa la ricevi con la valutazione gratuita.</small>',
        more='Scopri quanto può rendere la tua casa',
        cal_alt='Il calendario del portale proprietario Vesta con le prenotazioni in verde, le date tenute dal proprietario in arancio e il riquadro per bloccare le date',
        cal_cap='Come appare il calendario nel portale proprietario, con dati di esempio: in verde le prenotazioni, in arancio i giorni che tieni per te.',
        faq_kick='Domande frequenti', months=['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'],
        updated='Aggiornato a {m} {y}'),
    'en': dict(
        stats='Over 80 properties managed in Italy · 6,100 guests hosted from January to October 2026',
        cta='Request a free assessment', wa='Message us on WhatsApp', anchor='#assessment',
        services='<p class="svc-more" style="margin:22px 0 0">What is included, what is on request and what stays with you is listed item by item on the <a href="/en/services/">short-term rental management services</a> page.</p>',
        us='With Vesta', us_sub='Fee and tax calculated on the net amount', lo='Calculated on the gross',
        lo_sub='Lower fee, but tax on the full price', keep='You keep',
        leg=['Platform', 'Cleaning', 'Management fee', 'Cedolare secca 21%', 'You keep'],
        seg=['platform', 'cleaning', 'fee', 'cedolare secca', 'you keep'],
        group='Comparison on a 600 euro booking',
        gain='<b>+€36.44</b> for you on every €600 booking, with the same home and the same price.',
        why='Our fee in euros is higher, but you pay the cedolare secca on a much lower base: that is where the money comes back. <small style="display:block;margin-top:6px;font-size:12.5px;color:#5f7d78">Indicative example on a €600 booking with €67.90 cleaning: you get the estimate for your home with the free assessment.</small>',
        more='Find out what your home could earn',
        cal_alt='The Vesta owner portal calendar with bookings in green, dates kept by the owner in orange and the panel for blocking dates',
        cal_cap='How the calendar looks in the owner portal, with sample data: bookings in green, the days you keep for yourself in orange.',
        faq_kick='FAQ', months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        updated='Updated {m} {y}'),
}[L]

def eur(v):
    if L == 'it':
        return f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' €'
    return f'€{v:,.2f}'

def slug(t):
    t = t.lower()
    for a, b in (('à', 'a'), ('è', 'e'), ('é', 'e'), ('ì', 'i'), ('ò', 'o'), ('ù', 'u'), ("'", '-')):
        t = t.replace(a, b)
    return 'd-' + re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60]

def frag(markup):
    return BeautifulSoup(markup, 'html.parser')

esc = lambda t: H.escape(t, quote=False)
src = PAGE.read_text(encoding='utf-8')
soup = BeautifulSoup(src, 'html.parser')
body = soup.body

# ---------- stile ----------
for st in soup.head.find_all('style'):
    if st.get('id', '').startswith('v'):
        st.decompose()
if not soup.head.find('link', href='/css/proprietari.css'):
    first = soup.head.find('style')
    tag = frag('<link rel="stylesheet" href="/css/proprietari.css">').link
    (first.insert_after(tag) if first else soup.head.append(tag))

# ---------- hero ----------
hero = body.select_one('header.hero'); hi = hero.select_one('.hero-inner')
for sel in ('.hero-stats', '.hero-proof', '.hero-pts'):
    for n in hi.select(sel): n.decompose()
hi.select_one('.lead').string = cfg['hero']['lead']
hi.select_one('.updated').insert_after(frag(f'<p class="hero-stats">{esc(FIX["stats"])}</p>'))
pts = ''.join(f'<p><b>{esc(a)}</b>{esc(b)}</p>' for a, b in cfg['hero']['punti'])
if pts: hi.select_one('.lead').insert_after(frag(f'<div class="hero-proof">\n{pts}</div>'))
hact = hi.select_one('.hact')
hact.clear()
hact.append(frag(f'<a class="btn btn--solid" href="{FIX["anchor"]}">{esc(FIX["cta"])}</a><a class="btn" href="https://wa.me/393517407898" rel="noopener" target="_blank">{esc(FIX["wa"])}</a>'))

# ---------- sezioni esistenti ----------
secs = body.find_all('section', recursive=False)
h2t = lambda s: (s.find('h2').get_text(' ', strip=True) if s.find('h2') else '')
h2t = lambda s: (s.find('h2').get_text(' ', strip=True) if s.find('h2') else '')
def has(s, needle): return needle.lower() in h2t(s).lower()
sost = [x.lower() for x in cfg.get('sostituite', [])]
haid = lambda s, i: s.get('id') == i or s.find(id=i) is not None
come_t = cfg.get('come', {}).get('titolo', '').lower()
come = next((s for s in secs if haid(s, 'processo') or (come_t and come_t in h2t(s).lower())), None)
cta = next((s for s in secs if 'cta' in (s.get('class') or [])), None)
loc = next((s for s in secs if 'localita-box' in (s.get('class') or [])), None)
faq_src = []
for s in secs:
    cl = s.get('class') or []
    if s in (come, cta, loc) or 'svc-section' in cl or 'v3' in cl:
        continue
    if haid(s, 'faq') or any(x in h2t(s).lower() for x in sost):
        continue
    faq_src.append(s)
ordine = cfg.get('faq', {}).get('ordine')
if ordine:
    faq_src = [next(s for s in faq_src if has(s, o)) for o in ordine]

def qa_from(s):
    h2 = s.find('h2'); body_div = soup.new_tag('div', attrs={'class': 'body'})
    take = s.select('.prose > *, .split > div:not(.ph) > p:not(.kick), .feat, .gtable-wrap, .bullets, ul')
    take += [t for t in s.select('table') if not t.find_parent(class_='gtable-wrap')]
    seen = []
    for n in take:
        if any(n is x or x in n.parents for x in seen): continue
        if n.find_parent(class_='feat') and 'feat' not in (n.get('class') or []): continue
        seen.append(n)
    for n in seen: body_div.append(n.extract())
    btn = s.select_one('a.btn')
    if btn and not btn.find_parent(class_='body'): body_div.append(btn.extract())
    d = soup.new_tag('details', attrs={'class': 'qa'})
    ids = [x.get('id') for x in s.find_all(id=True) if x is not h2]
    for i in ('mercato', 'zone', 'valutazione', 'assessment'):
        if i in ids: d['id'] = i
    if h2.has_attr('style'): del h2['style']
    sm = soup.new_tag('summary'); sm.append(h2.extract()); d.append(sm); d.append(body_div)
    return d

faq_cfg = cfg.get('faq', {})
items = [qa_from(s) for s in faq_src]
for d in items:  # titoli che non sono domande
    h2 = d.summary.h2; t = h2.get_text(' ', strip=True)
    for old, new in faq_cfg.get('titoli', {}).items():
        if t.startswith(old): h2.string = new; t = new
    first = d.select_one('.body').find(True, recursive=False)
    if t.endswith('?') and 'faq-q' not in (h2.get('class') or []) and first is not None and first.name == 'p':
        # nello schema solo se la risposta comincia con un paragrafo vero
        h2['class'] = (h2.get('class') or []) + ['faq-q']
        if 'faq-a' not in (first.get('class') or []): first['class'] = (first.get('class') or []) + ['faq-a']
for da, a, togli in faq_cfg.get('unisci', []):  # unisce due voci e toglie i punti doppi
    src_d = next(d for d in items if d.summary.get_text().strip().startswith(da))
    dst = next(d for d in items if d.summary.get_text().strip().startswith(a))
    b = dst.select_one('.body')
    for n in list(src_d.select_one('.body').children): b.append(n.extract())
    if src_d.get('id') and not dst.get('id'): dst['id'] = src_d['id']
    for f in b.select('.feat > div'):
        if any(f.get_text(' ', strip=True).startswith(x) for x in togli): f.decompose()
    feats = b.select('.feat')
    for f in feats[1:]:
        for c in list(f.children): feats[0].append(c.extract())
        f.decompose()
    for p in b.select('p.stats-line'): p.decompose()
    items.remove(src_d)
for pos, q, paras in faq_cfg.get('aggiungi', []):  # domande nuove scritte nel file di testi
    ps = ''.join(('<p class="faq-a">' if i == 0 else '<p>') + esc(x) + '</p>' for i, x in enumerate(paras))
    d = frag(f'<details class="qa"><summary><h2 class="faq-q" id="{slug(q)}">{esc(q)}</h2></summary><div class="body">{ps}</div></details>').details
    idx = next((i for i, x in enumerate(items) if x.summary.get_text(' ', strip=True).startswith(pos)), len(items))
    items.insert(idx, d)
not_q = [d.summary.get_text(' ', strip=True) for d in items if not d.summary.get_text(strip=True).endswith('?')]

# ---------- nuove sezioni ----------
def h2q(t, extra=''):
    """H2 nello schema FAQ solo se e' una domanda."""
    cl = ' '.join(x for x in (('faq-q' if t.endswith('?') else ''), extra) if x)
    attr = ' class="' + cl + '"' if cl else ''
    return f'<h2{attr} id="{slug(t)}">{esc(t)}</h2>'
def qa_inline(c):
    """Intro della sezione; con "domanda"/"risposta" aggiunge una domanda in H3 che entra nello schema FAQ."""
    out = f'<p class="intro{" faq-a" if c["titolo"].endswith("?") else ""}">{esc(c["intro"])}</p>' if c.get('intro') else ''
    if c.get('domanda'):
        out += f'<h3 class="faq-q sub-q" id="{slug(c["domanda"])}">{esc(c["domanda"])}</h3><p class="faq-a sub-a">{esc(c["risposta"])}</p>'
    return out

def from_faq(start):
    """Toglie una voce dalle FAQ e restituisce il suo contenuto (titolo, id, corpo) per farne una sezione."""
    d = next((x for x in items if x.summary.get_text(' ', strip=True).startswith(start)), None)
    if d is None: sys.exit('voce FAQ non trovata: ' + start)
    items.remove(d)
    h2 = d.summary.h2
    return h2, d.select_one('.body')

s_canali = ''
CA = cfg.get('canali')
if CA:
    chips = ''.join(f'<li>{esc(v)}</li>' for v in CA['voci'])
    s_canali = f'''<section class="v3 canali"><div class="in">
<p class="kick">{esc(CA["kick"])}</p>
<h2 id="{slug(CA["titolo"])}">{esc(CA["titolo"])}</h2>
<p class="intro">{esc(CA["intro"])}</p>
</div><div class="marquee" role="region" aria-label="{esc(CA["titolo"])}"><ul class="mq-track">{chips}</ul><ul class="mq-track" aria-hidden="true">{chips}</ul></div></section>'''

s_term = ''
T = cfg.get('termine')
if T:
    h2, b = from_faq(T['da'])
    h2.string = T['titolo']; h2['class'] = ['faq-q'] if T['titolo'].endswith('?') else []
    first = b.find('p')
    rest = [n for n in list(b.children) if getattr(n, 'name', None) and n is not first]
    cards = ''.join(f'<div class="term-card"><p class="term-k">{esc(k)}</p><h3>{esc(t)}</h3><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in pts) + '</ul></div>' for k, t, pts in T['colonne'])
    s_term = BeautifulSoup(f'''<section class="v3 alt"><div class="in"><p class="kick">{esc(T["kick"])}</p></div></section>''', 'html.parser')
    inn = s_term.select_one('.in')
    inn.append(h2)
    first['class'] = [c for c in (first.get('class') or []) if c != 'faq-a'] + ['intro', 'faq-a']
    if T.get('intro'): first.string = T['intro']
    if T.get('senza_resto'): rest = []
    inn.append(first)
    inn.append(frag(f'<div class="term-grid">{cards}</div>'))
    more = soup.new_tag('div', attrs={'class': 'term-more'})
    for n in rest: more.append(n.extract())
    inn.append(more)

s_why = ''
W = cfg.get('perche')
if W:
    h2, b = from_faq(W['da'])
    s_why = BeautifulSoup(f'''<section class="v3"><div class="in"><p class="kick">{esc(W["kick"])}</p></div></section>''', 'html.parser')
    inn = s_why.select_one('.in')
    inn.append(h2)
    for f in b.select('.feat > div'):
        if any(f.get_text(' ', strip=True).startswith(x) for x in W.get('togli', [])): f.decompose()
    grid = b.select_one('.feat')
    grid['class'] = ['why-grid']
    for ic in grid.select('.ic'): ic['class'] = ['i']
    for ic, tt, tx in W.get('aggiungi', []):
        grid.append(frag(f'<div><div class="i"><i data-lucide="{ic}"></i></div><h3>{esc(tt)}</h3><p>{esc(tx)}</p></div>'))
    inn.append(grid.extract())
    if W.get('citazioni'):
        def stars(n): return f'<span class="stars" role="img" aria-label="{n} su 5">' + '★' * n + '</span>' if n else ''
        qs = ''.join(f'<figure class="quote">{stars(c[2] if len(c) > 2 else 0)}<blockquote><p>{esc(c[0])}</p></blockquote><figcaption>{esc(c[1])}</figcaption></figure>' for c in W['citazioni'])
        inn.append(frag(f'<div class="quotes"><p class="quotes-k">{esc(W.get("citazioni_titolo", ""))}</p><div class="quotes-g">{qs}</div></div>'))

S = cfg['servizi']
svc = ''.join(f'<li><span class="i"><i data-lucide="{i}"></i></span><div><h3>{esc(t)}</h3><p>{esc(x)}</p></div></li>' for i, t, x in S['voci'])
s_serv = f'''<section class="v3 svc-section"><div class="in">
<p class="kick" id="servizi">{esc(S["kick"])}</p>
<h2 class="faq-q" id="{slug(S["titolo"])}">{esc(S["titolo"])}</h2>
<p class="intro faq-a">{esc(S["intro"])}</p>
<ul class="svc-list">{svc}</ul>
{FIX["services"]}
</div></section>'''

def bar(name, sub, us, vals):
    segs = list(zip(['p', 'c', 'v', 't', 'r'], FIX['seg'], vals))
    lab = f'{name}: ' + ', '.join(f'{n} {eur(v)}' for _, n, v in segs)
    inner = ''.join(f'<i class="s-{k}" style="width:{v/600*100:.2f}%" title="{n}: {eur(v)}">' + (f'<span>{eur(v)}</span>' if k in 'vtr' else '') + '</i>' for k, n, v in segs)
    return f'<div class="cmp-row{" us" if us else ""}"><div class="cmp-head"><p class="cmp-name">{name}</p><p class="cmp-sub">{sub}</p></div><div aria-label="{lab}" class="cmp-bar" role="img">{inner}</div><p class="cmp-res">{FIX["keep"]} <b>{eur(vals[-1])}</b></p></div>'
C = cfg['costi']
leg = ''.join(f'<span><i class="s-{k}"></i>{n}</span>' for k, n in zip(['p', 'c', 'v', 't', 'r'], FIX['leg']))
s_cost = f'''<section class="v3 alt"><div class="in">
<p class="kick">{esc(C["kick"])}</p>
{h2q(C["titolo"])}
{qa_inline(C)}
<div aria-label="{FIX["group"]}" class="cmp" role="group">{bar(FIX["us"], FIX["us_sub"], True, [90, 67.9, 134.84, 64.52, 242.74])}{bar(FIX["lo"], FIX["lo_sub"], False, [90, 67.9, 109.8, 126, 206.3])}<div class="cmp-leg">{leg}</div><p class="cmp-gain">{FIX["gain"]}</p></div>
<p class="money-why">{FIX["why"]}</p><p class="money-cta" style="margin:22px 0 6px"><a class="btn btn--solid" href="{FIX["anchor"]}">{FIX["more"]}</a></p>
</div></section>'''

P = cfg['portale']
shots = P.get('slide') or [['/images/portale-calendario.webp', FIX['cal_alt'], FIX['cal_cap'], 1400, 589]]
if len(shots) == 1:
    src, alt, cap, w, h = shots[0]
    portal_fig = f'<figure class="portal-shot"><img alt="{esc(alt)}" decoding="async" height="{h}" loading="lazy" src="{src}" width="{w}"><figcaption>{esc(cap)}</figcaption></figure>'
else:
    figs = ''.join(f'<figure class="portal-shot ps-slide" id="ps-{i+1}"><img alt="{esc(alt)}" decoding="async" height="{h}" loading="lazy" src="{src}" width="{w}"><figcaption>{esc(cap)}</figcaption></figure>' for i, (src, alt, cap, w, h) in enumerate(shots))
    dots = ''.join(f'<a href="#ps-{i+1}" aria-label="{i+1}"></a>' for i in range(len(shots)))
    portal_fig = f'<div class="pslider" aria-roledescription="carousel"><div class="ps-track">{figs}</div><div class="ps-dots">{dots}</div></div>'
pp = ''.join(f'<li><div class="i"><i data-lucide="{i}"></i></div><div><h3>{esc(t)}</h3><p>{esc(x)}</p></div></li>' for i, t, x in P['punti'])
s_ctrl_old = f'''<section class="v3"><div class="in ctrl">
<div><p class="kick">{esc(P["kick"])}</p>
{h2q(P["titolo"], "big")}
<p class="intro{" faq-a" if P["titolo"].endswith("?") else ""}">{esc(P["intro"])}</p>
<ul class="points">{pp}</ul></div>
{portal_fig}
</div></section>'''

s_ctrl = s_ctrl_old
if P.get('carosello'):
    n = len(P['punti'])
    slides = ''.join(f'<figure class="pc-slide" id="pc-{i+1}"><div class="pc-img"><img alt="{esc(sh[1])}" decoding="async" height="{sh[3]}" loading="lazy" src="{sh[0]}" width="{sh[2]}"></div><figcaption><span class="pc-n">{i+1:02d} / {n:02d}</span><h3>{esc(pt[1])}</h3><p>{esc(pt[2])}</p>' + (f'<small>{esc(sh[4])}</small>' if len(sh) > 4 and sh[4] else '') + '</figcaption></figure>' for i, (pt, sh) in enumerate(zip(P['punti'], P['carosello'])))
    dots = ''.join(f'<a href="#pc-{i+1}" aria-label="{esc(pt[1])}"></a>' for i, pt in enumerate(P['punti']))
    prev, nxt = ('Precedente', 'Successiva') if L == 'it' else ('Previous', 'Next')
    s_ctrl = f'''<section class="v3 pcar-sec"><div class="in pc-head"><p class="kick">{esc(P["kick"])}</p>
{h2q(P["titolo"], "big")}
<p class="intro">{esc(P["intro"])}</p></div>
<div class="pcar" aria-roledescription="carousel"><button class="pc-btn pc-prev" type="button" aria-label="{prev}">‹</button><div class="pc-track">{slides}</div><button class="pc-btn pc-next" type="button" aria-label="{nxt}">›</button></div>
<div class="pc-dots">{dots}</div></section>'''

s_casa = ''
K = cfg.get('casa')
if K:
    apt = BeautifulSoup((ROOT / K['scheda_da']).read_text(encoding='utf-8'), 'html.parser').select_one('.apt.apt-feat')
    if not apt: sys.exit('scheda .apt.apt-feat non trovata in ' + K['scheda_da'])
    s_casa = f'''<section class="v3 alt"><div class="in">
<p class="kick">{esc(K["kick"])}</p>
<h2 id="{slug(K["titolo"])}">{esc(K["titolo"])}</h2>
<p class="intro">{esc(K["intro"])}</p>
<div id="casa-slot">{apt}</div></div></section>'''

F = faq_cfg
s_faq = BeautifulSoup(f'''<section class="v3"><div class="in"><p class="kick" id="faq">{FIX["faq_kick"]}</p><h2>{esc(F["titolo"])}</h2><p class="intro">{esc(F["intro"])}</p><div class="faqs"></div></div></section>''', 'html.parser')
fq = s_faq.select_one('.faqs')
for d in items: fq.append(d)

if come:
    if 'alt' in (come.get('class') or []): come['class'] = [c for c in come['class'] if c != 'alt']
    for p in come.find_all('p'):
        if any(x in p.get_text() for x in cfg.get('come', {}).get('togli_frasi', [])): p.decompose()

# ---------- montaggio ----------
for s in secs:
    if s not in (come, cta, loc): s.decompose()
parti = {'servizi': s_serv, 'canali': s_canali, 'termine': s_term, 'costi': s_cost, 'portale': s_ctrl, 'perche': s_why, 'casa': s_casa}
alt = True  # sfondi alternati: la prima sezione (servizi) e' su fondo chiaro colorato
for k in cfg.get('ordine_sezioni', ['servizi', 'costi', 'portale', 'casa']):
    part = parti.get(k)
    if not part: continue
    node = (frag(part) if isinstance(part, str) else part).find('section')
    cl = [c for c in (node.get('class') or []) if c != 'alt']
    if alt and k != 'servizi': cl.append('alt')
    node['class'] = cl
    alt = not alt
    cta.insert_before(node)
if come: cta.insert_before(come.extract())
cta.insert_before(s_faq)
if P.get('carosello') and not soup.find('script', src=re.compile('portal-carousel')):
    body.append(frag('<script src="/js/portal-carousel.js"></script>'))
elif P.get('slide') and len(P['slide']) > 1 and not soup.find('script', src=re.compile('portal-slider')):
    body.append(frag('<script src="/js/portal-slider.js"></script>'))
if K and not soup.find('script', src=re.compile('apt-carousel')):
    body.append(frag('<script src="/js/apt-carousel.js"></script>'))

# ---------- schema, date ----------
out = soup.decode(formatter=FMT)
out = re.sub(r' (crossorigin|defer|async|required|hidden|open|checked|selected|disabled|novalidate|multiple|playsinline|muted|autoplay|loop)=""', r' \1', out)
def clean(x): return re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', '', x))).strip()
vis = [(clean(a), clean(b)) for _, a, b in re.findall(r'<h([23]) class="faq-q[^"]*"[^>]*>(.*?)</h\1>.*?<p class="[^"]*\bfaq-a\b[^"]*">(.*?)</p>', out, re.S)]
bm = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', out, re.S)
data = json.loads(bm.group(2))
oggi = cfg.get('data') or datetime.date.today().isoformat()
y, m, _ = oggi.split('-')
for n in data['@graph']:
    if n.get('@type') == 'FAQPage':
        n['mainEntity'] = [{'@type': 'Question', 'name': a, 'acceptedAnswer': {'@type': 'Answer', 'text': b}} for a, b in vis]
    if n.get('@type') == 'WebPage' and 'dateModified' in n: n['dateModified'] = oggi
out = out[:bm.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + out[bm.end(2):]
out = re.sub(r'(<p class="updated">)[^<]*', lambda mm: mm.group(1) + FIX['updated'].format(m=FIX['months'][int(m) - 1], y=y), out, count=1)
if not out.lstrip().lower().startswith('<!doctype'): out = '<!DOCTYPE html>\n' + out

# ---------- scrittura ----------
url_path = '/' + str(PAGE.parent).strip('/') + '/'
if PROVA:
    dest = ROOT / '_anteprima' / f'MODELLO-{PAGE.parent.name}-{L}.html'
    dest.write_text(out.replace('<head>', '<head><base href="https://vestadomus.it' + url_path + '">', 1), encoding='utf-8')
else:
    dest = PAGE; dest.write_text(out, encoding='utf-8')
    sm = ROOT / 'sitemap.xml'
    t = sm.read_text(encoding='utf-8') if sm.exists() else ''
    t2 = re.sub(r'(<loc>https://vestadomus\.it' + re.escape(url_path) + r'</loc>\s*<lastmod>)[^<]*', r'\g<1>' + oggi, t)
    if t: sm.write_text(t2, encoding='utf-8')
print('scritto:', dest)
print('FAQ nello schema:', len(vis))
if not_q: print('ATTENZIONE, titoli FAQ che non sono domande (aggiungerli in "faq.titoli"):', ' | '.join(not_q))
print('Ora: python3 tools/verifica.py, poi controllare la pagina (anche su mobile).')
