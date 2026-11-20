/* mortups · tema claro / oscuro. Se carga en <head> para evitar el parpadeo. */
(function () {
  'use strict';
  var d = document.documentElement, KEY = 'mu_theme';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function put(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function current() { return get() || (mq && mq.matches ? 'dark' : 'light'); }
  function apply(t) {
    d.setAttribute('data-theme', t);
    var m = document.querySelector('meta[name=theme-color]');
    if (m) m.setAttribute('content', t === 'dark' ? '#121016' : '#FFFFFF');
    [].forEach.call(document.querySelectorAll('.theme'), function (b) {
      b.setAttribute('aria-pressed', String(t === 'dark'));
      b.setAttribute('aria-label', t === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
    });
  }
  apply(current());
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (!get()) apply(current()); });
  document.addEventListener('DOMContentLoaded', function () { apply(current()); });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.theme');
    if (!b) return;
    var t = current() === 'dark' ? 'light' : 'dark';
    put(t); apply(t);
  });
})();
