/* Slider orizzontale delle case gestite (.apts-slider): frecce che scorrono di una scheda.
   Le frecce si nascondono all'inizio e alla fine, e anche quando tutte le schede stanno in vista. */
(function () {
  document.querySelectorAll('.apts-slider').forEach(function (box) {
    var row = box.querySelector('.apts-row');
    var prev = box.querySelector('.apts-prev');
    var next = box.querySelector('.apts-next');
    if (!row) return;
    function step() {
      var card = row.querySelector('.apt');
      if (!card) return row.clientWidth;
      var gap = parseFloat(getComputedStyle(row).columnGap) || 0;
      return card.getBoundingClientRect().width + gap;
    }
    function update() {
      var max = row.scrollWidth - row.clientWidth - 2;
      if (prev) prev.hidden = row.scrollLeft <= 2;
      if (next) next.hidden = row.scrollLeft >= max;
    }
    if (prev) prev.addEventListener('click', function () { row.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { row.scrollBy({ left: step(), behavior: 'smooth' }); });
    var t;
    row.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();
