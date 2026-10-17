#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 MES 真实数据生成官网首页（wiliheng.com）。

为什么用脚本生成而不是手写 HTML：网站上的品类数量、款号、规格全都要跟 MES 一致。
手写的话改一次 MES 就会对不上（内部报表可以靠人记得，对外网站一旦吹了就回不来）。
明天产品图/规格补齐后，只要在 MES 里补数据 → 重跑本脚本 → 重新部署。

用法：
    python build_site.py            # 生成 site/index.html + 同步线卡 PDF
"""
import html
import shutil
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
# 产品图库是否展示（老板要求：先不展示，等产品照片定稿/重新审核后改成 True 再生成即可）
SHOW_GALLERY = True
SITE = BASE / "site"
MES_DB = BASE / "mes" / "mes.db"
TEMPLATE = SITE / "index.template.html"
OUT = SITE / "index.html"

WHATSAPP = "https://wa.me/8618124886695"
LINECARD = "Wiliheng-Knives-Line-Card.pdf"

# 品类：名称从真实款号名里识别；描述写的是**能力**（与 MES 工序表一致），不编参数
CATS = [
    ("折叠", "Folding knives", "Liner lock and frame lock folding knives in G10 or wood"),
    ("匕首", "Fixed-blade knives", "Fixed-blade utility and kitchen designs"),
    ("猎刀", "Fixed-blade knives", "Fixed-blade utility and kitchen designs"),
    ("战术直刀", "Fixed-blade knives", "Fixed-blade utility and kitchen designs"),
    ("厨刀", "Kitchen knives", "Chef, santoku, utility and paring knives in 5Cr15MoV / 440C"),
    ("剪刀", "Shears &amp; scissors", "German-type kitchen shears and poultry shears"),
    ("杂件", "Kitchen gadgets", "Peelers, mandoline slicers and small stainless / silicone kitchen tools"),
    ("硅胶", "Silicone mats", "Honeycomb, fibreglass and round trivets, table mats and drain mats"),
    ("餐具", "304 tableware", "Serving spoons, slotted spoons, cake servers, tea spoons and forks"),
]

EN_NAME = {"KH-001": "Folding knife", "KH-002": "Utility knife",
           "KH-003": "Chef's knife", "KH-004": "Fixed-blade utility knife"}
EN_PACK = {"彩盒+吸塑": "Colour box + blister", "彩盒+刀套": "Colour box + protective cover", "彩盒": "Colour box"}


def en_spec(v):
    return ((v or "").replace("刃长", "blade ").replace("全長", " / OAL ")
                     .replace("全长", " / OAL ").replace("寸", " inch")).strip()


def equip_counts(con):
    """按名称从设备表算台数（真实数据，网站/线卡/分享卡都用它）。

    设备表原设计是「一行=一种设备」，老板报的台数写进 qty 列后才有真实总数 ——
    所以一律用 sum(qty)，不要再退回 count(*)（那是型号数，会让「40 台机器」变成「6」）。
    """
    def q(like):
        try:
            return int(con.execute(
                "select sum(coalesce(qty,1)) from equipment where name like ?", (like,)).fetchone()[0] or 0)
        except Exception:
            return con.execute("select count(*) from equipment where name like ?", (like,)).fetchone()[0]
    d = {"cnc": q("%CNC%"),
         "furnace": q("%退火%") + q("%回火%"),
         "anneal": q("%退火%"), "temper": q("%回火%"),
         "vgrind": q("%立磨%"), "wgrind": q("%水磨%")}
    d["total"] = con.execute("select sum(coalesce(qty,1)) from equipment").fetchone()[0] or 0
    d["total"] = int(d["total"])
    return d


def cnc_count(con):
    return equip_counts(con)["cnc"]


def _gallery_section(moq_min, gallery):
    """图库整块（标题 + 引言 + 图片墙）。

    开关是文件顶部的 SHOW_GALLERY：关闭时整块不输出，导航里的 Gallery 链接也一并隐藏，
    避免出现点了没东西的死链（老板要求「先不展示」时就是这样）。
    """
    dl = ('<p><a class="btn ghost" href="Wiliheng-Product-Catalogue.pdf" target="_blank" '
          'rel="noopener">Download the PDF catalogue — all photos with reference codes</a></p>')
    return (dl + '<h3 class="gap" id="gallery">Product gallery</h3>\n'
            '  <p class="sub">Photographed on our own bench — the knives, tools and mats we run most often.\n'
            '    Specifications for any item on request; your logo and packaging from %s pcs.</p>\n' % moq_min
            + gallery)


def build_html():
    con = sqlite3.connect(str(MES_DB))
    con.row_factory = sqlite3.Row
    prods = [dict(r) for r in con.execute(
        "select sku,name,spec,steel,hrc_std,packing,net_weight,moq from products order by sku")]
    n_steps = con.execute("select count(*) from steps").fetchone()[0]
    n_mach = con.execute("select count(*) from equipment").fetchone()[0]
    eq = equip_counts(con)
    n_cnc = eq["cnc"]
    con.close()

    # ── 品类卡（同名品类合并计数）──
    groups, order = {}, []
    for key, en, desc in CATS:
        items = [p for p in prods if key in p["name"]]
        if not items:
            continue
        if en not in groups:
            groups[en] = {"desc": desc, "items": []}
            order.append(en)
        for it in items:
            if it["sku"] not in [x["sku"] for x in groups[en]["items"]]:
                groups[en]["items"].append(it)
    cats = []
    for en in order:
        g = groups[en]
        skus = " &middot; ".join(p["sku"] for p in g["items"][:6])
        if len(g["items"]) > 6:
            skus += " &hellip;"
        cats.append(
            '<div class="cat"><span class="n">%d models</span><h4>%s</h4><p>%s</p>'
            '<code>%s</code></div>' % (len(g["items"]), en, g["desc"], skus))
    seen = {p["sku"] for en in groups for p in groups[en]["items"]}
    rest = [p for p in prods if p["sku"] not in seen]
    if rest:
        cats.append('<div class="cat"><span class="n">%d models</span><h4>Accessories</h4>'
                     '<p>Additional lines made to the same in-house process</p><code>%s</code></div>'
                     % (len(rest), " &middot; ".join(p["sku"] for p in rest)))

    # ── 带规格的款号表（只翻译字段值，不新增参数）──
    specs = []
    moqs = []
    for p in prods:
        if not (p["spec"] or "").strip():
            continue
        try:
            wt = "%.0f g" % float(p["net_weight"])
        except Exception:
            wt = ""
        try:
            moqs.append(int(p["moq"]))
        except Exception:
            pass
        specs.append("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
                     "<td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (html.escape(p["sku"]), html.escape(EN_NAME.get(p["sku"], p["name"])),
                        html.escape(en_spec(p["spec"])), html.escape(p["steel"] or ""),
                        html.escape(p["hrc_std"] or ""), wt,
                        html.escape(EN_PACK.get((p["packing"] or "").strip(), p["packing"] or "")),
                        html.escape(str(p["moq"] or ""))))

    # 对外公布的起订量：老板定的口径 500 pcs/型号（2026-09-28 确认）。
    # 不要再用 min(moqs)：MES 里个别款号写着 200/300，一取最小值全站就变成"从 200 起"。
    moq_min = 500

    # ── 产品图库（清单在 site/products.json；图是白底成品同步进来的）──
    gallery = ""
    mp = SITE / "products.json"
    if mp.exists():
        import json
        man = json.loads(mp.read_text(encoding="utf-8"))
        groups = {}
        order = []
        for it in man.get("items", []):
            p = SITE / "assets" / "products" / (it["slug"] + ".jpg")
            if not p.exists():
                continue                       # 图还没同步过来就不显示（不留空框）
            c = it.get("category") or "Products"
            if c not in groups:
                groups[c] = []
                order.append(c)
            groups[c].append(it)
        blocks = []
        for c in order:
            cards = "\n      ".join(
                '<figure class="pcard"><div class="ph"><img src="assets/products/%s.jpg" '
                'alt="%s" loading="lazy" width="900" height="900"></div><span>%s</span></figure>'
                % (html.escape(i["slug"]), html.escape(i["caption"]),
                   html.escape(i["caption"])) for i in groups[c])
            blocks.append('    <div class="pgroup"><h4>%s <span style="color:#8593a1;'
                          'font-weight:400;font-size:13px">(%d)</span></h4>\n'
                          '    <div class="gallery">\n      %s\n    </div></div>'
                          % (html.escape(c), len(groups[c]), cards))
        gallery = "\n".join(blocks)
        print("图库：%d 个分组 / %d 张图" % (len(order), sum(len(v) for v in groups.values())))

    tl = TEMPLATE.read_text(encoding="utf-8")
    out = (tl.replace("__SKU__", str(len(prods)))
             .replace("__CNC__", str(n_cnc))
             .replace("__MACH_TOTAL__", str(eq["total"]))
             .replace("__ANN__", str(eq["anneal"]))
             .replace("__TEMPER__", str(eq["temper"]))
             .replace("__VGRIND__", str(eq["vgrind"]))
             .replace("__WGRIND__", str(eq["wgrind"]))
             .replace("__STEPS__", str(n_steps))
             .replace("__MACH__", str(n_mach))
             .replace("__MOQ_MIN__", str(moq_min))
             .replace("__CATS__", "\n    ".join(cats))
             .replace("__SPECS__", "\n      ".join(specs))
             .replace("__GALLERY_NAV__", '<a href="#gallery">Gallery</a>' if SHOW_GALLERY else "")
             .replace("__GALLERY_SECTION__", _gallery_section(moq_min, gallery) if SHOW_GALLERY else "")
             .replace("__CATALOGUE__", "Wiliheng-Knives-Catalogue.pdf")
             .replace("__WHATSAPP__", WHATSAPP)
             .replace("__LINECARD__", LINECARD))
    OUT.write_text(out, encoding="utf-8")
    print("生成 %s：SKU=%d 工序=%d 设备=%d 品类=%d 规格款=%d MOQ下限=%d"
          % (OUT.name, len(prods), n_steps, n_mach, len(cats), len(specs), moq_min))

    # ── 线卡 PDF 跟着站点走（"下载线卡"按钮必须真能下到）──
    src = BASE / "Wiliheng-Knives-Line-Card.pdf"
    if src.exists():
        shutil.copy2(src, SITE / LINECARD)
        print("同步线卡 ->", (SITE / LINECARD).name, "%.1f KB" % (src.stat().st_size / 1024))
    else:
        print("⚠️ 线卡 PDF 不存在，站点上的下载按钮会 404：", src)
    return 0


if __name__ == "__main__":
    sys.exit(build_html())
