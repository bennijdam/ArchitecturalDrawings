/* Architectural Drawings London — Service Worker
   Cache-first strategy for static assets, network-first for HTML.
   Version bumped to invalidate old caches on deploy.
*/
const VERSION = 'ad-v2';
const STATIC_CACHE = `ad-static-${VERSION}`;
const HTML_CACHE = `ad-html-${VERSION}`;

const PRECACHE = [
  '/',
  '/services.html',
  '/pricing.html',
  '/about.html',
  '/quote.html',
  '/offline.html',
  '/assets/css/style.css',
  '/assets/js/app.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(PRECACHE).catch(() => null))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => !k.endsWith(VERSION)).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // HTML: network-first with cache fallback, offline.html last resort
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(HTML_CACHE).then((cache) => cache.put(request, copy));
          return res;
        })
        .catch(() => caches.match(request).then((cached) => cached || caches.match('/offline.html')))
    );
    return;
  }

  // Static assets (CSS/JS/fonts/images): cache-first
  if (/\.(css|js|woff2?|ttf|otf|svg|png|jpg|jpeg|webp|avif|ico)$/i.test(url.pathname)) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(STATIC_CACHE).then((cache) => cache.put(request, copy));
          }
          return res;
        });
      })
    );
  }
});
