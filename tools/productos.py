#!/usr/bin/env python3
"""Genera la tienda de productos digitales a partir de tools/productos.json.

Uso:  python3 tools/productos.py

Escribe:
  public/productos-digitales/index.html          (tienda)
  public/productos-digitales/<slug>/index.html   (una página por planilla)
  la sección #productos de public/index.html     (destacados de la portada)
  las URLs de productos en public/sitemap.xml

El encabezado y el pie se copian de public/catalogo-web/index.html, así que
siempre quedan iguales al resto del sitio.
"""
import datetime, html, json, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
DATA = json.loads((ROOT / "tools" / "productos.json").read_text(encoding="utf-8"))
RUBROS = DATA["rubros"]
PRODS = DATA["productos"]
SITE = "https://mortups.com.ar"
WA = "https://wa.me/5492634279451?text="
HOY = datetime.date.today().isoformat()

ICO = {
    "chat": '<path d="M20 11.5a8 8 0 0 1-11.6 7.1L4 20l1.4-4.2A8 8 0 1 1 20 11.5z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "sheet": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 9.5h16M4 15h16M10 4v16"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
}
def ico(n):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICO[n]}</svg>'

e = html.escape
def wa(texto):
    return WA + urllib.parse.quote(texto, safe="")
def money(n):
    return "$" + f"{n:,}".replace(",", ".")
def url(p):
    return f"/productos-digitales/{p['slug']}/"

# --- partes compartidas tomadas de una página existente ---
ref = (PUB / "catalogo-web" / "index.html").read_text(encoding="utf-8")
def between(s, a, b, incl=True):
    i = s.index(a); j = s.index(b, i) + len(b)
    return s[i:j]
TOP = between(ref, '<div class="lb">', "</header>")
TOP = TOP.replace('<a href="/productos-digitales/">', '<a href="/productos-digitales/" aria-current="page">')
FOOT = between(ref, '<footer class="ft">', "</footer>")
FAB = between(ref, '<a class="btn fab"', "</a>")
HEADCOMMON = between(ref, '<link rel="icon"', '<link rel="stylesheet" href="/site.css">')

def page(title, desc, path, body, jsonld=(), scripts=("/track.js",)):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in jsonld)
    sc = "".join(f'<script src="{s}" defer></script>\n' for s in scripts)
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
{HEADCOMMON}
{ld}</head>
<body>
{TOP}
<main class="pg">
{body}
</main>
{FOOT}
{FAB}
{sc}</body>
</html>
"""

def sheet(p, filas=4, cols=4, cls="sheet"):
    v = p["vista"]
    head = "".join(f"<th>{e(c)}</th>" for c in v["columnas"][:cols])
    rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in f[:cols]) + "</tr>" for f in v["filas"][:filas])
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'

def price_line(p):
    if p["estado"] == "disponible" and p.get("precio"):
        return f'<span class="pp-price">{money(p["precio"])}</span>'
    return '<span class="status">En preparación</span>'

def ctas(p, origen, big=False):
    if p["estado"] == "disponible":
        b = f'<a class="btn" href="{wa("Hola, quiero comprar la planilla: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">{ico("chat")}Comprar por WhatsApp</a>'
        if p.get("mp"):
            b += f'<a class="btn l" href="{e(p["mp"])}" rel="noopener">{ico("card")}Pagar con Mercado Pago</a>'
        return b
    return f'<a class="btn{"" if big else " l"}" href="{wa("Hola, quiero anotarme para: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">{ico("bell")}Avisarme cuando esté lista</a>'

def card(p):
    return (f'<article class="pcard" data-r="{p["rubro"]}"{" id=" + chr(34) + p["ancla"] + chr(34) if p.get("ancla") else ""}>'
            f'<a class="pcard-media" href="{url(p)}" tabindex="-1" aria-hidden="true">{sheet(p, 4, 3, "sheet mini")}</a>'
            f'<div class="pcard-bd"><h3><a href="{url(p)}">{e(p["nombre"])}</a></h3><p class="pcard-r">{e(RUBROS[p["rubro"]])}</p><p>{e(p["resumen"])}</p>'
            f'<div class="pcard-ft">{price_line(p)}<a class="lnk" href="{url(p)}">Ver planilla{ico("arrow")}</a></div></div></article>')

# ---------- tienda ----------
usados = [r for r in RUBROS if any(p["rubro"] == r for p in PRODS)]
filtros = '<div class="filters" role="group" aria-label="Filtrar por rubro"><button type="button" aria-pressed="true" data-f="todas">Todas</button>' + "".join(
    f'<button type="button" aria-pressed="false" data-f="{r}">{e(RUBROS[r])}</button>' for r in usados) + "</div>"
grid = '<div class="shop">' + "".join(card(p) for p in PRODS) + "</div>"
disp = sum(1 for p in PRODS if p["estado"] == "disponible")
estado_txt = (f"{disp} disponibles y {len(PRODS) - disp} en preparación." if disp else
              "Están en preparación: anotate en la que te sirva y te avisamos primero, con precio de lanzamiento.")
FAQ = [
    ("¿En qué formato se entregan?", "En Google Sheets (una copia para tu cuenta) y en Excel. Los datos que cargues quedan en tu archivo."),
    ("¿Cómo se compran?", "Tocás el botón de la planilla y nos escribís por WhatsApp. Ahí coordinamos el pago y te mandamos tu copia."),
    ("¿Necesito saber usar planillas?", "No. Están pensadas para completar datos y mirar los resultados. Si querés, te mostramos cómo se usa por WhatsApp."),
    ("¿Hay una para mi rubro?", "Vamos sumando una por rubro y por actividad. Si la tuya no está, escribinos y contanos qué te cuesta ordenar."),
    ("¿Y si después quiero una web o un sistema propio?", "Podés pasar a los paquetes de mortups cuando quieras. Un catálogo web, un menú QR o un registro de ventas a medida parten de lo mismo que ya ordenaste en la planilla."),
]
faq_html = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
body = f"""<section class="page-hero"><div class="w"><nav class="bc" aria-label="Ruta"><a href="/">Inicio</a> <span>/</span> Productos digitales</nav>
<h1>Planillas listas para ordenar tu negocio</h1>
<p class="lead">Archivos de Google Sheets y Excel ya armados para tu rubro: los copiás, cargás tus datos y tenés ventas, stock y precios en orden. Sin web, sin instalación y sin esperar una demo.</p>
<p class="shop-meta">{len(PRODS)} planillas · {estado_txt}</p></div></section>
<section id="tienda"><div class="w">
{filtros}
{grid}
</div></section>
<section class="alt"><div class="w"><h2>Cómo es la compra</h2>
<ol class="steps three"><li><h3>Elegís la planilla</h3><p>Mirás la vista de ejemplo y lo que incluye, y tocás el botón para escribirnos.</p></li><li><h3>Coordinamos el pago</h3><p>Por WhatsApp te pasamos el precio y la forma de pago.</p></li><li><h3>Recibís tu copia</h3><p>Te llega la copia para tu Google Sheets y el archivo de Excel, listos para cargar tus datos.</p></li></ol></div></section>
<section><div class="w faqg"><h2>Preguntas frecuentes</h2><div class="qa">{faq_html}</div></div></section>
<section class="cta"><div class="w"><h2>¿Qué planilla te haría falta?</h2><p>Contanos qué te cuesta ordenar y te decimos si ya la tenemos en preparación o la armamos para vos.</p><div class="actions"><a class="btn" href="{wa('Hola, quiero contar qué planilla me haría falta (productos-digitales-cta)')}" rel="noopener">{ico("chat")}Escribir por WhatsApp</a></div><div class="rel"><a href="/">Inicio</a><a href="/para/">Soluciones por rubro</a><a href="/#paquetes">Paquetes y precios</a></div></div></section>"""
ld = [
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Productos digitales", "item": SITE + "/productos-digitales/"}]},
    {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + url(p), "name": p["nombre"]} for i, p in enumerate(PRODS)]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]
(PUB / "productos-digitales" / "index.html").write_text(page(
    "Planillas de Excel y Google Sheets para tu negocio | mortups",
    "Planillas listas para usar en Google Sheets y Excel: ventas y caja, stock, lista de precios, presupuestos y una versión para cada rubro.",
    "/productos-digitales/", body, ld, ("/tienda.js", "/track.js")), encoding="utf-8")

# ---------- una página por planilla ----------
for p in PRODS:
    rub = RUBROS[p["rubro"]]
    inc = "".join(f"<li>{ico('check')}<span>{e(x)}</span></li>" for x in p["incluye"])
    rel = [q for q in PRODS if q is not p and (q["rubro"] == p["rubro"] or q["rubro"] == "general")][:3]
    rubro_link = (f'<p class="pp-rubro">Pensada para <a href="/para/{p["rubro"]}/">{e(rub.lower())}</a></p>' if p["rubro"] != "general" else '<p class="pp-rubro">Sirve para cualquier negocio</p>')
    nota = ("" if p["estado"] == "disponible" else
            '<p class="fine">Todavía no tiene precio publicado. Anotate y te avisamos primero, con precio de lanzamiento.</p>')
    body = f"""<section class="page-hero pp"><div class="w"><nav class="bc" aria-label="Ruta"><a href="/">Inicio</a> <span>/</span> <a href="/productos-digitales/">Productos digitales</a> <span>/</span> {e(p["nombre"])}</nav>
<div class="pp-info"><h1>{e(p["nombre"])}</h1>{rubro_link}<p class="lead">{e(p["resumen"])}</p>
<div class="pp-buy">{price_line(p)}</div><div class="actions">{ctas(p, "producto-" + p["slug"], big=True)}</div>{nota}</div>
<figure class="pp-preview"><div class="win"><div class="win-bar"><div class="dots"><i></i><i></i><i></i></div><div class="url">{ico("sheet")}{e(p["nombre"])}</div></div>{sheet(p, 9, 6, "sheet big")}</div><figcaption>Vista de ejemplo con datos de muestra</figcaption></figure>
</div></section>
<section><div class="w pp-grid"><div><h2>Qué incluye</h2><ul class="ck">{inc}</ul></div>
<div><h2>Cómo la recibís</h2><p>En Google Sheets (una copia para tu cuenta) y en Excel. Coordinamos el pago por WhatsApp y te mandamos tu copia, lista para cargar tus datos.</p></div></div></section>
{"<section class='alt'><div class='w'><h2>Otras planillas que te pueden servir</h2><div class='shop'>" + "".join(card(q) for q in rel) + "</div></div></section>" if rel else ""}
<section class="cta"><div class="w"><h2>¿Tenés dudas sobre esta planilla?</h2><p>Escribinos y te mostramos cómo se usa antes de comprarla.</p><div class="actions"><a class="btn" href="{wa("Hola, tengo una consulta sobre la planilla: " + p["nombre"] + " (producto-" + p["slug"] + "-cta)")}" rel="noopener">{ico("chat")}Escribir por WhatsApp</a></div><div class="rel"><a href="/productos-digitales/">Ver todas las planillas</a>{f'<a href="/para/{p["rubro"]}/">Soluciones para {e(rub.lower())}</a>' if p["rubro"] != "general" else ""}<a href="/#paquetes">Paquetes y precios</a></div></div></section>"""
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Productos digitales", "item": SITE + "/productos-digitales/"},
        {"@type": "ListItem", "position": 3, "name": p["nombre"], "item": SITE + url(p)}]}]
    if p["estado"] == "disponible" and p.get("precio"):
        ld.append({"@context": "https://schema.org", "@type": "Product", "name": p["nombre"], "description": p["resumen"],
                   "brand": {"@type": "Brand", "name": "mortups"},
                   "offers": {"@type": "Offer", "price": p["precio"], "priceCurrency": "ARS", "availability": "https://schema.org/InStock", "url": SITE + url(p)}})
    d = PUB / "productos-digitales" / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(f'{p["nombre"]} en Excel y Google Sheets | mortups', p["resumen"], url(p), body, ld), encoding="utf-8")

# ---------- portada: sección #productos ----------
home = PUB / "index.html"
s = home.read_text(encoding="utf-8")
dest = [p for p in PRODS if p.get("destacado")][:4]
sec = f"""<section id="productos"><div class="w">
 <div class="sh"><h2>Planillas listas para usar</h2><p class="sub">Archivos de Google Sheets y Excel ya armados: los copiás, cargás tus datos y ordenás tu negocio desde hoy. Hay una para cada rubro y vamos sumando más.</p></div>
 <div class="shop four">{"".join(card(p) for p in dest)}</div>
 <div class="more"><p>{len(PRODS)} planillas, una para cada rubro y actividad.</p><a class="btn l" href="/productos-digitales/">Ver todas las planillas</a></div>
</div></section>"""
s = re.sub(r'<section id="productos">.*?</section>', lambda m: sec, s, count=1, flags=re.S)
home.write_text(s, encoding="utf-8")

# ---------- páginas de rubro: enlace a su planilla ----------
for p in PRODS:
    if p["rubro"] == "general":
        continue
    f = PUB / "para" / p["rubro"] / "index.html"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        t = t.replace('href="/productos-digitales/">Ver todos los productos digitales</a>', f'href="{url(p)}">Ver la planilla</a>')
        f.write_text(t, encoding="utf-8")

# ---------- sitemap ----------
sm = PUB / "sitemap.xml"
x = sm.read_text(encoding="utf-8")
x = re.sub(r'\s*<url><loc>https://mortups\.com\.ar/productos-digitales/[^<]+/</loc>.*?</url>', "", x)
nuevas = "".join(f"\n  <url><loc>{SITE}{url(p)}</loc><lastmod>{HOY}</lastmod></url>" for p in PRODS)
x = x.replace("\n</urlset>", nuevas + "\n</urlset>")
sm.write_text(x, encoding="utf-8")

print(f"Listo: tienda + {len(PRODS)} páginas de producto + portada + sitemap.")
