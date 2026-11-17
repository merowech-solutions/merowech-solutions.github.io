(function () {
  try {
    var savedTheme = localStorage.getItem("mw-theme");
    if (savedTheme === "light" || savedTheme === "dark") {
      document.documentElement.setAttribute("data-theme", savedTheme);
    }
    if (document.documentElement.hasAttribute("data-root-entry")) {
      var savedLang = localStorage.getItem("mw-lang");
      if (savedLang === "de") {
        window.location.replace("/de/");
      }
    }
  } catch (_) {
    /* Storage unavailable — fall back cleanly to CSS prefers-color-scheme */
  }
})();
