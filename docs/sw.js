// Cloudflare Pages already provides strong caching at the edge.
// This Service Worker is intentionally conservative to avoid "stale docs" after deployments.
const CACHE_NAME = "pcf-toolkit-docs-v3";
const PRECACHE_URLS = [
  "./",
  "index.html",
  "_sidebar.md",
  "_navbar.md",
  "_coverpage.md",
  "README.md",
  "guide/getting-started.md",
  "guide/quickstart.md",
  "guide/installation.md",
  "guide/first-proxy.md",
  "guide/architecture.md",
  "cli/overview.md",
  "cli/commands.md",
  "manifest/overview.md",
  "manifest/control.md",
  "manifest/properties.md",
  "manifest/property-sets.md",
  "manifest/resources.md",
  "manifest/datasets.md",
  "manifest/events.md",
  "manifest/dependencies.md",
  "manifest/type-groups.md",
  "manifest/property-dependencies.md",
  "manifest/feature-usage.md",
  "manifest/external-services.md",
  "manifest/platform-action.md",
  "manifest/full-example.md",
  "proxy/overview.md",
  "proxy/configuration.md",
  "proxy/workflow.md",
  "proxy/doctor.md",
  "proxy/troubleshooting.md",
  "integrations/pac-cli.md",
  "integrations/ci-cd.md",
  "integrations/editor.md",
  "api/python.md",
  "advanced/best-practices.md",
  "advanced/performance.md",
  "advanced/security.md",
  "advanced/troubleshooting.md",
  "advanced/faq.md",
  "project/contributing.md",
  "project/changelog.md",
  "project/roadmap.md",
  "project/license.md",
  "meta/keyboard-shortcuts.md",
  "meta/accessibility.md",
  "meta/glossary.md",
  "assets/css/theme.css",
  "assets/js/docsify-plugins.js",
  "assets/img/vectorfy-logo.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      // Be resilient: one missing file should not prevent SW installation.
      await Promise.all(
        PRECACHE_URLS.map(async (url) => {
          try {
            await cache.add(url);
          } catch (_) {
            // ignore individual precache failures
          }
        })
      );
      await self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);

  // Don't try to cache cross-origin requests (e.g. jsdelivr). It can quickly bloat caches.
  if (url.origin !== self.location.origin) return;

  const accept = event.request.headers.get("Accept") || "";
  const isNavigation =
    event.request.mode === "navigate" ||
    (accept.includes("text/html") && !url.pathname.match(/\.(css|js|png|jpg|jpeg|gif|svg|webp|ico|map|json|txt)$/i));

  const isMarkdown = url.pathname.endsWith(".md");

  // Navigations + markdown are network-first so new deploys show up immediately.
  if (isNavigation || isMarkdown) {
    event.respondWith(
      (async () => {
        try {
          const response = await fetch(event.request);
          const cache = await caches.open(CACHE_NAME);
          cache.put(event.request, response.clone());
          return response;
        } catch (_) {
          const cached = await caches.match(event.request);
          if (cached) return cached;
          // Fallback to app shell only for HTML navigations
          if (isNavigation) return (await caches.match("index.html")) || (await caches.match("./"));
          throw _;
        }
      })()
    );
    return;
  }

  // Static assets: cache-first with background refresh.
  event.respondWith(
    (async () => {
      const cached = await caches.match(event.request);
      const fetchAndCache = (async () => {
        const response = await fetch(event.request);
        const cache = await caches.open(CACHE_NAME);
        cache.put(event.request, response.clone());
        return response;
      })();

      if (cached) {
        event.waitUntil(fetchAndCache.catch(() => {}));
        return cached;
      }
      return fetchAndCache;
    })()
  );
});
