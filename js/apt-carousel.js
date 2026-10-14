/* Card degli appartamenti (.apt): scorrimento foto con frecce e pallini.
   Tutta la card apre la scheda Kross tramite il link sul titolo (.apt-link);
   la striscia di foto sta sopra quel link per permettere lo swipe, quindi il click
   sulla foto lo inoltra al link. Le frecce scorrono e non aprono nulla. */
(function () {
  document.querySelectorAll('.apt').forEach(function (card) {
    var track = card.querySelector('.apt-track');
    if (!track) return;
    var prev = card.querySelector('.apt-prev');
    var next = card.querySelector('.apt-next');
    var dots = card.querySelectorAll('.apt-dots span');
    var link = card.querySelector('.apt-link');
    var n = track.children.length;

    function current() {
      return Math.round(track.scrollLeft / Math.max(track.clientWidth, 1));
    }
    function update() {
      var i = current();
      if (prev) prev.hidden = i <= 0;
      if (next) next.hidden = i >= n - 1;
      for (var k = 0; k < dots.length; k++) dots[k].classList.toggle('on', k === i);
    }
    function go(e, dir) {
      e.preventDefault();
      e.stopPropagation();
      track.scrollBy({ left: dir * track.clientWidth, behavior: 'smooth' });
    }

    if (prev) prev.addEventListener('click', function (e) { go(e, -1); });
    if (next) next.addEventListener('click', function (e) { go(e, 1); });

    var t;
    track.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(update, 60);
    }, { passive: true });
    window.addEventListener('resize', update);

    track.addEventListener('click', function () {
      if (link) link.click();
    });

    update();
  });
})();
