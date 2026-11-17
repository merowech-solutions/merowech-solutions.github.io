export const SITE_CONFIG = {
  brandName: "Merowech Solutions",
  domain: "merowech-solutions.de",
  canonicalOrigin: "https://merowech-solutions.de",
  email: "contact@merowech-solutions.de",
  linkedinUrl: "https://www.linkedin.com/in/udo-schlegel/",
  linkedinLabel: "linkedin.com/in/udo-schlegel",
  founder: "Udo Schlegel"
};

export function renderLogoMark(size = 40) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 120 120" fill="none" aria-hidden="true">
    <circle cx="60" cy="60" r="58" fill="#C2410C"/>
    <path d="M 34 52 V 24 L 60 42 L 86 24 V 52" fill="none" stroke="#FFF7ED" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 34 68 V 96 L 60 78 L 86 96 V 68" fill="none" stroke="#2B1A12" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}
