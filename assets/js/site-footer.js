import { SITE_CONFIG, renderLogoMark } from "./config.js";

const FOOTER_I18N = {
  en: {
    tagline: "Engineering-first consulting for Data Science, Machine Learning, and Explainable AI (XAI).",
    colPractice: "Practice Areas",
    colCompany: "Organization & Legal",
    practiceLinks: [
      { label: "01 · Machine Learning & Data Science", href: "/en/services/machine-learning/" },
      { label: "02 · Explainable AI (XAI) & Auditing", href: "/en/services/explainable-ai/" },
      { label: "03 · AI & Data Strategy", href: "/en/services/ai-strategy/" },
      { label: "04 · LLM / GenAI & Verifiable RAG", href: "/en/services/genai-systems/" }
    ],
    companyLinks: [
      { label: "About Us", href: "/en/about/" },
      { label: "Insights & Publications", href: "/en/insights/" },
      { label: "Contact", href: "/en/contact/" },
      { label: "RSS Feed", href: "/en/insights/rss.xml" },
      { label: "Imprint (Impressum)", href: "/en/imprint/" },
      { label: "Privacy Policy", href: "/en/privacy/" }
    ],
    badge: "Zero Cookies · Self-Hosted Fonts · GDPR-Clean"
  },
  de: {
    tagline: "Engineering-orientierte Beratung für Data Science, Machine Learning und Explainable AI (XAI).",
    colPractice: "Leistungsbereiche",
    colCompany: "Unternehmen & Rechtliches",
    practiceLinks: [
      { label: "01 · Machine Learning & Data Science", href: "/de/leistungen/machine-learning/" },
      { label: "02 · Explainable AI (XAI) & Audits", href: "/de/leistungen/explainable-ai/" },
      { label: "03 · KI- & Datenstrategie", href: "/de/leistungen/ki-strategie/" },
      { label: "04 · LLM / GenAI & Nachvollziehbares RAG", href: "/de/leistungen/genai-systeme/" }
    ],
    companyLinks: [
      { label: "Über uns", href: "/de/ueber-uns/" },
      { label: "Insights & Fachbeiträge", href: "/de/insights/" },
      { label: "Kontakt", href: "/de/kontakt/" },
      { label: "RSS-Feed", href: "/de/insights/rss.xml" },
      { label: "Impressum", href: "/de/impressum/" },
      { label: "Datenschutzerklärung", href: "/de/datenschutz/" }
    ],
    badge: "Ohne Cookies · Lokal gehostet · DSGVO-konform"
  }
};

class SiteFooter extends HTMLElement {
  connectedCallback() {
    const lang = document.documentElement.lang === "de" ? "de" : "en";
    const t = FOOTER_I18N[lang];
    const year = new Date().getFullYear();

    this.innerHTML = `
      <footer class="site-footer">
        <div class="container">
          <div class="footer-grid">
            <div>
              <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.9rem;">
                ${renderLogoMark(32)}
                <div class="brand-wordmark">
                  <span class="brand-wordmark-top" style="font-size:0.95rem;">MEROWECH</span>
                  <span class="brand-wordmark-sub" style="font-size:0.55rem;">SOLUTIONS</span>
                </div>
              </div>
              <p style="max-width:38ch;line-height:1.6;margin-bottom:1rem;">${t.tagline}</p>
              <div class="font-mono" style="display:flex;flex-direction:column;gap:0.35rem;">
                <a href="mailto:${SITE_CONFIG.email}" class="text-accent">${SITE_CONFIG.email}</a>
                <a href="${SITE_CONFIG.linkedinUrl}" target="_blank" rel="noopener noreferrer">${SITE_CONFIG.linkedinLabel} ↗</a>
              </div>
            </div>

            <div>
              <div class="footer-col-title">${t.colPractice}</div>
              <ul class="footer-links">
                ${t.practiceLinks.map((l) => `<li><a href="${l.href}">${l.label}</a></li>`).join("")}
              </ul>
            </div>

            <div>
              <div class="footer-col-title">${t.colCompany}</div>
              <ul class="footer-links">
                ${t.companyLinks.map((l) => `<li><a href="${l.href}">${l.label}</a></li>`).join("")}
              </ul>
            </div>
          </div>

          <div class="footer-bottom">
            <span>© ${year} ${SITE_CONFIG.brandName} · ${SITE_CONFIG.domain}</span>
            <span class="privacy-badge">${t.badge}</span>
          </div>
        </div>
      </footer>
    `;
  }
}

if (!customElements.get("site-footer")) {
  customElements.define("site-footer", SiteFooter);
}
