/* Filtro per zona nelle pagine ospiti (.zidx): un clic su una zona la evidenzia e
   lascia visibili solo le sue case; "Tutte le zone" (o un secondo clic sulla zona
   attiva) le mostra di nuovo tutte. Senza JavaScript i pulsanti restano link alle zone. */
(function () {
  var bar = document.querySelector('.zidx');
  if (!bar) return;
  var chips = [].slice.call(bar.querySelectorAll('a'));
  var zones = [].slice.call(document.querySelectorAll('.zone[id]'));
  if (!zones.length) return;
  var ids = zones.map(function (z) { return z.id; });

  function zoneOf(chip) {
    var id = (chip.getAttribute('href') || '').replace('#', '');
    return ids.indexOf(id) > -1 ? id : '';
  }

  function show(id) {
    chips.forEach(function (c) { c.classList.toggle('on', zoneOf(c) === id); });
    zones.forEach(function (z) {
      var grid = z.nextElementSibling;
      var vis = !id || z.id === id;
      [z, grid].forEach(function (el) {
        if (!el) return;
        el.classList.toggle('zhide', !vis);
        el.classList.remove('zfade');
      });
      if (!vis) return;
      void z.offsetWidth;
      z.classList.add('zfade');
      if (!grid) return;
      [].slice.call(grid.children).forEach(function (card, i) {
        card.classList.remove('zfade');
        card.style.animationDelay = Math.min(i, 8) * 45 + 'ms';
        void card.offsetWidth;
        card.classList.add('zfade');
      });
    });
  }

  chips.forEach(function (c) {
    c.addEventListener('click', function (e) {
      e.preventDefault();
      var id = zoneOf(c);
      if (id && c.classList.contains('on')) id = '';
      show(id);
    });
  });
})();
