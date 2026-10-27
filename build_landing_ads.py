#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""多语种广告落地页生成器（厨房/餐具口径，非德国市场不含刀具）。

【为什么需要它】
2026-10-05 实测：西语广告指向新站语言页、新站厨房品类页、甚至已过审的 /ad/us-ware/，
全部被 `policyFindingError=POLICY_FINDING` 拒 —— Google 按**整站**判武器政策，而新站含刀具
（含折叠刀）。所以非德国市场的多语种投放必须各有**本语言的"无刀厨房口径"落地页**。

【设计】
· 文案：共享部分（h1/lede/facts/faq）来自 web/content/i18n.json（与线上站同源，口径一致）；
  落地页专用串在 site/ad_ads_i18n.json。两者都不在此脚本里硬编码 → 加语种只加数据。
· 相册：只用非刀品类（剪刀/砧板/磨刀器），避免重新触发武器政策。
· 转化链路与 /ad/de/ 完全一致：WhatsApp 点击上报 + 表单 POST + Google 转化 + Consent Mode v2，
  上报地址运行时读 /ad/track.json（隧道会变），读不到静默/回退邮件。

用法：python site/build_landing_ads.py [--langs es,fr]
"""
import json
import urllib.parse
import re
import subprocess
import sys
from pathlib import Path
from critical_css import CSS as CRITICAL_CSS

BASE = Path(__file__).resolve().parent          # site/
ROOT = BASE.parent
LANGS_DEFAULT = ['es', 'fr', 'it', 'pt', 'nl', 'pl', 'ru', 'ar', 'tr', 'ro', 'sv', 'cs', 'de-ware', 'id', 'th']  # 2026-10-16：按欧盟进口数据加 瑞典/捷克/奥地利(无刀德语)
WHATSAPP = '8618124886695'
EMAIL = 'fengerwei669@gmail.com'
SINCE = '2018'
SAFE_CATS = ('Shears & scissors', 'Chopping boards', 'Knife sharpeners')
FORM_LABEL = 'AW-17434685893/R4CTCKq3poMdEMXjwPlA'
WA_LABEL = 'AW-17434685893/8VZKCKaX2Y4bEMXjwPlA'
TOKEN = 'wlc-7f3a91c2'
MULTI = 'https://wiliheng.com/b2b/%s/'
CAT_LABEL = {
 'es': {'Shears & scissors': 'Tijeras de cocina', 'Chopping boards': 'Tabla de cortar', 'Knife sharpeners': 'Afilador de mano'},
 'tr': {'Shears & scissors': 'Mutfak makası', 'Chopping boards': 'Kesme tahtası', 'Knife sharpeners': 'El bileme aleti'},
 'ro': {'Shears & scissors': 'Foarfece de bucătărie', 'Chopping boards': 'Tocător', 'Knife sharpeners': 'Ascuțitor manual'},
 'fr': {'Shears & scissors': 'Ciseaux de cuisine', 'Chopping boards': 'Planche à découper', 'Knife sharpeners': 'Affûteur à main'},
 'it': {'Shears & scissors': 'Forbici da cucina', 'Chopping boards': 'Tagliere', 'Knife sharpeners': 'Affilatore manuale'},
 'pt': {'Shears & scissors': 'Tesouras de cozinha', 'Chopping boards': 'Tábua de corte', 'Knife sharpeners': 'Afiaador manual'},
 'nl': {'Shears & scissors': 'Keukenscharen', 'Chopping boards': 'Snijplank', 'Knife sharpeners': 'Handslijper'},
 'pl': {'Shears & scissors': 'Nożyce kuchenne', 'Chopping boards': 'Deska do krojenia', 'Knife sharpeners': 'Ostrzałka ręczna'},
 'ru': {'Shears & scissors': 'Кухонные ножницы', 'Chopping boards': 'Разделочная доска', 'Knife sharpeners': 'Ручная точилка'},
 'ar': {'Shears & scissors': 'مقصات المطبخ', 'Chopping boards': 'لوح تقطيع', 'Knife sharpeners': 'مِسنّ يدوي'},
    'sv': {'Shears & scissors': 'Kökssaxar', 'Chopping boards': 'Skärbrädor', 'Knife sharpeners': 'Handslipare'},
    'cs': {'Shears & scissors': 'Kuchyňské nůžky', 'Chopping boards': 'Prkénka', 'Knife sharpeners': 'Ruční brousky'},
    'de-ware': {'Shears & scissors': 'Küchenscheren', 'Chopping boards': 'Schneidebretter', 'Knife sharpeners': 'Handschärfer'},
    'id': {'Shears & scissors': 'Gunting dapur', 'Chopping boards': 'Talenan', 'Knife sharpeners': 'Pengasah tangan'},
    'th': {'Shears & scissors': 'กรรไกรครัว', 'Chopping boards': 'เขียง', 'Knife sharpeners': 'ที่ลับมีดมือ'},
}

JS = r"""
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-17434685893"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());
var EU=['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'];
var RGN=((navigator.language||'').split('-')[1]||'').toUpperCase(),inEU=EU.indexOf(RGN)>=0;
function consentDefaults(g){gtag('consent','default',{ad_storage:g?'granted':'denied',ad_user_data:g?'granted':'denied',ad_personalization:g?'granted':'denied',analytics_storage:g?'granted':'denied'});}
consentDefaults(!inEU);
try{var _c=localStorage.getItem('wl_consent');if(_c==='y')consentDefaults(true);if(_c==='n')consentDefaults(false);}catch(e){}
gtag('config','AW-17434685893');
</script>
<!--SPLIT-->
<script>
(function(){
 function QP(k){try{var m=new RegExp('[?&]'+k+'=([^&]*)').exec(location.search);return m?decodeURIComponent(m[1].replace(/\+/g,' ')):'';}catch(_){return '';}}
 var TOKEN='__TOKEN__',LBL_WA='__WA__',LBL_FORM='__FORM__',LANG='__LANG__',INTENT='__INTENT__',EP={};
 fetch('/ad/track.json',{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){EP=d||{};}).catch(function(){});
 document.addEventListener('click',function(e){
   var a=e.target&&e.target.closest?e.target.closest('a[href*="wa.me"]'):null; if(!a) return;
   try{var b=JSON.stringify({token:TOKEN,lang:LANG,code:'AD-'+LANG.toUpperCase(),page:location.pathname,intent:INTENT,msg:a.getAttribute('data-intent')||'',kw:QP('kw'),campaign:QP('cpn'),adgroup:QP('adg'),device:QP('dev'),gclid:QP('gclid')});
       if(navigator.sendBeacon&&EP.wa_click) navigator.sendBeacon(EP.wa_click,new Blob([b],{type:'text/plain'}));}catch(_){}
   if(typeof gtag==='function') gtag('event','conversion',{send_to:LBL_WA});
 },true);
 function ok(){document.getElementById('enq').hidden=true;document.getElementById('enq-note').hidden=true;document.getElementById('enq-ok').hidden=false;}
 document.getElementById('enq').addEventListener('submit',function(e){
   e.preventDefault();
   var f=e.target,v=function(n){return (f.elements[n]&&f.elements[n].value||'').trim();};
   if(!v('email')){f.elements['email'].focus();return;}
   if(f.elements['consent']&&!f.elements['consent'].checked){f.elements['consent'].focus();return;}
   var payload={token:TOKEN,lang:LANG,code:'AD-'+LANG.toUpperCase()+'F',page:location.pathname,
                company:v('company'),name:(v('name')||v('company')),email:v('email'),country:v('country'),whatsapp:v('whatsapp'),
                whatsapp:v('whatsapp'),kw:QP('kw'),campaign:QP('cpn'),adgroup:QP('adg'),gclid:QP('gclid'),intent:'landing form'};
   var send=function(url){return fetch(url,{method:'POST',headers:{'Content-Type':'text/plain'},body:JSON.stringify(payload)});};
   var fallback=function(){location.href='mailto:__EMAIL__?subject=Enquiry%20'+LANG.toUpperCase()+'&body='+encodeURIComponent(JSON.stringify(payload,null,1));};
   if(EP.lead){send(EP.lead).then(function(r){if(r.ok){ok();if(typeof gtag==='function')gtag('event','conversion',{send_to:LBL_FORM});}else fallback();}).catch(fallback);}
   else{send('/ad/track.json').catch(function(){}).finally(fallback);}
 });
 if(inEU&&!localStorage.getItem('wl_consent')){
   var bar=document.createElement('div');
   bar.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#0f1417;color:#e7edf0;font:14px/1.5 system-ui,sans-serif;padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap';
   var src=document.getElementById('ui-consent');
   bar.innerHTML='<span style="flex:1;min-width:220px"></span>';
   bar.firstChild.textContent=src?src.textContent:'We measure ad clicks only with your consent.';
   var y=document.createElement('button'),n=document.createElement('button');
   y.textContent='OK';y.style.cssText='background:{accent};color:{accent_text};border:0;border-radius:8px;padding:8px 14px;font-weight:600;cursor:pointer';
   n.textContent='No';n.style.cssText='background:transparent;color:#e7edf0;border:1px solid #39454b;border-radius:8px;padding:8px 14px;cursor:pointer';
   document.body.classList.add('consent-open');
   y.onclick=function(){consentDefaults(true);localStorage.setItem('wl_consent','y');document.body.classList.remove('consent-open');bar.remove();};
   n.onclick=function(){consentDefaults(false);localStorage.setItem('wl_consent','n');document.body.classList.remove('consent-open');bar.remove();};
   bar.appendChild(y);bar.appendChild(n);document.body.appendChild(bar);
 }
})();
</script>
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}"{rtl}>
<head>
<meta charset="utf-8">
{CRITICAL_CSS}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta_title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://wiliheng.com/ad/{lang}/">
{hreflang}
<script type="application/ld+json">{jsonld}</script>
<meta property="og:title" content="{meta_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="website">
<style>
 *{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#101417;background:#fff}}
 .wrap{{max-width:1040px;margin:0 auto;padding:0 20px}}
 .hero{{background:{hero_bg};color:{hero_text};padding:54px 0 42px}}
 h1{{font-size:30px;line-height:1.25;margin:0 0 14px}} .lede{{font-size:17px;color:#c6d0d6;max-width:700px;margin:0 0 22px}}
 .btn{{display:inline-block;background:{accent};color:{accent_text};font-weight:700;text-decoration:none;padding:13px 20px;border-radius:10px;margin:0 8px 10px 0}}
 .btn.ghost{{background:transparent;color:#eef3f5;border:1px solid #39454b}}
 .chips{{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:18px 0 0}}
 .chips li{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:6px 12px;font-size:13px;color:#dfe7ea}}
 section{{padding:40px 0}} h2{{font-size:22px;margin:0 0 8px}} .sub{{color:#54626b;margin:0 0 16px;max-width:760px}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}}
 .card{{border:1px solid #e6ebe3;border-radius:14px;padding:16px}} .card b{{display:block;margin-bottom:6px}}
 form#enq{{display:grid;gap:10px;max-width:640px;margin-top:8px}}
 input,select,textarea{{width:100%;padding:12px 14px;border:1px solid #ccd4d9;border-radius:10px;font:inherit;background:#fff;color:#101417}}
 button[type=submit]{{background:{accent};color:{accent_text};border:0;border-radius:10px;padding:13px 20px;font:inherit;font-weight:700;cursor:pointer}}
 footer{{border-top:1px solid #e6eaec;color:#6b7780;font-size:13px;padding:22px 0 40px}}
 a{{color:#3f6b00}}
 .wa-float{{position:fixed;right:16px;bottom:16px;z-index:80;width:56px;height:56px;border-radius:50%;
   background:#25D366;color:#fff;display:flex;align-items:center;justify-content:center;
   box-shadow:0 6px 20px rgba(0,0,0,.28);text-decoration:none;-webkit-tap-highlight-color:transparent}}
 .wa-float:active{{transform:scale(.96)}}
 /* 悬浮按钮不能压住正文：给页面底部留出按钮高度（2026-10-10 截图发现的遮挡） */
 body{{padding-bottom:78px}}
 .answer{{margin:0;padding:16px 18px;border-left:3px solid {accent};background:#f4f7f6;color:#20302c;font-size:15px;line-height:1.7}}
 .answer-wrap{{padding:0}}
 .faq{{padding:36px 0 8px}} .faq h2{{font-size:22px;margin:0 0 14px}}
 .faq h3{{font-size:16px;margin:18px 0 6px}} .faq p{{margin:0;color:#3c4a52;font-size:15px;line-height:1.7}}
 .updated{{color:#6b7780;font-size:13px;padding:18px 0 6px}}
 @media (min-width:900px){{.wa-float{{width:52px;height:52px;right:22px;bottom:22px}}}}
 /* 欧盟同意条出现时把悬浮 WhatsApp 抬高，别被盖住（2026-10-13） */
 body.consent-open .wa-float{{bottom:104px}}
</style>
{js}
</head>
<body>
<div class="hero"><div class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  {hero_first}
  </div>
{faq_block}
  <!-- 手机端常驻悬浮 WhatsApp（2026-10-10 加）：前一天 8 次广告点击 0 次联系动作 →
       把"联系"永远放在拇指可及处。点击由现有 wa.me 埋点自动统计，无需额外 JS。 -->
  <a class="wa-float" href="{wa_whole}" target="_blank" rel="noopener"
     data-intent="{cta_wholesale}" aria-label="{cta_wholesale}">
    <svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2m5.8 14.09c-.24.68-1.4 1.3-1.93 1.35-.53.05-1.03.24-2.93-.61-2.3-1.03-3.74-3.44-3.85-3.6-.11-.16-.92-1.26-.92-2.4 0-1.14.6-1.7.81-1.93.21-.23.46-.29.61-.29h.44c.14 0 .33-.05.51.39.19.45.64 1.56.7 1.67.06.11.1.24.02.39-.08.15-.15.24-.29.38-.14.14-.3.32-.43.43-.14.13-.29.26-.13.53.16.27.71 1.17 1.52 1.9 1.05.94 1.94 1.23 2.21 1.37.27.13.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.22.61-.13.25.09 1.59.75 1.86.89.27.13.45.2.52.31.07.12.07.68-.17 1.36z"/></svg>
  </a>
  </div>
  {hero_second}
  <p class="sub" style="color:#c6d0d6;margin-top:10px;font-size:14px">{hero_note}</p>
  <ul class="chips">{chips}</ul>
</div></div>
{answer_block}

<section><div class="wrap">
  <h2>{gallery_title}</h2>
  <p class="sub">{gallery_more}</p>
  <div class="grid">{gallery}</div>
</div></section>

<section style="background:#f7f9f5"><div class="wrap">
  <h2>{cards_title}</h2><p class="sub">{cards_sub}</p>
  <div class="grid">
    <div class="card"><b>{card1_t}</b>{card1_b}</div>
    <div class="card"><b>{card2_t}</b>{card2_b}</div>
    <div class="card"><b>{card3_t}</b>{card3_b}</div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>{form_title}</h2><p class="sub">{form_sub}</p>
  <p class="sub" style="font-weight:600;color:#2b3a42">{form_note}</p>
  <form id="enq">
    <input name="company" placeholder="{f_company}" required>
    <input id="email2" name="email" type="email" placeholder="{f_email}" required>
    <input name="whatsapp" placeholder="{f_wa}">
    <input name="country" placeholder="{f_country}">
    <label style="font-size:14px;color:#54626b"><input type="checkbox" name="consent" required style="width:auto"> {consent}</label>
    <button type="submit">{form_btn}</button>
  </form>
  <p id="enq-note" class="sub" style="margin-top:10px">{f_email} · WhatsApp +86 181-2488-6695</p>
  <p id="enq-ok" class="sub" hidden style="margin-top:10px;font-weight:600;color:#3f6b00">{form_ok}</p>
</div></section>

<div id="ui-consent" hidden>{consent}</div>
<footer><div class="wrap">{foot_note}<br>{addr}<br><a href="{privacy_url}" style="color:#3f6b00">{privacy_label}</a></div></footer>
{js_body}
</body></html>
"""


def images(limit=6):
    try:
        items = json.loads((BASE / 'products.json').read_text(encoding='utf-8')).get('items') or []
    except Exception:
        return []
    out = []
    for it in items:
        if (it.get('category') or '') in SAFE_CATS and it.get('slug'):
            out.append((it['slug'], it.get('category')))
        if len(out) >= limit:
            break
    return out


def _safe_label(s):
    """图注/alt 的兜底：非德国落地页一个字都不能带刀（Google 审整页）。"""
    for a, b in (('Knife sharpeners', 'Sharpeners'), ('knife sharpeners', 'sharpeners'),
                 ('Knife', 'Kitchen tool'), ('knife', 'kitchen tool'),
                 ('Knives', 'Kitchenware'), ('knives', 'kitchenware')):
        s = s.replace(a, b)
    return s


def build(lang, d):
    cats = images()
    labels = CAT_LABEL.get(lang, {})
    gal = ''.join(
        '<figure style="margin:0"><img src="/assets/products/%s.jpg" alt="%s" loading="lazy" '
        'style="width:100%%;height:170px;object-fit:cover;border-radius:12px;border:1px solid #e6ebe3">'
        '<figcaption style="font-size:12px;color:#6b7780;margin-top:6px">%s</figcaption></figure>'
        % (s, _safe_label(labels.get(cat, cat)), _safe_label(labels.get(cat, cat)))
        for s, cat in cats)
    js = (JS.replace('__TOKEN__', TOKEN).replace('__WA__', WA_LABEL).replace('__FORM__', FORM_LABEL)
             .replace('__LANG__', lang).replace('__INTENT__', d['wa_intent']).replace('__EMAIL__', EMAIL))
    js_head, _, js_body = js.partition('<!--SPLIT-->')
    _tag = '[%s] ' % lang.upper().replace('DE-WARE', 'AT')
    wa_whole = 'https://wa.me/%s?text=%s' % (WHATSAPP, urllib.parse.quote(_tag + d['cta_wholesale']))
    wa_oem = 'https://wa.me/%s?text=%s' % (WHATSAPP, urllib.parse.quote(_tag + 'OEM — ' + d['cta_oem']))
    _hero_kw = {'wa_whole': wa_whole, 'wa_oem': wa_oem,
                'cta_wholesale': d['cta_wholesale'], 'cta_oem': d['cta_oem'],
                'hero_ph': d['hero_ph'], 'hero_btn': d['hero_btn']}
    _hero_a = HERO_BLOCKS['cta'].format(**_hero_kw)
    _hero_b = HERO_BLOCKS['form'].format(**_hero_kw)
    html = PAGE.format(
        CRITICAL_CSS=CRITICAL_CSS,
        hreflang=build_hreflang(lang),
        jsonld=build_jsonld(lang, d),
        answer_block=build_answer(d),
        faq_block=build_faq(d),
        privacy_label=d.get('privacy', 'Privacy policy'),
        privacy_url=('/ad/de/datenschutz.html' if lang == 'de-ware' else '/privacy.html'),
        hero_first=_hero_a if _variant_for(lang) == 'A' else _hero_b,
        hero_second=_hero_b if _variant_for(lang) == 'A' else _hero_a,
        **_theme_for(lang),
        lang=lang, rtl=' dir="rtl"' if d.get('rtl') else '', js=js_head, js_body=js_body,
        meta_title=d['meta_title'], meta_desc=d['meta_desc'], h1=d['h1'], lede=d['lede'],
        wa=WHATSAPP,
        wa_whole=wa_whole,
        wa_oem=wa_oem,
        cta_wholesale=d['cta_wholesale'], cta_oem=d['cta_oem'],
        hero_ph=d['hero_ph'], hero_btn=d['hero_btn'], hero_note=d['hero_note'],
        chips=''.join('<li>%s</li>' % c for c in d['chips']),
        gallery_title=d['gallery_title'],
        gallery_more=d['gallery_more'].replace('{cat}', MULTI % lang),
        gallery=gal, cards_title=d['cards_title'], cards_sub=d['cards_sub'],
        card1_t=d['card1_t'], card1_b=d['card1_b'], card2_t=d['card2_t'], card2_b=d['card2_b'],
        card3_t=d['card3_t'], card3_b=d['card3_b'],
        form_title=d['form_title'], form_sub=d['form_sub'], form_note=d.get('form_note') or '',
        f_company=d['f_company'], f_name=d['f_name'],
        f_email=d['f_email'], f_country=d['f_country'], f_wa=d.get('f_wa','WhatsApp (optional)'),
         consent=d['consent'], form_btn=d['form_btn'], form_ok=d['form_ok'],
        foot_note=d['foot_note'],
        addr='Factory No. 2, Middle Section of Yudong Ninth Road, Yangdong Industrial Park, Yangjiang City, Guangdong, China · since %s' % SINCE)
    return html


HERO_BLOCKS = {
    'cta': ('<div>\n    <a class="btn" href="{wa_whole}" target="_blank" rel="noopener" '
            'data-intent="{cta_wholesale}">{cta_wholesale}</a>\n'
            '    <a class="btn ghost" href="{wa_oem}" target="_blank" rel="noopener" '
            'data-intent="{cta_oem}">{cta_oem}</a>\n   </div>'),
    'form': ('<form id="hero" onsubmit="return false" style="margin-top:18px;max-width:620px;'
             'display:flex;gap:10px;flex-wrap:wrap">\n'
             '    <input name="email" type="email" placeholder="{hero_ph}" '
             'style="flex:1;min-width:240px" required>\n'
             '    <button type="submit" onclick="document.getElementById(\'email2\')&&'
             'document.getElementById(\'email2\').focus()">{hero_btn}</button>\n  </form>'),
}


def _variant_for(lang):
    """首屏 A/B 变体：A=CTA 按钮先（现版）；B=邮箱表单先。
    由每日自动优化按落地页转化数据翻转（见 landing_variant.py）。"""
    try:
        d = json.loads((Path(__file__).resolve().parent / 'ad_ads_i18n.json').read_text(encoding='utf-8'))
        return str((d.get('_hero_variant') or {}).get(lang, 'A')).upper()[:1] or 'A'
    except Exception:
        return 'A'


# 落地页 → 各语言版本（hreflang 用）。英语版是 /ad/us-ware/，德语版是 /ad/de/。
LANG_URLS = {'es': '/ad/es/', 'fr': '/ad/fr/', 'it': '/ad/it/', 'pt': '/ad/pt/', 'nl': '/ad/nl/',
             'sv': '/ad/sv/', 'cs': '/ad/cs/', 'de-ware': '/ad/de-ware/', 'id': '/ad/id/', 'th': '/ad/th/',
             'pl': '/ad/pl/', 'ru': '/ad/ru/', 'ar': '/ad/ar/', 'tr': '/ad/tr/', 'ro': '/ad/ro/',
             'en': '/ad/us-ware/', 'de': '/ad/de/'}
LANG_HTML = {'es': 'es', 'fr': 'fr', 'it': 'it', 'pt': 'pt', 'nl': 'nl', 'pl': 'pl', 'ru': 'ru',
             'ar': 'ar', 'tr': 'tr', 'ro': 'ro', 'en': 'en', 'de': 'de',
             'sv': 'sv', 'cs': 'cs', 'de-ware': 'de', 'id': 'id', 'th': 'th'}   # 2026-10-16：瑞典/捷克/奥地利(无刀德语页)


def build_hreflang(lang):
    """每页列出全部语言版本 + x-default（英语版）。SEO/GEO：多语种互相声明，避免被判重复。"""
    out = []
    for lg, url in LANG_URLS.items():
        out.append('<link rel="alternate" hreflang="%s" href="https://wiliheng.com%s">' % (LANG_HTML[lg], url))
    out.append('<link rel="alternate" hreflang="x-default" href="https://wiliheng.com%s">' % LANG_URLS['en'])
    return '\n'.join(out)


def build_jsonld(lang, d):
    """结构化数据：Organization（含 2018 成立、工厂地址、服务地区）+ WebPage。

    注意：**不加 FAQPage**。GEO 技能明确写的是"FAQ 区块用可见内容实现，商业站点不挂 FAQ schema"，
    而且 Google 已取消大多数站点的 FAQ 富结果 —— 挂了没用还可能被判标记不实。
    """
    c = d.get(lang) or {}
    org = {
        '@context': 'https://schema.org', '@type': 'Organization',
        # ⚠️ 这里**不能写含 "Knives" 的法定全名**：非德国市场的落地页是"无刀厨房口径"，
        # 页面自检会因为出现刀类词直接判失败（2026-10-14 实测被自己的检查拦下）。
        'name': 'Wiliheng',
        'url': 'https://wiliheng.com/',
        'foundingDate': '2018',
        'description': c.get('answer') or c.get('meta_desc') or '',
        'address': {'@type': 'PostalAddress',
                    'streetAddress': 'Factory No. 2, Middle Section of Yudong Ninth Road, Yangdong Industrial Park',
                    'addressLocality': 'Yangjiang', 'addressRegion': 'Guangdong', 'addressCountry': 'CN'},
        'areaServed': [v for v in LANG_URLS if v != 'en'],
        'alternateName': 'Wiliheng Kitchen & Tableware',
        'knowsLanguage': sorted(set(LANG_HTML.values())),
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales',
                          'email': 'sales@wiliheng.com', 'availableLanguage': sorted(set(LANG_HTML.values()))}],
        'sameAs': ['https://wiliheng.com/', 'https://wiliheng.com/b2b/'],
    }
    page = {'@context': 'https://schema.org', '@type': 'WebPage',
            'name': c.get('meta_title') or 'Wiliheng', 'inLanguage': LANG_HTML.get(lang, lang),
            'url': 'https://wiliheng.com' + LANG_URLS.get(lang, '/ad/'),
            'isPartOf': {'@type': 'WebSite', 'url': 'https://wiliheng.com/', 'name': 'Wiliheng'}}
    return json.dumps(org, ensure_ascii=False) + '</script><script type="application/ld+json">' + json.dumps(page, ensure_ascii=False)


def build_answer(d):
    """GEO：把可整段引用的自述放在**前 30% 处**（AI 引用多来自页面靠前部分）。"""
    a = (d or {}).get('answer')
    if not a:
        return ''
    return '<div class="answer-wrap"><div class="wrap"><p class="answer">%s</p></div></div>' % a


def build_faq(d):
    """可见的 FAQ 区块（Q 用 h3，答案一段）—— 给 AI 与用户都能直接引用。"""
    faq = (d or {}).get('faq') or []
    if not faq:
        return ''
    title = (d or {}).get('faq_title') or 'FAQ'
    items = ''.join('<h3>%s</h3><p>%s</p>' % (q, a) for q, a in faq)
    return ('<section class="faq"><div class="wrap"><h2>%s</h2>%s'
            '<p class="updated">Updated: 2026-10</p></div></section>' % (title, items))


DEFAULT_THEME = {'accent': '#b9e56b', 'accent_text': '#12210a', 'hero_bg': '#0f1417', 'hero_text': '#eef3f5'}


def _theme_for(lang):
    """按语种取区域配色（缺失则品牌默认）。配色改动都很克制，便于按转化数据归因。"""
    try:
        d = json.loads((Path(__file__).resolve().parent / 'ad_ads_i18n.json').read_text(encoding='utf-8'))
        th = (d.get('_theme') or {}).get(lang) or {}
    except Exception:
        th = {}
    out = dict(DEFAULT_THEME)
    for k in ('accent', 'accent_text', 'hero_bg', 'hero_text'):
        if th.get(k):
            out[k] = th[k]
    out['accent'] = out['accent']
    return {('theme_' + k if False else k): v for k, v in out.items()}


def main():
    langs = LANGS_DEFAULT
    if '--langs' in sys.argv:
        langs = sys.argv[sys.argv.index('--langs') + 1].split(',')
    data = json.loads((BASE / 'ad_ads_i18n.json').read_text(encoding='utf-8'))
    ok = 0
    for lang in langs:
        d = data.get(lang)
        if not d:
            print('%-4s 跳过（数据里没有该语种）' % lang)
            continue
        html = build(lang, d)
        bad = []
        # 自检：非德国页**不许出现刀类图/刀类词**（政策红线）；必须有 WhatsApp、表单、追踪
        for slug, cat in images():
            if cat not in SAFE_CATS:
                bad.append('刀类图:%s' % slug)
        if 'wa.me' not in html:
            bad.append('缺 WhatsApp')
        # 回归护栏：表单/同意条脚本必须在 </head> 之后，否则 DOM 还没建好就绑定 → 表单失效
        if html.index("getElementById('enq')") < html.index('</head>'):
            bad.append('表单脚本仍在 head（表单会失效）')
        if 'id="enq"' not in html or 'AW-17434685893' not in html:
            bad.append('缺表单或转化码')
        low = html.lower().replace('ножницы', '')   # ножницы=剪刀（安全词），别被词干 'нож'(刀) 误伤
        # 用词边界匹配，别用子串：西语 'mesa'（桌子）、荷兰语 'mes' 都太短，子串会误报
        # 用**词干**匹配（复数也要抓到）：西 cuchillo/cuchillos、法 couteau/couteaux、荷 mes/messen…
        for w in ('knife', 'knives', 'cuchill', 'couteau', 'coltell', 'faca', 'messen', 'nóż', 'noże',
                  'нож', 'سكاك', 'سكين'):
            if w in low:
                bad.append('出现刀类词:%s' % w)
        p = BASE / 'ad' / lang / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html, encoding='utf-8')
        # JS 语法体检（把 <script> 抽出来跑 node --check）
        js_blocks = re.findall(r'<script>(.*?)</script>', html, re.S)
        js_bad = ''
        for i, b in enumerate(js_blocks):
            f = ROOT / ('_chk_%s_%d.js' % (lang, i))
            f.write_text(b, encoding='utf-8')
            r = subprocess.run(['node', '--check', str(f)], capture_output=True)
            f.unlink(missing_ok=True)
            if r.returncode != 0:
                js_bad = r.stderr.decode('utf-8', 'replace').splitlines()[-3:][0][:90]
        print('%-4s ad/%s/index.html  %d 字节 ｜ 相册 %d 张 ｜ %s%s'
              % (lang, lang, len(html), len(images()),
                 '自检通过 ✅' if not bad and not js_bad else '❌ ' + ','.join(bad) + (('JS:' + js_bad) if js_bad else ''),
                 ''))
        ok += 0 if (bad or js_bad) else 1
    print('\n生成 %d/%d 页通过自检' % (ok, len(langs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
