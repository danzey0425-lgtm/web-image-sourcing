# web-image-sourcing — 中文网络图片素材搜集 Agent Skill

> 中文场景下「找案例照片 / 参考图 / 素材图 / 图集」的完整方法论，打包成 AI Agent Skill（Anthropic/OpenAI/Hermes 等兼容 SKILL.md 格式）。

## 这是什么

中文互联网搜图三大痛点：**搜索引擎图片结果污染**（Bing 中文词被广告/无关图霸榜）、**需登录平台防盗链**、**视觉验证缺失**（AI 凭标题写 caption 与实图不符）。

本 skill 把 2026-08 实测验证的完整路径固化下来，覆盖：

| 模块 | 内容 |
|---|---|
| **权威源直采** | 官网图片 CDN 直下（松赞/Dwarika's）、媒体报道原文页整篇抓图（一篇文章 20-30 张）、设计站 CDN |
| **搜索引擎补充** | Bing async 端点一次 30 条直链、污染黑名单、360 限流/百度反爬应对 |
| **批量下载卫生** | UA/Referer、魔数校验、<4KB 丢弃、域名黑名单 |
| **视觉筛选流水线** | 蒙太奇拼图批量核查 → 关键图单张复核 → 诚实标注缺口 |
| **需登录平台采集** ⭐ | 小红书/抖音：**真实 Edge + cua-driver 桌面操控截图**（Playwright 自动化指纹必被风控 300012；防盗链只挡直链下载不挡渲染截图 → 窗口截图即高清原图） |
| **图鉴交付管线** | 批量压缩（15:1）→ HTML 图鉴（19 页 1920×1080）→ 视觉 QC 红线 → 原帖链接标注（xsec_token 过期 → 永久 note_id）→ PDF 导出（Playwright + 三坑修复） |

## 目录结构

```
web-image-sourcing/
├── SKILL.md                          # 主技能：工作流 + 关键陷阱
├── references/
│   ├── chinese-social-platforms.md   # 小红书/抖音桌面通道完整工作流 + 全部坑位
│   ├── endpoint-matrix.md            # 图片搜索端点实测矩阵 + 污染案例
│   ├── html-casebook-integration.md  # 素材→HTML/PDF 交付管线 + QC 红线 + 字号定稿
│   ├── xhs-url-annotation.md         # 截图→笔记 URL 映射重建 + token 过期处理
│   └── prompt-template.md            # 可复用提示词模板（分享给任何 AI）
└── scripts/
    ├── extract_xhs_notes.py          # cua-driver UIA 树 → 小红书笔记卡片 token
    ├── batch_download.py             # 带魔数/大小卫生检查的批量下载
    ├── bing_async_search.py          # Bing async 图片搜索（30 直链/查询）
    ├── make_montage.py               # 文件名标注拼图生成器（视觉批量筛选）
    ├── compress_for_casebook.py      # 截图批量压缩（720px JPEG q82，~15:1）
    └── verify_casebook.py            # 图鉴交付前全量校验（结构/引用/页码/tile）
```

## 安装

- **Hermes**：`hermes skills install <本目录>` 或手动放入 `skills/research/web-image-sourcing/`
- **Claude Code / Codex / OpenCode 等**：按各平台 skill 目录规范放入 `web-image-sourcing/` 文件夹
- **依赖**：cua-driver（MCP 注册 `hermes mcp add cua-driver`）、真实 Edge 浏览器（已登录目标平台）、Python 3 + PIL

## 核心结论（实测 2026-08）

1. **Playwright/无头浏览器在需登录平台必死**：小红书返回错误码 300012「IP 存在风险」——是自动化指纹检测，不是 IP 问题。换真实浏览器 + cua-driver 桌面通道。
2. **防盗链不挡截图**：小红书防盗链只拦「直接下载图片 URL」（返回 23,846 字节缩略图），浏览器渲染后的窗口截图就是高清原图像素。
3. **视觉验证是红线**：凭笔记标题/搜索词写 caption 必翻车（白天客房标"夜景"、佛堂标"石墙"、湖泊标"玛尼堆"、插画标"经幡"均被用户当场抓到）。每张图必须 vision 复核。
4. **xsec_token 会话级过期**：采集数小时后带 token 的链接打开即 404。交付标注用永久 `explore/{note_id}` 直链。

## 实战成绩

2026-08 藏式庭院景观图鉴：13 组 × 2 词 × 4 篇 = **108 张高清实拍**（1568×832 渲染像素）→ 19 页 HTML 图鉴 + 19 页 PDF（10MB，含 108 张素材墙 + 每图 🔗原帖 溯源链接），全程 3-4 小时含 7 轮视觉 QC 与 11 处内容更正。

## License

MIT — 自由使用/修改/再分发，保留出处即可。
