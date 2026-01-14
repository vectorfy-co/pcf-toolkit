(function () {
  const BASE_URL =
    document.querySelector('link[rel="canonical"]')?.getAttribute('href') ||
    "https://vectorfy.co/pcf-toolkit/";
  const THEME_STORAGE_KEY = "pcf-toolkit-theme";
  const THEME_ATTR = "data-theme";

  function titleCase(input) {
    return input
      .replace(/[-_]/g, " ")
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
    const pageTitle = title ? `${title} · ${siteTitle}` : siteTitle;
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

  function createBreadcrumb(routePath) {
    const container = document.createElement("nav");
    container.className = "breadcrumb";

    const list = document.createElement("ol");
    const home = document.createElement("li");
    home.innerHTML = '<a href="#/">Home</a>';
    list.appendChild(home);

    if (routePath && routePath !== "/") {
      const parts = routePath.replace(/^\//, "").split("/");
      let current = "";
      parts.forEach((part) => {
        current += `/${part}`;
        const item = document.createElement("li");
        item.innerHTML = `<a href="#${current}">${titleCase(part)}</a>`;
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
    const crumb = createBreadcrumb(vm.route.path || "/");
    section.prepend(crumb);
  }

  function injectEditLink(vm) {
    const section = document.querySelector(".markdown-section");
    if (!section) return;
    const existing = section.querySelector(".edit-link");
    if (existing) existing.remove();
    const file = vm.route.file || "README.md";
    const url = `https://github.com/vectorfy-co/pcf-toolkit/blob/main/docs/${file}`;
    const wrapper = document.createElement("div");
    wrapper.className = "edit-link";
    wrapper.innerHTML = `<a href="${url}" target="_blank" rel="noopener">Edit this page on GitHub</a>`;
    section.appendChild(wrapper);
  }

  function ensureBackToTop() {
    if (document.querySelector(".back-to-top")) return;
    const btn = document.createElement("button");
    btn.className = "back-to-top";
    btn.type = "button";
    btn.textContent = "Back to top";
    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    document.body.appendChild(btn);

    window.addEventListener("scroll", () => {
      btn.classList.toggle("visible", window.scrollY > 400);
    });
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute(THEME_ATTR, theme);
  }

  function initThemeToggle() {
    const existing = document.querySelector(".theme-toggle");
    if (existing) return;

    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    const initial = stored || (prefersDark.matches ? "dark" : "light");
    applyTheme(initial);

    const button = document.createElement("button");
    button.className = "theme-toggle";
    button.type = "button";
    button.setAttribute("aria-label", "Toggle theme");
    button.innerHTML = `<span class="theme-toggle__icon"></span><span class="theme-toggle__text">${initial === "dark" ? "Dark" : "Light"} mode</span>`;

    button.addEventListener("click", () => {
      const next = document.documentElement.getAttribute(THEME_ATTR) === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem(THEME_STORAGE_KEY, next);
      button.querySelector(".theme-toggle__text").textContent = `${next === "dark" ? "Dark" : "Light"} mode`;
    });

    if (!stored) {
      prefersDark.addEventListener("change", (event) => {
        const current = localStorage.getItem(THEME_STORAGE_KEY);
        if (current) return;
        const next = event.matches ? "dark" : "light";
        applyTheme(next);
        button.querySelector(".theme-toggle__text").textContent = `${next === "dark" ? "Dark" : "Light"} mode`;
      });
    }

    const target = document.querySelector(".sidebar-nav") || document.querySelector(".sidebar");
    if (target) {
      const wrapper = document.createElement("div");
      wrapper.className = "theme-toggle-wrapper";
      wrapper.appendChild(button);
      target.prepend(wrapper);
    }
  }


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

  function initShortcuts() {
    if (window.__pcfToolkitShortcuts) return;
    window.__pcfToolkitShortcuts = true;

    let gPressed = false;
    document.addEventListener("keydown", (event) => {
      if (event.key === "k" && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        const input = document.querySelector(".search input") || document.querySelector("input[type='search']");
        if (input) input.focus();
        return;
      }

      if (event.key.toLowerCase() === "g") {
        gPressed = true;
        setTimeout(() => (gPressed = false), 600);
        return;
      }

      if (gPressed) {
        gPressed = false;
        if (event.key.toLowerCase() === "h") {
          window.location.hash = "#/";
        }
        if (event.key.toLowerCase() === "s") {
          window.location.hash = "#/guide/quickstart";
        }
      }
    });
  }

  window.docsifyCustomPlugins = function (hook, vm) {
    hook.beforeEach(function (markdown) {
      const parsed = parseFrontMatter(markdown);
      vm.frontmatter = parsed.data || {};
      return parsed.body || markdown;
    });

    hook.afterEach(function (html) {
      const title = vm.frontmatter.title;
      const description = vm.frontmatter.description;
      const path = vm.route.path || "/";
      const url = `${BASE_URL}#${path}`;
      updateMeta({ title, description, url });
      return html;
    });

    hook.doneEach(function () {
      injectBreadcrumb(vm);
      injectEditLink(vm);
      ensureBackToTop();
      initThemeToggle();
      initShortcuts();
      initVersionSelect();
    });
  };
})();
