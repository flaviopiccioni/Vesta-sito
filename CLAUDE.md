# vestadomus.it — istruzioni per Claude Code

Sito di Vesta Srls Unipersonale, società di gestione affitti brevi e medi. Le pagine località parlano al PROPRIETARIO di casa, non all'ospite: il profilo degli ospiti serve solo a dimostrare conoscenza del mercato.

Sul sito lavorano due persone (Flavio e Federico). Rispondi sempre in italiano.

## Come si lavora

- All'inizio di ogni sessione esegui `git pull` per partire dall'ultima versione.
- Prima di applicare una modifica mostrala e aspetta conferma.
- "Pubblica" significa: commit con messaggio chiaro in italiano + `git push` su `main`. Netlify pubblica in automatico in circa un minuto. Mai pubblicare senza richiesta esplicita.
- Non trascinare mai cartelle su Netlify: il repo è l'unica fonte del sito.
- Il repo è PUBBLICO: non aggiungere note interne, dati di proprietari, contratti, prezzi riservati o credenziali.
- Prima di ogni commit che tocca le pagine lancia `python3 tools/verifica.py` (controlla canonical, hreflang, sitemap, meta, H1, JSON-LD e FAQ, div per sezione, griglie nelle sezioni con foto, foto ripetute, form, link interni, "Vesta Domus", "deduzione" e la duplicazione tra pagine IT). Se trova errori, non si pubblica.
- Dopo ogni pubblicazione ricorda all'utente: reinviare sitemap.xml su Google Search Console e Bing Webmaster Tools, richiedere l'indicizzazione delle pagine nuove o modificate (max 10-12 URL al giorno, sempre con slash finale), controllare online che le copertine si vedano.

## Struttura

- HTML statico puro, nessun build system. Una cartella per pagina con `index.html`, cartelle `it/` ed `en/`.
- Nella radice: `sitemap.xml`, `robots.txt`, `llms.txt`, `_redirects` (deve restare in radice: contiene il 301 di /referral-materiali verso /it/), cartella `og/`, script `self-host-immagini.py`.
- La root vestadomus.it è solo un redirect verso /it/: non arricchirla.
- 18 coppie IT/EN. Slug IT: milano, lago-di-como, lombardia, cervinia, valtournenche, courmayeur, valle-d-aosta, cortina, sardegna, stintino, porto-san-paolo, teulada, sicilia, marzamemi, palermo, privacy, cookie-policy, più la home /it/.
- Slug EN diversi: lake-como, lombardy, aosta-valley, sardinia, sicily. Gli altri sono uguali (anche /en/milano/).
- Hub regionali: Lombardia (Milano, Lago di Como), Valle d'Aosta (Cervinia, Valtournenche, Courmayeur), Sardegna (Stintino, Porto San Paolo, Teulada), Sicilia (Marzamemi, Palermo). Cortina non ha hub.
- Tutti gli URL interni, canonical, og:url, hreflang, sitemap e llms.txt usano lo SLASH FINALE (es. /it/milano/).
- Tre hreflang per pagina (it-IT, en-US, x-default), reciproci; il selettore `<a class="lang">` punta all'hreflang dell'altra lingua.
- Ogni modifica trasversale a più pagine va fatta con uno script, poi verificata su tutte le pagine coinvolte.
- `tools/` (script di verifica) sta nel repo ma è bloccata online da `_redirects`.
- `docs/` contiene la documentazione interna (dati località verificati, note di progetto, brief, lista Da fare in `docs/da-fare.md`): è in `.gitignore`, resta SOLO in locale e non va mai committata né pubblicata. Si condivide a parte. Se manca, chiedila all'utente. Dove i brief contraddicono questo file, vale questo file.
- Quando si prende una decisione nuova o si chiude un punto, aggiorna questo file (se la regola non è riservata) e `docs/da-fare.md`.

## Pagina località

Ordine sezioni: nav con selettore lingua e dropdown per regione → hero (breadcrumb visibile, kicker, H1, riga "Aggiornato a <mese anno>", lead) → mercato (id="mercato", con frase e link all'hub) → punti di forza → servizi → sezioni locali (zone id="zone", prezzi e stagionalità, adempimenti) → FAQ (id="faq") → form (id="valutazione") → box "Altre località" (Mare/Montagna/Città/Laghi) → footer con colonne Regioni e Località.

- Stile: sfondo #FAFAFA, teal #2A7971, teal scuro #184440, grigio-verde #5f7d78; Cormorant Garamond per i titoli, Inter per il testo; icone Lucide caricate a fine body.
- Sezioni con foto: struttura `wrap split` (immagine in `.ph`, testo a fianco), alternate con `.rev`. Sezioni solo testo: `sec-head` + `prose`. Mai griglie di card dentro una sezione con foto.
- Breadcrumb: `div class="bcn" role="navigation"`, MAI il tag `nav` (il sito rende sticky ogni nav).
- Menu mobile: ordine flex brand, burger, nlinks, nav-r; non alterarlo.
- Un solo blocco JSON-LD con `@graph`. Le FAQ dello schema coincidono parola per parola con quelle visibili; name/description del nodo WebPage coincidono con title e meta description. Convenzione @id: `<base>/#organization`, `<base>/#website`, `<url>#webpage`, `#breadcrumb`, `#place`, `#service`, `#faq`.
- Nuova pagina = copia di una esistente. Subito dopo correggi: canonical, og:url, hreflang, selettore lingua, oggetto del form e campo nascosto pagina/page. Aggiungila a sitemap.xml, llms.txt, dropdown, footer e box "Altre località" di tutte le pagine della lingua.

## Regole editoriali

- Title sotto 60 caratteri, formato "Gestione Affitti Brevi a <Località> | Vesta". Description 120-160 caratteri, commerciale, chiusa dalla valutazione gratuita; senza CIN/CIR/IUN, senza "property manager", senza riferimenti turistici.
- Mai scrivere "Vesta Domus": il nome è "Vesta". Restano invariati dominio, email e ragione sociale.
- I sei blocchi (gestione completa, fiscalità, valorizzazione, per chi è il servizio, chi siamo, processo) stanno su tutte le pagine città, MAI sugli hub. Ogni pagina li ha formulati in modo diverso, con la località nel titolo. Restano identici di proposito solo l'elenco dei 16 servizi e i 4 passaggi del processo. Non copiare testi da una pagina all'altra.
- Messaggio fiscale: Vesta fa da sostituto d'imposta, versa la cedolare secca calcolata sulla quota netta del proprietario (al netto di commissione e costi) e, dove previsto, inquadra parte delle spese come rimborso spese, così non rientrano nei ricavi e non vengono tassate. Vesta NON restituisce soldi al proprietario: mai "ti rimborsiamo", "ti riconosciamo il rimborso", "deduzione delle spese". Formulazione variata da pagina a pagina, sempre con "dove previsto" o equivalente. Il titolo della sezione fiscale non contiene la città e parla di vantaggi fiscali gestiti da Vesta, non di imposte o di netto. Sugli hub la sezione fiscale è solo un breve rimando alle pagine città.
- Milano non è una "curva piatta": mercato attivo tutto l'anno ma dinamico, con picchi di fiere ed eventi.
- Pagine di servizio (Vesta non ha immobili lì): Cortina, Courmayeur, Valtournenche, Palermo. Niente "i nostri immobili", niente numeri di unità o recensioni; i collaboratori sono "attivati sul posto". Leve consentite: "già operativi in Valle d'Aosta" (Cervinia) e "già operativi in Sicilia" (Marzamemi). Ammesso anche qui il dato aziendale "Oltre 80 immobili gestiti in Italia" (non è un dato locale). Non presentare la gestione come "a distanza" (né nei titoli né in evidenza).
- Valtournenche non riusa dati o testi della pagina Cervinia; Cervinia cita Valtournenche solo col link alla sua pagina. Copertura di Valtournenche: paese e zone limitrofe, non tutto il comune.
- Imposta di soggiorno: mai indicare importi.
- Pagine Sicilia: non parlare di modalità di check-in.
- Numeri e statistiche solo da fonti ufficiali verificate (vedi `docs/dati-localita.md`), con fonte, anno e perimetro territoriale (comune, comprensorio, provincia, regione). Niente BnbCalc per occupazione e tariffe. Mai lasciare segnaposto tipo "[DA VERIFICARE]" in pagina.
- Dopo ogni modifica di contenuto aggiorna la riga "Aggiornato a", il dateModified dello schema e il lastmod in sitemap.

## Adempimenti per regione

- Lombardia: CIR (uno per unità, da ROSS1000 dopo la comunicazione al SUAP, prima del CIN, da indicare negli annunci), CIN, ROSS1000 entro il 5 del mese, Questura entro 24 ore, imposta comunale.
- Valle d'Aosta: CIR dal Comune tramite piattaforma regionale, da esporre, poi CIN; ISTAT mensile; Questura entro 24 ore; imposta di soggiorno versata due volte l'anno.
- Veneto (Cortina): CIN da esporre e negli annunci, Alloggiati Web entro 24 ore, statistiche regionali, imposta comunale.
- Sardegna: IUN regionale e CIN, statistiche (SIRED/ROSS1000), Alloggiati Web, imposta comunale.
- Sicilia: CIR su Turist@t e CIN, entrambi da esporre; trasmissione giornaliera anche a movimento zero; Alloggiati Web.

## Dati aziendali

- Vesta Srls Unipersonale, Via della Moscova 40-4, 20121 Milano, P.IVA 13127250960.
- Email info@vestadomus.it, PEC vesta.s.r.l@pec.it, WhatsApp https://wa.me/393517407898, Instagram https://www.instagram.com/vesta_domus
- Form Formspree: action https://formspree.io/f/mvzepzya; oggetto "Valutazione gratuita – <Località>" (EN "Free assessment – <Location>"; home "Contatto – Home – vestadomus.it") + campo nascosto "pagina" (EN "page") con l'URL.
- Prenotazioni: Krossbooking, vestadomus.kross.travel; foto degli appartamenti dal CDN cdn.krossbooking.com.
- GA4 G-91YC2FYM24, caricato SOLO dopo il consenso cookie (funzione vdApplyConsent). Eventi: generate_lead, whatsapp_click, booking_click, email_click.

## Foto

- Nessuna foto dipende da Base44: sono state tutte scaricate. Prima di toccare una foto controlla nel codice se il `src` punta a un file del sito o a images.unsplash.com.
- Foto nuove da Unsplash: `https://images.unsplash.com/<photo-id>?w=1600&q=80&auto=format&fit=crop`, preferendo foto geolocalizzate nella località. Con `python3 self-host-immagini.py` si possono poi ospitare sul sito in WebP 1600px qualità 80.
- Mai la stessa foto due volte nella stessa pagina; prima di sostituirne una, controlla in quali pagine compare.
- Un ID non valido fa sparire l'immagine senza errori (`onerror="this.remove()"`): verifica online prima di dichiarare rotta una foto, mai sostituirla per deduzione.
- Gli alt descrivono solo ciò che si vede; se non si sa dove è scattata, non nominare la località.
- Niente vedute grigie o tristi di Milano.

## Checklist prima di pubblicare

canonical = og:url = URL reale con slash · tre hreflang reciproci · selettore lingua coerente con l'hreflang dell'altra lingua · nessun link interno rotto · pagina in sitemap con lastmod aggiornato · dateModified e "Aggiornato a" aggiornati · title < 60 e description 120-160 · un solo H1 · JSON-LD valido con FAQ allineate · div bilanciate sezione per sezione (non solo sul totale) · nessuna foto ripetuta nella pagina · oggetto del form con la località giusta · nessun "Vesta Domus".

L'unico `href="#"` ammesso è il pulsante "Impostazioni cookie" nel footer.
