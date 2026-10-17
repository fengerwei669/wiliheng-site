#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把白底成品图同步进站点（按 products.json 的清单，改名成有意义的英文名）。

为什么要有这一步：客户拍的图叫「微信图片_20260923181456_44_16.jpg」，
直接放上站点对搜索和分享都不友好，也看不出是什么；同步时统一改成
`chef-knife-damascus.jpg` 这种 slug，同时只搬 **web 尺寸（900px）** 的那张
（原图 4000px 一张 4MB，站点上十张就崩）。

用法：
    python site/sync_products.py            # 按清单同步（缺图会列出来）
    python site/sync_products.py --check    # 只看清单里哪些图还没生成
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SITE = BASE / "site"
DEST = SITE / "assets" / "products"
MANIFEST = SITE / "products.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    srcdir = Path(m.get("_src_dir") or "")
    items = m["items"]
    DEST.mkdir(parents=True, exist_ok=True)

    ok, missing = 0, []
    for it in items:
        for cand in ("%s_白底_web.jpg" % it["src"], "%s_白底.jpg" % it["src"]):
            p = srcdir / cand
            if p.exists():
                break
        else:
            missing.append(it["src"]); continue
        if a.check:
            ok += 1; continue
        shutil.copy2(p, DEST / (it["slug"] + ".jpg"))
        ok += 1

    print("同步 %d/%d 张 → %s" % (ok, len(items), DEST))
    if missing:
        print("⚠️ 还没生成白底图的 %d 张：" % len(missing))
        for s in missing[:12]:
            print("   -", s)
        print("   （跑 _bgvenv/Scripts/python.exe make_white_bg.py \"D:\\产品白底图\" "
              "--out \"D:\\产品白底图\\白底图成品\" --web 900 --skip-existing）")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
