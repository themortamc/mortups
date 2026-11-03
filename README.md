# mortups

Sitio estático de mortups, listo para Cloudflare Workers (static assets). Sin build ni dependencias.

```
public/            sitio (index, terminos/, privacidad/, cookies/, img/, 404.html)
wrangler.jsonc     configuración de Cloudflare
```

## Antes de publicar

Completa los datos marcados con `[COMPLETAR]` (CUIT, domicilio y horario de atención):

```
grep -rn "COMPLETAR" public
```

## Probar en local

```
npx wrangler dev
```

## Subir a GitHub

```
git init
git add .
git commit -m "Sitio de mortups"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mortups.git
git push -u origin main
```

## Deploy en Cloudflare

**Opción A, desde GitHub:** Cloudflare → Workers & Pages → Create → Import a repository. Elige el repo, deja el build command vacío y usa `npx wrangler deploy` como deploy command. Cada push a `main` publica solo.

**Opción B, desde la terminal:**

```
npx wrangler login
npx wrangler deploy
```

Para dominio propio: Workers & Pages → mortups → Settings → Domains & Routes.

## Mantenimiento legal

- Botón de arrepentimiento y de baja (Disposición 954/2025): al recibir una solicitud por WhatsApp, responde dentro de las 24 horas con un código de registro.
- Si agregas analítica o píxeles (Meta, TikTok, Google), actualiza `public/cookies/index.html` y agrega un aviso de consentimiento antes de activarlos.

## Medición (Google, Meta, TikTok)

1. En `public/track.js` completá `C` con los IDs públicos (GA4 `G-…`, Ads `AW-…` y etiqueta de conversión, Meta, TikTok). Sin IDs no se carga nada ni aparece el banner.
2. Server-side (Meta y TikTok): poné los IDs de píxel en `wrangler.jsonc` (`vars`) y los tokens como secretos:
   `npx wrangler secret put META_TOKEN` y `npx wrangler secret put TIKTOK_TOKEN`. Para probar, `META_TEST_CODE` / `TIKTOK_TEST_CODE`.
3. Verificá en Events Manager (Meta), Events Manager (TikTok) y GA4 DebugView que el `event_id` llega por navegador y servidor (se deduplica).
4. Cuando tengas el dominio: `grep -rl mortups.lautaby12.workers.dev public | xargs sed -i 's#mortups.lautaby12.workers.dev#TUDOMINIO.com.ar#g'`
5. Ventas cerradas: cada clic agrega “Ref: XXXXXX” al mensaje de WhatsApp; anotalo en tu registro de ventas para subir conversiones offline a Google/Meta/TikTok.
