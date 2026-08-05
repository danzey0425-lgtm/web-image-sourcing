#!/usr/bin/env python3
# 蒙太奇拼图生成器 — 每格左上角荧光黄文件名标签，供 vision 批量筛选
# 用法: python make_montage.py <图片目录> [输出路径]
# 说明: 一次 vision 调用看 4-6 张；但最终入选关键图必须单张复核（拼图易致视觉模型幻觉）
import glob, os, sys
from PIL import Image, ImageDraw

CELL = (480, 360)


def fit(img, size):
    img.thumbnail(size, Image.LANCZOS)
    c = Image.new('RGB', size, (20, 20, 20))
    c.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2))
    return c


def montage(files, out, cols=2, label_color=(237, 255, 69)):
    rows = (len(files) + cols - 1) // cols
    m = Image.new('RGB', (CELL[0] * cols, CELL[1] * rows), (20, 20, 20))
    d = ImageDraw.Draw(m)
    for i, f in enumerate(files):
        try:
            im = Image.open(f).convert('RGB')
        except Exception:
            continue
        cell = fit(im, CELL)
        x, y = (i % cols) * CELL[0], (i // cols) * CELL[1]
        m.paste(cell, (x + (CELL[0] - im.width) // 2, y + (CELL[1] - im.height) // 2))
        d.rectangle([x, y, x + 110, y + 22], fill=label_color)
        d.text((x + 5, y + 3), os.path.basename(f), fill=(0, 0, 0))
    m.save(out, quality=82)
    print(f'saved {out} ({len(files)} imgs)')


if __name__ == '__main__':
    d = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join('montages', os.path.basename(d) + '.jpg')
    files = sorted(glob.glob(os.path.join(d, '*.*')))[:12]
    for g in range(0, len(files), 4):
        montage(files[g:g + 4], f'{os.path.splitext(out)[0]}_g{g // 4}.jpg')
