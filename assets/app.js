/* Wiliheng site — small progressive-enhancement script. No dependencies. */
(function () {
  "use strict";

  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Close the language dropdown when clicking outside it */
  document.addEventListener("click", function (e) {
    var open = document.querySelectorAll("details.lang[open]");
    for (var i = 0; i < open.length; i++) {
      if (!open[i].contains(e.target)) open[i].removeAttribute("open");
    }
  });

  /* Quote form -> POST /api/quote */
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var submit = form.querySelector("button[type=submit]");

  function say(kind, msg) {
    if (!status) return;
    status.className = "form-status " + kind;
    status.textContent = msg;
    status.setAttribute("role", kind === "err" ? "alert" : "status");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = Object.fromEntries(new FormData(form).entries());
    if (submit) { submit.disabled = true; }
    say("ok", form.dataset.sending || "Sending…");

    /* 2026-11-20: 原端点 /api/quote 是 Cloudflare Pages Function，线上从未生效
       （POST 返回 405，官网表单因此一直收不到询盘）。改投已验证可用的询盘 Worker：
       api.wiliheng.com/lead（实测 200 + {ok:true, ref:INQ-...}）。 */
    var payload = Object.assign({
      token: "wlc-7f3a91c2", lang: "en", code: "CONTACT", hero: 0, page: "/contact/"
    }, data);
    if (data.product && !data.product_line) { payload.product_line = data.product; }

    fetch("https://api.wiliheng.com/lead", {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().then(function (b) { return { ok: r.ok, body: b }; }); })
      .then(function (res) {
        if (res.ok && res.body && res.body.ok) {
          say("ok", res.body.message || form.dataset.success || "Thank you — we will reply shortly.");
          form.reset();
        } else {
          say("err", (res.body && res.body.error) || form.dataset.error || "Something went wrong. Please email us instead.");
        }
      })
      .catch(function () {
        say("err", form.dataset.error || "Something went wrong. Please email us instead.");
      })
      .then(function () { if (submit) { submit.disabled = false; } });
  });
})();
