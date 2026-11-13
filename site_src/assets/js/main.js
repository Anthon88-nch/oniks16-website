/* ОНИКС — interactions: menu, modals, lead forms, gallery */
(function () {
  "use strict";

  var WA = "79061222999";

  /* ---------- burger ---------- */
  var burger = document.querySelector("[data-burger]");
  var nav = document.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- modals ---------- */
  var lastFocus = null;

  function openModal(id, product) {
    var m = document.getElementById(id);
    if (!m) return;
    lastFocus = document.activeElement;
    if (product) {
      var msg = m.querySelector("#order-msg");
      if (msg) msg.value = "Интересует: " + product + ". ";
    }
    m.hidden = false;
    document.body.style.overflow = "hidden";
    var first = m.querySelector("input, textarea, button");
    if (first) first.focus();
  }

  function closeModal(m) {
    m.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    var cb = e.target.closest("[data-open-callback]");
    var od = e.target.closest("[data-open-order]");
    if (cb) { openModal("modal-callback"); return; }
    if (od) { openModal("modal-order", od.getAttribute("data-product")); return; }

    var close = e.target.closest("[data-close]");
    if (close) { closeModal(close.closest(".modal")); return; }

    var backdrop = e.target.classList && e.target.classList.contains("modal");
    if (backdrop) closeModal(e.target);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var m = document.querySelector(".modal:not([hidden])");
    if (m) closeModal(m);
  });

  /* ---------- toast ---------- */
  var toast = document.getElementById("toast");
  var toastTimer = null;
  function showToast(text) {
    if (!toast) return;
    toast.textContent = text;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.hidden = true; }, 4000);
  }

  /* ---------- lead forms -> WhatsApp ---------- */
  document.querySelectorAll("[data-lead-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fd = new FormData(form);
      var kind = form.getAttribute("data-lead-form");
      var lines = [];
      if (kind === "callback") {
        lines.push("Здравствуйте! Прошу перезвонить.");
        lines.push("Имя: " + (fd.get("name") || ""));
        lines.push("Телефон: " + (fd.get("phone") || ""));
        var t = (fd.get("time") || "").trim();
        if (t) lines.push("Удобное время: " + t);
      } else {
        lines.push("Здравствуйте! Заявка с сайта oniks16.ru.");
        lines.push("Имя: " + (fd.get("name") || ""));
        lines.push("Телефон: " + (fd.get("phone") || ""));
        var msg = (fd.get("msg") || "").trim();
        if (msg) lines.push("Запрос: " + msg);
      }
      var url = "https://wa.me/" + WA + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
      showToast("Заявка готова — открыли WhatsApp, нажмите «отправить»");
      var m = form.closest(".modal");
      if (m) closeModal(m);
      form.reset();
    });
  });

  /* ---------- product gallery ---------- */
  var mainImg = document.getElementById("gallery-main");
  document.querySelectorAll("[data-thumb]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!mainImg) return;
      mainImg.src = btn.getAttribute("data-thumb");
      document.querySelectorAll("[data-thumb]").forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
    });
  });
})();
