(function () {
  'use strict';
  var d = document;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function fmt(n) { return '$' + Number(n).toLocaleString('es-AR'); }

  var tabs = $$('.mockup-tabs [role=tab]');
  var views = $$('.mw-view');
  var urlBar = $('.mw-url-text');

  var urlsMap = {
    cat: 'demo.mortups.com.ar/repuestos-san-isidro',
    qr: 'demo.mortups.com.ar/menu-qr-restaurante',
    ind: 'demo.mortups.com.ar/tienda-indumentaria',
    pos: 'demo.mortups.com.ar/admin/caja'
  };

  function switchTab(id) {
    tabs.forEach(function (t) {
      var sel = t.getAttribute('data-t') === id;
      t.setAttribute('aria-selected', String(sel));
      t.classList.toggle('active', sel);
    });
    views.forEach(function (v) {
      v.hidden = v.id !== 'v-' + id;
    });
    if (urlBar && urlsMap[id]) {
      urlBar.textContent = urlsMap[id];
    }
  }

  function updateView(p) {
    if (!p) return;
    var tot = 0, count = 0, lines = [], rows = $$('.p-item[data-p]', p);
    rows.forEach(function (r) {
      var qEl = $('.q-num', r);
      var q = qEl ? +qEl.textContent : 0;
      var pr = +r.getAttribute('data-p');
      var name = r.getAttribute('data-n');
      var sku = r.getAttribute('data-sku') ? ' (cód. ' + r.getAttribute('data-sku') + ')' : '';
      if (q > 0) {
        tot += q * pr;
        count += q;
        lines.push(q + ' × ' + name + sku + ' · ' + fmt(q * pr));
      }
      var st = $('.st-left', r);
      if (st) {
        var base = +r.getAttribute('data-s') || 20;
        var left = Math.max(0, base - q);
        st.textContent = 'Stock: ' + left + (left <= 3 ? ' · quedan pocos' : '');
      }
    });

    var badgeCart = $('.cart-count', p);
    if (badgeCart) badgeCart.textContent = count + ' ítems (' + fmt(tot) + ')';

    var totEl = $('.tot-val', p);
    if (totEl) totEl.textContent = fmt(tot);

    var out = $('.wa-body', p);
    if (!out) return;

    if (!out.hasAttribute('data-empty')) out.setAttribute('data-empty', out.innerHTML);
    if (lines.length === 0) {
      out.innerHTML = out.getAttribute('data-empty');
      return;
    }

    var mesa = $('.mesas-pill [aria-pressed=true]', p);
    var isPos = p.id === 'v-pos';
    var title = isPos ? 'Cierre de caja' : (mesa ? 'Pedido para la mesa ' + mesa.textContent : 'Hola, quiero hacer este pedido:');
    var msgHtml = '<b>' + title + '</b><br><br>' +
      lines.join('<br>') + '<br><br>' +
      '<b>Total: ' + fmt(tot) + '</b>' +
      '<small>' + (isPos ? 'Listo para exportar a Excel' : 'Sin comisiones · listo para confirmar') + '</small>';

    out.innerHTML = msgHtml;
  }

  function filterItems(view, query) {
    var items = $$('.p-item', view);
    var q = query.toLowerCase().trim();
    items.forEach(function (it) {
      var text = (it.getAttribute('data-n') + ' ' + (it.getAttribute('data-sku') || '')).toLowerCase();
      it.style.display = text.includes(q) ? '' : 'none';
    });
  }

  function downloadCsv(p) {
    var l = ['codigo,producto,precio_unitario,cantidad_vendida,stock_restante'];
    $$('.p-item[data-p]', p).forEach(function (r) {
      var qEl = $('.q-num', r);
      var q = qEl ? +qEl.textContent : 0;
      var sku = r.getAttribute('data-sku') || 'SKU-GEN';
      l.push([sku, '"' + r.getAttribute('data-n') + '"', r.getAttribute('data-p'), q, (+r.getAttribute('data-s') || 10) - q].join(','));
    });
    var a = d.createElement('a');
    a.href = URL.createObjectURL(new Blob(['﻿' + l.join('\n')], { type: 'text/csv;charset=utf-8' }));
    a.download = 'reporte-caja-mortups.csv';
    d.body.appendChild(a);
    a.click();
    a.remove();
  }

  d.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('.mockup-tabs [role=tab]') : null;
    if (t) {
      switchTab(t.getAttribute('data-t'));
      return;
    }
    var btnQ = e.target.closest('.q-btn');
    if (btnQ) {
      var row = btnQ.closest('.p-item');
      var numEl = $('.q-num', row);
      var delta = +btnQ.getAttribute('data-d');
      var cur = +numEl.textContent;
      numEl.textContent = Math.max(0, cur + delta);
      updateView(row.closest('.mw-view'));
      return;
    }
    var m = e.target.closest('.mesas-pill button');
    if (m) {
      var view = m.closest('.mw-view');
      $$('.mesas-pill button', view).forEach(function (x) {
        x.setAttribute('aria-pressed', String(x === m));
      });
      updateView(view);
      return;
    }
    var csvBtn = e.target.closest('[data-csv]');
    if (csvBtn) {
      downloadCsv(csvBtn.closest('.mw-view'));
      return;
    }
    var varBtn = e.target.closest('.v-btn');
    if (varBtn) {
      var pItem = varBtn.closest('.p-item');
      $$('.v-btn', pItem).forEach(function (b) { b.classList.remove('sel'); });
      varBtn.classList.add('sel');
    }
  });

  d.addEventListener('input', function (e) {
    if (e.target.classList.contains('mw-search-input')) {
      var view = e.target.closest('.mw-view');
      filterItems(view, e.target.value);
    }
  });

  // Init views
  views.forEach(updateView);
})();