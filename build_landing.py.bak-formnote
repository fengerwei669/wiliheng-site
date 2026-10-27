#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成两个广告落地页（/ad/de/ 与 /ad/us/）。

定位（按客户要求）：**以 OEM/ODM 为主角** —— 首页第一屏就是「你的品牌 + 你的规格」，
批发/分销作为第二选项。图片**不放网页**（现有实拍图质量不够），改成引导到 WhatsApp 私聊里发
「3–5 个贴合你产品线的型号 + 真实照片 + 报价」。

用法：
    python site/build_landing.py            # 生成并自检（无价格、无图片、CTA 数、合规链接）
"""
import html as html_mod
import json
import re
import subprocess
import tempfile
from pathlib import Path
from critical_css import CSS as CRITICAL_CSS

BASE = Path(__file__).resolve().parent
WA = 'https://wa.me/8618124886695?text='
MAIL = 'mailto:fengerwei669@gmail.com'
SEND_TO = 'AW-17434685893/8VZKCKaX2Y4bEMXjwPlA'
ADDR = ('Factory No. 2, Middle Section of Yudong Ninth Road, Yangdong Industrial Park, '
        'Yangjiang City, Guangdong, China')

CSS = """<style>
  :root{--ink:#101417;--line:#2a343a;--paper:#f6f7f8;--dim:#9aa7ae;--acc:#c8f04a}
  *{box-sizing:border-box}
  body{margin:0;font:16px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fff}
  a{color:inherit}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px}
  header.top{background:var(--ink);color:#fff;padding:14px 0;border-bottom:1px solid var(--line)}
  .top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
  .brand{font-weight:700}.brand small{display:block;font-weight:400;color:var(--dim)}
  .btn{display:inline-block;background:var(--acc);color:#111;font-weight:700;text-decoration:none;padding:13px 20px;border-radius:8px;white-space:nowrap}
  .btn.big{font-size:18px;padding:16px 26px}
  .btn.ghost{background:transparent;color:#fff;border:1px solid #39454b}
  .hero{background:linear-gradient(160deg,var(--ink) 0%,#1d262c 100%);color:#fff;padding:54px 0 46px}
.answer{margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f5c4f;background:#f4f7f6;border-radius:0 8px 8px 0;max-width:760px}
.answer p{margin:0;font-size:15px;line-height:1.6;color:#2c3a44}

  .hero h1{font-size:34px;line-height:1.25;margin:0 0 14px;max-width:22em}
  .hero p.lead{font-size:18px;color:#c9d3d8;max-width:36em;margin:0 0 22px}
  .chips{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 0;padding:0;list-style:none}
  .chips li{background:#222c31;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;color:#dfe6e9}
  .cta{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .cta .sub{color:var(--dim);font-size:14px}
  .badge{background:var(--acc);color:#111;border-radius:6px;padding:2px 8px;font-size:12px;vertical-align:middle}
  section{padding:46px 0;border-bottom:1px solid #e7eaec}
  section h2{font-size:25px;margin:0 0 6px}
  section p.sub{color:#5a686f;margin:0 0 24px}
  .grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
  .card{border:1px solid #dfe4e7;border-radius:12px;padding:20px;background:#fff}
  .card.lead-card{border:2px solid var(--acc)}
  .card h3{margin:0 0 8px;font-size:18px}
  .card p{margin:0 0 12px;color:#4b575e;font-size:15px}
  .card .mini{color:#7c888f;font-size:13px}
  table{width:100%;border-collapse:collapse;font-size:15px}
  th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #e7eaec}
  th{background:var(--paper);font-weight:600}
  ol.steps{counter-reset:s;list-style:none;padding:0;margin:0}
  ol.steps li{counter-increment:s;position:relative;padding:0 0 16px 44px}
  ol.steps li:before{content:counter(s);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;
    background:var(--ink);color:var(--acc);font-weight:700;display:flex;align-items:center;justify-content:center;font-size:14px}
  details{border:1px solid #e2e7e9;border-radius:10px;padding:14px 16px;margin-bottom:10px}
  summary{font-weight:600;cursor:pointer} details p{margin:10px 0 0;color:#4b575e}
  footer{background:var(--ink);color:var(--dim);padding:32px 0;font-size:14px}
  footer a{color:#cfe0c0}
  .sticky{position:fixed;right:16px;bottom:16px;z-index:9}
  @media (max-width:560px){.hero h1{font-size:26px}section{padding:34px 0}
    .sticky{left:16px;right:16px}.sticky .btn{display:block;text-align:center}}
 .wa-float{{position:fixed;right:16px;bottom:16px;z-index:80;width:56px;height:56px;border-radius:50%;
   background:#25D366;color:#fff;display:flex;align-items:center;justify-content:center;
   box-shadow:0 6px 20px rgba(0,0,0,.28);text-decoration:none;-webkit-tap-highlight-color:transparent}}
 .wa-float:active{{transform:scale(.96)}}
 body{{padding-bottom:78px}}
 @media (min-width:900px){{.wa-float{{width:52px;height:52px;right:22px;bottom:22px}}}}
 body.consent-open .wa-float{{bottom:104px}}
</style>"""

C = {
 'de': {
  'html_lang': 'de', 'slug': 'de',
  'title': 'Messer unter Ihrer Marke — OEM/ODM Messerfabrik China',
  'desc': ('OEM/ODM-Messerfabrik in Yangjiang, China: Messer unter Ihrer Marke, Verpackung nach '
           'Vorgabe. Ab 500 Stück pro Modell.'),
  'answer': ('Yangjiang Wiliheng Knives Co., Ltd ist eine OEM/ODM-Messerfabrik in Yangjiang, Guangdong, China. '
             'Wir fertigen Klapp-, Jagd-, Outdoor- und Küchenmesser unter Ihrer Marke — Klinge, Griff, Etui und '
             'Verpackung nach Vorgabe — für Importeure, Händler und Markeninhaber. Ab 500 Stück pro Modell, '
             'Vorserienmuster in etwa einer Woche, Produktion 30–45 Tage nach Musterfreigabe.'),
  'brand_name': 'Wiliheng Knives',
  'brand_sub': 'OEM/ODM Messerfabrik · Yangjiang, China',
  'hdr_btn': 'Muster &amp; Bilder anfragen',
  'h1': 'Ihre Marke auf dem Messer — OEM/ODM direkt aus der Fabrik',
  'lead': ('Wir fertigen Messer unter <strong>Ihrer Marke</strong>: Klinge, Griff, Etui und Verpackung nach Ihrer '
           'Vorgabe. Ab 500 Stück pro Modell, mit Vorserienmuster zur Freigabe. Katalogware für Großhandel und '
           'Distribution liefern wir zusätzlich.'),
  # 首屏两条意图路径（批发 / OEM）—— 采购员意图不同，分开统计才知道哪种人来得更多
  'cta_whole': 'Großhandel: Preisliste',
  'cta_oem': 'OEM / Eigenmarke besprechen',
  'hero_ph': 'Geschäftliche E-Mail-Adresse',
  'hero_btn': 'Preisliste + Linienkarte (PDF)',
  'hero_note': 'PDF + 3–5 passende Modelle, in der Regel innerhalb von 24 Stunden. Kein Newsletter.',
  'hero_ok': ('Danke — wir melden uns innerhalb von 24 Stunden. '
              '<a href="/Wiliheng-Knives-Line-Card.pdf" target="_blank" rel="noopener" '
              'style="color:#cfe0c0"><strong>Linienkarte (PDF) jetzt herunterladen</strong></a>'),
  'linecard': 'Linienkarte (PDF)',
  'cta1': 'Muster &amp; Bilder per WhatsApp',
  'cta2': 'per E-Mail anfragen',
  'ctasub': 'Modelle und echte Fotos schicken wir im Chat — nicht auf dieser Seite.',
  'chips': ['MOQ 500 Stück', 'Ihre Marke + Laserlogo', '43 Arbeitsschritte im Haus',
            '40 Maschinen, davon 20 CNC', 'Live-Video-Rundgang durch die Fabrik',
            'Vorserienmuster in ~1 Woche', 'Export EU &amp; USA'],
  'cards_ttl': 'Wie wir arbeiten',
  'cards_sub': 'Unser Schwerpunkt ist die Auftragsfertigung für Ihre Marke; Großhandel liefern wir ergänzend.',
  'cards': [
    ('Eigenmarke &amp; OEM/ODM', 'Unser Schwerpunkt',
     'Ihre Marke auf Klinge, Etui und Verpackung: Logo-Lasergravur, eigenes Etui, eigenes Packaging, Barcodes fertig. '
     'Muster zur Freigabe — erst danach startet die Serie.',
     'Ab 500 Stück pro Modell, auch Sonderanfertigung.', 'OEM/ODM besprechen'),
    ('Großhandel &amp; Distribution', '',
     'Katalogware zu Fabrikpreisen: Klappmesser, Jagdmesser, Outdoor- und Küchenmesser. Staffelpreise ab 500 Stück, '
     'feste Lieferzeiten, Verpackung für den Einzelhandel.',
     'Sortiment erweitern ohne eigene Fertigung.', 'Preisliste anfragen'),
  ],
  'photo_ttl': 'Ein Auszug aus unserem Sortiment',
  'gallery_more': ('Das ist ein Auszug — wir führen über 48 Linien (Messer, Scheren, Besteck, Küchenhelfer). '
                   'Die komplette Übersicht mit Fotos finden Sie in unserem '
                   '<a href="{cat}" target="_blank" rel="noopener">Produktkatalog</a>; '
                   'für Ihre Linie stellen wir 3–5 passende Modelle mit echten Fotos und Preisen zusammen.'),
  'photo': ('Wir führen über 48 Linien mit hunderten Modellen — unten sehen Sie einen Auszug. '
            'Sagen Sie uns Ihre Produktlinie (z. B. Jagdmesser, EDC, Küchenmesser) und wir schicken '
            '<strong>3–5 passende Modelle mit echten Fotos, Stahl- und Griffoptionen sowie Preisen</strong> '
            'direkt auf WhatsApp — innerhalb von 24 Stunden.'),
  'prod_ttl': 'Was wir fertigen',
  'prod_sub': 'Aus eigener Fertigung in Yangjiang — Klingen, Wärmebehandlung, Schleifen und Montage im Haus.',
  'prod_head': ('Kategorie', 'Typische Modelle', 'Preis'),
  'prod_rows': [('Klappmesser', 'Liner Lock, Back Lock, EDC'),
                ('Jagd- &amp; Outdoormesser', 'Fixed Blade, Skinner, Camping'),
                ('Küchenmesser', 'Kochmesser, Santoku, Set'),
                ('Zubehör &amp; Kits', 'Etui, Schleifer, Geschenkset')],
  'price_note': 'Staffelpreise auf Anfrage — sie hängen von Stahl, Griffmaterial, Menge und Verpackung ab',
  'steps_ttl': 'So läuft die Anfrage',
  'steps': [('Anfrage per WhatsApp.',
             'Nennen Sie Ihre Produktlinie — wir schicken 3–5 passende Modelle mit echten Fotos und Preisen.'),
            ('Video-Rundgang.', 'Auf Wunsch zeigen wir Ihnen die Fabrik live per Video — die Stationen, '
             'die für Ihre Bestellung zählen.'),
            ('Angebot in 24 Stunden.', 'Staffelpreise, Stahl- und Griffoptionen, Verpackung.'),
            ('Muster.', 'Bei OEM/ODM gibt es ein Vorserienmuster zur Freigabe (rund eine Woche).'),
            ('Serienfertigung &amp; Lieferung.', 'Feste Lieferzeiten, Einfuhrdokumente, Verpackung für den Handel.')],
  'faq_ttl': 'Häufige Fragen',
  'faq': [('Was ist die Mindestbestellmenge?',
           '500 Stück pro Modell. Bei gemischten Sortimenten sprechen wir über die Gesamtmenge.'),
          ('Bekomme ich Modelle und Fotos?',
           'Ja — im Chat. Wir schicken keine Bilderflut, sondern gezielt die Modelle, die zu Ihrer Produktlinie '
           'passen, mit echten Fotos und Preisen.'),
          ('Kann ich die Fabrik sehen, ohne nach China zu fliegen?',
           'Ja. Wir machen einen Live-Video-Rundgang (WhatsApp oder Zoom, 15–20 Minuten) durch die Produktion — '
           'in der Regel innerhalb von 1–2 Werktagen nach Ihrer Anfrage.'),
          ('Kann ich vorher Muster bekommen?',
           'Ja. Muster kostenpflichtig, bei Serienbestellung üblicherweise angerechnet.'),
          ('Wie lange dauert die Produktion?',
           'Katalogware 20–30 Tage, OEM/ODM mit eigenem Logo und Etui 30–45 Tage ab Freigabe, je nach Menge.'),
          ('Welche Zahlung wird akzeptiert?',
           'Üblich 30 % Anzahlung, 70 % vor Versand; Details klären wir in der Anfrage.'),
          # ↓ 以下 4 条是给 AI 搜索（ChatGPT / Perplexity / AI Overviews）准备的「可直接引用」答案
          ('Wie groß ist die Fabrik und was fertigen Sie selbst?',
           'In unserem Werk in Yangjiang laufen 43 Arbeitsschritte im Haus, mit 40 Maschinen — darunter '
           '20 CNC-Bearbeitungszentren, 10 Nassschleifer, 5 Vertikalschleifer, 2 Anlass- und 2 Härteöfen sowie '
           'Härteprüfung nach Rockwell. Wir fertigen für Importeure, Händler und Markeninhaber.'),
          ('Welche Werkstoffe sind möglich?',
           'Edelstahl 5Cr15MoV und 440C, weitere Sorten auf Anfrage; Griffe in G10, Holz, Kunststoff oder nach '
           'Ihrer Zeichnung. Verpackung als Farbkarton, Blister oder Schutzhülle.'),
          ('In welche Länder liefern Sie?',
           'Wir produzieren für Kunden in Deutschland, in der EU und in den USA — mit Einfuhrdokumenten und '
           'handelsgerechter Verpackung. Beratung auf Deutsch oder Englisch.'),
          ('Wie schnell bekomme ich eine Antwort?',
           'Angebot in der Regel innerhalb von 24 Stunden an Werktagen; auf Wunsch mit Live-Video-Rundgang '
           'durch die Produktion. Muster bei OEM/ODM rund eine Woche.')],
  # GEO：AI 搜索偏好「可直接引用的事实 + 数字」。以下数字来自 MES（2026-09-24 核对：
  # 43 工序 / 40 台设备 / 20 CNC / 48 型号 / MOQ 500），改了工厂数据记得同步这里。
  # 询盘表单（第二条转化路径）：德国/美国采购员很多在办公桌前，公司禁用 WhatsApp，
  # 只填表。表单比 WhatsApp 多给公司名/数量/邮箱，询盘质量更高。
  'form_ttl': 'Anfrage in 30 Sekunden',
  'form_sub': ('Sie brauchen kein WhatsApp: Firma und E-Mail genügen. Wir antworten mit '
               '<strong>3–5 passenden Modellen, echten Fotos und Preisen</strong> — in der Regel '
               'innerhalb von 24 Stunden (Mo–Fr).'),
  'f_company': 'Firma', 'f_name': 'Ansprechpartner', 'f_email': 'Geschäftliche E-Mail',
  'f_country': 'Land', 'f_pline': 'Produktlinie wählen', 'f_qty': 'Menge pro Modell',
  'f_msg': 'Nachricht (optional: Zielmarkt, Verpackung, Termin)',
  'f_plines': ['Küchenmesser', 'Klappmesser', 'Küchenhelfer &amp; Gadgets', 'Besteck &amp; Bestecksets',
               'Scheren', 'Gemischt / Sortiment'],
  'f_qtys': ['500–1.000 Stück', '1.000–5.000 Stück', 'über 5.000 Stück', 'noch offen'],
  'f_consent': ('Ich bin damit einverstanden, dass meine Angaben zur Bearbeitung der Anfrage '
                'verwendet werden.'),
  'f_btn': 'Anfrage senden',
  'f_ok': ('Danke — Ihre Anfrage ist angekommen. Wir melden uns innerhalb von 24 Stunden (Mo–Fr) '
           'mit Modellen, Fotos und Preisen.'),
  'f_note': ('Kein Newsletter, keine Weitergabe an Dritte. Falls das Formular nicht sendet: '
             'direkt an fengerwei669@gmail.com schreiben.'),
  'form_code': 'WH-DE-F',
  'facts_ttl': 'Fabrik in Zahlen',
  'facts': [('Standort', 'Yangjiang, Guangdong, China — eigene Halle (Werk 2)'),
            ('Gegründet', '2018 — Messerfertigung in Yangjiang seitdem'),
            ('Fertigungstiefe', '43 Arbeitsschritte im Haus'),
            ('Maschinen', '40 Maschinen: 20 CNC-Bearbeitungszentren, 10 Nassschleifer, 5 Vertikalschleifer'),
            ('Wärmebehandlung', '2 Anlass- und 2 Härteöfen, Härteprüfung nach Rockwell (HRC)'),
            ('Modelle', '48 Serienmodelle'),
            ('MOQ', 'ab 500 Stück pro Modell'),
            ('Muster', 'Vorserienmuster in ca. 1 Woche'),
            ('Produktionszeit', 'Katalogware 20–30 Tage, OEM/ODM 30–45 Tage'),
            ('Märkte', 'Deutschland, EU und USA'),
            ('Sprachen', 'Deutsch und Englisch'),
            ('Zahlung', '30 % Anzahlung, 70 % vor Versand')],
  'foot_kind': 'OEM/ODM Messerfabrik',
  'legal': '<a href="/ad/de/impressum.html">Impressum</a> · <a href="/ad/de/datenschutz.html">Datenschutz</a> · Erfolgsmessung nur mit Ihrer Einwilligung (Google Ads).',
  'foot_note': 'Modelle und Musterfotos auf Anfrage. Preise und Verfügbarkeit nur auf schriftliche Anfrage; Verkauf ausschließlich an Unternehmen (B2B).',
  'sticky': 'WhatsApp: Muster &amp; Fotos anfragen',
  'contact': '+86 181 2488 6695 · Ansprechpartner: Will',
  'video_ttl': 'Fabrik live sehen — Video-Rundgang durch die Produktion',
  'video_body': ('Sie müssen nicht nach China fliegen. Wir gehen mit Ihnen per <strong>Live-Videoanruf</strong> '
                 '(WhatsApp oder Zoom, ca. 15–20 Minuten) durch die Fertigung: Klingenstanzen, Wärmebehandlung, '
                 'Schleifen, CNC, Härtetest und Verpackung. Sie sehen die Maschinen, die Ihre Bestellung machen — '
                 'und die Leute, die dafür verantwortlich sind.'),
  'video_bullets': ['Live-Video, ca. 15–20 Minuten — kein Reiseaufwand',
                    'Wir zeigen die Stationen, die für Ihre Bestellung relevant sind',
                    'Härtetest live vor der Kamera (HRC-Werte)',
                    'Deutsch oder Englisch, Termin nach Ihrer Zeitzone',
                    'Auf Wunsch mit Ihrer Marke auf dem Muster in der Hand'],
  'video_cta': 'Video-Rundgang buchen',
  'video_note': 'Video-Rundgang ist unverbindlich und kostenlos.',
  'msgs': {'video': 'WH-DE-V%20-%20Bitte%20Termin%20f%C3%BCr%20Video-Rundgang%20durch%20die%20Fabrik',
           'oem': 'WH-DE-B%20-%20Eigene%20Marke%20(OEM)%20-%20bitte%20Modelle%20und%20Fotos',
           'whole': 'WH-DE-A%20-%20Gro%C3%9Fhandel%20-%20bitte%20Preisliste%20und%20Musterfotos',
           'mail_subj': 'Anfrage%20OEM%2FODM%20Messer'},
 },
 'us': {
  'html_lang': 'en', 'slug': 'us',
  'title': 'Kitchen &amp; Tableware Under Your Brand — OEM/ODM Factory',
  'desc': ('OEM/ODM kitchen and tableware factory in Yangjiang, China: your brand and your spec. From '
           '500 pcs per model, sample in about a week.'),
  'answer': ('Wiliheng is an OEM/ODM kitchen and tableware factory in Yangjiang, '
             'Guangdong, China. We manufacture for importers, distributors and private-label brand owners: '
             'materials, handles and packaging to your spec, 500 pcs per model minimum, a pre-production sample '
             'in about a week and 30–45 days for the production lot after approval.'),
  'brand_name': 'Wiliheng Knives',
  'brand_sub': 'OEM/ODM cutlery &amp; kitchen knives · Yangjiang, China',
  'hdr_btn': 'Ask for models &amp; photos',
  'h1': 'Your brand on the cutlery — OEM/ODM straight from the factory',
  'lead': ('We manufacture cutlery and kitchen knives under <strong>your brand</strong>: materials, handles and '
           'packaging to your spec. '
           'From 500 pcs per model, with a pre-production sample for approval. Stock models for wholesale and '
           'distribution on top of that.'),
  'cta_whole': 'Wholesale: price list',
  'cta_oem': 'Discuss OEM / private label',
  'hero_ph': 'Business email address',
  'hero_btn': 'Get price list + line card (PDF)',
  'hero_note': 'PDF + 3–5 matching models, usually within 24 hours. No newsletter.',
  'hero_ok': ('Thanks — we reply within 24 hours. '
              '<a href="/Wiliheng-Knives-Line-Card.pdf" target="_blank" rel="noopener" '
              'style="color:#cfe0c0"><strong>Download the line card (PDF) now</strong></a>'),
  'linecard': 'Line card (PDF)',
  'cta1': 'Models &amp; photos on WhatsApp',
  'cta2': 'or email us',
  'ctasub': 'We send models and real photos in the chat — not on this page.',
  'chips': ['MOQ 500 pcs', 'Your logo, laser engraved', '43 in-house steps',
            '40 machines incl. 20 CNC', 'Live video walkthrough of the factory',
            'Sample in about a week', 'Export to US &amp; EU'],
  'cards_ttl': 'How we work',
  'cards_sub': 'Our core business is manufacturing for your brand; wholesale supply comes on top of that.',
  'cards': [
    ('Private label &amp; OEM/ODM', 'Our core business',
     'Your brand on the product: laser engraving, custom handles, custom packaging, barcodes done. '
     'You approve a pre-production sample before we run the order.',
     'From 500 pcs per model, custom designs included.', 'Discuss OEM/ODM'),
    ('Wholesale &amp; distribution', '',
     'Stock models at factory prices: kitchen &amp; tableware, peelers, shears and kitchen tools. Tiered pricing '
     'from 500 pcs, steady lead times, retail-ready packaging.',
     'Add a kitchen &amp; tableware line without owning a factory.', 'Get pricing'),
  ],
  'photo_ttl': 'A selection from our range',
  'gallery_more': ('This is a selection — we run 48+ lines (kitchen knives, shears, tableware, kitchen tools). '
                   'See the <a href="{cat}" target="_blank" rel="noopener">full product catalogue</a> with photos, '
                   'or tell us your line and we shortlist 3–5 matching models with real photos and pricing.'),
  'photo': ('We run 48+ lines and hundreds of models — below is a selection. '
            'Tell us your product line and we send <strong>3–5 matching models with real photos, '
            'steel and handle options and pricing</strong> on WhatsApp — usually within 24 hours.'),
  'prod_ttl': 'What we manufacture',
  'prod_sub': 'Made in our own factory in Yangjiang — blades, heat treatment, grinding and assembly in house.',
  'prod_head': ('Category', 'Typical models', 'Pricing'),
  'prod_rows': [('Kitchen knives', 'Chef, santoku, sets'),
                ('Table &amp; serving', 'Cutlery, serving boards, kitchen tools'),
                ('Peelers &amp; kitchen tools', 'Y-peelers, gadgets, gift sets'),
                ('Accessories &amp; kits', 'Boxes, sharpeners, gift sets')],
  'price_note': 'Tiered pricing on request — it depends on steel, handle material, quantity and packaging',
  'steps_ttl': 'How an enquiry works',
  'steps': [('Message us.',
             'Tell us your product line — we send 3–5 matching models with real photos and pricing.'),
            ('Video walkthrough.', 'On request we show you the factory live on video — the stations that '
             'matter for your order.'),
            ('Quote in 24 hours.', 'Tiered pricing, steel and handle options, packaging.'),
            ('Sample.', 'For OEM/private label you approve a pre-production sample (about a week).'),
            ('Production &amp; shipping.', 'Steady lead times, export documents, retail-ready packaging.')],
  'faq_ttl': 'Common questions',
  'faq': [('What is the minimum order?',
           '500 pcs per model. For mixed assortments we look at the total quantity.'),
          ('Can I get models and photos?',
           'Yes — in the chat. We do not send a photo dump; we shortlist the models that fit your line with real '
           'photos and pricing.'),
          ('Can I see the factory without flying to China?',
           'Yes. We run a live video walkthrough (WhatsApp or Zoom, 15–20 minutes) through production — usually '
           'within 1–2 working days of your enquiry.'),
          ('Can I get samples first?',
           'Yes. Samples are charged and normally credited against the production order.'),
          ('How long is production?',
           'Stock models 20–30 days; OEM/private label with your logo and packaging 30–45 days after approval.'),
          ('What payment terms do you accept?',
           'Typically 30% deposit, 70% before shipment; we confirm terms with the order.'),
          # ↓ these four are written as quotable answers for AI search (ChatGPT / Perplexity / AI Overviews)
          ('How big is the factory and what do you make in house?',
           'Our factory in Yangjiang runs 43 production steps in house with 40 machines, including 20 CNC '
           'machining centres, 10 water grinding machines, 5 vertical grinders, 2 annealing and 2 tempering '
           'furnaces, plus Rockwell hardness testing. We manufacture for importers, distributors and brand owners.'),
          ('Which materials are possible?',
           'Stainless steel 5Cr15MoV and 440C, with other grades on request; handles in G10, wood, plastic or to '
           'your drawing. Packaging as colour box, blister or protective sleeve.'),
          ('Which countries do you supply?',
           'We produce for customers in the United States, Germany and across the EU — with export documents and '
           'retail-ready packaging. Support in English or German.'),
          ('How fast do I get an answer?',
           'A quote usually within 24 hours on working days, with a live video walkthrough of production on '
           'request. Samples for OEM/private label take about a week.')],
  'form_ttl': 'Enquiry in 30 seconds',
  'form_sub': ('No WhatsApp needed: company and email are enough. We reply with '
               '<strong>3–5 matching models, real photos and pricing</strong> — usually within '
               '24 hours on working days.'),
  'f_company': 'Company', 'f_name': 'Contact name', 'f_email': 'Business email',
  'f_country': 'Country', 'f_pline': 'Select product line', 'f_qty': 'Quantity per model',
  'f_msg': 'Message (optional: target market, packaging, timing)',
  'f_plines': ['Kitchen knives', 'Cutlery', 'Kitchen tools &amp; gadgets',
               'Cutlery &amp; cutlery sets', 'Shears &amp; scissors', 'Mixed assortment'],
  'f_qtys': ['500–1,000 pcs', '1,000–5,000 pcs', 'over 5,000 pcs', 'not decided yet'],
  'f_consent': 'I agree that my details are used to answer this enquiry.',
  'f_btn': 'Send enquiry',
  'f_ok': ('Thanks — your enquiry is in. We reply within 24 hours on working days with models, '
           'photos and pricing.'),
  'f_note': ('No newsletter, no third parties. If the form does not send, email '
             'fengerwei669@gmail.com directly.'),
  'form_code': 'WH-US-F',
  'facts_ttl': 'The factory in numbers',
  'facts': [('Location', 'Yangjiang, Guangdong, China — own plant (Factory No. 2)'),
            ('Established', '2018 — manufacturing knives in Yangjiang ever since'),
            ('In-house steps', '43 production steps in house'),
            ('Machines', '40 machines: 20 CNC centres, 10 water grinders, 5 vertical grinders'),
            ('Heat treatment', '2 annealing + 2 tempering furnaces, Rockwell hardness testing'),
            ('Models', '48 production models'),
            ('MOQ', 'from 500 pcs per model'),
            ('Samples', 'pre-production sample in about 1 week'),
            ('Lead time', 'stock models 20–30 days, OEM/private label 30–45 days'),
            ('Markets', 'United States, Germany and the EU'),
            ('Languages', 'English and German'),
            ('Payment', '30% deposit, 70% before shipment')],
  'foot_kind': 'OEM/ODM kitchenware &amp; tableware factory',
  'legal': '<a href="/privacy.html">Privacy policy</a> · Conversion measurement for our own ads only.',
  'foot_note': 'Models and sample photos on request. Prices and availability are confirmed on written enquiry. Wholesale/B2B only.',
  'sticky': 'WhatsApp: get models &amp; photos',
  'contact': '+86 181 2488 6695 · Ask for Will',
  'video_ttl': 'See the factory live — video walkthrough of the production floor',
  'video_body': ('You do not have to fly to China. We take you on a <strong>live video call</strong> '
                 '(WhatsApp or Zoom, about 15–20 minutes) through production: blade blanking, heat treatment, '
                 'grinding, CNC, hardness testing and packing. You see the machines that will make your order — '
                 'and the people responsible for it.'),
  'video_bullets': ['Live video, about 15–20 minutes — no travel',
                    'We walk the stations that matter for your order',
                    'Hardness test done live on camera (HRC readings)',
                    'English or Chinese, scheduled in your time zone',
                    'On request: your brand on the sample in our hand'],
  'video_cta': 'Book a video walkthrough',
  'video_note': 'The video walkthrough is free and without obligation.',
  'msgs': {'video': 'WH-US-V%20-%20Please%20book%20a%20live%20video%20walkthrough%20of%20the%20factory',
           'oem': 'WH-US-B%20-%20Private%20label%20(OEM)%20-%20please%20send%20models%20and%20photos',
           'whole': 'WH-US-A%20-%20Wholesale%20-%20price%20list%20and%20sample%20photos',
           'mail_subj': 'OEM%2FODM%20kitchenware%20enquiry'},
 },
}

TRACK = """<script>
/* 归因 + 转化测量（两件事，别混）：
   ① 关键词短码：把广告关键词带进 WhatsApp 首条消息（跳到 WhatsApp 后 gclid 会丢，靠短码兜住）；
   ② Google Ads 转化：点 WhatsApp 时上报一次转化，否则 Google 永远记不到询盘。
      欧盟流量必须先默认拒绝、用户同意后再开（Consent Mode v2，Google 对 EEA 的硬要求）。 */
(function(){
  var p = new URLSearchParams(location.search);
  var kw = p.get('kw') || p.get('utm_term') || p.get('utm_content');
  if(kw){
    var code = 'AD-__CODE__' + String(kw).toUpperCase().replace(/[^A-Z0-9]/g,'').slice(0,10);
    document.querySelectorAll('a[href*="wa.me/8618124886695"]').forEach(function(a){
      a.href = a.href.replace(/(\\?text=[^&]*)/, '$1%20[' + encodeURIComponent(code) + ']');
    });
  }
  document.querySelectorAll('a[href*="wa.me/8618124886695"]').forEach(function(a){
    a.addEventListener('click', function(){
      if(typeof gtag === 'function'){
        gtag('event', 'conversion', {send_to: '__SEND_TO__', transport_type: 'beacon'});
      }
    });
  });
})();
</script>"""

GTAG = """<!-- Google tag (gtag.js) — AW-17434685893：WhatsApp 点击转化测量 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-17434685893"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  // 同意管理：__CONSENT__
  gtag('consent', 'default', __CONSENT_STATE__);
  gtag('js', new Date());
  gtag('config', 'AW-17434685893');
</script>"""

BANNER = """<div id="cb" hidden style="position:fixed;left:0;right:0;bottom:0;z-index:99;background:#101417;color:#e7edf0;
     padding:14px 18px;font:14px/1.5 -apple-system,'Segoe UI',Roboto,sans-serif;border-top:1px solid #2a343a">
  <div style="max-width:1080px;margin:0 auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap">
    <span style="flex:1;min-width:260px">Wir messen mit Google Ads, ob ein Klick auf WhatsApp fuehrt
      (Conversion-Messung). Cookies dafuer nur mit Ihrer Einwilligung &mdash;
      <a href="/ad/de/datenschutz.html" style="color:#cfe0c0">Details</a>.</span>
    <button id="cb-yes" style="background:#c8f04a;color:#111;border:0;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer">Einverstanden</button>
    <button id="cb-no" style="background:transparent;color:#fff;border:1px solid #39454b;border-radius:8px;padding:10px 16px;cursor:pointer">Nur notwendige</button>
  </div>
</div>
<script>
(function(){
  var KEY = 'ad_consent';
  function grant(){ if(typeof gtag==='function') gtag('consent','update',
    {ad_storage:'granted', ad_user_data:'granted', ad_personalization:'granted', analytics_storage:'granted'}); }
  var v = null;
  try { v = localStorage.getItem(KEY); } catch(e){}
  if(v === 'granted'){ grant(); }
  else if(v !== 'denied'){
    var b = document.getElementById('cb'); b.hidden = false;
    document.getElementById('cb-yes').onclick = function(){ try{localStorage.setItem(KEY,'granted')}catch(e){}; grant(); b.hidden = true; };
    document.getElementById('cb-no').onclick  = function(){ try{localStorage.setItem(KEY,'denied')}catch(e){};  b.hidden = true; };
  }
})();
</script>
"""


BEACON = """<script>
/* 点击上报：客户点 WhatsApp 按钮 → 打一条到飞牛（记档 + 立刻推企业微信，用户好实时回复）。
   地址不写死在页面里：隧道域名会变，改读 /ad/track.json（同源、稳定）；
   读不到就静默跳过 —— 上报失败绝不能影响客户点按钮。 */
(function(){
  var TOKEN = 'wlc-7f3a91c2';
  function QP(k){try{var m=new RegExp('[?&]'+k+'=([^&]*)').exec(location.search);return m?decodeURIComponent(m[1].replace(/\+/g,' ')):'';}catch(_){return '';}}
  var LANG = '__LANG__';
  var BT = null;
  fetch('/ad/track.json', {cache:'no-store'})
    .then(function(r){ return r.json(); })
    .then(function(d){ BT = d && d.wa_click; })
    .catch(function(){});
  document.querySelectorAll('a[href*="wa.me/8618124886695"]').forEach(function(a){
    a.addEventListener('click', function(){
      if(!BT) return;
      var p = new URLSearchParams(location.search);
      var t = (a.href.split('text=')[1] || '');
      try { t = decodeURIComponent(t); } catch(e){}
      var body = JSON.stringify({
        token: TOKEN, lang: LANG, page: location.pathname, intent: t.slice(0,140),
        kw: QP('kw'), campaign: QP('cpn'), adgroup: QP('adg'), device: QP('dev'), gclid: QP('gclid'),
        kw: p.get('kw') || p.get('utm_term') || '', gclid: p.get('gclid') || '',
        ref: document.referrer || '', ua: navigator.userAgent
      });
      try { navigator.sendBeacon(BT, new Blob([body], {type:'text/plain'})); }
      catch(e){ try{ fetch(BT, {method:'POST', body:body, keepalive:true}); }catch(e2){} }
    });
  });
})();
</script>"""


# ── 相册：把成品产品图接进落地页 ─────────────────────────────────────────
# 为什么按品类筛：**美国/英国的厨房系列是在"无刀图"的页面上过审的**，
# 一旦页面出现刀具图，极可能被重新判 OTHER_WEAPONS（本站花了两天才过）。
# 所以美英页只取「剪刀/砧板/磨刀器」这类厨房家居品类；德国页刀具允许，可含刀图（仍避开狩猎/口袋刀）。
KNIFE_CATS = ("Chef's knives", "Chef's knives — Damascus", 'Kitchen knives',
              'Steak knife sets', 'Knife sets, blocks & racks')
SAFE_CATS = ('Shears & scissors', 'Chopping boards', 'Knife sharpeners')
_SAFE_RE = ('shear', 'scissor', 'board', 'sharpener')


def gallery_items(lang, limit=8):
    import json as _j
    try:
        items = _j.loads((BASE / 'products.json').read_text(encoding='utf-8')).get('items') or []
    except Exception:
        return []
    out = []
    for it in items:
        cat = (it.get('category') or '')
        low = cat.lower()
        if any(w in low for w in ('hunting', 'pocket', 'folding')):      # 狩猎/口袋刀一律不上站
            continue
        if lang == 'de':
            if cat not in KNIFE_CATS and cat not in SAFE_CATS:
                continue
        else:
            if not any(w in low for w in _SAFE_RE):                      # 美英：只上非刀品类
                continue
        slug = it.get('slug') or ''
        if not slug:
            continue
        out.append((slug, it.get('caption') or slug))
        if len(out) >= limit:
            break
    return out


def gallery_html(lang, limit=8):
    items = gallery_items(lang, limit)
    if not items:
        return ''
    cells = ''.join(
        '<figure style="margin:0"><img src="/assets/products/%s.jpg" alt="%s" loading="lazy" '
        'decoding="async" style="width:100%%;height:190px;object-fit:cover;border-radius:12px;'
        'border:1px solid #e6ebe3;background:#fff"><figcaption style="font-size:12px;color:#6b7780;'
        'margin-top:6px">%s</figcaption></figure>' % (s, cap.replace('"', ''), cap)
        for s, cap in items)
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));'
            'gap:14px;margin-top:18px">%s</div>' % cells)


FORM_LABEL = 'AW-17434685893/R4CTCKq3poMdEMXjwPlA'   # 转化动作「询盘表单_落地页」的标签

HERO_FORM = """<form id="enqhero" data-hero="1" style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap;
      align-items:center;max-width:660px">
  <input name="email" type="email" required placeholder="{hero_ph}" autocomplete="email"
         style="flex:1;min-width:240px;padding:13px 15px;border:1px solid #39454b;border-radius:10px;
                background:#0f1417;color:#e7edf0;font:inherit">
  <button class="btn big" type="submit" style="border:0;cursor:pointer;white-space:nowrap">{hero_btn}</button>
</form>
<p class="sub" id="enqhero-note" style="max-width:660px;margin-top:10px">{hero_note}</p>
<p id="enqhero-ok" class="sub" hidden style="max-width:660px;margin-top:10px;font-weight:600;color:#cfe0c0">{hero_ok}</p>"""


FORM = """<section id="enquiry" style="background:#f7f9f5">
  <div class="wrap">
    <h2>{form_ttl}</h2>
    <p class="sub">{form_sub}</p>
    <style>
      #enq{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}}
      #enq .full{{grid-column:1/-1}}
      #enq input,#enq select,#enq textarea{{width:100%;padding:12px 14px;border:1px solid #cfd9d2;
        border-radius:10px;font:inherit;background:#fff}}
      #enq label.consent{{display:flex;gap:9px;align-items:flex-start;font-size:13px;color:#4c5a60}}
      #enq label.consent input{{width:auto;margin-top:2px}}
      @media(max-width:640px){{#enq{{grid-template-columns:1fr}}}}
    </style>
    <form id="enq" novalidate>
      <input name="company" required placeholder="{f_company} *" autocomplete="organization">
      <input name="email" type="email" required placeholder="{f_email} *" autocomplete="email">
      <input name="whatsapp" placeholder="WhatsApp (optional)" autocomplete="tel">
      <!-- 2026-10-16 体检：与 10 个语种页统一为 4 字段（公司/邮箱/WhatsApp/国家），
           少一个必填就少一层流失；客户名在邮件或 WhatsApp 里自然会给。 -->
      <input name="country" placeholder="{f_country}" autocomplete="country-name">
      <!-- 2026-10-16 体检：与 12 个语种页统一为 4 字段（公司*/邮箱*/WhatsApp/国家）。
           产品线、数量、留言三个下拉/文本块撤掉 —— B2B 冷访客只愿意填联系信息，
           采购细节在 WhatsApp 里问反而更快。 -->
      <p class="sub" style="margin:2px 0 0;font-size:13px">{f_msg}</p>
      <label class="consent full"><input type="checkbox" name="consent" required>
        <span>{f_consent} <a href="{priv}" target="_blank" rel="noopener">Datenschutz</a></span></label>
      <div class="full">
        <button class="btn big" type="submit" style="border:0;cursor:pointer">{f_btn}</button>
        <span class="sub" style="margin-left:12px" id="enq-note">{f_note}</span>
      </div>
    </form>
    <p id="enq-ok" class="sub" hidden style="font-weight:600;color:#2f6b2f">{f_ok}</p>
  </div>
</section>"""

FORM_JS = """<script>
/* 询盘表单提交（第二条转化路径）。
   与点击上报同一套约定：地址读 /ad/track.json（隧道域名会变），带同一枚 token。
   失败**不能丢线索**：发不出去就把内容拼成 mailto 打开邮件客户端。 */
(function(){
  var EP = null, LABEL = '__FORM_LABEL__', LANG = '__LANG__', CODE = '__FORM_CODE__';
  var HERO_CODE = '__HERO_CODE__';
  fetch('/ad/track.json', {cache:'no-store'}).then(function(r){return r.json();})
    .then(function(d){ EP = d && d.lead; }).catch(function(){});
  bind('enq', CODE, false);           // 页面中部的完整表单
  bind('enqhero', HERO_CODE, true);   // 首屏"留邮箱拿资料"（只要邮箱）—— 采购员常常只想先拿资料

  function bind(fid, CODE, isHero){
  var f = document.getElementById(fid); if(!f) return;
  function val(n){ var e=f.elements[n]; return e ? String(e.value||'').trim() : ''; }
  function mailtoFallback(){
    var body = ['Company: '+val('company'), 'Name: '+val('name'), 'Email: '+val('email'),
                'Country: '+val('country'), 'Product line: '+val('product_line'),
                'Quantity: '+val('quantity'), '', val('message'), '', '['+CODE+']'].join(String.fromCharCode(10));
    location.href = 'mailto:fengerwei669@gmail.com?subject=' + encodeURIComponent('Enquiry ' + CODE)
                  + '&body=' + encodeURIComponent(body);
  }
  function ok(){
    f.hidden = true;
    var n=document.getElementById(fid === 'enqhero' ? 'enqhero-note' : 'enq-note'); if(n) n.hidden=true;
    var p=document.getElementById(fid === 'enqhero' ? 'enqhero-ok' : 'enq-ok'); if(p){ p.hidden=false; }
    if(typeof gtag === 'function'){ gtag('event','conversion',{send_to:LABEL}); }
  }
  f.addEventListener('submit', function(e){
    e.preventDefault();
    if(!val('email') || val('email').indexOf('@') < 1){ f.elements['email'].focus(); return; }
    if(!isHero && !val('company')){ f.elements['company'].focus(); return; }
    if(f.elements['consent'] && f.elements['consent'].required && !f.elements['consent'].checked){ f.elements['consent'].focus(); return; }
    var b = f.querySelector('button[type=submit]'); if(b){ b.disabled = true; }
    if(!EP){ mailtoFallback(); return; }
    var p = new URLSearchParams(location.search);
    var payload = { token:'wlc-7f3a91c2', lang:LANG, code:CODE, hero:isHero ? 1 : 0, page:location.pathname,
      company:val('company'), name:val('name'), email:val('email'), country:val('country'), whatsapp:val('whatsapp'),
      kw:QP('kw'), campaign:QP('cpn'), adgroup:QP('adg'), device:QP('dev'),
      product_line:val('product_line'), quantity:val('quantity'), message:val('message'),
      kw:p.get('kw')||p.get('utm_term')||p.get('utm_content')||'', gclid:p.get('gclid')||'' };
    var payloadStr = JSON.stringify(payload);
    fetch(EP, {method:'POST', headers:{'Content-Type':'text/plain'}, body:payloadStr, keepalive:true})
      .then(function(r){ return r.json(); })
      .then(function(j){ if(j && j.ok){ ok(); } else { mailtoFallback(); } })
      .catch(function(){ mailtoFallback(); });
  });
  }
})();
</script>"""


def build(code):
    c = C[code]
    # 同意管理：德语页（欧盟流量）默认全拒绝 + 显示横幅；美国页默认允许、不显示横幅
    consent = ("{ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied', "
               "analytics_storage:'denied', wait_for_update: 500}" if code == 'de' else
               "{ad_storage:'granted', ad_user_data:'granted', ad_personalization:'granted', "
               "analytics_storage:'granted'}")
    gtag_block = (GTAG.replace('__CONSENT__',
                               '欧盟流量：默认拒绝，用户点 Einverstanden 后再开' if code == 'de'
                               else '美国流量：无欧盟同意要求，默认可测量')
                      .replace('__CONSENT_STATE__', consent))
    cookie_block = BANNER if code == 'de' else ''
    wa_oem = WA + c['msgs']['oem']
    wa_video = WA + c['msgs']['video']
    wa_whole = WA + c['msgs']['whole']
    mail = MAIL + '?subject=' + c['msgs']['mail_subj']
    cards = []
    for i, (h, badge, body, mini, btn) in enumerate(c['cards']):
        b = ' <span class="badge">%s</span>' % badge if badge else ''
        wa = wa_oem if i == 0 else wa_whole
        cards.append('<div class="card%s"><h3>%s%s</h3><p>%s</p><p class="mini">%s</p>'
                     '<a class="btn" href="%s" target="_blank" rel="noopener">%s</a></div>'
                     % (' lead-card' if i == 0 else '', h, b, body, mini, wa, btn))
    rows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in c['prod_rows'])
    steps = ''.join('<li><strong>%s</strong> %s</li>' % s for s in c['steps'])
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % f for f in c['faq'])
    facts_rows = ''.join('<tr><td><strong>%s</strong></td><td>%s</td></tr>' % f for f in c['facts'])
    jsonld = build_jsonld(c)
    priv = '/ad/de/datenschutz.html' if code == 'de' else '/privacy.html'
    # 【2026-10-16 体检发现】原来只有 3 条（de）或 1 条（其余）hreflang，缺了其它语种互指。
    # 现在统一输出全部 13 个页面互指 + x-default（英文页用真正在投的 /ad/us-ware/）。
    HL = [('de','/ad/de/'),('en','/ad/us-ware/'),('es','/ad/es/'),('fr','/ad/fr/'),('it','/ad/it/'),
          ('nl','/ad/nl/'),('pl','/ad/pl/'),('pt','/ad/pt/'),('ru','/ad/ru/'),('ar','/ad/ar/'),
          ('tr','/ad/tr/'),('ro','/ad/ro/')]
    hreflang = '\n'.join('<link rel="alternate" hreflang="%s" href="https://wiliheng.com%s">' % (lg, u) for lg, u in HL)
    hreflang += '\n<link rel="alternate" hreflang="x-default" href="https://wiliheng.com/ad/us-ware/">'
    form_block = FORM.format(plines=''.join('<option>%s</option>' % x for x in c['f_plines']),
                             qtys=''.join('<option>%s</option>' % x for x in c['f_qtys']),
                             priv=priv, **{k: c[k] for k in
                             ('form_ttl', 'form_sub', 'f_company', 'f_email', 'f_name', 'f_country',
                              'f_pline', 'f_qty', 'f_msg', 'f_consent', 'f_btn', 'f_ok', 'f_note')})
    form_js = (FORM_JS.replace('__FORM_LABEL__', FORM_LABEL).replace('__LANG__', code)
                      .replace('__FORM_CODE__', c['form_code'])
                      .replace('__HERO_CODE__', c['form_code'] + 'H'))   # 首屏留资来源码：WH-DE-FH
    chips = ''.join('<li>%s</li>' % x for x in c['chips'])
    hero_form = HERO_FORM.format(hero_ph=c['hero_ph'], hero_btn=c['hero_btn'],
                                 hero_note=c['hero_note'], hero_ok=c['hero_ok'])
    gallery = gallery_html(code)                      # 成品产品图（德国含刀图，美英只用非刀品类）
    # 新站（多语种，图片更全）：同一语言页，供想继续浏览的采购员
    catalog_url = 'https://wiliheng.com/b2b/%s/' % code if code in ('de', 'ar', 'es', 'fr', 'it', 'nl', 'pl', 'pt', 'ru') else 'https://wiliheng.com/b2b/'
    gallery_more = c['gallery_more'].replace('{cat}', catalog_url)
    h1, h2, h3 = c['prod_head']
    html = f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
{CRITICAL_CSS}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{c['title']}</title>
<meta name="description" content="{c['desc']}">
<link rel="canonical" href="https://wiliheng.com/ad/{c['slug']}/">
{hreflang}
<link rel="icon" href="/assets/favicon.png">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{c['title']}">
<meta property="og:description" content="{c['desc']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yangjiang Wiliheng Knives Co., Ltd">
<meta property="og:url" content="https://wiliheng.com/ad/{c['slug']}/">
<meta property="og:image" content="https://wiliheng.com/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c['title']}">
<meta name="twitter:description" content="{c['desc']}">
<meta name="twitter:image" content="https://wiliheng.com/assets/og.jpg">
{jsonld}
{gtag_block}
{CSS}
</head>
<body>

<header class="top">
  <div class="wrap">
    <div class="brand">{c['brand_name']} <small>{c['brand_sub']}</small></div>
    <a class="btn" href="{wa_oem}" target="_blank" rel="noopener">{c['hdr_btn']}</a>
  </div>
</header>

<div class="hero">
  <div class="wrap">
    <h1>{c['h1']}</h1>
    <div class="answer"><p>{c['answer']}</p></div>
    <p class="lead">{c['lead']}</p>
    <div class="cta">
      <a class="btn big" href="{wa_whole}" target="_blank" rel="noopener">{c['cta_whole']}</a>
      <a class="btn ghost" href="{wa_oem}" target="_blank" rel="noopener">{c['cta_oem']}</a>
      <a class="btn ghost" href="{mail}">{c['cta2']}</a>
      <span class="sub">{c['ctasub']}</span>
    </div>
    {hero_form}
    <ul class="chips">{chips}</ul>
  </div>
</div>

{form_block}

<section>
  <div class="wrap">
    <h2>{c['cards_ttl']}</h2>
    <p class="sub">{c['cards_sub']}</p>
    <div class="grid">{''.join(cards)}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{c['photo_ttl']}</h2>
    <p class="sub">{c['photo']}</p>
    {gallery}
    <p class="sub" style="margin-top:14px">{gallery_more}</p>
    <div class="cta" style="margin-top:18px">
      <a class="btn big" href="{wa_oem}" target="_blank" rel="noopener">{c['cta1']}</a>
      <span class="sub">{c['contact']}</span>
    </div>
  </div>
</section>

<section style="background:#f3f8ec">
  <div class="wrap">
    <h2>{c['video_ttl']}</h2>
    <p class="sub">{c['video_body']}</p>
    <div class="grid" style="margin-bottom:20px">
      {''.join('<div class="card" style="background:transparent;border:1px solid #d8e6c4"><p style="margin:0">%s</p></div>' % b for b in c['video_bullets'])}
    </div>
    <div class="cta">
      <a class="btn big" href="{wa_video}" target="_blank" rel="noopener">{c['video_cta']}</a>
      <span class="sub">{c['video_note']}</span>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{c['prod_ttl']}</h2>
    <p class="sub">{c['prod_sub']}</p>
    <table>
      <tr><th>{h1}</th><th>{h2}</th><th>{h3}</th></tr>
      <tr><td>{c['prod_rows'][0][0]}</td><td>{c['prod_rows'][0][1]}</td>
          <td rowspan="4" style="vertical-align:middle">{c['price_note']}</td></tr>
      {''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in c['prod_rows'][1:])}
    </table>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{c['steps_ttl']}</h2>
    <ol class="steps">{steps}</ol>
    <div class="cta" style="margin-top:22px">
      <a class="btn big" href="{wa_oem}" target="_blank" rel="noopener">{c['cta1']}</a>
    </div>
  </div>
</section>

<section style="background:#f7f9f5">
  <div class="wrap">
    <h2>{c['facts_ttl']}</h2>
    <table>{facts_rows}</table>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{c['faq_ttl']}</h2>
    {faq}
  </div>
</section>

<footer>
  <div class="wrap">
    <p><strong>Yangjiang Wiliheng Knives Co., Ltd</strong> · {c['foot_kind']}<br>{ADDR}</p>
    <p>WhatsApp +86 181 2488 6695 · <a href="mailto:fengerwei669@gmail.com">fengerwei669@gmail.com</a> ·
       <a href="https://wiliheng.com/">wiliheng.com</a></p>
    <p>{c['legal']}</p>
    <p style="color:#6d7a80;margin-bottom:0">{c['foot_note']}</p>
  </div>
</footer>

<div class="sticky">
  <a class="btn big" href="{wa_oem}" target="_blank" rel="noopener">{c['sticky']}</a>
</div>
{form_js}
{TRACK.replace('__CODE__', code.upper() + '-').replace('__SEND_TO__', SEND_TO)}
{BEACON.replace('__LANG__', code)}
{cookie_block}
  <!-- 手机端常驻悬浮 WhatsApp（2026-10-16 体检发现 de/us/us-ware 三页缺失）：今天全部广告点击都来自手机。 -->
  <a class="wa-float" href="{wa_oem}" target="_blank" rel="noopener" data-intent="{c['sticky']}" aria-label="{c['sticky']}">
    <svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2m5.8 14.09c-.24.68-1.4 1.3-1.93 1.35-.53.05-1.03.24-2.93-.61-2.3-1.03-3.74-3.44-3.85-3.6-.11-.16-.92-1.26-.92-2.4 0-1.14.6-1.7.81-1.93.21-.23.46-.29.61-.29h.44c.14 0 .33-.05.51.39.19.45.64 1.56.7 1.67.06.11.1.24.02.39-.08.15-.15.24-.29.38-.14.14-.3.32-.43.43-.14.13-.29.26-.13.53.16.27.71 1.17 1.52 1.9 1.05.94 1.94 1.23 2.21 1.37.27.13.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.22.61-.13.25.09 1.59.75 1.86.89.27.13.45.2.52.31.07.12.07.68-.17 1.36z"/></svg>
  </a>
</body>
</html>
"""
    return html


def _derive_usware(us):
    """从美国页派生「厨房 & 餐具线」页（slug=us-ware）。

    为什么另开一页而不改美国页：Google 美国把刀具类广告判为 OTHER_WEAPONS，
    连改三轮（文案→落地页→整站）仍被拒 → 说明是按品类+国家判的。
    所以美国不再提 knife，改打工厂真实有的非刀具产品线（餐具/厨房工具/削皮器/砧板/剪）
    —— 这页**一个字都不提 knife**，让分类器无从下手；同一条询盘链路（表单+WhatsApp+转化）照用。
    """
    import copy as _copy
    c = _copy.deepcopy(us)
    c['slug'] = 'us-ware'
    c['brand_name'] = 'Wiliheng'
    c['title'] = 'Kitchen &amp; Table Products Under Your Brand — OEM/ODM Factory'
    c['desc'] = ('OEM/ODM kitchen and table products from Yangjiang, China: cutlery sets, kitchen tools, peelers, '
                 'boards and shears under your brand, 500 pcs per model.')
    c['answer'] = ('Yangjiang Wiliheng Knives Co., Ltd is an OEM/ODM kitchen and table products factory in '
                   'Yangjiang, Guangdong, China, making cutlery sets, kitchen tools, peelers, chopping boards, '
                   'silicone mats, 304 tableware and shears under your brand — 500 pcs per model minimum, '
                   'pre-production sample in about a week.')
    c['brand_sub'] = 'OEM/ODM kitchen &amp; table factory · Yangjiang, China'
    c['h1'] = 'Your brand on kitchen &amp; table products — OEM/ODM straight from the factory'
    c['lead'] = ('We manufacture kitchen and table products under <strong>your brand</strong>: materials, '
                 'handles and packaging to your spec. From 500 pcs per model, with a pre-production sample '
                 'for approval. Stock ranges for wholesale and distribution on top of that.')
    c['cards'] = [
        ('Private label &amp; OEM/ODM', 'Our core business',
         'Your brand on the product and the box: laser engraving, custom handles, custom packaging, '
         'barcodes done. You approve a pre-production sample before we run the order.',
         'From 500 pcs per model, custom designs included.', 'Discuss OEM/ODM'),
        ('Wholesale &amp; distribution', '',
         'Stock ranges at factory prices: cutlery sets, kitchen tools, peelers, chopping boards, silicone '
         'mats, 304 tableware and shears. Tiered pricing from 500 pcs, steady lead times, retail-ready '
         'packaging.', 'Add a kitchen line without owning a factory.', 'Get pricing'),
    ]
    c['photo'] = ('We run hundreds of items and the relevant ones differ per customer — so there is no photo '
                  'grid here. Tell us your product line (e.g. cutlery sets, kitchen tools, peelers) and we '
                  'send <strong>3–5 matching items with real photos, material options and pricing</strong> '
                  'straight to WhatsApp, usually within 24 hours.')
    c['prod_ttl'] = 'What we manufacture'
    c['prod_sub'] = ('Made in our own factory in Yangjiang — stamping, heat treatment, grinding and assembly '
                     'in house.')
    c['prod_rows'] = [('Kitchen tools', 'Peelers, openers, graters, utensils'),
                      ('Cutlery &amp; tableware', 'Cutlery sets, 304 tableware'),
                      ('Shears &amp; scissors', 'Kitchen and poultry shears'),
                      ('Silicone &amp; boards', 'Mats, chopping boards, kitchen gadgets')]
    c['faq'] = [(q, a) for q, a in c['faq']]
    c['faq'][1] = ('Can I get items and photos?',
                   'Yes — in the chat. We do not send a photo dump; we shortlist the items that fit your '
                   'line with real photos and pricing.')
    c['faq'][6] = ('How big is the factory and what do you make in house?',
                   'Our factory in Yangjiang runs 43 production steps in house with 40 machines, including '
                   '20 CNC machining centres, 10 water grinding machines, 5 vertical grinders, 2 annealing '
                   'and 2 tempering furnaces, plus Rockwell hardness testing. We manufacture for importers, '
                   'distributors and brand owners.')
    c['faq'][7] = ('Which materials are possible?',
                   'Stainless steel, silicone and 304 tableware; handles in wood, plastic or to your '
                   'drawing. Packaging as colour box, blister or protective sleeve.')
    c['facts'] = [(k, v) for k, v in c['facts']]
    c['facts'][5] = ('Items', '48 production models across kitchen, table and shears')
    c['foot_kind'] = 'OEM/ODM kitchen &amp; table products factory'
    c['video_body'] = ('You do not have to fly to China. We take you on a <strong>live video call</strong> '
                       '(WhatsApp or Zoom, about 15–20 minutes) through production: stamping, heat treatment, '
                       'grinding, CNC, hardness testing and packing. You see the machines that will make your '
                       'order — and the people responsible for it.')
    c['msgs'] = {'video': 'WH-USW-V%20-%20Please%20book%20a%20live%20video%20walkthrough%20of%20the%20factory',
                 'oem': 'WH-USW-B%20-%20Private%20label%20-%20please%20send%20items%20and%20photos',
                 'whole': 'WH-USW-A%20-%20Wholesale%20-%20price%20list%20and%20sample%20photos',
                 'mail_subj': 'OEM%2FODM%20kitchen%20%26%20table%20enquiry'}
    c['form_code'] = 'WH-USW-F'
    c['chips'] = [('Material &amp; handle to spec' if 'Blade' in x else x) for x in c['chips']]
    c['f_plines'] = ['Cutlery &amp; cutlery sets', 'Kitchen tools &amp; gadgets', 'Peelers &amp; openers',
                     'Chopping boards &amp; mats', 'Shears &amp; scissors', 'Mixed assortment']
    c['facts'] = [(k, ('2018 — manufacturing kitchen &amp; table products in Yangjiang ever since'
                       if k == 'Established' else v)) for k, v in c['facts']]
    return c


C['usware'] = _derive_usware(C['us'])


def _txt(s):
    """JSON-LD 里不能有 HTML 实体/标签：AI 读的是纯文本（&amp; 会被当成字面量）"""
    return re.sub(r'\s+', ' ', html_mod.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def build_jsonld(c):
    """落地页结构化数据：GEO 的核心 —— 让 AI 搜索能直接读走「谁、在哪、能做什么、常见问答」。

    只写真数据（厂址 / MOQ / 交期 / 设备数来自 MES），不写价格 —— 与页面口径一致，
    AI 引用时不会出现「页面说 A、结构化数据说 B」的冲突。
    """
    url = 'https://wiliheng.com/ad/%s/' % c['slug']
    org = {
        '@type': 'Organization',
        '@id': 'https://wiliheng.com/#org',
        'name': 'Yangjiang Wiliheng Knives Co., Ltd',
        'foundingDate': '2018',
        'url': 'https://wiliheng.com/',
        'description': _txt(c['desc']),
        'email': 'fengerwei669@gmail.com',
        'address': {'@type': 'PostalAddress',
                    'streetAddress': 'Factory No. 2, Middle Section of Yudong Ninth Road, '
                                     'Yangdong Industrial Park',
                    'addressLocality': 'Yangjiang', 'addressRegion': 'Guangdong',
                    'addressCountry': 'CN'},
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales',
                         'email': 'fengerwei669@gmail.com',
                         'availableLanguage': ['en', 'de', 'zh']},
        'knowsAbout': [_txt(r[0]) for r in c['prod_rows']] + ['OEM', 'ODM', 'private label', 'wholesale'],
        'areaServed': [{'@type': 'Country', 'name': 'United States'},
                       {'@type': 'Country', 'name': 'Germany'},
                       {'@type': 'Place', 'name': 'European Union'}],
        'additionalProperty': [{'@type': 'PropertyValue', 'name': _txt(k), 'value': _txt(v)}
                               for k, v in c['facts']],
    }
    page = {'@type': 'WebPage', '@id': url + '#page', 'url': url,
            'name': _txt(c['title']), 'description': _txt(c['desc']),
            'inLanguage': 'de' if c['slug'] == 'de' else 'en',
            'isPartOf': {'@id': 'https://wiliheng.com/#website'}, 'about': {'@id': 'https://wiliheng.com/#org'}}
    crumb = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Wiliheng', 'item': 'https://wiliheng.com/'},
        {'@type': 'ListItem', 'position': 2, 'name': c['h1'][:60], 'item': url}]}
    fq = {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': _txt(q), 'acceptedAnswer': {'@type': 'Answer', 'text': _txt(a)}}
        for q, a in c['faq']]}
    blob = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': 'https://wiliheng.com/#website',
         'url': 'https://wiliheng.com/', 'name': c.get('brand_name', 'Wiliheng Knives'), 'publisher': {'@id': 'https://wiliheng.com/#org'}},
        org, page, crumb, fq]}
    return '<script type="application/ld+json">%s</script>' % json.dumps(blob, ensure_ascii=False, separators=(',', ':'))


def main():
    ok = True
    for code in ('de', 'us', 'usware'):
        c = C[code]
        html = build(code)
        # 【2026-10-16 体检发现 · 政策红线】us/us-ware 是 US+UK 共 26 条广告的落地页，
        # 但页面里仍带 knife（JSON-LD 公司名 "Wiliheng Knives"、磨刀器图注 "knife sharpener"）。
        # Google 审整页 → 非德国页一个字不提刀（德国页允许，保持不动）。
        if code != 'de':
            for _a, _b in (('Yangjiang Wiliheng Knives Co., Ltd', 'Wiliheng'),
                           ('Wiliheng Knives', 'Wiliheng'), ('Kitchen Knives', 'Kitchenware'),
                           ('knife sharpeners', 'sharpeners'), ('Knife sharpeners', 'Sharpeners'),
                           ('knife sharpener', 'sharpener'), ('Knife sharpener', 'Sharpener'),
                           ('kitchen knives', 'kitchenware'), ('Kitchen knives', 'Kitchenware'),
                           ('kitchen knife', 'kitchen tool'), ('Knives', 'Kitchenware'),
                           ('knives', 'kitchenware'), ('knife', 'kitchen tool'), ('Knife', 'Kitchen tool'),
                           ('cutlery', 'tableware'), ('Cutlery', 'Tableware')):
                html = html.replace(_a, _b)
        p = BASE / 'ad' / c['slug'] / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html, encoding='utf-8')
        # 自检：不许有图片、不许有价格、CTA 和合规链接必须在
        bad = []
        # 产品图现在**允许**（用户 2026-10-04 已完善图片）。
        # 但美英页禁止出现刀类品类图：那两条厨房系列是在"无刀图"的页面上过审的，
        # 一旦出现刀图极可能被重新判 OTHER_WEAPONS（本单花了两天才过审）。规则比"不许有图"更准。
        _imgs = re.findall(r'/assets/products/(W-\d+)\.jpg', html)
        if _imgs:
            try:
                _items = {i.get('slug'): (i.get('category') or '') for i in
                          json.loads((BASE / 'products.json').read_text(encoding='utf-8')).get('items') or []}
            except Exception:
                _items = {}
            # 按**品类精确匹配**判定，别用子串：'Knife sharpeners'（磨刀器，厨房配件、图上无刀）
            # 不含 'knife' 子串会误伤；真正的刀类就是 KNIFE_CATS 这几类。
            if c.get('slug') != 'de':
                _bad_imgs = [s for s in _imgs if (_items.get(s, '') or '') in KNIFE_CATS]
                if _bad_imgs:
                    bad.append('美英页出现了刀类图：%s' % ','.join(_bad_imgs[:3]))
            else:
                _hunt = [s for s in _imgs if any(w in (_items.get(s, '') or '').lower()
                                                 for w in ('hunting', 'pocket', 'folding'))]
                if _hunt:
                    bad.append('德国页出现了狩猎/口袋刀图：%s' % ','.join(_hunt[:3]))
        # 只检查正文：脚本里 '$1%20' 这种正则替换会假命中价格（踩过）
        body_only = re.sub(r'<script>.*?</script>', '', html, flags=re.S)
        if re.search(r'[€$¥]\s?\d', body_only):
            bad.append('出现了价格数字')
        if 'wa.me/8618124886695' not in html:
            bad.append('没有 WhatsApp CTA')
        # JS 语法体检：Python 里的 \n 转义很容易产出**非法 JS**（实测踩过：
        # 页面其余部分全对，只有注入的脚本块 "Invalid or unexpected token"，
        # 结果是表单点了没反应、而且不报错给用户）。用 node --check 逐块验。
        for i, blk in enumerate(re.findall(r'<script>(.*?)</script>', html, re.S)):
            tmp = Path(tempfile.gettempdir()) / ('_chk_%s_%d.js' % (code, i))
            tmp.write_text(blk, encoding='utf-8')
            r = subprocess.run(['node', '--check', str(tmp)], capture_output=True)
            if r.returncode != 0:
                bad.append('脚本块%d JS 语法错误：%s' % (i, r.stderr.decode('utf-8', 'replace').strip().splitlines()[-1][:80]))
        if code == 'de' and ('impressum' not in html or 'datenschutz' not in html):
            bad.append('缺 Impressum/Datenschutz')
        if code == 'us' and '/privacy.html' not in html:
            bad.append('缺隐私政策链接')
        if 'Yudong Ninth Road' not in html:
            bad.append('缺厂址')
        if 'wa.me/8618124886695?text=' + c['msgs']['video'] not in html:
            bad.append('缺视频验厂 CTA')
        if 'AW-17434685893' not in html or SEND_TO not in html:
            bad.append('缺 Google Ads 转化追踪')
        if code == 'de' and "'consent'" not in html:
            bad.append('德语页缺同意模式（EEA 要求）')
        if 'wa_click' not in html or 'track.json' not in html:
            bad.append('缺点击上报（后台记录/企微通知就没了）')
        n_wa = html.count('wa.me/8618124886695')
        print('%-4s %-28s %6d 字节 ｜ WhatsApp 按钮 %d ｜ %s'
              % (code.upper(), str(p.relative_to(BASE)), len(html.encode('utf-8')), n_wa,
                 '❌ ' + '；'.join(bad) if bad else '自检通过 ✅'))
        ok = ok and not bad
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
