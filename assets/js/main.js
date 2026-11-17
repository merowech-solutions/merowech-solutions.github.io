import { SITE_CONFIG } from "./config.js";
import "./site-header.js";
import "./site-footer.js";

function initCopyEmailButtons() {
  const isDe = document.documentElement.lang === "de";
  document.querySelectorAll("[data-copy-email]").forEach((btn) => {
    const defaultLabel = btn.textContent.trim();
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(SITE_CONFIG.email);
        btn.textContent = isDe ? "Kopiert ✓" : "Copied ✓";
        setTimeout(() => {
          btn.textContent = defaultLabel;
        }, 1800);
      } catch (_) {
        window.location.href = `mailto:${SITE_CONFIG.email}`;
      }
    });
  });
}

function initInsightsFilter() {
  const buttons = document.querySelectorAll("[data-filter-tag]");
  const items = document.querySelectorAll("[data-post-tags]");
  if (!buttons.length || !items.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const selected = btn.getAttribute("data-filter-tag");
      buttons.forEach((b) => {
        const active = b === btn;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", active ? "true" : "false");
      });

      items.forEach((item) => {
        if (selected === "all") {
          item.classList.remove("hidden");
          return;
        }
        const tags = (item.getAttribute("data-post-tags") || "")
          .split(",")
          .map((s) => s.trim().toLowerCase());
        item.classList.toggle("hidden", !tags.includes(selected.toLowerCase()));
      });
    });
  });
}

function initArticleToc() {
  const tocLinks = Array.from(document.querySelectorAll(".toc-list a[href^='#']"));
  if (!tocLinks.length || !("IntersectionObserver" in window)) return;

  const targets = tocLinks
    .map((link) => document.getElementById(link.getAttribute("href").slice(1)))
    .filter(Boolean);

  if (!targets.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = entry.target.id;
        tocLinks.forEach((l) => {
          l.classList.toggle("is-active", l.getAttribute("href") === `#${id}`);
        });
      });
    },
    { rootMargin: "-15% 0px -72% 0px", threshold: 0 }
  );

  targets.forEach((t) => observer.observe(t));
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    initCopyEmailButtons();
    initInsightsFilter();
    initArticleToc();
  });
} else {
  initCopyEmailButtons();
  initInsightsFilter();
  initArticleToc();
}
