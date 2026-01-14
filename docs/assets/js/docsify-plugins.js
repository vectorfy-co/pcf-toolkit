(function () {
  "use strict";

  // =========================================================================
  // Configuration
  // =========================================================================

  // Compute the base URL dynamically from the current location.
  // This avoids hard-coding production URLs, which can break Cloudflare Pages preview deployments.
  // Example: https://<project>.pages.dev/ -> base "https://<project>.pages.dev/"
  // Example: https://example.com/pcf-toolkit/ -> base "https://example.com/pcf-toolkit/"
  const BASE_URL = (function () {
    try {
      const url = new URL(window.location.href);
      url.hash = "";
      url.search = "";
      // Ensure we end with a trailing slash representing the "site root" for this deployment.
      url.pathname = url.pathname.endsWith("/") ? url.pathname : url.pathname.replace(/\/[^/]*$/, "/");
      return url.toString();
    } catch (_) {
      return "/";
    }
  })();
  const THEME_STORAGE_KEY = "pcf-toolkit-theme";
  const THEME_ATTR = "data-theme";

  // =========================================================================
  // Utility Functions
  // =========================================================================

  function titleCase(input) {
    return input
      .replace(/[-_]/g, " ")
      .replace(/\.md$/i, "")
      .replace(/\b\w/g, (match) => match.toUpperCase());
  }

  function parseFrontMatter(markdown) {
    const match = markdown.match(/^---\n([\s\S]*?)\n---/);
    if (!match) {
      return { body: markdown, data: {} };
    }
    const frontMatter = match[1];
    const data = {};
    frontMatter.split("\n").forEach((line) => {
      const idx = line.indexOf(":");
      if (idx === -1) return;
      const key = line.slice(0, idx).trim();
      const value = line.slice(idx + 1).trim();
      if (key) data[key] = value.replace(/^"|"$/g, "");
    });
    return { body: markdown.replace(match[0], "").trim(), data };
  }

  function setMeta(name, content) {
    const element = document.querySelector(`meta[name="${name}"]`);
    if (element) element.setAttribute("content", content);
  }

  function setPropertyMeta(property, content) {
    const element = document.querySelector(`meta[property="${property}"]`);
    if (element) element.setAttribute("content", content);
  }

  function updateMeta({ title, description, url }) {
    const siteTitle = "PCF Toolkit";
    const pageTitle = title ? `${title} - ${siteTitle}` : siteTitle;
    document.title = pageTitle;
    if (description) {
      setMeta("description", description);
      setPropertyMeta("og:description", description);
      setMeta("twitter:description", description);
    }
    setPropertyMeta("og:title", pageTitle);
    setMeta("twitter:title", pageTitle);
    if (url) {
      setPropertyMeta("og:url", url);
      const canonical = document.querySelector('link[rel="canonical"]');
      if (canonical) canonical.setAttribute("href", url);
    }
  }

  // =========================================================================
  // Breadcrumb Component
  // =========================================================================

  function createBreadcrumb(routePath) {
    const container = document.createElement("nav");
    container.className = "breadcrumb";
    container.setAttribute("aria-label", "Breadcrumb");

    const list = document.createElement("ol");
    const home = document.createElement("li");
    home.innerHTML = '<a href="#/">Home</a>';
    list.appendChild(home);

    if (routePath && routePath !== "/") {
      const parts = routePath
        .replace(/^\//, "")
        .replace(/\.md$/i, "")
        .split("/");
      let current = "";
      parts.forEach((part, index) => {
        current += `/${part}`;
        const item = document.createElement("li");
        const isLast = index === parts.length - 1;
        if (isLast) {
          item.innerHTML = `<span aria-current="page">${titleCase(part)}</span>`;
        } else {
          item.innerHTML = `<a href="#${current}">${titleCase(part)}</a>`;
        }
        list.appendChild(item);
      });
    }

    container.appendChild(list);
    return container;
  }

  function injectBreadcrumb(vm) {
    const section = document.querySelector(".markdown-section");
    if (!section) return;
    const existing = section.querySelector(".breadcrumb");
    if (existing) existing.remove();

    // Don't show breadcrumb on home page
    const path = vm.route.path || "/";
    if (path === "/" || path === "/README") return;

    const crumb = createBreadcrumb(path);
    section.prepend(crumb);
  }

  // =========================================================================
  // Edit Link Component
  // =========================================================================

  function injectEditLink(vm) {
    const section = document.querySelector(".markdown-section");
    if (!section) return;
    const existing = section.querySelector(".edit-link");
    if (existing) existing.remove();

    const file = vm.route.file || "README.md";
    const url = `https://github.com/vectorfy-co/pcf-toolkit/blob/main/docs/${file}`;
    const wrapper = document.createElement("div");
    wrapper.className = "edit-link";
    wrapper.innerHTML = `<a href="${url}" target="_blank" rel="noopener noreferrer">Edit this page on GitHub</a>`;
    section.appendChild(wrapper);
  }

  // =========================================================================
  // Back to Top Button
  // =========================================================================

  function ensureBackToTop() {
    if (document.querySelector(".back-to-top")) return;

    const btn = document.createElement("button");
    btn.className = "back-to-top";
    btn.type = "button";
    btn.setAttribute("aria-label", "Scroll back to top");
    btn.setAttribute("title", "Back to top");

    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    document.body.appendChild(btn);

    // Throttled scroll handler
    let ticking = false;
    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            btn.classList.toggle("visible", window.scrollY > 300);
            ticking = false;
          });
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  // =========================================================================
  // Theme Toggle
  // =========================================================================

  function applyTheme(theme) {
    document.documentElement.setAttribute(THEME_ATTR, theme);
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute("content", theme === "dark" ? "#0C0F1A" : "#4F46E5");
    }
  }

  function getThemeIcon(theme) {
    if (theme === "dark") {
      return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>`;
    }
    return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="5"/>
      <line x1="12" y1="1" x2="12" y2="3"/>
      <line x1="12" y1="21" x2="12" y2="23"/>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
      <line x1="1" y1="12" x2="3" y2="12"/>
      <line x1="21" y1="12" x2="23" y2="12"/>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>`;
  }

  function initThemeToggle() {
    const existing = document.querySelector(".theme-toggle");
    const appNav = document.querySelector(".app-nav");
    if (existing) {
      if (appNav && !appNav.contains(existing)) {
        let actions = appNav.querySelector(".app-nav-actions");
        if (!actions) {
          actions = document.createElement("div");
          actions.className = "app-nav-actions";
          appNav.appendChild(actions);
        }
        actions.appendChild(existing);
        const wrapper = existing.closest(".theme-toggle-wrapper");
        if (wrapper) wrapper.remove();
      }
      return;
    }

    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    const initial = stored || (prefersDark.matches ? "dark" : "light");
    applyTheme(initial);

    const button = document.createElement("button");
    button.className = "theme-toggle";
    button.type = "button";
    button.setAttribute("aria-label", "Toggle color theme");
    button.setAttribute("title", `Switch to ${initial === "dark" ? "light" : "dark"} mode`);

    function updateButton(theme) {
      button.innerHTML = `
        <span class="theme-toggle__icon">${getThemeIcon(theme)}</span>
        <span class="theme-toggle__text">${theme === "dark" ? "Dark" : "Light"}</span>
      `;
      button.setAttribute("title", `Switch to ${theme === "dark" ? "light" : "dark"} mode`);
    }

    updateButton(initial);

    button.addEventListener("click", () => {
      const current = document.documentElement.getAttribute(THEME_ATTR);
      const next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem(THEME_STORAGE_KEY, next);
      updateButton(next);
    });

    // Listen for system theme changes if no stored preference
    if (!stored) {
      prefersDark.addEventListener("change", (event) => {
        const currentStored = localStorage.getItem(THEME_STORAGE_KEY);
        if (currentStored) return; // User has manual preference
        const next = event.matches ? "dark" : "light";
        applyTheme(next);
        updateButton(next);
      });
    }

    // Find the best place to insert the toggle
    if (appNav) {
      let actions = appNav.querySelector(".app-nav-actions");
      if (!actions) {
        actions = document.createElement("div");
        actions.className = "app-nav-actions";
        appNav.appendChild(actions);
      }
      actions.appendChild(button);
      return;
    }

    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
      const wrapper = document.createElement("div");
      wrapper.className = "theme-toggle-wrapper";
      wrapper.appendChild(button);

      // Insert after search
      const search = sidebar.querySelector(".search");
      if (search) {
        search.after(wrapper);
      } else {
        sidebar.appendChild(wrapper);
      }
    }
  }

  // =========================================================================
  // Service Worker Registration
  // =========================================================================

  function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    const isLocalhost =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1";
    if (isLocalhost) {
      navigator.serviceWorker.getRegistrations().then((registrations) => {
        registrations.forEach((registration) => registration.unregister());
      });
      return;
    }
    if (window.__pcfToolkitSw) return;
    window.__pcfToolkitSw = true;

    navigator.serviceWorker.register("sw.js", { scope: "./" }).catch((err) => {
      console.warn("Service worker registration failed:", err);
    });
  }

  // =========================================================================
  // Version Selector
  // =========================================================================

  function initVersionSelect() {
    const select = document.getElementById("version-select");
    if (!select || select.dataset.bound) return;
    select.dataset.bound = "true";

    select.addEventListener("change", (event) => {
      const value = event.target.value;
      if (!value) return;
      window.location.href = value;
    });
  }

  // =========================================================================
  // Keyboard Shortcuts
  // =========================================================================

  function initShortcuts() {
    if (window.__pcfToolkitShortcuts) return;
    window.__pcfToolkitShortcuts = true;

    let gPressed = false;
    let gTimeout = null;

    document.addEventListener("keydown", (event) => {
      // Ignore if user is typing in an input
      const activeElement = document.activeElement;
      const isInput =
        activeElement &&
        (activeElement.tagName === "INPUT" ||
          activeElement.tagName === "TEXTAREA" ||
          activeElement.isContentEditable);
      if (isInput) return;

      // Cmd/Ctrl + K for search
      if (event.key === "k" && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        const input =
          document.querySelector(".search input") ||
          document.querySelector('input[type="search"]');
        if (input) {
          input.focus();
          input.select();
        }
        return;
      }

      // Theme toggle with T
      if (event.key.toLowerCase() === "t" && !event.metaKey && !event.ctrlKey) {
        const toggle = document.querySelector(".theme-toggle");
        if (toggle) toggle.click();
        return;
      }

      // G + key shortcuts
      if (event.key.toLowerCase() === "g") {
        gPressed = true;
        if (gTimeout) clearTimeout(gTimeout);
        gTimeout = setTimeout(() => {
          gPressed = false;
        }, 600);
        return;
      }

      if (gPressed) {
        gPressed = false;
        if (gTimeout) clearTimeout(gTimeout);

        switch (event.key.toLowerCase()) {
          case "h":
            window.location.hash = "#/";
            break;
          case "s":
            window.location.hash = "#/guide/quickstart";
            break;
          case "m":
            window.location.hash = "#/manifest/overview";
            break;
          case "p":
            window.location.hash = "#/proxy/overview";
            break;
        }
      }
    });
  }

  // =========================================================================
  // Smooth Page Transitions
  // =========================================================================

  function initPageTransitions() {
    // Add a subtle fade when navigating between pages
    const content = document.querySelector(".content");
    if (!content) return;

    window.addEventListener("hashchange", () => {
      const section = document.querySelector(".markdown-section");
      if (section) {
        section.style.animation = "none";
        requestAnimationFrame(() => {
          section.style.animation = "";
        });
      }
    });
  }

  // =========================================================================
  // External Link Icons
  // =========================================================================

  function addExternalLinkIcons() {
    const section = document.querySelector(".markdown-section");
    if (!section) return;

    const links = section.querySelectorAll('a[target="_blank"]');
    links.forEach((link) => {
      if (link.querySelector(".external-icon")) return;
      const icon = document.createElement("span");
      icon.className = "external-icon";
      icon.innerHTML = " ↗";
      icon.style.fontSize = "0.8em";
      icon.style.opacity = "0.6";
      link.appendChild(icon);
    });
  }

  // =========================================================================
  // Main Plugin Export
  // =========================================================================

  window.docsifyCustomPlugins = function (hook, vm) {
    // Before each page render
    hook.beforeEach(function (markdown) {
      const parsed = parseFrontMatter(markdown);
      vm.frontmatter = parsed.data || {};
      return parsed.body || markdown;
    });

    // After each page render (before DOM insert)
    hook.afterEach(function (html) {
      const title = vm.frontmatter.title;
      const description = vm.frontmatter.description;
      // In hash router mode, treat the deployment root as canonical.
      // (Hash fragments are client-side state and typically shouldn't be used as canonical URLs.)
      const url = BASE_URL;
      updateMeta({ title, description, url });
      return html;
    });

    // After each page is fully rendered
    hook.doneEach(function () {
      injectBreadcrumb(vm);
      injectEditLink(vm);
      ensureBackToTop();
      initThemeToggle();
      initShortcuts();
      initVersionSelect();
      addExternalLinkIcons();
    });

    // After initial load
    hook.ready(function () {
      registerServiceWorker();
      initPageTransitions();
    });
  };
})();
