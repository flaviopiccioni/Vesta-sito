#!/usr/bin/env python3
"""Genera le immagini del portale proprietario (ricostruzioni con dati di esempio, come nella
presentazione "Portale proprietari Vesta"): images/portale-statistiche.svg e images/portale-distinta.svg.
Lingua: it (default) o en. Uso: python3 tools/portale-svg.py [it|en]"""
import sys
L = sys.argv[1] if len(sys.argv) > 1 else 'it'
F = 'font-family="Inter, Arial, sans-serif"'
def t(x, y, s, txt, w=400, c='#143C38', a='start'):
    return f'<text x="{x}" y="{y}" {F} font-size="{s}" font-weight="{w}" fill="{c}" text-anchor="{a}">{txt}</text>'
T = {
 'it': dict(stat='Statistiche', anno='Anno 2026', cols=['Mese', 'Notti vendute', 'Occupazione', 'Tariffa media', 'Tua quota', 'Imposta', 'Netto'],
            mesi=['Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'], arr='in arrivo', eur=lambda v: f'{v:,.0f} €'.replace(',', '.'),
            dist='Distinta di pagamento', num='n. 12 · 15 ottobre 2026', dcols=['Soggiorno', 'Notti', 'Tot. proprietario', 'Imposta', 'Netto'],
            add='Addebiti al proprietario', imp='Importo', voce='Serratura smart', tratt='Totale trattenuto', netto='Netto proprietario',
            e2=lambda v: f'{v:,.2f} €'.replace(',', 'X').replace('.', ',').replace('X', '.')),
 'en': dict(stat='Statistics', anno='Year 2026', cols=['Month', 'Nights sold', 'Occupancy', 'Average rate', 'Your share', 'Tax', 'Net'],
            mesi=['July', 'August', 'September', 'October', 'November', 'December'], arr='upcoming', eur=lambda v: f'€{v:,.0f}',
            dist='Payment statement', num='no. 12 · 15 October 2026', dcols=['Stay', 'Nights', 'Owner total', 'Tax', 'Net'],
            add='Charges to the owner', imp='Amount', voce='Smart lock', tratt='Total withheld', netto='Owner net', e2=lambda v: f'€{v:,.2f}'),
}[L]
# --- statistiche ---
rows = [(29, 94, 155, 3049, 640, 2409), (31, 100, 170, 3575, 751, 2824), (28, 93, 141, 2633, 553, 2080),
        (24, 77, 130, 2117, 444, 1673), (17, 57, 125, 1442, 303, 1139), (12, 39, 160, 1303, 274, 1029)]
xs = [330, 470, 620, 770, 890, 1008]
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 413" width="1040" height="413">',
     '<rect width="1040" height="413" rx="16" fill="#FFFFFF"/>', t(32, 50, 26, T['stat'], 600),
     '<rect x="860" y="24" width="148" height="38" rx="10" fill="#F4F7F5"/>', t(934, 49, 16, T['anno'], 600, a='middle'),
     '<rect x="16" y="78" width="1008" height="40" rx="8" fill="#F4F7F5"/>', t(32, 104, 15, T['cols'][0], 600, '#4F6A66')]
o += [t(x, 104, 15, c, 600, '#4F6A66', 'end') for x, c in zip(xs, T['cols'][1:])]
for i, (m, r) in enumerate(zip(T['mesi'], rows)):
    y = 148 + i * 46
    if i == 2: o.append(f'<rect x="16" y="{y-34}" width="1008" height="40" rx="8" fill="#E3F0EC"/>')
    o.append(t(32, y, 17, m, 600))
    vals = [str(r[0]), f'{r[1]}%', T['eur'](r[2]), T['eur'](r[3]), T['eur'](r[4]), T['eur'](r[5])]
    o += [t(x, y, 17, v, 600 if j == 5 else 400, a='end') for j, (x, v) in enumerate(zip(xs, vals))]
    if i >= 4: o += [f'<rect x="132" y="{y-17}" width="112" height="22" rx="11" fill="#FBEBD2"/>', t(188, y-1, 13, T['arr'], 600, a='middle')]
    o.append(f'<line x1="16" y1="{y+16}" x2="1024" y2="{y+16}" stroke="#D5E0DC"/>')
o.append('</svg>')
open('images/portale-statistiche' + ('' if L == 'it' else '-en') + '.svg', 'w').write('\n'.join(o))
# --- distinta ---
st = [('01/09 – 04/09', 3, 256.20, 53.80, 202.40), ('04/09 – 09/09', 5, 485.80, 102.02, 383.78), ('09/09 – 13/09', 4, 357.60, 75.10, 282.50),
      ('14/09 – 20/09', 6, 604.80, 127.01, 477.79), ('20/09 – 23/09', 3, 246.06, 51.67, 194.39), ('23/09 – 30/09', 7, 683.00, 143.43, 539.57)]
d = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 448" width="1000" height="448">',
     '<rect width="1000" height="448" rx="16" fill="#F4F7F5"/>', '<rect x="40" y="16" width="920" height="432" rx="4" fill="#FFFFFF" stroke="#D5E0DC" stroke-width="1.5"/>',
     t(72, 66, 30, 'V E S T A', 500, '#2A7971'), t(928, 52, 18, T['dist'], 600, a='end'), t(928, 76, 15, T['num'], 400, '#4F6A66', 'end'),
     '<line x1="72" y1="96" x2="928" y2="96" stroke="#143C38" stroke-width="1.5"/>', t(80, 126, 14, T['dcols'][0], 600, '#4F6A66')]
d += [t(x, 126, 14, c, 600, '#4F6A66', 'end') for x, c in zip([380, 600, 760, 920], T['dcols'][1:])]
for i, (p, n, a, b, c) in enumerate(st):
    y = 155 + i * 28
    d += [t(80, y, 15, p), t(380, y, 15, str(n), a='end'), t(600, y, 15, T['e2'](a), a='end'), t(760, y, 15, T['e2'](b), a='end'), t(920, y, 15, T['e2'](c), a='end'),
          f'<line x1="72" y1="{y+7}" x2="928" y2="{y+7}" stroke="#D5E0DC"/>']
d += ['<rect x="72" y="312" width="856" height="66" rx="8" fill="#FBEBD2"/>', t(88, 338, 15, T['add'], 600), t(912, 338, 14, T['imp'], 600, '#4F6A66', 'end'),
      t(88, 364, 16, T['voce']), t(912, 364, 16, T['e2'](39), 600, a='end'),
      t(760, 402, 15, T['tratt'], 500, '#4F6A66', 'end'), t(920, 402, 15, T['e2'](39), a='end'),
      t(760, 428, 17, T['netto'], 600, a='end'), t(920, 428, 17, T['e2'](2041.43), 600, a='end'), '</svg>']
open('images/portale-distinta' + ('' if L == 'it' else '-en') + '.svg', 'w').write('\n'.join(d))
print('ok', L)
# --- documenti (sezione Distinte del portale) ---
D = {'it': dict(tit='Distinte', sub='Scarica i PDF per te o per il commercialista', rows=[('Distinta n. 12', '15 ottobre 2026', '2.041,43 €'), ('Distinta n. 11', '15 settembre 2026', '2.386,10 €'), ('Distinta n. 10', '15 agosto 2026', '2.512,75 €'), ('Distinta n. 9', '15 luglio 2026', '1.987,20 €'), ('Distinta n. 8', '15 giugno 2026', '1.744,60 €')], dl='Scarica PDF'),
     'en': dict(tit='Statements', sub='Download the PDFs for you or your accountant', rows=[('Statement no. 12', '15 October 2026', '€2,041.43'), ('Statement no. 11', '15 September 2026', '€2,386.10'), ('Statement no. 10', '15 August 2026', '€2,512.75'), ('Statement no. 9', '15 July 2026', '€1,987.20'), ('Statement no. 8', '15 June 2026', '€1,744.60')], dl='Download PDF')}[L]
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 413" width="1040" height="413">', '<rect width="1040" height="413" rx="16" fill="#FFFFFF"/>',
     t(32, 50, 26, D['tit'], 600), t(32, 76, 15, D['sub'], 400, '#4F6A66')]
for i, (n, dt, v) in enumerate(D['rows']):
    y = 100 + i * 60
    o += [f'<rect x="16" y="{y}" width="1008" height="50" rx="10" fill="{"#F4F7F5" if i % 2 == 0 else "#FFFFFF"}"/>',
          f'<rect x="32" y="{y+11}" width="28" height="28" rx="6" fill="#FBEBD2"/>', t(46, y+30, 11, 'PDF', 700, '#143C38', 'middle'),
          t(76, y+31, 17, n, 600), t(330, y+31, 16, dt, 400, '#4F6A66'), t(700, y+31, 17, v, 600, a='end'),
          f'<rect x="840" y="{y+9}" width="168" height="32" rx="16" fill="#2A7971"/>', t(924, y+30, 14, D['dl'], 600, '#FFFFFF', 'middle')]
o.append('</svg>')
open('images/portale-documenti' + ('' if L == 'it' else '-en') + '.svg', 'w').write('\n'.join(o))
# --- burocrazia (schema illustrativo, non e' una schermata del portale) ---
B = {'it': dict(tit='Pratiche della tua casa', sub='Le seguiamo noi, a nome di Vesta', rows=[('CIR e CIN', 'Intestati a Vesta'), ('Comunicazione ospiti alla Questura', 'A ogni arrivo'), ('Comunicazioni ISTAT', 'Ogni mese'), ('Imposta di soggiorno', 'Versata da Vesta'), ('Cedolare secca', 'Versata da Vesta')], ok='Fatto'),
     'en': dict(tit='Your home\'s paperwork', sub='We handle it, in Vesta\'s name', rows=[('CIR and CIN', 'Registered to Vesta'), ('Guest reporting to the police', 'At every arrival'), ('ISTAT reporting', 'Every month'), ('Tourist tax', 'Paid by Vesta'), ('Cedolare secca', 'Paid by Vesta')], ok='Done')}[L]
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 413" width="1040" height="413">', '<rect width="1040" height="413" rx="16" fill="#FFFFFF"/>',
     t(32, 50, 26, B['tit'], 600), t(32, 76, 15, B['sub'], 400, '#4F6A66')]
for i, (n, w) in enumerate(B['rows']):
    y = 100 + i * 60
    o += [f'<line x1="16" y1="{y+55}" x2="1024" y2="{y+55}" stroke="#D5E0DC"/>',
          f'<circle cx="48" cy="{y+27}" r="14" fill="#E3F0EC"/>', f'<path d="M41 {y+27} l5 5 l10 -10" stroke="#2A7971" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
          t(76, y+33, 18, n.replace("'", '&#39;'), 600), t(700, y+33, 16, w, 400, '#4F6A66', 'end'),
          f'<rect x="900" y="{y+12}" width="108" height="30" rx="15" fill="#E3F0EC"/>', t(954, y+32, 14, B['ok'], 600, '#2A7971', 'middle')]
o.append('</svg>')
open('images/portale-burocrazia' + ('' if L == 'it' else '-en') + '.svg', 'w').write('\n'.join(o).replace("Your home's", 'Your home&#39;s').replace("Vesta's", 'Vesta&#39;s'))
