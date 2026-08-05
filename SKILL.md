---
name: web-image-sourcing
description: Use when 找图/素材/案例/对标报告/搜集信息. 中文网络三维采集（搜索/专业/UGC平台）+视觉QC+HTML/PDF图鉴交付.
version: 3.2.0
author: danzey0425-lgtm
license: MIT
metadata:
  hermes:
    tags: [image-sourcing, research, china-web, cua-driver, visual-qc, casebook]
    related_skills: [reference-case-research, visual-case-research]
---

# Web Image Sourcing — 中文网络图片+信息采集总纲

## Overview

中文场景下"找案例照片/参考图/素材图/对标案例/搜集信息"的完整方法论。核心经验：**中文搜索引擎图片污染严重（Bing 中文词→丝袜广告），权威源/专业平台直采 + 批量视觉验证才是可靠路径**；**需登录平台必须用真实 Edge + cua-driver 桌面通道**（Playwright 自动化指纹必被风控 300012，防盗链只挡直链下载不挡渲染截图 → 窗口截图即高清原图）。定位：**图片+信息双输出**——不只找图，也采集项目名/设计师/材料/施工做法（B站专栏、有方项目页、建材商名录、搜索线索）。**用户要的是清单元素级特写照（玛尼堆特写、铺装纹样、标识细部），不是大场景全景**——拿到图先问"这图讲的是清单哪一项"，对不上就砍。

## When to Use

- 用户要"找图 / 素材 / 案例照片 / 对标案例 / 图集 / 图文并茂交付 / 搜集信息"
- 需从小红书/抖音/B站/gooood/有方等平台采集高清实拍或权威案例
- 需把素材做成 HTML 图鉴 / PDF / 图文报告

**Don't use for**: 用户只要单张图且明确给了 URL（直接下载即可）；纯文字调研无图片需求（用 `web-research-reports` / `reference-case-research`）。

## 0. 任务启动器（接到新主题的 SOP）

1. **确认主题与清单**：用户给的词是演示；新主题先确认（用户没给就问，或按项目工程量清单拆解：雕塑/水景/景石/铺装/树池/廊架/草阶/标识/照明/假山/围墙/种植…）。完成标准：得到明确的关键词清单或"按清单拆"的确认。
2. **拆关键词**：每元素 1-2 词，词要"行业语境"（例：藏式酒店+玛尼堆，而非裸词玛尼堆）。完成标准：词清单落盘（如 `keywords.md`）。
3. **三维开火**（见 §1）：② 专业平台拿权威案例 → ③ UGC 补真实细节 → ① 搜索平台查漏补缺。每平台采 3-4 篇/条。完成标准：每个平台截图 ≥ 3 张/关键词。
4. **采集期顺手记录**：窗口标题、平台、URL 映射在采集当下就存（事后从缓存重建是最后手段）。完成标准：每张截图在 `shot_urls.json` 或等价映射里有记录。
5. **采集完立即 QC**（窗口还开着可重截）：MD5 去重 → 大小扫描（23,846B=防盗链废图）→ 拼图批量 vision 核查 → 单张复核关键图。完成标准：全部截图 vision 过一遍、无未核实图。
6. **交付**：HTML 图鉴（先预览再导出 PDF），素材墙全量收录，🔗 溯源标注。完成标准：`verify_casebook.py` 通过 + 浏览器渲染 0 破损。
7. **复盘**：新坑/新平台结论写回本 skill（见 §7 更新日志）。完成标准：更新日志追加一条。

## 1. 三维采集层（方法论骨架）

| 维度 | 是什么 | 平台 | 用法与特点 |
|---|---|---|---|
| **① 搜索平台** | 通用搜索引擎 | Bing async、百度、360、搜狗 | **用途是"发现线索"不是"拿图"**：查项目名/设计师/术语/概念验证 → 反查专业站；Bing 图片 async 端点一次 30 条直链可用，但中文词污染严重，图片仅作补充 |
| **② 专业平台** | 垂直分享站 | gooood 谷德、有方 archiposition、在库言库 ikuku、ArchDaily 中文、ABBS、站酷、花瓣、拓者 | **质量最高、信息密度大**（项目名+设计师+年份+官方摄影）；gooood 建材区=材料选型直链；适合案例对标 |
| **③ 多用户平台** | UGC 社区 | 小红书、抖音、B站、微博、知乎 | **真实场景实拍最多**（施工现场/细节特写/本地做法）；跑题与广告混入多，QC 必做 |

**执行顺序**：② 权威案例 → ③ 真实特写 → ① 查漏补缺。
**每平台采集模式**：`references/platform-matrix.md`（总表+接入流程）→ `chinese-social-platforms.md`（UGC 实测）→ `professional-platforms.md`（专业站实测）→ `endpoint-matrix.md`（搜索端点）。

**通用桌面通道（需登录或反爬平台，真实 Edge + cua-driver）**：
```
launch_app(msedge --new-window + 搜索URL) → sleep 10-12s → get_window_state 抓树
→ 按平台形态提取卡片 token（Hyperlink 直取 / Group 点击）→ click → sleep 10-12s
→ 截图落盘 {组}_{词}_note{N}.png → 返回 → 下一卡片/下一词
```
- 前提：cua-driver MCP 已注册；`start_session(capture_scope="window")`（desktop 作用域禁用窗口工具）
- 需登录平台（小红书/抖音/微博）：用户扫码一次即可；Playwright profile 复用会触发 300012 指纹风控，勿用
- 页面内容不进 UIA 树的平台（抖音卡片是 Group 非链接）：截图+vision 定位或点 Group token
- **省 token**：抓树用 max_elements 限制；树落盘后脚本本地解析，只回传卡片 token 摘要（勿把 100KB 原树回传会话）

## 2. QC 与处理层（红线）

**图片-说明一致性（用户 QC 红线，凭标题写 caption 必翻车）**：
1. **采集时**：窗口标题含英文哲思/无主题词（impermanent/option/better）→ 当场标可疑；
2. **批量拼图核查**（4-6 张/次，左上角标文件名，vision 读图内标题逐一判定"是/否+实际标题"）→ 7 批查 40+ 张；
3. **关键图单张复核**（拼图+JPEG 会致视觉模型幻觉，入选图必须单张看）；
4. **水印三档**：商业图库水印（摄图网等）→ 必换；来源署名水印（建构物语）→ 可留但 caption 写明出处；无 → 正常；
5. **问题图黑名单零残留**：下架图写黑名单，全文 grep 确认；
6. **要点文字核查**：换图必查同页文字（要点孤儿）；无法核实的术语删/软化；统计数字对实情；废图如实标注。

**完成标准**：交付物中每张图都经过 vision 核实，黑名单零残留，无未标注的存疑图。

## 3. 交付层（HTML 图鉴 / PDF）

完整管线见 `references/html-casebook-integration.md`，要点：
- 压缩先做（720px JPEG q82，~15:1）；嵌入保留设计 tokens；素材墙 10 列全量收录
- **1920×1080 舞台最小字号（用户三次纠正后定稿）**：正文 ≥20px、要点标题 ≥28px、图注 ≥16px、主图 ≥335px、tile ≥150px
- 校验：`scripts/verify_casebook.py`（npm 挂 node 版）→ 真实渲染验证（broken 空数组 + 无 JS 错 + 溢出检查用 offsetHeight 非 getBoundingClientRect——stage scale 陷阱）
- 🔗 溯源：xsec_token 会过期（404 实测），标注用永久 note_id 直链 + "失效可按标题站内搜索"；注入用精确 str.replace 勿用模糊正则（group 错乱毁过整份 HTML）
- PDF：Playwright page.pdf() + 打印副本 inline style（**保留 class！**）+ 封面单独截图合成（三坑详见 reference）

## 4. 边界与诚实规则

- **不做**：绕过登录墙的灰色手段（硬闯只浪费时间——小红书未登录 404、百度 antiFlag、搜狗 forbid）；伪造 token（404 实测）；把推断写成事实
- **做不了就直说**：找不到可靠特写照的元素 → 相近做法图+明确标注"特写照待补"，绝不拿垃圾图充数
- **版权**：素材仅作设计参考；商用需授权（尤其含人脸/品牌/平台 UI 的截图）；来源署名如实
- **登录依赖**：需登录平台先请用户扫码（抖音搜索结果必须登录；小红书已有登录态；B站免登录）

## 5. 平台能力矩阵（总表）

| 平台 | 维度 | 登录 | UIA 形态 | 卡片提取 | 截图内容 | 坑 |
|---|---|---|---|---|---|---|
| 小红书 | ③ | 需（已登录） | 250+ 元素 Hyperlink | value 含 search_result/{note_id} | 笔记图文页 | token 过期；插画蹭标签；店名霸榜 |
| 抖音 | ③ | 需（扫码） | 登录后 286 元素，卡片=Group | Group token 点击 | 视频帧（正在播放） | 未登录 16 元素空树；泛内容混入 |
| B站 | ③ | 免 | 211 元素 Hyperlink | value 含 /video/BV | 视频页/专栏 | 游戏内容混入；广告标签 |
| gooood | ② | 免 | 147 元素 Hyperlink | value 含 .htm + Image | 项目页多图 | 招聘/广告混入；建材区 mike-x 短链 |
| 有方 | ② | 免 | 138 元素 Hyperlink | value 含 /items/ | 项目页多图+信息 | 轮播重复；商城/招聘噪音 |
| Bing 图片 | ① | 免 | curl async | murl 直链 | 原图下载 | 中文词污染严重；<4KB 丢 |
| 官网/媒体 | ② | 免 | curl 直下 | 正则提全部图 URL | 官方摄影 | CDN 防盗链需 Referer |

**新平台接入流程**：真实 Edge 打开 → 抓树判形态（Hyperlink→extract 模式 / Group→点击模式 / 空树→登录墙）→ 实测 1 卡片 → 结论写回对应 reference + 本表。

## Common Pitfalls

1. **用 Playwright/无头浏览器采集需登录平台** → 300012 指纹风控必死。换真实 Edge + cua-driver 桌面通道。
2. **凭标题/搜索词写 caption** → 必翻车（白天客房标"夜景"、佛堂标"石墙"、湖泊标"玛尼堆"、插画标"经幡"，全被用户当场抓到）。每图必须 vision 复核。
3. **把 xsec_token 当永久链接交付** → 隔天 404。用永久 note_id 直链。
4. **模糊正则注入 HTML 链接** → group 错乱毁整份文件（26 处 img 结构破坏+108 处 tno/tcap 互换事故）。用精确 str.replace + 注入后 html.parser 验证。
5. **getBoundingClientRect 判断布局溢出** → stage scale 缩放坐标误导（178.9px 量成 103px）。用 offsetHeight/computedStyle。
6. **抓树结果全文回传会话** → 单次 110KB ≈ 30K token，108 张浪费数百万。落盘+本地解析，只回传摘要。
7. **忽略登录墙** → 未登录平台（抖音/小红书未登录态）只有 10-20 个 chrome 元素，先请用户扫码再继续。
8. **单平台采集就交付** → 三维框架缺腿（案例质量/实拍细节/线索验证缺一不可）。

## Verification Checklist

- [ ] 关键词清单按主题确认（非沿用上次任务）
- [ ] 三维平台各采 ≥3 张/关键词，采集期记录了 URL 映射
- [ ] 全部截图 vision 核实过（拼图+单张），黑名单零残留
- [ ] 水印三档判定完成，商业水印图已替换
- [ ] 交付物压缩（720px）、校验脚本通过、浏览器渲染 0 破损
- [ ] 🔗 链接用永久 note_id，失效提示已写
- [ ] 新平台/新坑已写回 references + 更新日志

## 6. 脚本与参考索引

**scripts/**：`bing_async_search.py`（Bing 30 条直链）、`batch_download.py`（魔数/大小卫生）、`make_montage.py`（拼图）、`extract_xhs_notes.py`（UIA 树卡片提取）、`compress_for_casebook.py`（720px JPEG）、`verify_casebook.py`（交付校验）
**references/**：`platform-matrix.md`（平台总表+接入流程）、`chinese-social-platforms.md`（小红书/抖音/B站实测+坑位）、`professional-platforms.md`（gooood/有方实测+待测清单）、`endpoint-matrix.md`（搜索端点实测）、`xhs-url-annotation.md`（链接重建与标注）、`html-casebook-integration.md`（交付管线+QC+字号定稿+PDF 三坑）、`github-publish.md`（发布更新流程）、`prompt-template.md`（可复用提示词）
**联用**：`reference-case-research`（图文报告撰写）——本 skill 负责采集验证，该 skill 负责组织成报告。

## 7. 更新日志

- 2026-08-05 v3.2 规范对齐：frontmatter 补全（version/author/license/metadata/related_skills）、description 改 Use when 开头、补 Overview/When to Use/Common Pitfalls/Verification Checklist、每步骤加完成标准。参照 hermes-agent-skill-authoring 规范。
- 2026-08-05 v3.1：platform-matrix.md 独立成文；README 更新。
- 2026-08-05 v3 重构：踩坑史→方法树（任务启动器/三维采集/QC/交付/边界五层）；平台矩阵；双输出定位；QC 前置；诚实边界。
- 2026-08-05 v2：三维采集框架（gooood/有方 + 抖音/B站 + 关键词参数化 + GitHub 发布）。
- 2026-08-05 v1：小红书 108 张全链路沉淀，上传 GitHub。
