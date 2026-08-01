const languageNames = {
  arem: "AREM",
  en: "EN",
  vela: "VELA",
};

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

const displayFolio = (id) => String(id).replace(/^RP-/, "");

async function loadArchive() {
  const container = document.querySelector("#generated-list");
  if (!container) return;

  try {
    const response = await fetch("archive.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`archive request failed: ${response.status}`);

    const entries = await response.json();
    if (!Array.isArray(entries) || entries.length === 0) {
      container.innerHTML = '<p class="archive-empty">最初の連載詩篇を待っています。</p>';
      return;
    }

    container.innerHTML = entries
      .map((entry) => {
        const language = languageNames[entry.source_language] || entry.source_language;
        return `
          <article class="work-entry archive-entry">
            <div class="work-folio">
              <span>${escapeHtml(displayFolio(entry.id))}</span>
              <span>${escapeHtml(language)}</span>
            </div>
            <div class="work-copy">
              <p class="work-label">${escapeHtml(entry.date)} / 原詩：${escapeHtml(language)}</p>
              <h3>${escapeHtml(entry.title)}</h3>
              <p>${escapeHtml(entry.summary)}</p>
              <a href="${escapeHtml(entry.href)}">三つの詩形を読む</a>
            </div>
            <blockquote class="poem-fragment archive-fragment">
              <p>${escapeHtml(entry.theme)}</p>
            </blockquote>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    console.error(error);
    container.innerHTML = '<p class="archive-empty">連載詩篇の目次を読み込めませんでした。</p>';
  }
}

loadArchive();
