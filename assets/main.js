/* Документи з України — скрипти сайту (без залежностей) */
(function () {
  var FORM_ENDPOINT = "https://formspree.io/f/xppdzqra";
  var TG = "https://t.me/Online_Advokat_UA", WA = "https://wa.me/380937688416", VB = "viber://chat?number=%2B380937688416";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- тост ---------- */
  var toaster;
  function toast(kind, title, text) {
    if (!toaster) { toaster = document.createElement("div"); toaster.className = "toaster"; toaster.setAttribute("aria-live", "polite"); document.body.appendChild(toaster); }
    var el = document.createElement("div"); el.className = "toast " + kind;
    el.innerHTML = '<span class="toast-icon">' + (kind === "ok" ? "✓" : "!") + '</span><div><strong></strong><p></p></div>';
    $("strong", el).textContent = title; $("p", el).textContent = text;
    toaster.appendChild(el);
    setTimeout(function () { el.classList.add("out"); setTimeout(function () { el.remove(); }, 260); }, 5000);
  }

  /* ---------- мобільне меню ---------- */
  var burger = $(".burger"), mnav = $(".mnav");
  if (burger && mnav) {
    burger.addEventListener("click", function () { var o = mnav.classList.toggle("open"); burger.setAttribute("aria-expanded", o ? "true" : "false"); });
    mnav.addEventListener("click", function (e) { if (e.target.tagName === "A") { mnav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); } });
  }

  /* ---------- форми ---------- */
  function wireForm(form) {
    if (form.dataset.wired) return; form.dataset.wired = "1";
    var status = $(".form-status", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var honey = $(".honey", form); if (honey && honey.value) return;
      var btn = $("button[type=submit]", form), contact = $("[name=contact]", form);
      if (!contact || contact.value.trim().length < 5) { toast("err", "Вкажіть контакт", "Telegram, WhatsApp або телефон — щоб ми могли відповісти."); contact && contact.focus(); return; }
      btn.disabled = true;
      var data = new FormData(form); data.append("page", location.href);
      function fail() { toast("err", "Не вдалося надіслати", "Напишіть нам у Telegram — відповімо так само швидко."); }
      fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) return fail();
          form.reset();
          toast("ok", "Заявку отримано", "Відповімо за 15 хвилин у робочий час.");
          if (status) { status.className = "form-status ok"; status.textContent = "Дякуємо! Заявку отримано."; }
          if (window.gtag) gtag("event", "generate_lead", { event_category: "form", event_label: data.get("doc") });
          var dr = form.closest("dialog"); if (dr) setTimeout(function () { dr.close(); }, 900);
        }).catch(fail).finally(function () { btn.disabled = false; });
    });
  }
  $$("form[data-lead]").forEach(wireForm);

  function setSel(sel, val) { if (!sel || !val) return; for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === val) { sel.selectedIndex = i; return; } }

  /* ---------- конфігуратор ---------- */
  var D = {
    svid: { t: "від 1", u: "роб. дня", p: 80, m: "За ордером адвоката, без довіреності й консульства." },
    vyt: { t: "від 1", u: "роб. дня", p: 80, m: "За ордером адвоката, без довіреності й консульства." },
    nes: { t: "від 5", u: "роб. днів", p: 100, m: "Паперовий, з печаткою МВС. Регламентний строк — до 30 днів, зазвичай швидше." },
    rnokpp: { t: "від 1", u: "роб. дня", p: 50, m: "Потрібна нотаріальна довіреність — зразок надамо." },
    apostyl: { t: "4–10", u: "роб. днів", p: 50, m: "Мін'юст, МЗС або МОН — залежно від документа." }
  };
  var cDoc = $("#cDoc"), cC = $("#cCountry");
  function pick() { return cDoc ? cDoc.options[cDoc.selectedIndex] : null; }
  function msgText() { var o = pick(); return "Вітаю! Потрібен документ з України: " + o.text + ", я в країні: " + cC.value + ". Підкажіть ціну і строк."; }
  function setLinks() { var t = encodeURIComponent(msgText()); $("#cTg").href = TG + "?text=" + t; $("#cWa").href = WA + "?text=" + t; $("#cVb").href = VB + "&text=" + t; }
  function applyPick() {
    var o = pick(), d = D[o.getAttribute("data-k")] || D.svid;
    $("#cTerm").innerHTML = d.t + " <span>" + d.u + "</span>";
    $("#cPrice").innerHTML = "від " + d.p + " <span>€</span>";
    $("#cMeta").textContent = d.m;
    var dt = $("#destT"); if (dt) dt.textContent = cC.value === "Інша країна" ? "Ваша країна" : cC.value;
    setLinks();
  }
  if (cDoc && cC) { cDoc.addEventListener("change", applyPick); cC.addEventListener("change", applyPick); setLinks(); }

  /* ---------- діалог заявки ---------- */
  var tpl = $("#lead-form-tpl"), dlg = null;
  function openLead(prefill, doc) {
    if (!tpl || !("HTMLDialogElement" in window)) { var f0 = $("#form"); if (f0) f0.scrollIntoView(); return; }
    if (!dlg) {
      dlg = document.createElement("dialog"); dlg.className = "dlg"; dlg.setAttribute("aria-label", "Заявка");
      dlg.innerHTML = '<div class="dlgin"><div class="dlghead"><div><span class="eyebrow" style="margin:0">Заявка</span><p class="h">Опишіть ситуацію — відповімо за 15 хвилин</p></div><button class="x" type="button" aria-label="Закрити">×</button></div><div class="dlgbody"></div><div class="msgs" style="margin-top:14px">або одразу: <a href="' + TG + '" target="_blank" rel="noopener">Telegram</a><a href="' + WA + '" target="_blank" rel="noopener">WhatsApp</a><a href="' + VB + '">Viber</a></div></div>';
      document.body.appendChild(dlg);
      $(".dlgbody", dlg).appendChild(tpl.content.cloneNode(true));
      wireForm($("form", dlg));
      $(".x", dlg).addEventListener("click", function () { dlg.close(); });
      dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    }
    var f = $("form", dlg);
    if (prefill && cDoc) { setSel($("[name=doc]", f), cDoc.value); setSel($("[name=country]", f), cC.value); }
    if (doc) setSel($("[name=doc]", f), doc);
    dlg.showModal();
    setTimeout(function () { var i = $("[name=name]", f); i && i.focus(); }, 60);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href="#form"],[data-lead-open]'); if (!a) return;
    var sec = $("#form"), inCfg = !!a.closest(".cfg");
    if (!inCfg && sec) { var r = sec.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) return; }
    e.preventDefault(); openLead(inCfg, a.getAttribute("data-doc"));
  });
  var qdoc = new URLSearchParams(location.search).get("doc");
  if (qdoc) $$("select[name=doc]").forEach(function (s) { setSel(s, qdoc); });

  /* ---------- сцена: шлях документа ---------- */
  var sc = $("#scene");
  function initScene() {
    var route = $("#route"), prog = $("#prog"), pack = $("#pack"), doc = $("#doc"), sig = $("#sig"), order = $("#order"), apo = $("#apo"),
      envg = $("#envg"), envf = $("#envf"), flap = $("#flap"), flapb = $("#flapb"), seal = $("#seal"), done = $("#done"), dest = $("#dest"),
      destRing = $("#destRing"), noteT = $("#noteT"), bar = $("#bar"), ct = $("#ct"), cd = $("#cd"), st = $$(".st", sc), stage = $(".stage", sc);
    var L = route.getTotalLength(); prog.style.strokeDasharray = L; var SL = sig.getTotalLength(); sig.style.strokeDasharray = SL;
    var T = st.map(function (li) { return [$("b", li).textContent, $(".d", li).textContent]; });
    var N = ["Договір підписано", "Ордер подано, документ отримано", "Апостиль і відправка", "Доставлено до дверей"], cur = -1;
    var cl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; }, ph = function (p, a, b) { return cl((p - a) / (b - a)); }, ez = function (t) { return t * t * (3 - 2 * t); };
    var pop = function (el, t) { el.setAttribute("opacity", t); var tr = el.getAttribute("data-tr"); if (tr === null) { tr = el.getAttribute("transform") || ""; el.setAttribute("data-tr", tr); } el.setAttribute("transform", tr + " scale(" + (1.6 - .6 * t) + ")"); };
    var render = function (p) {
      sig.style.strokeDashoffset = SL * (1 - ez(ph(p, .03, .2)));
      pop(order, ez(ph(p, .24, .32)));
      pop(apo, ez(ph(p, .5, .57)));
      var into = ez(ph(p, .6, .74));
      doc.setAttribute("transform", "translate(0," + (40 * into) + ") scale(" + (1 - .45 * into) + ")");
      envg.setAttribute("opacity", into > 0 ? 1 : 0); envf.setAttribute("opacity", ph(p, .66, .7));
      var fl = -1 + 2 * ez(ph(p, .72, .78));
      flap.setAttribute("transform", "translate(0,-30) scale(1," + fl + ") translate(0,30)");
      flapb.setAttribute("transform", "translate(0,-30) scale(1," + (fl < 0 ? -fl : 0) + ") translate(0,30)");
      flap.setAttribute("opacity", fl < 0 ? 0 : 1); seal.setAttribute("opacity", ez(ph(p, .78, .81)));
      var t = ez(ph(p, .82, .96)), pt = route.getPointAtLength(t * L), lift = Math.sin(t * Math.PI);
      pack.setAttribute("transform", "translate(" + pt.x + "," + pt.y + ") rotate(" + (10 * lift) + ") scale(" + (1 - .12 * lift) + ")");
      prog.style.strokeDashoffset = L * (1 - t);
      dest.setAttribute("opacity", .55 + .45 * t); destRing.setAttribute("r", 12 + 6 * ez(ph(p, .95, 1)));
      pop(done, ez(ph(p, .96, 1)));
      bar.style.width = (p * 100) + "%";
      var i = p < .22 ? 0 : p < .48 ? 1 : p < .8 ? 2 : 3;
      if (i !== cur) { cur = i; ct.textContent = T[i][0]; cd.textContent = T[i][1]; noteT.textContent = N[i]; st.forEach(function (li, k) { li.className = "st" + (k < i ? " done" : k === i ? " on" : ""); }); }
    };
    var tick = false, onS = function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () { tick = false; var r = sc.getBoundingClientRect(), m = sc.offsetHeight - stage.offsetHeight; render(cl(-r.top / m)); });
    };
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) render(1);
    else { addEventListener("scroll", onS, { passive: true }); addEventListener("resize", onS); render(0); onS(); }
  }
  if (sc) {
    if ("IntersectionObserver" in window) { var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { io.disconnect(); initScene(); } }, { rootMargin: "600px 0px" }); io.observe(sc); }
    else initScene();
  }
})();
