(function () {
  'use strict';
  var bar = document.querySelector('.filters');
  if (!bar) return;
  var cards = [].slice.call(document.querySelectorAll('#tienda .pcard'));
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-f]');
    if (!b) return;
    var f = b.getAttribute('data-f');
    [].forEach.call(bar.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    cards.forEach(function (c) {
      var r = c.getAttribute('data-r');
      c.hidden = !(f === 'todas' || r === f || (r === 'general' && f !== 'general'));
    });
  });
})();
