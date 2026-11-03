// Eventos server-side (Meta Conversions API + TikTok Events API). Solo atiende /api/track.
// Variables: META_PIXEL_ID, TIKTOK_PIXEL_ID (vars) · META_TOKEN, TIKTOK_TOKEN (secretos) · META_TEST_CODE, TIKTOK_TEST_CODE (opcionales, para pruebas)
const GRAPH = 'v23.0';
const J = { 'content-type': 'application/json' };
const s = (v, n) => String(v || '').slice(0, n);

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    if (u.pathname !== '/api/track') return new Response('Not found', { status: 404 });
    if (req.method !== 'POST') return new Response(null, { status: 405 });
    const o = req.headers.get('origin');
    if (o && o !== u.origin) return new Response(null, { status: 403 });
    let b;
    try { b = await req.json(); } catch { return new Response(null, { status: 400 }); }
    if (!b || typeof b.event_id !== 'string' || b.event_id.length > 64) return new Response(null, { status: 400 });

    const ip = req.headers.get('cf-connecting-ip') || '';
    const ua = req.headers.get('user-agent') || '';
    const t = Math.floor(Date.now() / 1000);
    const url = s(b.url, 300);
    const jobs = [];

    if (env.META_PIXEL_ID && env.META_TOKEN) {
      jobs.push(fetch(`https://graph.facebook.com/${GRAPH}/${env.META_PIXEL_ID}/events`, {
        method: 'POST', headers: J,
        body: JSON.stringify({
          access_token: env.META_TOKEN,
          ...(env.META_TEST_CODE ? { test_event_code: env.META_TEST_CODE } : {}),
          data: [{
            event_name: 'Lead', event_time: t, event_id: b.event_id, action_source: 'website', event_source_url: url,
            user_data: { client_ip_address: ip, client_user_agent: ua, fbp: s(b.fbp, 100) || undefined, fbc: s(b.fbc, 200) || undefined },
            custom_data: { content_name: s(b.name, 60), ref: s(b.ref, 12) }
          }]
        })
      }));
    }
    if (env.TIKTOK_PIXEL_ID && env.TIKTOK_TOKEN) {
      jobs.push(fetch('https://business-api.tiktok.com/open_api/v1.3/event/track/', {
        method: 'POST', headers: { ...J, 'Access-Token': env.TIKTOK_TOKEN },
        body: JSON.stringify({
          event_source: 'web', event_source_id: env.TIKTOK_PIXEL_ID,
          ...(env.TIKTOK_TEST_CODE ? { test_event_code: env.TIKTOK_TEST_CODE } : {}),
          data: [{
            event: 'Contact', event_time: t, event_id: b.event_id,
            user: { ip, user_agent: ua, ttp: s(b.ttp, 100) || undefined, ttclid: s(b.ttclid, 200) || undefined },
            page: { url }, properties: { content_name: s(b.name, 60) }
          }]
        })
      }));
    }
    ctx.waitUntil(Promise.allSettled(jobs));
    return new Response(null, { status: 204 });
  }
};
