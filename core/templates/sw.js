const CACHE_NAME = 'circlo-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/manifest.json',
  // Add other static assets here
];

// Install event: cache initial assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
  );
});

// Activate event: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      );
    })
  );
});

// Fetch event: Network-first strategy for HTML navigation, Cache-first for static assets
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // For navigation requests (pages), try network, fall back to cache
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
            return caches.match(event.request);
        })
    );
    return;
  }

  // For other requests (images, css, js), try cache, fall back to network
  event.respondWith(
      caches.match(event.request)
        .then(cachedResponse => {
            return cachedResponse || fetch(event.request);
        })
  );
});
