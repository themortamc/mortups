---
version: 1
slug: "public-index-html"
primary_target: "public/index.html"
related_targets: ["public/para/index.html"]
---

# Surface brief: sitio mortups (home + páginas internas)

Scope: todo el sitio público (home, /para/ y rubros, catálogo web, menú QR, productos digitales, casos, sobre mí, legales, 404). Mode: Persuade (legales y sobre-mí: Read).

Audiencia: dueños de comercios y pymes de Argentina, mayormente en celular, que llegan por anuncios, Google o recomendación. Acción: escribir por WhatsApp para pedir la demo o asesoramiento. Prueba: demo interactiva, precios publicados, casos reales (Todo y Más, Repuestos San Isidro). Restricciones: estático, sin build, CSP propia (fuentes autoalojadas), track.js/demo.js funcionando, botones legales visibles.

## Direction contract

THESIS: El estándar de la categoría (agencia/SaaS claro) hecho con oficio de nivel Stripe y cercanía de Tiendanube/Mercado Pago: el producto se demuestra, no se adorna. Rechaza el look oscuro con glows, emojis y violeta brillante del sitio anterior.

OWN-WORLD: Fondo blanco y gris muy claro apenas tintado a violeta; tinta casi negra; el violeta #8B2CFF solo en el botón principal, el logo, la selección y una cifra clave. Filetes de 1 px, radios 10–16, sombras neutras chicas solo en capturas y mockups. Hanken Grotesk autoalojada (reemplazó a Geist por ser una fuente sobreusada en sitios generados), 400/500/600, cifras tabulares. Íconos de línea propios en un solo trazo. Cierre de cada página en una banda tinta (#17141F) con el botón violeta: único bloque oscuro, como ancla final. Verde WhatsApp solo en el globo del pedido.

STORY: El visitante entiende en una pantalla qué hace mortups (catálogo/menú con pedido armado en WhatsApp), cree porque ve un pedido armándose, precios a la vista y dos sitios reales online, y escribe por WhatsApp.

FIRST VIEWPORT: Izquierda: titular (≈56–60px), bajada, botón violeta "Pedir asesoramiento gratis" (CTA original del sitio) y botón secundario a la demo; debajo cuatro datos verificables en grilla 2×2. Derecha (≈50% del ancho): ventana de navegador con la captura real del catálogo de Todo y Más (la única evidencia real disponible es una captura de escritorio; un teléfono implicaría inventar una vista) y, montado sobre su borde, el mensaje de WhatsApp con un pedido de productos de ese catálogo, marcado como ejemplo. En celular: texto, botones y luego la captura recortada a la esquina superior izquierda para que se lea.

FORM: canon (salida estándar elegida por el usuario en la segunda tirada); seed:8e0dda687fb27a6b. Interacción firma: la demo interactiva por rubro donde sumar productos arma el mensaje en vivo. Movimiento: una sola entrada suave del hero; transiciones cortas de color y transform.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
