# 小红书截图 → 原笔记链接标注（2026-08 实测）

给 HTML 交付物（casebook/图鉴）的每张小红书实拍图加"🔗原帖"链接时的完整流程。

## 1. 重建 截图文件名 → 笔记 URL 映射

截图命名规律：采集时对每个搜索词窗口，`extract_notes.py` 输出的第 N 个卡片 = 该词 `note{N}` 截图。

数据源：cua-driver `get_window_state` 落盘 JSON（Hermes 结果缓存目录
`~/AppData/Local/hermes/profiles/<profile>/cache/terminal/hermes-results/call_*.txt`）。

关键字段：
- 窗口标题：`structuredContent.tree_markdown` 首行 `- Window "关键词 - 小红书搜索 - ..."` → 关键词 ↔ 截图前缀（如 `12_毛石墙肌理`）
- 笔记 URL：element 的 `value` 字段，格式
  `https://www.xiaohongshu.com/search_result/{note_id}?xsec_token=...&xsec_source=pc_search`

重建脚本逻辑（每个窗口取 URL 数最多的一份快照作为搜索页代表）：
```python
import json, glob, re
RES = r"...\hermes-results"
windows = {}  # window_id -> {"title","urls"}
for f in glob.glob(RES + r"\call_*.txt"):
    data = json.load(open(f, encoding='utf-8', errors='replace'))
    sc = data.get('structuredContent', {})
    tree = sc.get('tree_markdown', '') or ''
    urls, seen = [], set()
    for e in sorted(sc.get('elements', []) or [], key=lambda x: x.get('element_index', 0)):
        val = e.get('value') or ''
        if 'xsec_token' in val and 'search_result/' in val:
            nid = val.split('?')[0].rstrip('/').split('/')[-1]
            if nid in seen: continue
            seen.add(nid); urls.append(val)
    if not urls: continue
    w = windows.setdefault(sc.get('window_id'), {"title": tree.split('\n')[0], "urls": []})
    if len(urls) > len(w["urls"]): w.update(urls=urls, title=tree.split('\n')[0])
# 关键词匹配 → 第 N 个 URL = {前缀}_note{N}.jpg
```

## 2. xsec_token 会话性过期（实测）

采集当天生成的 `explore/{id}?xsec_token=...` 链接，隔天用真实 Edge 打开返回
**「小红书 - 你访问的页面不见了」**（404）。token 是会话级凭据，不可伪造、不可复用。

**标注策略**：交付物中链接一律去掉过期 token，只保留永久 note_id 直链：
`https://www.xiaohongshu.com/explore/{note_id}`
并在交付物结尾注明："🔗 为小红书原笔记直链（笔记 ID 永久，token 过期时可按标题站内搜索）"。

## 3. HTML 注入 🔗原帖 链接

- 元素页 caption：在 `<div class="cap">…</div>` 文本尾部追加
  `<a href="{url}" target="_blank" title="小红书原笔记">🔗原帖</a>`
- 素材墙 tile：tcap 尾部追加 `<a class="xlink" href="{url}" target="_blank">🔗</a>`
- 注入用 Python 精确替换（锚定完整 URL），**不要用 patch 工具的模糊匹配**——fuzzy match
  会把所有结构相似的 img 行当成同一目标（实测 10 处匹配），要用 `str.replace` 或
  唯一上下文锚定。

## 4. 注入脚本的正则陷阱（血泪）

给 img 行注入时正则捕获组顺序写错（`group(1)/group(2)` 与替换模板错位）会**破坏原 HTML**：
`<img src=" alt="xxx""caption<div class="cap">filename</div>` 这种损坏串。修复法：匹配
`<img src=" alt="([^"]*)"(.*?)<div class="cap">(deck_assets/xhs_web/[^<]+)</div>` 反向重建。
教训：**先对副本测试注入脚本**，或注入后立即跑结构校验（html.parser 标签配对 + 图片存在性）。

## 5. 验证

- `npm run test`（若项目挂了 verify_casebook.js）：173 imgs / 108 tiles / 19 slides
- 浏览器 console：`[...document.images].filter(i => i.complete && i.naturalWidth === 0).length` 应 = 0
- 链接计数：`document.querySelectorAll('a').length` 与预期一致（元素页 53 + 素材墙 108 + 其他）
