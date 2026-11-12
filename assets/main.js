/* Документи з України — site scripts (no dependencies) */
(function () {
  // ---- CONFIG -----------------------------------------------------------
  var FORM_ENDPOINT = "https://formspree.io/f/xppdzqra";
  var TELEGRAM_URL = "https://t.me/Online_Advokat_UA";
  var WHATSAPP_URL = "https://wa.me/380937688416";
  // ----------------------------------------------------------------------

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  $$("[data-tg]").forEach(function (a) { a.href = TELEGRAM_URL; });
  $$("[data-wa]").forEach(function (a) { a.href = WHATSAPP_URL; });

  /* ---------- toast (Sonner-like) ---------- */
  var toaster;
  function toast(kind, title, text) {
    if (!toaster) { toaster = document.createElement("div"); toaster.className = "toaster"; toaster.setAttribute("aria-live", "polite"); document.body.appendChild(toaster); }
    var el = document.createElement("div");
    el.className = "toast " + kind;
    var icon = kind === "ok"
      ? '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
      : '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M12 7v6M12 17h.01"/></svg>';
    el.innerHTML = '<span class="toast-icon">' + icon + '</span><div><strong></strong><p></p></div>';
    $("strong", el).textContent = title; $("p", el).textContent = text;
    toaster.appendChild(el);
    setTimeout(function () { el.classList.add("out"); setTimeout(function () { el.remove(); }, 260); }, 5000);
  }

  /* ---------- mobile nav ---------- */
  var toggle = $(".nav-toggle"), nav = $(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }); });
  }

  /* ---------- lead forms ---------- */
  function wireForm(form) {
    if (form.dataset.wired) return; form.dataset.wired = "1";
    var status = $(".form-status", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var honey = $(".honey", form); if (honey && honey.value) return;
      var btn = $("button[type=submit]", form), contact = $("[name=contact]", form);
      if (!contact || contact.value.trim().length < 5) {
        toast("err", "Вкажіть контакт", "Telegram, WhatsApp або email — щоб ми могли відповісти.");
        contact && contact.focus(); return;
      }
      btn.disabled = true; btn.setAttribute("aria-busy", "true");
      var data = new FormData(form); data.append("page", location.href);
      fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (r.ok) {
            form.reset();
            toast("ok", "Заявку отримано", "Відповімо протягом робочого дня.");
            if (status) { status.className = "form-status ok"; status.textContent = "Дякуємо! Заявку отримано. Відповімо протягом робочого дня."; }
            if (window.gtag) gtag("event", "generate_lead", { event_category: "form", event_label: data.get("doc") });
            var dr = form.closest("dialog"); if (dr) setTimeout(function () { dr.close(); }, 900);
          } else { fail(); }
        })
        .catch(fail)
        .finally(function () { btn.disabled = false; btn.removeAttribute("aria-busy"); });
      function fail() { toast("err", "Не вдалося надіслати", "Напишіть нам у Telegram — відповімо так само швидко."); }
    });
  }
  $$("form[data-lead]").forEach(wireForm);

  /* ---------- prefill ?doc= ---------- */
  var doc = new URLSearchParams(location.search).get("doc");
  if (doc) $$("select[name=doc]").forEach(function (s) { for (var i = 0; i < s.options.length; i++) if (s.options[i].value === doc) s.selectedIndex = i; });

  /* ---------- mobile drawer (Vaul-like) ---------- */
  var mq = window.matchMedia("(max-width:900px)");
  var sourceForm = $(".hero form[data-lead], .page-hero form[data-lead]");
  if (sourceForm && "HTMLDialogElement" in window) {
    var dialog = document.createElement("dialog");
    dialog.className = "drawer"; dialog.setAttribute("aria-label", "Форма заявки");
    var panel = document.createElement("div"); panel.className = "drawer-panel";
    panel.innerHTML = '<div class="drawer-handle"></div><button type="button" class="drawer-close" aria-label="Закрити"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
    var clone = sourceForm.cloneNode(true); clone.removeAttribute("id"); clone.dataset.wired = "";
    $$("[id]", clone).forEach(function (n) { var id = n.id; n.id = "d-" + id; var l = $('label[for="' + id + '"]', clone); if (l) l.htmlFor = "d-" + id; });
    panel.appendChild(clone); dialog.appendChild(panel); document.body.appendChild(dialog);
    wireForm(clone);
    $(".drawer-close", dialog).addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });

    var bar = document.createElement("div"); bar.className = "sticky-cta";
    bar.innerHTML = '<a class="btn btn-secondary" href="' + TELEGRAM_URL + '" rel="noopener" target="_blank">Telegram</a><button type="button" class="btn btn-primary">Отримати розрахунок</button>';
    document.body.appendChild(bar);
    $("button", bar).addEventListener("click", function () { dialog.showModal(); });

    // on mobile, every "#form" link opens the drawer
    document.addEventListener("click", function (e) {
      var a = e.target.closest('a[href="#form"]'); if (!a || !mq.matches) return;
      e.preventDefault(); dialog.showModal();
    });
    // hide bar when footer is visible
    var footer = $(".footer");
    if (footer && "IntersectionObserver" in window) new IntersectionObserver(function (en) { bar.classList.toggle("hidden", en[0].isIntersecting); }, { threshold: 0.1 }).observe(footer);
  }

  /* ---------- number count-up (NumberFlow-like) ---------- */
  function countUp(el) {
    var raw = el.textContent.trim(), m = raw.match(/^(\d[\d\s ]*)(\+?)$/); if (!m) return;
    var target = parseInt(m[1].replace(/\D/g, ""), 10), suffix = m[2], start = null, dur = 1100;
    var fmt = function (n) { return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "); };
    if (target > 1900 && target < 2100) { fmt = function (n) { return String(n); }; } // year
    function step(ts) { if (!start) start = ts; var p = Math.min((ts - start) / dur, 1), e = 1 - Math.pow(1 - p, 3); el.textContent = fmt(Math.round(target * e)) + suffix; if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  /* ---------- reveal on scroll ---------- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        if (en.target.matches(".stat")) { var b = $("b", en.target); if (b && !b.dataset.done) { b.dataset.done = "1"; countUp(b); } }
        io.unobserve(en.target);
      });
    }, { threshold: 0.2 });
    $$(".card, .tile, .stat, .step, .faq details").forEach(function (el, i) { el.classList.add("reveal"); el.style.transitionDelay = (i % 4) * 60 + "ms"; io.observe(el); });
  }
})();
