import { renderLogoMark } from "./config.js";

const NAV_I18N = {
  en: {
    homeHref: "/en/",
    skip: "Skip to main content",
    navLabel: "Main navigation",
    menuOpen: "Open navigation menu",
    menuClose: "Close navigation menu",
    themeLabel: "Toggle light or dark color theme",
    langLabel: "Switch website language to German",
    items: [
      { label: "Overview", href: "/en/", match: (p) => p === "/" || p === "/index.html" || p === "/en/" || p === "/en/index.html" },
      { label: "Services", href: "/en/services/machine-learning/", match: (p) => p.startsWith("/en/services/") },
      { label: "Insights", href: "/en/insights/", match: (p) => p.startsWith("/en/insights/") },
      { label: "About", href: "/en/about/", match: (p) => p.startsWith("/en/about/") },
      { label: "Contact", href: "/en/contact/", match: (p) => p.startsWith("/en/contact/") }
    ]
  },
  de: {
    homeHref: "/de/",
    skip: "Zum Hauptinhalt springen",
    navLabel: "Hauptnavigation",
    menuOpen: "Navigationsmenü öffnen",
    menuClose: "Navigationsmenü schließen",
    themeLabel: "Helles oder dunkles Farbschema umschalten",
    langLabel: "Sprache auf Englisch umstellen",
    items: [
      { label: "Übersicht", href: "/de/", match: (p) => p === "/de/" || p === "/de/index.html" },
      { label: "Leistungen", href: "/de/leistungen/machine-learning/", match: (p) => p.startsWith("/de/leistungen/") },
      { label: "Insights", href: "/de/insights/", match: (p) => p.startsWith("/de/insights/") },
      { label: "Über uns", href: "/de/ueber-uns/", match: (p) => p.startsWith("/de/ueber-uns/") },
      { label: "Kontakt", href: "/de/kontakt/", match: (p) => p.startsWith("/de/kontakt/") }
    ]
  }
};

function getEffectiveTheme() {
  const explicit = document.documentElement.getAttribute("data-theme");
  if (explicit === "light" || explicit === "dark") return explicit;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function getAlternateHref(targetLang) {
  const link = document.querySelector(`link[rel="alternate"][hreflang="${targetLang}"]`);
  if (link && link.getAttribute("href")) {
    try {
      const url = new URL(link.getAttribute("href"), window.location.origin);
      return url.pathname;
    } catch (_) {
      return link.getAttribute("href");
    }
  }
  return targetLang === "de" ? "/de/" : "/en/";
}

class SiteHeader extends HTMLElement {
  connectedCallback() {
    const lang = document.documentElement.lang === "de" ? "de" : "en";
    const t = NAV_I18N[lang];
    const path = window.location.pathname;
    const targetLang = lang === "en" ? "de" : "en";
    const altHref = getAlternateHref(targetLang);

    const desktopLinks = t.items
      .map((item) => {
        const active = item.match(path);
        return `<a href="${item.href}" class="nav-link${active ? " is-active" : ""}"${active ? ' aria-current="page"' : ""}>${item.label}</a>`;
      })
      .join("");

    const mobileLinks = t.items
      .map((item) => {
        const active = item.match(path);
        return `<a href="${item.href}" class="${active ? "is-active" : ""}"${active ? ' aria-current="page"' : ""}>${item.label}</a>`;
      })
      .join("");

    this.innerHTML = `
      <a href="#main-content" class="skip-link">${t.skip}</a>
      <header class="site-header">
        <div class="container site-header-inner">
          <a href="${t.homeHref}" class="brand-lockup" aria-label="Merowech Solutions">
            ${renderLogoMark(40)}
            <span class="brand-wordmark">
              <span class="brand-wordmark-top">MEROWECH</span>
              <span class="brand-wordmark-sub">SOLUTIONS</span>
            </span>
          </a>

          <nav class="desktop-nav" aria-label="${t.navLabel}">
            ${desktopLinks}
          </nav>

          <div class="header-controls">
            <a href="${altHref}" class="control-btn" data-lang-switch="${targetLang}" aria-label="${t.langLabel}">
              <span class="${lang === "en" ? "lang-active" : ""}">EN</span>
              <span aria-hidden="true">/</span>
              <span class="${lang === "de" ? "lang-active" : ""}">DE</span>
            </a>

            <button type="button" class="control-btn" data-theme-toggle aria-label="${t.themeLabel}" title="${t.themeLabel}">
              <svg data-icon-sun width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <circle cx="12" cy="12" r="4"></circle>
                <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41m11.32-11.32l1.41-1.41"></path>
              </svg>
              <svg data-icon-moon width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>
            </button>

            <button type="button" class="control-btn mobile-menu-btn" data-menu-open aria-label="${t.menuOpen}" aria-haspopup="dialog">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <dialog class="nav-dialog" aria-label="${t.navLabel}">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <span class="brand-wordmark-top" style="font-size:0.95rem;">MEROWECH</span>
          <button type="button" class="control-btn" data-menu-close aria-label="${t.menuClose}">✕</button>
        </div>
        <nav class="nav-dialog-links" aria-label="${t.navLabel}">
          ${mobileLinks}
        </nav>
      </dialog>
    `;

    this.syncThemeIcons();

    const themeBtn = this.querySelector("[data-theme-toggle]");
    themeBtn?.addEventListener("click", () => {
      const next = getEffectiveTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try {
        localStorage.setItem("mw-theme", next);
      } catch (_) {}
      this.syncThemeIcons();
    });

    const langLink = this.querySelector("[data-lang-switch]");
    langLink?.addEventListener("click", () => {
      try {
        localStorage.setItem("mw-lang", targetLang);
      } catch (_) {}
    });

    const dialog = this.querySelector("dialog");
    const openBtn = this.querySelector("[data-menu-open]");
    const closeBtn = this.querySelector("[data-menu-close]");

    openBtn?.addEventListener("click", () => dialog?.showModal());
    closeBtn?.addEventListener("click", () => dialog?.close());
    dialog?.addEventListener("click", (e) => {
      if (e.target === dialog) dialog.close();
    });
  }

  syncThemeIcons() {
    const isDark = getEffectiveTheme() === "dark";
    const sun = this.querySelector("[data-icon-sun]");
    const moon = this.querySelector("[data-icon-moon]");
    sun?.classList.toggle("hidden", !isDark);
    moon?.classList.toggle("hidden", isDark);
  }
}

if (!customElements.get("site-header")) {
  customElements.define("site-header", SiteHeader);
}
