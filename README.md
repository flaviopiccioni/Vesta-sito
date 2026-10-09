# Vesta Domus — Sito statico bilingue (IT / EN)

Sito statico in **raw-HTML**: ogni pagina è leggibile da tutti i motori (Google, AI Overview, ChatGPT, Perplexity) senza JavaScript. Risolve il limite client-side di Base44.

## Struttura
- `/it/` — Home
- `/it/cervinia/` — Landing Cervinia (13 sezioni + FAQ schema)
- `/it/stintino/` — Landing Stintino
- `/it/privacy/` — Privacy Policy
- `/it/cookie-policy/` — Cookie Policy
- `sitemap.xml`, `robots.txt` — SEO
- `index.html` (root) — redirect a `/it`

## Cosa è già incluso
- Design reale (teal #2A7971 / Cormorant Garamond / #FAFAFA) + icone Lucide
- Contenuti IT verbatim, foto reali (CDN/Krossbooking), footer coerenti
- `<head>` SEO: title, meta description, canonical (non-www), Open Graph
- Schema JSON-LD: RealEstateAgent (dati azienda), WebSite, FAQPage (Cervinia/Stintino)
- Link reali: menu, destinazioni, appartamenti→Krossbooking, Instagram, WhatsApp

## IMPORTANTE: rendere autonome le immagini
Le foto delle sezioni sono ospitate sul CDN di Base44: se elimini l'app Base44, si rompono.
PRIMA di spegnere Base44, esegui una volta (con internet):

    cd vesta-sito
    python3 self-host-immagini.py

Scarica tutte le immagini in /images e aggiorna l'HTML: il sito diventa 100% indipendente.

## Deploy
**Vercel/Netlify (consigliato):** trascina la cartella `vesta-sito` su app.netlify.com/drop, oppure importa il repo. Online in ~1 minuto, HTTPS incluso, ripubblicazione automatica.
**Aruba (FTP):** carica il contenuto di `vesta-sito/` nella cartella pubblica del dominio.

## Formspree (form di contatto)
I form usano `action="https://formspree.io/f/YOUR_FORM_ID"`. Per attivarli:
1. crea un account gratuito su formspree.io e un form collegato a info@vestadomus.it
2. Form ID collegato: **mvzepzya** (→ info@vestadomus.it). Alla prima richiesta conferma il form dall'email di Formspree.

## Banner cookie
Consenso granulare (3 categorie: tecnici sempre attivi, analitici e marketing con toggle) su tutte le pagine IT+EN. Scelta salvata in localStorage. Link "Impostazioni cookie / Cookie settings" nel footer per riaprire il pannello.

## Da completare (step successivi)
- Versioni **EN** (/en, /en/cervinia, …) + hreflang + link appartamenti EN
- (Opzionale) self-hosting immagini in /og/ e CMS visuale (Decap/Tina)
