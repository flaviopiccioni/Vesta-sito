/* Invia a HubSpot una copia di ogni richiesta inviata dai form Formspree del sito.
   Formspree resta il canale principale (email): se HubSpot non risponde, il form funziona comunque.
   Form HubSpot di destinazione: "Valutazione gratuita – sito" (account Vesta). */
(function () {
  var PORTAL = '148661351';
  var FORM = '112a7080-3d69-4b9f-a004-e0421ace947f';
  // Base legale del form (interesse legittimo, iscrizione "Marketing Information")
  var PRIVACY = {
    legitimateInterest: {
      value: true,
      subscriptionTypeId: 2878022551,
      legalBasis: 'LEAD',
      text: "Conserveremo ed elaboreremo queste informazioni per fornirti i nostri prodotti e servizi. Puoi richiedere l'annullamento dell'iscrizione in qualsiasi momento."
    }
  };
  var URL = 'https://api.hsforms.com/submissions/v3/integration/submit/' + PORTAL + '/' + FORM;

  // Pagina del sito (secondo pezzo dell'URL) -> valore del campo "Località" in HubSpot
  var LOCALITA = {
    'milano': 'Milano', 'lombardia': 'Milano', 'lombardy': 'Milano',
    'lago-di-como': 'Lago di Como', 'lake-como': 'Lago di Como',
    'cervinia': 'Cervinia', 'valtournenche': 'Cervinia',
    'courmayeur': 'Courmayeur',
    'valle-d-aosta': 'Altre località', 'aosta-valley': 'Altre località',
    'cortina': "Cortina d'Ampezzo",
    'sardegna': 'Sardegna', 'sardinia': 'Sardegna', 'stintino': 'Sardegna',
    'teulada': 'Sardegna', 'porto-san-paolo': 'Sardegna',
    'sicilia': 'Sicilia', 'sicily': 'Sicilia', 'palermo': 'Sicilia', 'marzamemi': 'Sicilia',
    'liguria': 'Liguria'
  };

  // Nome del campo nel form del sito (IT o EN) -> proprietà del contatto in HubSpot
  var CAMPI = {
    nome: 'firstname', name: 'firstname',
    email: 'email',
    telefono: 'phone', phone: 'phone',
    comune: 'comune__zona_immobile', area: 'comune__zona_immobile',
    tipologia: 'tipologia_immobile', type: 'tipologia_immobile',
    periodo: 'periodo_disponibile', availability: 'periodo_disponibile',
    messaggio: 'message', message: 'message',
    pagina: 'pagina_di_provenienza', page: 'pagina_di_provenienza'
  };

  function cookie(n) {
    var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.action || f.action.indexOf('formspree') === -1) return;
    if (!f.checkValidity()) return;
    var dati = new FormData(f);
    if (dati.get('_gotcha')) return; // campo anti-spam compilato: è un bot

    var fields = [];
    var visti = {};
    dati.forEach(function (v, k) {
      var p = CAMPI[k];
      v = String(v).trim();
      if (!p || !v || visti[p]) return;
      visti[p] = true;
      fields.push({ objectTypeId: '0-1', name: p, value: v });
    });
    if (!visti.email) return;

    fields.push({ objectTypeId: '0-1', name: 'ruolo', value: 'Proprietario' });
    fields.push({ objectTypeId: '0-1', name: 'origine_lead', value: 'Form sito' });
    var luogo = LOCALITA[location.pathname.split('/')[2] || ''];
    if (luogo) fields.push({ objectTypeId: '0-1', name: 'localita', value: luogo });

    var context = { pageUri: location.href, pageName: document.title };
    var hutk = cookie('hubspotutk');
    if (hutk) context.hutk = hutk;

    try {
      fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fields: fields, context: context, legalConsentOptions: PRIVACY }),
        keepalive: true
      }).catch(function () {});
    } catch (x) {}
  }, true);
})();
