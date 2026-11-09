(function () {
  'use strict';
  var d = document;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function fmt(n) { return '$' + n.toLocaleString('es-AR'); }
  var tabs = $$('.tabs [role=tab]');
  function show(id) {
    tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-t') === id)); });
    $$('.dm').forEach(function (p) { p.hidden = p.id !== 'p-' + id; });
  }
  function update(p) {
    var tot = 0, lines = [], rows = $$('.row[data-p]', p);
    rows.forEach(function (r) {
      var q = +$('output', r).textContent, pr = +r.getAttribute('data-p');
      if (q) { tot += q * pr; lines.push(q + ' x ' + r.getAttribute('data-n') + ' — ' + fmt(q * pr)); }
      var st = $('.st', r);
      if (st) { var left = +r.getAttribute('data-s') - q; st.textContent = 'Stock: ' + left + (left <= +r.getAttribute('data-m') ? ' · stock bajo' : ''); }
    });
    var t = $('.tot', p); if (t) t.textContent = 'Total vendido: ' + fmt(tot);
    var out = $('.msg', p); if (!out) return;
    if (!lines.length) { out.textContent = 'Sumá productos para ver el mensaje.'; return; }
    var mesa = $('.mesas [aria-pressed=true]', p);
    out.textContent = (mesa ? 'Pedido en la mesa ' + mesa.textContent + '\n' : 'Hola, quiero hacer este pedido:\n') + lines.join('\n') + '\nTotal: ' + fmt(tot) + (mesa ? '\nPagado con Mercado Pago (demostración)' : '');
  }
  function csv(p) {
    var l = ['producto,precio,vendidas,stock'];
    $$('.row[data-p]', p).forEach(function (r) {
      var q = +$('output', r).textContent;
      l.push(['"' + r.getAttribute('data-n') + '"', r.getAttribute('data-p'), q, +r.getAttribute('data-s') - q].join(','));
    });
    var a = d.createElement('a');
    a.href = URL.createObjectURL(new Blob(['\ufeff' + l.join('\n')], { type: 'text/csv;charset=utf-8' }));
    a.download = 'ventas-demo.csv'; d.body.appendChild(a); a.click(); a.remove();
  }
  d.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('.tabs [role=tab]') : null;
    if (t) { show(t.getAttribute('data-t')); return; }
    var b = e.target.closest('.q button');
    if (b) { var o = $('output', b.closest('.row')); o.textContent = Math.max(0, +o.textContent + +b.getAttribute('data-d')); update(b.closest('.dm')); return; }
    var m = e.target.closest('.mesas button');
    if (m) { $$('.mesas button', m.closest('.dm')).forEach(function (x) { x.setAttribute('aria-pressed', String(x === m)); }); update(m.closest('.dm')); return; }
    var c = e.target.closest('[data-csv]');
    if (c) csv(c.closest('.dm'));
  });
  $$('.dm').forEach(update);
})();
