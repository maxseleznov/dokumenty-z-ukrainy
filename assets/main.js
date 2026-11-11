/* Документи з України — site scripts */
(function () {
  // ---- CONFIG: замініть на свої значення -------------------------------
  var FORM_ENDPOINT = "https://formspree.io/f/xppdzqra"; // Formspree / Basin / свій бекенд
  var TELEGRAM_URL = "https://t.me/rozlucheni";
  var WHATSAPP_URL = "https://wa.me/380XXXXXXXXX";
  // ----------------------------------------------------------------------

  document.querySelectorAll("[data-tg]").forEach(function (a) { a.href = TELEGRAM_URL; });
  document.querySelectorAll("[data-wa]").forEach(function (a) { a.href = WHATSAPP_URL; });

  // mobile nav
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); });
    });
  }

  // lead form
  document.querySelectorAll("form[data-lead]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".honey") && form.querySelector(".honey").value) return;
      var btn = form.querySelector("button[type=submit]");
      var contact = form.querySelector("[name=contact]");
      if (!contact || contact.value.trim().length < 5) {
        showStatus("err", "Вкажіть, будь ласка, контакт — Telegram, WhatsApp або email.");
        contact && contact.focus();
        return;
      }
      btn.disabled = true;
      var data = new FormData(form);
      data.append("page", location.href);
      fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (r.ok) {
            form.reset();
            showStatus("ok", "Дякуємо! Заявку отримано. Відповімо протягом робочого дня.");
            if (window.gtag) gtag("event", "generate_lead", { event_category: "form", event_label: data.get("doc") });
          } else {
            showStatus("err", "Не вдалося надіслати. Напишіть нам у Telegram або WhatsApp.");
          }
        })
        .catch(function () { showStatus("err", "Не вдалося надіслати. Напишіть нам у Telegram або WhatsApp."); })
        .finally(function () { btn.disabled = false; });
    });
    function showStatus(kind, text) {
      if (!status) return;
      status.className = "form-status " + kind;
      status.textContent = text;
    }
  });

  // prefill doc select from ?doc=
  var params = new URLSearchParams(location.search);
  var doc = params.get("doc");
  if (doc) {
    document.querySelectorAll("select[name=doc]").forEach(function (s) {
      for (var i = 0; i < s.options.length; i++) if (s.options[i].value === doc) s.selectedIndex = i;
    });
  }
})();
