# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dueños y encargados de comercios y pymes de Argentina (ferreterías, repuestos, gastronomía, indumentaria, barberías, kioscos, talleres, gimnasios, clínicas, distribuidoras) que hoy reciben consultas y pedidos por WhatsApp y quieren vender más sin plataformas que cobren comisión. Llegan por varios caminos a la vez: anuncios de Meta/TikTok en el celular, búsquedas en Google ("catálogo web", "menú QR") y recomendaciones o contactos directos. Deciden si escribir por WhatsApp.

Audiencia secundaria (página /sobre-mi/): empleadores que evalúan a Lautaro como Administrador de Marketing Digital o Desarrollador de Software.

## Product Purpose

mortups es el emprendimiento de Lautaro Mortarotti (Mendoza): diseño web y marketing online para que un negocio reciba pedidos ordenados por WhatsApp. Vende catálogos web, menús digitales con QR, sistemas de registro de ventas (POS), campañas en Meta/Google/TikTok y planillas digitales. El éxito es que el visitante escriba por WhatsApp pidiendo su demo o asesoramiento.

## Positioning

Primero la demo funcionando con los productos del propio negocio (24–72 h, sin pagar), después la charla. Sin comisiones por venta, sin contratos de permanencia, precios publicados. El pedido llega al WhatsApp del dueño ya armado (productos, cantidades, total). Puede sincronizar catálogos enormes (~30.000 productos) desde el sistema de gestión del negocio. Lo hace una sola persona, de punta a punta, y el propio sitio es su caso de medición.

## Operating Context

- La venta se cierra en WhatsApp, no en el sitio. Cada botón de WhatsApp agrega un código `Ref` al mensaje para atribuir la venta.
- Pago: demo sin costo; 50% para empezar, 50% al publicar; 2 rondas de ajustes. Mensual opcional de hosting y soporte, ajustado trimestralmente por IPC, con baja sin penalización.
- Atención por WhatsApp +54 9 2634 279451: lunes a miércoles 15–20 h, jueves y viernes 9–20 h.

## Capabilities and Constraints

- Sitio estático en Cloudflare Workers + Static Assets, HTML/CSS/JS a mano, sin framework, sin build y sin dependencias. Peso total objetivo < 0,5 MB.
- CSP estricta en `public/_headers`: scripts solo propios + GTM, Meta y TikTok; estilos propios o inline; sin fuentes ni imágenes de terceros (salvo los dominios de medición). Cualquier fuente web debe autoalojarse.
- `track.js` maneja consentimiento y eventos (no se carga medición antes de aceptar); `demo.js` maneja la demo interactiva de la portada. Los botones de WhatsApp y el banner de cookies dependen de ellos y deben seguir funcionando.
- Páginas: home, /para/ (índice + 10 rubros), /catalogo-web/, /menu-digital-qr/, /productos-digitales/, /casos/ (2), /sobre-mi/, legales (términos, privacidad, cookies) y 404. SEO: JSON-LD, sitemap, llms.txt, Open Graph.
- Legales argentinos obligatorios: botones de arrepentimiento y de baja visibles en todas las páginas, datos del responsable en el pie.

## Brand Commitments

- Nombre y logotipo "mortups" (wordmark) se mantienen.
- El violeta de marca (#8B2CFF) se mantiene como color de marca.
- Pedido explícito del dueño: que no parezca un sitio "moderno genérico hecho con IA" (nada de gradientes violeta brillantes, glows, emojis como íconos, etiquetas en mayúsculas espaciadas).
- Dirección visual elegida por el dueño (nov 2026): el estándar de la categoría (sitio de agencia/SaaS claro y convencional), ejecutado con oficio. Referencias de calidad elegidas por Claude por delegación del dueño: Tiendanube y Mercado Pago (cercanía con el comerciante argentino) y Stripe (terminación).
- Voz: español rioplatense, tuteo con voseo ("contanos", "elegí"), directa y concreta.

## Evidence on Hand

- Casos reales online: Todo y Más (tienda, 236 productos, Mercado Pago y Go Cuotas, panel de ventas) y Repuestos San Isidro (~30.000 productos sincronizados). Capturas en `public/img/` (todoymas.webp, panel-todoymas.webp, repuestos.webp) y og.jpg.
- Precios publicados (noviembre 2026): Presencia $120.000 pago único; Web $200.000 + $30.000/mes; Ventas $550.000 + $60.000/mes (lanzamiento $450.000 para los primeros 3 clientes hasta el 31/12/2026); Crecimiento a consultar.
- No hay testimonios de clientes todavía: no inventar testimonios, logos de clientes ni métricas.

## Product Principles

1. Mostrar antes que prometer: la demo y los casos reales valen más que cualquier adjetivo.
2. Todo termina en WhatsApp: cada página tiene un camino claro a escribir.
3. Precios y condiciones a la vista, sin letra chica.
4. Liviano y rápido en un celular de gama media con datos móviles.
5. Hablarle a un comerciante, no a un desarrollador.

## Accessibility & Inclusion

Público mayormente en celular, con niveles variados de familiaridad con la tecnología: texto legible en pantallas chicas, contraste AA, objetivos táctiles amplios, sin depender de animaciones.
