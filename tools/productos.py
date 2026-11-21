#!/usr/bin/env python3
"""Genera la tienda de productos digitales a partir de tools/productos.json.

Uso:  python3 tools/productos.py

Tipos de producto: planilla (Excel / Google Sheets), software y guia (PDF).

Escribe:
  public/productos-digitales/index.html          (tienda)
  public/productos-digitales/<slug>/index.html   (una página por producto)
  la sección #productos de public/index.html     (destacados de la portada)
  el enlace a su producto en cada página de rubro
  las URLs de productos en public/sitemap.xml

El encabezado y el pie se copian de public/catalogo-web/index.html, así que
siempre quedan iguales al resto del sitio.
"""
import datetime, html, json, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
DATA = json.loads((ROOT / "tools" / "productos.json").read_text(encoding="utf-8"))
RUBROS = DATA["rubros"]
TIPOS = DATA["tipos"]
TIPOS_PL = DATA["tipos_plural"]
PROX = DATA.get("proximamente", {})
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
    "app": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 9v11"/>',
    "book": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
}
TIPO_ICO = {"planilla": "sheet", "software": "app", "guia": "book"}
def ico(n):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICO[n]}</svg>'

e = html.escape
def wa(texto):
    return WA + urllib.parse.quote(texto, safe="")
def money(n):
    return "$" + f"{n:,}".replace(",", ".")
def url(p):
    return f"/productos-digitales/{p['slug']}/"

ENTREGA = {
    "planilla": "En Google Sheets (una copia para tu cuenta) y en Excel. Coordinamos el pago por WhatsApp y te mandamos tu copia, lista para cargar tus datos.",
    "software": "Coordinamos el pago por WhatsApp y te explicamos cómo se instala o cómo entrás, paso a paso.",
    "guia": "Es un archivo PDF. Coordinamos el pago por WhatsApp y te lo mandamos para que lo leas en el celular, la compu o impreso.",
}
TITULO_SUF = {"planilla": "en Excel y Sheets", "software": "· software para tu negocio", "guia": "· guía en PDF"}

# --- partes compartidas tomadas de una página existente ---
ref = (PUB / "catalogo-web" / "index.html").read_text(encoding="utf-8")
def between(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b)
    return s[i:j]
TOP = between(ref, '<div class="lb">', "</header>").replace(
    '<a href="/productos-digitales/">', '<a href="/productos-digitales/" aria-current="page">')
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

# --- vistas de ejemplo según el tipo ---
def table(p, filas, cols, cls):
    v = p.get("vista") or {"columnas": [], "filas": []}
    head = "".join(f"<th>{e(c)}</th>" for c in v["columnas"][:cols])
    rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in f[:cols]) + "</tr>" for f in v["filas"][:filas])
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'

def cover(p, size):
    g = p.get("guia", {})
    sub = f'<span class="cover-s">{e(g["subtitulo"])}</span>' if g.get("subtitulo") else ""
    pags = f' · {g["paginas"]} páginas' if g.get("paginas") else ""
    return (f'<div class="cover {size}"><span class="cover-brand">mort<b>ups</b></span>'
            f'<span class="cover-t">{e(p["nombre"])}</span>{sub}<span class="cover-f">Guía en PDF{pags}</span></div>')

def app(p, filas, cols, size):
    return (f'<div class="appshot {size}"><div class="appshot-side"><i></i><i></i><i></i><i></i></div>'
            f'<div class="appshot-main"><div class="appshot-top">{e(p["nombre"])}</div>{table(p, filas, cols, "sheet app")}</div></div>')

def media(p, big=False):
    t = p.get("tipo", "planilla")
    if t == "guia":
        return cover(p, "big" if big else "mini")
    if t == "software":
        return app(p, 6 if big else 3, 4 if big else 3, "big" if big else "mini")
    return table(p, 9 if big else 4, 6 if big else 3, "sheet big" if big else "sheet mini")

def price_line(p):
    if p["estado"] == "disponible" and p.get("precio"):
        return f'<span class="pp-price">{money(p["precio"])}</span>'
    return '<span class="status">En preparación</span>'

def ctas(p, origen, big=False):
    if p["estado"] == "disponible":
        b = f'<a class="btn" href="{wa("Hola, quiero comprar: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">{ico("chat")}Comprar por WhatsApp</a>'
        if p.get("mp"):
            b += f'<a class="btn l" href="{e(p["mp"])}" rel="noopener">{ico("card")}Pagar con Mercado Pago</a>'
        return b
    return f'<a class="btn{"" if big else " l"}" href="{wa("Hola, quiero anotarme para: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">{ico("bell")}Avisarme cuando esté listo</a>'

def label(p):
    return f'{TIPOS[p["tipo"]]} · {RUBROS[p["rubro"]]}'

def card(p, with_id=True):
    ident = f' id="{p["ancla"]}"' if with_id and p.get("ancla") else ""
    return (f'<article class="pcard t-{p["tipo"]}" data-r="{p["rubro"]}" data-t="{p["tipo"]}"{ident}>'
            f'<a class="pcard-media" href="{url(p)}" tabindex="-1" aria-hidden="true">{media(p)}</a>'
            f'<div class="pcard-bd"><h3><a href="{url(p)}">{e(p["nombre"])}</a></h3><p class="pcard-r">{e(label(p))}</p><p>{e(p["resumen"])}</p>'
            f'<div class="pcard-ft">{price_line(p)}<a class="lnk" href="{url(p)}">Ver detalle{ico("arrow")}</a></div></div></article>')

# ---------- tienda ----------
tipos_usados = [t for t in TIPOS if any(p["tipo"] == t for p in PRODS)]
rubros_usados = [r for r in RUBROS if any(p["rubro"] == r for p in PRODS)]
f_tipo = ('<div class="filters" role="group" aria-label="Filtrar por tipo" data-k="t"><button type="button" aria-pressed="true" data-f="todas">Todos</button>' + "".join(
    f'<button type="button" aria-pressed="false" data-f="{t}">{e(TIPOS_PL[t])}</button>' for t in tipos_usados) + "</div>") if len(tipos_usados) > 1 else ""
f_rubro = '<div class="filters" role="group" aria-label="Filtrar por rubro" data-k="r"><button type="button" aria-pressed="true" data-f="todas">Todos los rubros</button>' + "".join(
    f'<button type="button" aria-pressed="false" data-f="{r}">{e(RUBROS[r])}</button>' for r in rubros_usados) + "</div>"
grid = '<div class="shop">' + "".join(card(p) for p in PRODS) + "</div>"
disp = sum(1 for p in PRODS if p["estado"] == "disponible")
estado_txt = (f"Todos disponibles, con pago único." if disp == len(PRODS) else
              f"{disp} disponibles y {len(PRODS) - disp} en preparación." if disp else
              "Están en preparación: anotate en el que te sirva y te avisamos primero, con precio de lanzamiento.")
pendientes = [t for t in PROX if t not in tipos_usados]
prox_html = ""
if pendientes:
    items = "".join(
        f'<div class="soon"><span class="soon-ic">{ico(TIPO_ICO[t])}</span><div><h3>{e(PROX[t]["titulo"])}</h3><p>{e(PROX[t]["texto"])}</p>'
        f'<a class="lnk" href="{wa("Hola, quiero que me avisen cuando salgan: " + PROX[t]["titulo"] + " (productos-proximamente)")}" rel="noopener">Avisarme cuando salgan{ico("arrow")}</a></div></div>'
        for t in pendientes)
    prox_html = f'<section class="alt"><div class="w"><div class="sh"><h2>Lo que viene</h2><p class="sub">Además de las planillas, estamos preparando estos productos.</p></div><div class="soon-grid">{items}</div></div></section>'

FAQ = [
    ("¿En qué formato se entregan?", "Las planillas, en Google Sheets (una copia para tu cuenta) y en Excel. Las guías y libros, en PDF. El software, según cada producto: en su página te contamos cómo se instala o cómo entrás."),
    ("¿Cómo se compran?", "Tocás el botón del producto y nos escribís por WhatsApp. Ahí coordinamos el pago y te mandamos lo que compraste."),
    ("¿Necesito saber de tecnología?", "No. Están pensados para usarlos sin experiencia. Si querés, te mostramos cómo se usan por WhatsApp."),
    ("¿Hay uno para mi rubro?", "Vamos sumando productos para cada rubro y actividad. Si el tuyo no está, escribinos y contanos qué te cuesta ordenar o qué querés aprender."),
    ("¿Y si después quiero una web o un sistema propio?", "Podés pasar a los paquetes de mortups cuando quieras. Un catálogo web, un menú QR o un registro de ventas a medida parten de lo mismo que ya ordenaste."),
]
faq_html = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
compra_alt = '' if prox_html else ' class="alt"'
body = f"""<section class="page-hero"><div class="w"><nav class="bc" aria-label="Ruta"><a href="/">Inicio</a> <span>/</span> Productos digitales</nav>
<h1>Productos digitales para ordenar y hacer crecer tu negocio</h1>
<p class="lead">Planillas de Excel y Google Sheets listas para usar, software para tu negocio y guías en PDF para aprender marketing y administración. Pensados para comercios, pymes y empresas de Argentina.</p>
<p class="shop-meta">{len(PRODS)} productos · {estado_txt}</p></div></section>
<section id="tienda"><div class="w">
{f_tipo}{f_rubro}
{grid}
</div></section>
{prox_html}
<section{compra_alt}><div class="w"><h2>Cómo es la compra</h2>
<ol class="steps three"><li><h3>Elegís el producto</h3><p>Mirás la vista de ejemplo y lo que incluye, y tocás el botón para escribirnos.</p></li><li><h3>Coordinamos el pago</h3><p>Por WhatsApp te pasamos el precio y la forma de pago.</p></li><li><h3>Lo recibís</h3><p>Te mandamos tu copia de la planilla, el PDF o el acceso al software, listo para usar.</p></li></ol></div></section>
<section><div class="w faqg"><h2>Preguntas frecuentes</h2><div class="qa">{faq_html}</div></div></section>
<section class="cta"><div class="w"><h2>¿Qué te haría falta?</h2><p>Contanos qué te cuesta ordenar o qué querés aprender y te decimos si ya lo tenemos en preparación o lo armamos para vos.</p><div class="actions"><a class="btn" href="{wa('Hola, quiero contar qué producto me haría falta (productos-digitales-cta)')}" rel="noopener">{ico("chat")}Escribir por WhatsApp</a></div><div class="rel"><a href="/">Inicio</a><a href="/para/">Soluciones por rubro</a><a href="/#paquetes">Paquetes y precios</a></div></div></section>"""
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
    "Productos digitales para negocios: planillas, software y guías | mortups",
    "Planillas de Excel y Google Sheets listas para usar, software para tu negocio y guías en PDF de marketing y administración para comercios y pymes de Argentina.",
    "/productos-digitales/", body, ld, ("/tienda.js", "/track.js")), encoding="utf-8")

# ---------- una página por producto ----------
for p in PRODS:
    t = p["tipo"]
    rub = RUBROS[p["rubro"]]
    inc = "".join(f"<li>{ico('check')}<span>{e(x)}</span></li>" for x in p["incluye"])
    indice = p.get("guia", {}).get("indice") or []
    idx = ("<div><h2>Índice</h2><ol class='toc'>" + "".join(f"<li>{e(x)}</li>" for x in indice) + "</ol></div>") if indice else ""
    rel = [q for q in PRODS if q is not p and (q["rubro"] == p["rubro"] or q["rubro"] == "general")]
    rel = sorted(rel, key=lambda q: (q["rubro"] != p["rubro"], q["tipo"] != t))[:3]
    if p["rubro"] != "general":
        rubro_link = f'<p class="pp-rubro">{e(TIPOS[t])} pensada para <a href="/para/{p["rubro"]}/">{e(rub.lower())}</a></p>'
    else:
        rubro_link = f'<p class="pp-rubro">{e(TIPOS[t])} · sirve para cualquier negocio</p>'
    nota = ("" if p["estado"] == "disponible" else
            '<p class="fine">Todavía no tiene precio publicado. Anotate y te avisamos primero, con precio de lanzamiento.</p>')
    if t == "guia":
        fig = f'<figure class="pp-preview book">{cover(p, "big")}<figcaption>Portada</figcaption></figure>'
    else:
        bar_ico = "sheet" if t == "planilla" else "app"
        fig = (f'<figure class="pp-preview"><div class="win"><div class="win-bar"><div class="dots"><i></i><i></i><i></i></div><div class="url">{ico(bar_ico)}{e(p["nombre"])}</div></div>{media(p, big=True)}</div>'
               f'<figcaption>Vista de ejemplo con datos de muestra</figcaption></figure>')
    rel_html = ("<section class='alt'><div class='w'><h2>Otros productos que te pueden servir</h2><div class='shop'>"
                + "".join(card(q, False) for q in rel) + "</div></div></section>") if rel else ""
    rubro_rel = f'<a href="/para/{p["rubro"]}/">Soluciones para {e(rub.lower())}</a>' if p["rubro"] != "general" else ""
    body = f"""<section class="page-hero pp"><div class="w"><nav class="bc" aria-label="Ruta"><a href="/">Inicio</a> <span>/</span> <a href="/productos-digitales/">Productos digitales</a> <span>/</span> {e(p["nombre"])}</nav>
<div class="pp-info"><h1>{e(p["nombre"])}</h1>{rubro_link}<p class="lead">{e(p["resumen"])}</p>
<div class="pp-buy">{price_line(p)}</div><div class="actions">{ctas(p, "producto-" + p["slug"], big=True)}</div>{nota}</div>
{fig}
</div></section>
<section><div class="w pp-grid"><div><h2>Qué incluye</h2><ul class="ck">{inc}</ul></div>
{idx}<div><h2>Cómo lo recibís</h2><p>{e(p.get("entrega") or ENTREGA[t])}</p></div></div></section>
{rel_html}
<section class="cta"><div class="w"><h2>¿Tenés dudas sobre este producto?</h2><p>Escribinos y te contamos cómo se usa antes de comprarlo.</p><div class="actions"><a class="btn" href="{wa("Hola, tengo una consulta sobre: " + p["nombre"] + " (producto-" + p["slug"] + "-cta)")}" rel="noopener">{ico("chat")}Escribir por WhatsApp</a></div><div class="rel"><a href="/productos-digitales/">Ver todos los productos</a>{rubro_rel}<a href="/#paquetes">Paquetes y precios</a></div></div></section>"""
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Productos digitales", "item": SITE + "/productos-digitales/"},
        {"@type": "ListItem", "position": 3, "name": p["nombre"], "item": SITE + url(p)}]}]
    if p["estado"] == "disponible" and p.get("precio"):
        item = {"@context": "https://schema.org", "@type": {"guia": "Book", "software": "SoftwareApplication"}.get(t, "Product"),
                "name": p["nombre"], "description": p["resumen"],
                "offers": {"@type": "Offer", "price": p["precio"], "priceCurrency": "ARS", "availability": "https://schema.org/InStock", "url": SITE + url(p)}}
        if t == "software":
            item["applicationCategory"] = "BusinessApplication"
        ld.append(item)
    d = PUB / "productos-digitales" / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(f'{p["nombre"]} {TITULO_SUF[t]} | mortups', p["resumen"], url(p), body, ld), encoding="utf-8")

# ---------- portada: sección #productos ----------
home = PUB / "index.html"
s = home.read_text(encoding="utf-8")
dest = [p for p in PRODS if p.get("destacado")][:4]
sec = f"""<section id="productos"><div class="w">
 <div class="sh"><h2>Productos digitales listos para usar</h2><p class="sub">Planillas de Google Sheets y Excel ya armadas, software para tu negocio y guías en PDF para aprender marketing y administración. Vamos sumando uno para cada rubro y actividad.</p></div>
 <div class="shop four">{"".join(card(p, False) for p in dest)}</div>
 <div class="more"><p>{len(PRODS)} productos y sumando.</p><a class="btn l" href="/productos-digitales/">Ver todos los productos</a></div>
</div></section>"""
s = re.sub(r'<section id="productos">.*?</section>', lambda m: sec, s, count=1, flags=re.S)
home.write_text(s, encoding="utf-8")

# ---------- páginas de rubro: sección de su producto ----------
def seccion_rubro(p):
    origen = f'producto-{p["rubro"]}'
    li = "".join(f"<li>{e(x)}</li>" for x in p.get("incluye", []))
    ver = {"planilla": "Ver la planilla", "software": "Ver el software", "guia": "Ver la guía"}[p.get("tipo", "planilla")]
    if p["estado"] == "disponible" and p.get("precio"):
        estado = f'<p><span class="pp-price">{money(p["precio"])}</span> · pago único</p>'
        texto = ("Es un archivo listo para usar en Google Sheets o Excel, sin necesidad de contratar una web. "
                 "Lo pagás una vez y es tuyo; si te trabás, te ayudamos por WhatsApp a dejarlo andando.")
        botones = (f'<a class="btn" href="{wa("Hola, quiero comprar: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">Comprar por WhatsApp</a>'
                   f'<a class="btn l" href="{url(p)}">{ver}</a>')
    else:
        estado = '<p class="status">Producto digital en preparación</p>'
        texto = ("Es un archivo listo para usar en Google Sheets o Excel, sin necesidad de contratar una web. "
                 "Todavía no tiene precio publicado: anotate y te avisamos primero, con precio de lanzamiento.")
        botones = (f'<a class="btn" href="{wa("Hola, quiero anotarme para: " + p["nombre"] + " (" + origen + ")")}" rel="noopener">Anotarme</a>'
                   f'<a class="btn l" href="{url(p)}">{ver}</a>')
    return (f'<section><div class="w"><h2>Para ordenar tu negocio desde hoy: {e(p["nombre"])}</h2>{estado}\n'
            f'<p>{e(p["resumen"])}</p>\n<ul>{li}</ul>\n<p>{texto}</p>\n'
            f'<div class="actions">{botones}</div></div></section>')

for p in PRODS:
    if p["rubro"] == "general":
        continue
    f = PUB / "para" / p["rubro"] / "index.html"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        t = t.replace('href="/productos-digitales/">Ver todos los productos digitales</a>', f'href="{url(p)}">Ver la planilla</a>')
        t = re.sub(r'<section><div class="w"><h2>Para ordenar tu negocio desde hoy:.*?</div></section>',
                   lambda m: seccion_rubro(p), t, count=1, flags=re.S)
        f.write_text(t, encoding="utf-8")

# ---------- sitemap ----------
sm = PUB / "sitemap.xml"
x = sm.read_text(encoding="utf-8")
x = re.sub(r'\s*<url><loc>https://mortups\.com\.ar/productos-digitales/[^<]+/</loc>.*?</url>', "", x)
nuevas = "".join(f"\n  <url><loc>{SITE}{url(p)}</loc><lastmod>{HOY}</lastmod></url>" for p in PRODS)
x = x.replace("\n</urlset>", nuevas + "\n</urlset>")
sm.write_text(x, encoding="utf-8")

print(f"Listo: tienda + {len(PRODS)} páginas de producto + portada + sitemap.")
