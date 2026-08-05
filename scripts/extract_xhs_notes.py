#!/usr/bin/env python3
"""extract_xhs_notes.py — 从 cua-driver get_window_state 落盘的 JSON 里提取小红书笔记卡片元素。

用法:
    python extract_xhs_notes.py <get_window_state_落盘.json> [--head N]

输出每行: element_index element_token note_id
    (note_id 即 explore/<note_id>?xsec_token=... 中的 16 位 hex 笔记 ID)

配合 web-image-sourcing 技能「小红书真实浏览器截图」工作流使用：
搜索页加载后 get_window_state(include_screenshot=false, max_elements=400) 落盘，
用本脚本拿到前 N 张卡片的 element_token，逐个 click → 截图。
"""
import json
import re
import sys

NOTE_RE = re.compile(r"explore/([0-9a-f]{16,})")

def main():
    path = sys.argv[1]
    head = None
    if len(sys.argv) > 2 and sys.argv[2] == "--head":
        head = int(sys.argv[3])

    with open(path, encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    # 兼容两种形态：顶层含 elements 数组，或 result 字段里是文本树
    elements = data.get("elements") if isinstance(data, dict) else None
    snapshot_id = data.get("snapshot_id", "?") if isinstance(data, dict) else "?"

    if elements is None:
        # 退化：从 tree_markdown / result 文本里正则捞
        text = json.dumps(data, ensure_ascii=False)
        print(f"# no structured elements; falling back to regex (snapshot {snapshot_id})")
        for m in re.finditer(r"\[(\d+)\].*?explore/([0-9a-f]{16,})", text):
            idx, nid = m.groups()
            print(f"{idx} s{snapshot_id}:{idx} {nid}")
        return

    out = []
    for el in elements:
        blob = json.dumps(el, ensure_ascii=False)
        m = NOTE_RE.search(blob)
        if not m:
            continue
        idx = el.get("element_index")
        tok = el.get("element_token")
        if idx is None or not tok:
            continue
        out.append((idx, tok, m.group(1)))

    # 保持树顺序（元素索引递增），去重同 note_id 的重复元素
    seen = set()
    rows = []
    for idx, tok, nid in out:
        if nid in seen:
            continue
        seen.add(nid)
        rows.append((idx, tok, nid))

    print(f"# snapshot: {snapshot_id} total: {len(rows)}")
    for idx, tok, nid in rows[:head] if head else rows:
        print(f"{idx} {tok} {nid}")

if __name__ == "__main__":
    main()
