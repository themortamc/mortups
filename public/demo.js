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
    cat: 'https://demo.mortups.com.ar/repuestos-san-isidro (30.000 items sync)',
    qr: 'https://demo.mortups.com.ar/menu-qr-restaurante (Mesa 4)',
    ind: 'https://demo.mortups.com.ar/tienda-indumentaria (Talles & Cuotas)',
    pos: 'https://demo.mortups.com.ar/admin/caja-en-vivo'
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
      var sku = r.getAttribute('data-sku') ? ' (Cod: ' + r.getAttribute('data-sku') + ')' : '';
      if (q > 0) {
        tot += q * pr;
        count += q;
        lines.push('• ' + q + 'x ' + name + sku + ' -> ' + fmt(q * pr));
      }
      var st = $('.st-left', r);
      if (st) {
        var base = +r.getAttribute('data-s') || 20;
        var left = Math.max(0, base - q);
        st.textContent = 'Stock: ' + left + (left <= 3 ? ' (Casi agotado)' : '');
      }
    });

    var badgeCart = $('.cart-count', p);
    if (badgeCart) badgeCart.textContent = count + ' ítems (' + fmt(tot) + ')';

    var totEl = $('.tot-val', p);
    if (totEl) totEl.textContent = fmt(tot);

    var out = $('.wa-body', p);
    if (!out) return;

    if (lines.length === 0) {
      out.innerHTML = '<span class="wa-empty">Seleccioná productos en la pantalla interactiva para ver cómo se genera automáticamente el pedido formateado.</span>';
      return;
    }

    var mesa = $('.mesas-pill [aria-pressed=true]', p);
    var mesaText = mesa ? '📌 *MESA ' + mesa.textContent + '*\n' : '';

    var msgHtml = '<b>' + (mesa ? '🍔 PEDIDO EN MESA #' + mesa.textContent : '📦 NUEVO PEDIDO - CATALOGO ONLINE') + '</b><br>' +
      '<small style="opacity:.8">Cliente: Consumidor Final • WhatsApp Directo</small><br><br>' +
      lines.join('<br>') + '<br><br>' +
      '<b>TOTAL: ' + fmt(tot) + '</b><br>' +
      '<small style="color:#7CFFB2">✔ Cero comisiones • Listo para confirmar</small>';

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