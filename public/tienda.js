(function () {
  'use strict';
  var bars = [].slice.call(document.querySelectorAll('#tienda .filters'));
  if (!bars.length) return;
  var cards = [].slice.call(document.querySelectorAll('#tienda .pcard'));
  var sel = { t: 'todas', r: 'todas' };
  function apply() {
    cards.forEach(function (c) {
      var t = c.getAttribute('data-t'), r = c.getAttribute('data-r');
      var okT = sel.t === 'todas' || t === sel.t;
      var okR = sel.r === 'todas' || r === sel.r || (r === 'general' && sel.r !== 'general');
      c.hidden = !(okT && okR);
    });
  }
  bars.forEach(function (bar) {
    var k = bar.getAttribute('data-k');
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-f]');
      if (!b) return;
      sel[k] = b.getAttribute('data-f');
      [].forEach.call(bar.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      apply();
    });
  });
})();
