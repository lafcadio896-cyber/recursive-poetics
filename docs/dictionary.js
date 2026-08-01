(() => {
  const normalize = (value) =>
    String(value || "")
      .toLocaleLowerCase("ja")
      .normalize("NFKC")
      .replace(/\s+/g, " ")
      .trim();

  const input = document.querySelector("[data-dictionary-search]");
  const entries = [...document.querySelectorAll("[data-dictionary-entry]")];
  const result = document.querySelector("[data-dictionary-result]");
  const empty = document.querySelector("[data-dictionary-empty]");
  const filters = [...document.querySelectorAll("[data-dictionary-filter]")];

  if (!entries.length) return;

  let activeFilter = "all";

  const update = () => {
    const query = normalize(input?.value);
    let visible = 0;

    entries.forEach((entry) => {
      const searchable = normalize(
        `${entry.dataset.search || ""} ${entry.textContent || ""}`
      );
      const kind = entry.dataset.kind || "other";
      const matchesQuery = !query || searchable.includes(query);
      const matchesFilter = activeFilter === "all" || kind === activeFilter;
      const show = matchesQuery && matchesFilter;

      entry.hidden = !show;
      if (entry.classList.contains("phase-card")) {
        entry.style.display = show ? "block" : "none";
      } else {
        entry.style.removeProperty("display");
      }

      if (show) visible += 1;
    });

    if (result) result.textContent = `${visible} / ${entries.length}`;
    empty?.classList.toggle("is-visible", visible === 0);
  };

  input?.addEventListener("input", update);

  filters.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.dictionaryFilter || "all";
      filters.forEach((item) =>
        item.setAttribute("aria-pressed", String(item === button))
      );
      update();
    });
  });

  update();
})();
