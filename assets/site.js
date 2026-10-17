/* PyLab Studio - static site behaviour */
(function () {
  "use strict";

  const P = window.PROGRAMS || [];
  const S = window.STATS || {};
  const RAW = "https://raw.githubusercontent.com/Abhijeet-Kumar-Prajapati/pylab-studio/main";
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* theme */
  const body = document.body;
  const saved = localStorage.getItem("pylab-theme");
  if (saved) body.setAttribute("data-theme", saved);
  const tb = $("#themeBtn");
  if (tb) tb.addEventListener("click", () => {
    const next = body.getAttribute("data-theme") === "dark" ? "light" : "dark";
    body.setAttribute("data-theme", next);
    localStorage.setItem("pylab-theme", next);
  });

  /* home counters + quick grid */
  const total = $("#sTotal"); if (total) total.textContent = S.total ?? P.length;
  const cats = $("#sCats"); if (cats) cats.textContent = S.categories ?? 0;
  const web = $("#sWeb"); if (web) web.textContent = P.filter((p) => p.web).length;

  const quick = $("#quickGrid");
  if (quick) {
    const picks = ["area_circle", "quadratic_solver", "password_generator",
      "caesar_encrypt", "emi", "rock_paper_scissors", "countdown_timer", "bmi_calculator"];
    picks.map((s) => P.find((p) => p.slug === s)).filter(Boolean)
      .forEach((p) => {
        quick.insertAdjacentHTML("beforeend",
          `<article class="card"><span class="num">#${p.n}</span>
           <h3>${esc(p.name)}</h3><span class="badge">${esc(p.cat)}</span>
           <p>${esc(p.desc)}</p>
           <a class="btn sm" href="run.html?p=${p.slug}">Run</a></article>`);
      });
  }

  /* categories page */
  const intro = $("#intro");
  if (intro) intro.textContent = `${P.length} programs grouped into ${S.categories ?? 0} categories.`;
  const catsBox = $("#cats");
  if (catsBox) {
    const by = {};
    P.forEach((p) => (by[p.cat] = by[p.cat] || []).push(p));
    Object.keys(by).sort().forEach((c) => {
      catsBox.insertAdjacentHTML("beforeend",
        `<div class="catblock"><h2>${esc(c)} <span class="dim">(${by[c].length})</span></h2><div class="grid">` +
        by[c].map((p) => `<article class="card"><span class="num">#${p.n}</span><h3>${esc(p.name)}</h3>
            <p>${esc(p.desc)}</p>${p.web
              ? `<a class="btn sm" href="run.html?p=${p.slug}">Run</a>` : ""}
            <a class="btn sm ghost" href="${RAW}/${p.path}" download>Download .py</a>
            <a class="btn sm ghost" href="https://github.com/Abhijeet-Kumar-Prajapati/pylab-studio/blob/main/${p.path}" target="_blank" rel="noopener">Source</a>
            </article>`).join("") + "</div></div>");
    });
  }

  /* programs page */
  const grid = $("#grid");
  if (grid) {
    const catSel = $("#cat"), grpSel = $("#grp"), q = $("#q"), count = $("#count");
    [...new Set(P.map((p) => p.cat))].sort().forEach((c) => catSel.insertAdjacentHTML("beforeend", `<option>${esc(c)}</option>`));
    [...new Set(P.map((p) => p.group))].sort().forEach((g) => grpSel.insertAdjacentHTML("beforeend", `<option>${esc(g)}</option>`));

    function render() {
      const term = q.value.trim().toLowerCase();
      const cf = catSel.value, gf = grpSel.value;
      const list = P.filter((p) =>
        (!term || p.name.toLowerCase().includes(term) || p.desc.toLowerCase().includes(term) || p.path.toLowerCase().includes(term)) &&
        (!cf || p.cat === cf) && (!gf || p.group === gf));
      count.textContent = `Showing ${list.length} of ${P.length} programs`;
      grid.innerHTML = list.map((p) => `<article class="card">
          <span class="num">#${p.n}</span>
          <h3>${esc(p.name)}</h3><span class="badge">${esc(p.cat)}</span>
          <p>${esc(p.desc)}</p>
          <code class="path">${esc(p.path)}</code>
          ${p.web ? `<a class="btn sm" href="run.html?p=${p.slug}">Run</a>` : ""}
          <a class="btn sm ghost" href="${RAW}/${p.path}" download>Download .py</a>
          <a class="btn sm ghost" target="_blank" rel="noopener"
             href="https://github.com/Abhijeet-Kumar-Prajapati/pylab-studio/blob/main/${p.path}">Source</a>
        </article>`).join("") || '<p class="empty">Nothing matched.</p>';
    }
    $("#go").addEventListener("click", render);
    q.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); render(); } });
    catSel.addEventListener("change", render);
    grpSel.addEventListener("change", render);
    render();
  }

  /* download all helper */
  const dl = $("#dlAll");
  if (dl) {
    dl.addEventListener("click", () => {
      const b = dl; const old = b.textContent;
      b.textContent = "Preparing...";
      setTimeout(() => (b.textContent = old), 1200);
    });
  }

  /* runner page */
  const picker = $("#picker");
  if (picker) {
    const rq = $("#rq"), rcat = $("#rcat"), input = $("#input"), out = $("#out"), pdesc = $("#pdesc");
    const runnable = P.filter((p) => p.web);
    const cats = [...new Set(runnable.map((p) => p.cat))].sort();
    cats.forEach((c) => rcat.insertAdjacentHTML("beforeend", `<option>${esc(c)}</option>`));

    function fill() {
      const term = rq.value.trim().toLowerCase(), cf = rcat.value;
      const list = runnable.filter((p) =>
        (!term || p.name.toLowerCase().includes(term) || p.desc.toLowerCase().includes(term)) &&
        (!cf || p.cat === cf));
      picker.innerHTML = list.map((p) => `<option value="${p.slug}">${esc(p.name)}</option>`).join("")
        || '<option value="">No match</option>';
      update();
    }

    function update() {
      const slug = picker.value;
      const prog = P.find((p) => p.slug === slug);
      pdesc.textContent = prog ? prog.desc : "";
      if (prog) input.placeholder = window.PyLab.sample(slug) || "Enter your values, one per line";
    }

    rq.addEventListener("input", fill);
    rcat.addEventListener("change", fill);
    picker.addEventListener("change", update);
    $("#runBtn").addEventListener("click", () => {
      const slug = picker.value;
      if (!slug) return;
      const lines = window.PyLab.run(slug, input.value);
      out.textContent = lines.join("\n");
    });
    $("#sampleBtn").addEventListener("click", () => {
      input.value = window.PyLab.sample(picker.value);
    });
    $("#copyBtn").addEventListener("click", () => {
      navigator.clipboard.writeText(out.textContent).then(() => {
        const b = $("#copyBtn"); b.textContent = "Copied"; setTimeout(() => (b.textContent = "Copy"), 1200);
      });
    });

    fill();
    const want = new URLSearchParams(location.search).get("p");
    if (want && window.PyLab.has(want)) { picker.value = want; update(); }
  }
})();