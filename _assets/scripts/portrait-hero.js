// portrait-hero.js — the homepage portrait's page personality: hover fades
// the photograph in over the running chain; a clean click (not a drag, not
// a link, not a selection) swaps the model's code into the frame. The
// rendering itself is ascii-player.js's gibbs mode.
(function () {
  var wrap = document.getElementById('portraitWrap');
  if (!wrap) return;
  document.getElementById('portraitPhoto').src = '/assets/home/portrait.jpg';

  var fig = wrap.closest('.portrait-fig'), px = 0, py = 0;
  fig.addEventListener('pointerdown', function (e) {
    px = e.clientX; py = e.clientY;
  });
  fig.addEventListener('pointerup', function (e) {
    if (Math.hypot(e.clientX - px, e.clientY - py) > 6) return;
    if (e.target.closest('a')) return;
    if (wrap.classList.contains('show-code') && String(getSelection())) return;
    wrap.classList.toggle('show-code');
  });
})();
