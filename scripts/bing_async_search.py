#!/usr/bin/env python3
# Bing async 图片搜索 — 一次 30 条干净直链（2026-08 实测可用）
# 用法: python bing_async_search.py "玛尼堆 景观" [count]
# 注意: 中文词可能被污染（见 references/endpoint-matrix.md），结果务必视觉验证
import re, subprocess, urllib.parse, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
# 电商/字典/素材图标站黑名单
BLACK = ['eaton', 'chem17', 'zidian', 'bishun', 'hanyuguoxue', 'zitibang', 'lolbuku',
         'hanchacha', 'hgcha', 'hao86', 'pngsucai', 'logos', 'icon', '1688', 'taobao',
         'jd.com', 'shipin520', 'redocn', 'nipic', 'sucai', 'zcool', 'ppt', 'word']


def bing_async_images(query, first=0, count=30):
    q = urllib.parse.quote(query)
    url = f'https://cn.bing.com/images/async?q={q}&first={first}&count={count}&relp={count}'
    r = subprocess.run(['curl', '-s', '--max-time', '30', '-A', UA, url], capture_output=True)
    t = None
    for enc in ('utf-8', 'gb18030', 'gbk'):
        try:
            t = r.stdout.decode(enc)
            break
        except Exception:
            pass
    if not t:
        return []
    # Bing HTML 里图片直链格式: murl&quot;:&quot;URL&quot;
    murls = re.findall(r'murl&quot;:&quot;(.*?)&quot;', t)
    seen, out = set(), []
    for u in murls:
        u = u.replace('\\/', '/').replace('&amp;', '&')
        low = u.lower()
        if not u.startswith('http') or any(b in low for b in BLACK):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


if __name__ == '__main__':
    query = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    urls = bing_async_images(query, count=n)
    print(f'QUERY: {query} -> {len(urls)} urls')
    for u in urls:
        print(u)
