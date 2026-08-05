#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML casebook 交付前全量校验：结构、引用、页码、素材墙、问题图黑名单残留。

用法: python verify_casebook.py <casebook.html> [--banned "s8_taijie,s5_ditan,..."]
（--banned 传已下架问题图文件名前缀，逗号分隔，验证零残留）
"""
import sys, os, re
from html.parser import HTMLParser

VOID = {'img','br','hr','meta','link','input','source','area','base','col','embed','param','track','wbr'}

class Validator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.img_srcs = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        if tag == 'img':
            d = dict(attrs)
            if 'src' in d:
                self.img_srcs.append(d['src'])
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"多余闭合 </{tag}> @ {self.getpos()}")
            return
        top, pos = self.stack.pop()
        if top != tag:
            self.errors.append(f"标签不配对: <{top}> @{pos} 被 </{tag}> @{self.getpos()} 闭合")

def main():
    if len(sys.argv) < 2:
        print("用法: verify_casebook.py <casebook.html> [--banned \"a,b,c\"]"); sys.exit(2)
    path = sys.argv[1]
    banned = []
    if '--banned' in sys.argv:
        banned = sys.argv[sys.argv.index('--banned')+1].split(',')
    html = open(path, encoding='utf-8').read()
    base = os.path.dirname(os.path.abspath(path))

    v = Validator(); v.feed(html)
    leftover = [t for t,_ in v.stack]
    missing = [s for s in v.img_srcs if not os.path.exists(os.path.join(base, s))]
    pagenos = re.findall(r'<div class="pageno">(\d+) / (\d+)</div>', html)
    slides = len(re.findall(r'<section class="slide', html))
    total = pagenos[0][1] if pagenos else '?'
    seq_ok = all(int(a) == i+1 and b == total for i, (a, b) in enumerate(pagenos))
    els = re.findall(r'<section class="slide el">(.*?)</section>', html, re.S)
    walls = re.findall(r'<section class="slide wall">(.*?)</section>', html, re.S)
    img5 = all(len(re.findall(r'<img ', e)) == 5 for e in els)
    tiles = sum(len(re.findall(r'class="tile"', w)) for w in walls)
    residual = [b for b in banned if b in html]

    print(f"未闭合标签: {leftover if leftover else '无'}")
    print(f"解析错误: {v.errors if v.errors else '无'}")
    print(f"img 引用: {len(v.img_srcs)} 处, 缺失: {missing if missing else '无'}")
    print(f"slide={slides} 页码总数={total} 顺序: {'✓' if seq_ok and slides==int(total) else '✗'}")
    print(f"元素页={len(els)} 每页5图: {'✓' if img5 else '✗'}")
    print(f"素材墙 tile={tiles} (应108): {'✓' if tiles==108 else '✗'}")
    print(f"问题图残留: {residual if residual else '无 ✓'}")

    ok = not leftover and not v.errors and not missing and seq_ok and slides==int(total) \
         and img5 and tiles==108 and not residual
    print(f"\n总体: {'✅ 全部通过' if ok else '❌ 存在问题'}")
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
