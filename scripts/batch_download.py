#!/usr/bin/env python3
# 批量下载图片 + 卫生检查（魔数校验、大小过滤）
# 用法: 把 fetch() 循环套在自己的 URL 列表上；referer 按来源站调整
import subprocess, os

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def fetch(url, out, referer='https://cn.bing.com/', min_size=4000):
    """下载并校验；成功返回字节数，失败返回 0 并清理半成品。"""
    subprocess.run(['curl', '-s', '-L', '--max-time', '25',
                    '-A', UA, '-e', referer, '-o', out, url])
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    if sz < min_size:
        if os.path.exists(out):
            os.remove(out)
        return 0
    with open(out, 'rb') as f:
        head = f.read(12)
    # 魔数校验: JPEG / PNG
    if not (head[:3] == b'\xff\xd8\xff' or head[:8] == b'\x89PNG\r\n\x1a\n'):
        if os.path.exists(out):
            os.remove(out)
        return 0
    return sz


# 用法示例: 遍历 URL 列表下载；原图失败回退 thumb 缩略图直链
if __name__ == '__main__':
    import sys
    urls = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'imgs'
    os.makedirs(outdir, exist_ok=True)
    for i, u in enumerate(urls):
        ext = '.jpg'
        out = os.path.join(outdir, f'{i:02d}{ext}')
        sz = fetch(u, out)
        if sz:
            print(f'ok {i:02d} {sz//1024}KB {u[:80]}')
