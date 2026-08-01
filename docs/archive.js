const languageCodes = {
  arem: "A",
  en: "E",
  vela: "V",
};

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

async function loadArchive() {
  const container = document.querySelector("#generated-list");
  if (!container) return;

  try {
    const response = await fetch("archive.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`archive request failed: ${response.status}`);
    const entries = await response.json();

    if (!Array.isArray(entries) || entries.length === 0) {
      container.innerHTML = '<p class="archive-empty">最初の自動生成を待っています。</p>';
      return;
    }

    container.innerHTML = entries
      .map(
        (entry) => `
          <article class="archive-card">
            <div class="archive-index">${escapeHtml(entry.id)}</div>
            <div>
              <p class="meta">${escapeHtml(entry.date)} / ORIGINAL: ${escapeHtml(
                languageCodes[entry.source_language] || entry.source_language
              )}</p>
              <h3>${escapeHtml(entry.title)}</h3>
              <p>${escapeHtml(entry.summary)}</p>
              <p class="archive-theme">${escapeHtml(entry.theme)}</p>
            </div>
            <a href="${escapeHtml(entry.href)}">三つの詩形を読む</a>
          </article>
        `
      )
      .join("");
  } catch (error) {
    console.error(error);
    container.innerHTML = '<p class="archive-empty">アーカイブを読み込めませんでした。</p>';
  }
}

loadArchive();
