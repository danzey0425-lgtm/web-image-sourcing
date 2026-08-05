#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量压缩采集截图供 HTML casebook/PPT 嵌入。

用法: python compress_for_casebook.py [SRC_DIR] [DST_DIR] [MAX_WIDTH] [QUALITY]
默认:  src=../xhs_shots (当前目录下), dst=<src 同级>/xhs_web, 720px, q82
效果: 108 张 1-2MB PNG → 6MB JPEG（约 15:1），浏览器秒开。

只处理 *_note*.png（正式截图命名规范，跳过 _ 开头的调试图）。
"""
import os, glob, sys
from PIL import Image

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(base), "xhs_shots")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(src), "xhs_web")
    max_w = int(sys.argv[3]) if len(sys.argv) > 3 else 720
    q = int(sys.argv[4]) if len(sys.argv) > 4 else 82
    os.makedirs(dst, exist_ok=True)

    files = sorted(glob.glob(os.path.join(src, "*_note*.png")))
    total_in = total_out = 0
    for f in files:
        name = os.path.basename(f).replace(".png", ".jpg")
        out = os.path.join(dst, name)
        if os.path.exists(out):
            continue
        im = Image.open(f).convert("RGB")
        w, h = im.size
        if w > max_w:
            im = im.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
        im.save(out, "JPEG", quality=q, optimize=True)
        total_in += os.path.getsize(f)
        total_out += os.path.getsize(out)
        print(f"{name}: {os.path.getsize(f)//1024}KB -> {os.path.getsize(out)//1024}KB")

    print(f"\n完成: {len(files)} 张, 源 {total_in//1024//1024}MB -> 压缩 {total_out//1024//1024}MB")

if __name__ == "__main__":
    main()
