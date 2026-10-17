/* ==========================================================================
   PyLab Studio - browser side behaviour
   Favourites, theme, run history and keyboard shortcuts.
   ========================================================================== */
(function () {
  "use strict";

  const KEY_THEME = "pylab-theme";
  const KEY_FAVS = "pylab-favourites";
  const KEY_HISTORY = "pylab-history";
  const HISTORY_MAX = 25;

  // ---------------------------------------------------------------- storage
  function read(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function write(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      /* private mode / quota - ignore */
    }
  }

  // ------------------------------------------------------------------ theme
  const body = document.body;

  function applyTheme(theme) {
    body.setAttribute("data-theme", theme);
    write(KEY_THEME, theme);
    const btn = document.getElementById("themeBtn");
    if (btn) btn.textContent = theme === "dark" ? "\u263D" : "\u2600";
  }

  applyTheme(read(KEY_THEME, "dark"));
  const themeBtn = document.getElementById("themeBtn");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      applyTheme(body.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  // ------------------------------------------------------------- favourites
  const favourites = () => new Set(read(KEY_FAVS, []));

  function toggleFavourite(id) {
    const set = favourites();
    if (set.has(id)) {
      set.delete(id);
    } else {
      set.add(id);
    }
    write(KEY_FAVS, Array.from(set));
    paintFavourites();
    return set.has(id);
  }

  function paintFavourites() {
    const set = favourites();
    document.querySelectorAll("[data-fav]").forEach(function (el) {
      const on = set.has(el.dataset.fav);
      el.classList.toggle("is-fav", on);
      el.textContent = on ? "\u2605" : "\u2606";
      el.title = on ? "Remove from favourites" : "Add to favourites";
      el.setAttribute("aria-pressed", on ? "true" : "false");
    });
    const count = document.getElementById("favCount");
    if (count) count.textContent = set.size;
  }

  document.addEventListener("click", function (event) {
    const star = event.target.closest("[data-fav]");
    if (!star) return;
    event.preventDefault();
    toggleFavourite(star.dataset.fav);
  });

  // ---------------------------------------------------------------- history
  function pushHistory(entry) {
    const list = read(KEY_HISTORY, []).filter((e) => e.id !== entry.id);
    list.unshift(entry);
    write(KEY_HISTORY, list.slice(0, HISTORY_MAX));
    renderHistory();
  }

  function renderHistory() {
    const box = document.getElementById("historyBox");
    if (!box) return;
    const list = read(KEY_HISTORY, []);
    if (!list.length) {
      box.innerHTML = '<p class="dim small">Nothing yet - run a program and it shows up here.</p>';
      return;
    }
    box.innerHTML = list
      .map(function (e) {
        const status = e.ok ? "ok" : "bad";
        const secs = typeof e.seconds === "number" ? e.seconds + "s" : "";
        return (
          '<a class="hist" href="/run/' + encodeURIComponent(e.id) + '">' +
          '<span class="dot ' + status + '"></span>' +
          '<span class="hname">' + e.name + "</span>" +
          '<span class="hmeta">' + secs + "</span>" +
          "</a>"
        );
      })
      .join("");
  }

  // Record a run when the result panel appears on /run/<id>.
  const outputBox = document.getElementById("outputBox");
  if (outputBox && outputBox.dataset.programId) {
    pushHistory({
      id: outputBox.dataset.programId,
      name: outputBox.dataset.programName || outputBox.dataset.programId,
      ok: outputBox.dataset.ok === "1",
      seconds: parseFloat(outputBox.dataset.seconds) || 0,
    });
  }

  // ------------------------------------------------------------------- copy
  function copyText(text, btn) {
    const done = function () {
      const old = btn.textContent;
      btn.textContent = "Copied";
      setTimeout(function () {
        btn.textContent = old;
      }, 1400);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () {});
      return;
    }
    // Fallback for plain http://127.0.0.1 in older browsers.
    const area = document.createElement("textarea");
    area.value = text;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
      done();
    } catch (e) {
      /* ignore */
    }
    document.body.removeChild(area);
  }

  document.addEventListener("click", function (event) {
    const btn = event.target.closest("[data-copy]");
    if (!btn) return;
    event.preventDefault();
    const target = document.getElementById(btn.dataset.copy);
    copyText(target ? target.textContent : "", btn);
  });

  // ------------------------------------------------------- sample / clearing
  const sampleBtn = document.getElementById("sampleBtn");
  if (sampleBtn) {
    sampleBtn.addEventListener("click", function () {
      const area = document.getElementById("input");
      if (area) area.value = sampleBtn.dataset.sample || "";
    });
  }

  const clearBtn = document.getElementById("clearBtn");
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      const area = document.getElementById("input");
      if (area) area.value = "";
    });
  }

  // ------------------------------------------------------ favourites filter
  const favFilter = document.getElementById("favFilter");
  if (favFilter) {
    const only = new URLSearchParams(location.search).has("favourites");
    favFilter.classList.toggle("on", only);
    favFilter.setAttribute("aria-pressed", only ? "true" : "false");
    favFilter.addEventListener("click", function (event) {
      event.preventDefault();
      const params = new URLSearchParams(location.search);
      if (params.has("favourites")) {
        params.delete("favourites");
      } else {
        params.set("favourites", "1");
      }
      location.search = params.toString();
    });
  }

  // --------------------------------------------------- live client search
  const quickSearch = document.getElementById("quickSearch");
  if (quickSearch) {
    quickSearch.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        location.href = "/programs?q=" + encodeURIComponent(quickSearch.value.trim());
      }
    });
  }

  // ------------------------------------------------------ keyboard shortcuts
  const shortcuts = {
    "/": () => focusSearch(),
    "?": () => toggleHelp(),
    Escape: () => closeHelp(),
    c: () => {
      const area = document.getElementById("input");
      if (area) area.focus();
    },
    r: () => {
      const form = document.getElementById("runForm");
      if (form) form.requestSubmit ? form.requestSubmit() : form.submit();
    },
    p: () => {
      location.href = "/programs";
    },
    h: () => {
      location.href = "/";
    },
  };

  function focusSearch() {
    const field =
      document.getElementById("quickSearch") || document.getElementById("q");
    if (field) {
      field.focus();
      field.select();
    }
  }

  function toggleHelp() {
    const box = document.getElementById("shortcutHelp");
    if (box) box.classList.toggle("show");
  }

  function closeHelp() {
    const box = document.getElementById("shortcutHelp");
    if (box) box.classList.remove("show");
  }

  document.addEventListener("keydown", function (event) {
    const tag = (event.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") {
      if (event.key === "Escape") event.target.blur();
      return;
    }
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const action = shortcuts[event.key];
    if (action) {
      event.preventDefault();
      action();
    }
  });

  // ------------------------------------------------------------- page init
  paintFavourites();
  renderHistory();
  if (history.scrollRestoration) history.scrollRestoration = "manual";
})();