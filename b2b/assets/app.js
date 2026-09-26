/* Wiliheng Knives — 站点交互（零依赖，全部原生）
   1) 手机菜单  2) RFQ 表单：有 endpoint 就 POST，没有就组织成邮件（不假装发送成功）
   3) 型号预填： /contact/?model=KH-001  把 SKU / 分类填进表单  4) 页脚年份 */
(function () {
  'use strict';

  /* 1) 手机菜单 */
  var burger = document.getElementById('burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('#mobile-nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* 2) 型号/分类预填 */
  var params = new URLSearchParams(location.search);
  var model = params.get('model');
  if (model) {
    document.querySelectorAll('form.rfq').forEach(function (f) {
      var m = f.querySelector('[name="models"]');
      if (m && !m.value) { m.value = model; }
    });
    var h = document.getElementById('quote-form');
    if (h && location.hash !== '#quote-form') {
      var pageForm = document.getElementById(h.getAttribute('data-anchor') || 'quote-form');
      void pageForm;
    }
    // 锚点：分类页表单 id 不同，直接滚到第一个表单
    if (location.hash === '#quote-form') {
      var first = document.querySelector('form.rfq');
      if (first) { first.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
    }
  }

  /* 3) RFQ 表单 */
  function collect(form) {
    var out = {};
    form.querySelectorAll('input,select,textarea').forEach(function (el) {
      if (!el.name || el.name === 'website') { return; }
      var v = (el.value || '').trim();
      if (v) { out[el.name] = v; }
    });
    return out;
  }
  function compose(data) {
    var lines = ['Product enquiry from wiliheng.com', ''];
    var order = ['name', 'job', 'company', 'email', 'country', 'family', 'models', 'quantity', 'intent', 'timeline', 'message'];
    var label = { name: 'Name', job: 'Job title', company: 'Company', email: 'Email', country: 'Country / market',
      family: 'Product family', models: 'Models / SKUs', quantity: 'Estimated quantity', intent: 'OEM / ODM',
      timeline: 'Target timeline', message: 'Notes' };
    order.forEach(function (k) { if (data[k]) { lines.push(label[k] + ': ' + data[k]); } });
    return lines.join('\n');
  }
  document.querySelectorAll('form.rfq').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.rfq-note');
      var data = collect(form);
      var missing = [];
      ['name', 'company', 'email'].forEach(function (k) {
        if (!data[k]) { missing.push(k); }
      });
      if (missing.length) {
        if (note) {
          note.hidden = false; note.className = 'rfq-note fine err';
          note.textContent = 'Please fill in: ' + missing.join(', ') + '.';
        }
        return;
      }
      if (data.email && data.email.indexOf('@') < 1) {
        if (note) { note.hidden = false; note.className = 'rfq-note fine err'; note.textContent = 'That email address looks incomplete.'; }
        return;
      }
      var endpoint = form.getAttribute('data-endpoint') || '';
      var body = compose(data);
      if (endpoint) {
        if (note) { note.hidden = false; note.className = 'rfq-note fine'; note.textContent = 'Sending…'; }
        fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
          .then(function (r) { if (!r.ok) { throw new Error('HTTP ' + r.status); } return r.json().catch(function () { return {}; }); })
          .then(function () {
            form.reset();
            if (note) { note.hidden = false; note.className = 'rfq-note fine ok'; note.textContent = 'Thank you — your request is with us. You will hear back within 24 hours.'; }
          })
          .catch(function (err) {
            if (note) {
              note.hidden = false; note.className = 'rfq-note fine err';
              note.textContent = 'Automatic sending did not go through (' + err.message + '). Opening your email client instead — or write to sales@wiliheng.com.';
            }
            mailto(form, data, body);
          });
        return;
      }
      mailto(form, data, body);
    });
  });
  function mailto(form, data, body) {
    var to = form.getAttribute('data-mail') || 'sales@wiliheng.com';
    var subject = 'Product enquiry — ' + (data.company || '') + (data.models ? ' — ' + data.models : '');
    var href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    window.location.href = href;
    var note = form.querySelector('.rfq-note');
    if (note) {
      note.hidden = false; note.className = 'rfq-note fine ok';
      note.textContent = 'Your email client should open with the enquiry filled in. If nothing opens, copy and send it to ' + to + ' — the text above is ready.';
    }
  }

  /* 4) 型号卡片墙筛选（无 JS 时全部卡片照常显示） */
  document.querySelectorAll('.mgrid-cards').forEach(function (list) {
    const bar = list.previousElementSibling;
    if (!bar || !bar.classList.contains('mfilter')) { return; }
    const q = bar.querySelector('.mf-q');
    const only = bar.querySelector('.mf-spec');
    const cnt = bar.querySelector('.mf-count');
    const cards = [].slice.call(list.querySelectorAll('.mprod'));
    const empty = list.nextElementSibling && list.nextElementSibling.classList.contains('mf-empty')
      ? list.nextElementSibling : null;
    function apply() {
      const term = (q && q.value || '').trim().toLowerCase();
      const onlySpec = !!(only && only.checked);
      let n = 0;
      cards.forEach(function (card) {
        const hay = (card.getAttribute('data-sku') + ' ' + card.textContent).toLowerCase();
        const ok = (!term || hay.indexOf(term) >= 0) && (!onlySpec || card.getAttribute('data-spec') === '1');
        card.hidden = !ok;
        if (ok) { n++; }
      });
      if (cnt) { cnt.textContent = n + ' of ' + cards.length + ' models shown'; }
      if (empty) { empty.hidden = n !== 0; }
    }
    if (q) { q.addEventListener('input', apply); }
    if (only) { only.addEventListener('change', apply); }
    apply();
  });

  /* 5) 页脚年份（模板已写死，这里只兜底静态托管年份偏差） */
  var y = new Date().getFullYear();
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = y; });
})();
