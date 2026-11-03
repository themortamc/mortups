/* mortups · medición con consentimiento. Completá los IDs públicos; los tokens van como secretos del Worker. */
(function () {
  'use strict';
  var C = { ga4: '', ads: '', adsLabel: '', meta: '', tiktok: '' }; // ej: ga4:'G-XXXX', ads:'AW-123', adsLabel:'abc', meta:'123', tiktok:'C123'
  var d = document, KEY = 'mu_consent', CP = 'mu_cp';
  var on = C.ga4 || C.ads || C.meta || C.tiktok;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function ck(n) { var m = d.cookie.match('(?:^|; )' + n + '=([^;]*)'); return m ? decodeURIComponent(m[1]) : ''; }
  function uid() { return crypto.randomUUID ? crypto.randomUUID() : Date.now() + '-' + Math.random().toString(16).slice(2); }

  // Parámetros de campaña (solo se guardan si hay consentimiento)
  var q = new URLSearchParams(location.search), cp = {};
  try { cp = JSON.parse(get(CP) || '{}'); } catch (e) {}
  ['gclid', 'fbclid', 'ttclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
    if (q.get(k)) cp[k] = q.get(k).slice(0, 200);
  });
  function fbc() {
    if (!cp.fbclid) return '';
    if (!cp.fbc) cp.fbc = 'fb.1.' + Date.now() + '.' + cp.fbclid; // estable entre eventos
    return cp.fbc;
  }

  function gtagLoad() {
    var id = C.ga4 || C.ads; if (!id) return;
    var s = d.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id; d.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    if (C.ga4) gtag('config', C.ga4);
    if (C.ads) gtag('config', C.ads);
  }
  function metaLoad() {
    if (!C.meta) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, d, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', C.meta); fbq('track', 'PageView');
  }
  function ttLoad() {
    if (!C.tiktok) return;
    !function (w, D, t) { w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || []; ttq.methods = ['page', 'track', 'identify', 'instances', 'debug', 'on', 'off', 'once', 'ready', 'alias', 'group', 'enableCookie', 'disableCookie']; ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; }; for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]); ttq.load = function (e) { var n = 'https://analytics.tiktok.com/i18n/pixel/events.js'; ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = n; ttq._t = ttq._t || {}; ttq._t[e] = +new Date(); ttq._o = ttq._o || {}; var o = D.createElement('script'); o.async = !0; o.src = n + '?sdkid=' + e + '&lib=' + t; var a = D.getElementsByTagName('script')[0]; a.parentNode.insertBefore(o, a); }; ttq.load(C.tiktok); ttq.page(); }(window, d, 'ttq');
  }

  var granted = get(KEY) === 'yes';
  function start() { put(CP, JSON.stringify(cp)); gtagLoad(); metaLoad(); ttLoad(); }

  function banner() {
    if (!on || d.getElementById('mu-ck')) return;
    var st = d.createElement('style');
    st.textContent = '#mu-ck{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:60;max-width:560px;margin:0 auto;background:#14052A;color:#EFEBFF;padding:18px 20px;font:15px/1.45 system-ui,sans-serif;box-shadow:0 10px 60px rgba(0,0,0,.6);border:1px solid #8B2CFF}#mu-ck p{margin:0 0 14px}#mu-ck a{color:#C98BFF}#mu-ck div{display:flex;gap:10px}#mu-ck button{flex:1;font:700 15px system-ui,sans-serif;padding:12px;border:2px solid #C98BFF;cursor:pointer;background:transparent;color:#EFEBFF}#mu-ck button.y{background:#8B2CFF;border-color:#8B2CFF}';
    d.head.appendChild(st);
    var b = d.createElement('div'); b.id = 'mu-ck'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', 'Cookies');
    b.innerHTML = '<p>Usamos cookies de medición y publicidad (Google, Meta y TikTok) para saber qué funciona. Podés aceptarlas o rechazarlas. <a href="/cookies/">Más info</a></p><div><button type="button" data-v="no">Rechazar</button><button type="button" class="y" data-v="yes">Aceptar</button></div>';
    b.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-v'); if (!v) return;
      put(KEY, v); b.remove();
      if (v === 'yes') { granted = true; start(); } else { del(CP); }
    });
    d.body.appendChild(b);
  }

  if (granted) start(); else if (get(KEY) === null) banner();

  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-ck],a[href^="https://wa.me/"]'); if (!a) return;
    if (a.hasAttribute('data-ck')) { e.preventDefault(); del(KEY); del(CP); location.reload(); return; }
    var t = decodeURIComponent((a.href.split('text=')[1] || '').replace(/\+/g, ' '));
    if (/arrepentimiento|dar de baja/i.test(t)) return; // trámites legales: no se miden
    var id = uid(), ref = id.replace(/-/g, '').slice(0, 6).toUpperCase();
    a.href = a.href.replace(/%0A%0ARef%3A%20\w+$/, '');
    a.href += (a.href.indexOf('text=') > -1 ? '%0A%0A' : '?text=') + 'Ref%3A%20' + ref; // código para atribuir la venta cerrada en el chat
    if (!granted || !on) return;
    var name = (a.textContent || '').trim().slice(0, 60);
    if (window.gtag) {
      gtag('event', 'generate_lead', { method: 'whatsapp', content_name: name, ref: ref });
      if (C.ads && C.adsLabel) gtag('event', 'conversion', { send_to: C.ads + '/' + C.adsLabel, transaction_id: id });
    }
    if (window.fbq) fbq('track', 'Lead', { content_name: name }, { eventID: id });
    if (window.ttq) ttq.track('Contact', { content_name: name }, { event_id: id });
    put(CP, JSON.stringify(cp));
    var body = JSON.stringify({ event_id: id, ref: ref, name: name, url: location.href, fbp: ck('_fbp'), fbc: fbc(), ttp: ck('_ttp'), ttclid: cp.ttclid || '' });
    if (!(navigator.sendBeacon && navigator.sendBeacon('/api/track', new Blob([body], { type: 'application/json' })))) fetch('/api/track', { method: 'POST', body: body, keepalive: true, headers: { 'content-type': 'application/json' } }).catch(function () {});
  });
})();
