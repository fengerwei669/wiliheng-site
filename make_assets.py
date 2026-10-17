#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成站点所需的图片资源（用真实数据，不画假图）：
  · assets/og.jpg               1200×630 社交分享预览图（微信/WhatsApp/LinkedIn 发链接时的缩略图）
  · assets/apple-touch-icon.png 180×180 手机主屏图标
  · assets/favicon-32.png       32×32

为什么需要：og:image 指向不存在的文件时，分享链接时卡片是空的 —— 客户看到的是一片白。
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
SITE = BASE / "site"
ASSETS = SITE / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

NAVY = (20, 32, 46)
TEAL = (15, 92, 79)
WHITE = (255, 255, 255)
GREY = (169, 186, 201)
MINT = (120, 214, 190)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/msyhbd.ttc", "C:/Windows/Fonts/arial.ttf",
]


def font(size):
    for f in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()


def og(stats=None):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 14, H], fill=TEAL)
    d.rectangle([0, H - 8, W, H], fill=TEAL)

    # 右上角联系方式（放右下角和 stats 标签会撞、还会超出右边界 —— 实测踩过）
    f = font(21)
    line = "wiliheng.com  |  WhatsApp +86 181-2488-6695"
    d.text((W - 70 - d.textlength(line, font=f), 76), line, font=f, fill=GREY)

    d.text((70, 74), "YANGJIANG WILIHENG KNIVES CO., LTD", font=font(24), fill=GREY)
    d.text((70, 128), "Wholesale knives,", font=font(64), fill=WHITE)
    d.text((70, 206), "made in our own factory.", font=font(64), fill=WHITE)
    d.text((70, 318), "OEM / ODM manufacturer in Yangjiang, China", font=font(29), fill=GREY)
    d.text((70, 368), "Folding  ·  fixed blades  ·  kitchen knives  ·  silicone  ·  304 tableware",
           font=font(25), fill=(140, 162, 182))

    if stats:
        x = 70
        for num, label in stats:
            d.text((x, 468), num, font=font(44), fill=MINT)
            d.text((x, 524), label.upper(), font=font(18), fill=GREY)
            x += 260

    p = ASSETS / "og.jpg"
    im.save(p, "JPEG", quality=90, optimize=True, progressive=True)
    print("✓ %s  %dx%d  %.1f KB" % (p.name, W, H, p.stat().st_size / 1024))


def icons():
    src = ASSETS / "favicon.png"
    if src.exists():
        icon = Image.open(src).convert("RGBA")
    else:
        icon = Image.new("RGBA", (512, 512), NAVY)
        ImageDraw.Draw(icon).text((176, 150), "W", font=font(260), fill=WHITE)
    for size, name in ((180, "apple-touch-icon.png"), (32, "favicon-32.png")):
        im = Image.new("RGBA", (size, size), NAVY)
        r = icon.resize((int(size * 0.82), int(size * 0.82)), Image.LANCZOS)
        im.paste(r, ((size - r.width) // 2, (size - r.height) // 2), r)
        p = ASSETS / name
        im.convert("RGB").save(p, "PNG")
        print("✓ %s  %dx%d  %.1f KB" % (name, size, size, p.stat().st_size / 1024))


if __name__ == "__main__":
    import sqlite3
    con = sqlite3.connect(str(BASE / "mes" / "mes.db"))
    n_sku = con.execute("select count(*) from products").fetchone()[0]
    n_steps = con.execute("select count(*) from steps").fetchone()[0]
    n_cnc = int(con.execute(
        "select sum(coalesce(qty,1)) from equipment where name like '%CNC%'").fetchone()[0] or 0)
    n_total = int(con.execute("select sum(coalesce(qty,1)) from equipment").fetchone()[0] or 0)
    con.close()
    # 真实数字（来自 MES，与首页一致，绝不手写）
    og([(str(n_sku), "active models"), (str(n_total), "machines on site"),
        (str(n_cnc), "CNC machining centres"), (str(n_steps), "in-house processes")])
    icons()
    sys.exit(0)
