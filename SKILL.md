---
name: web-image-sourcing
description: Use when user asks 找图/素材/案例照片. 权威源直采、Bing async、蒙太奇拼图视觉筛选。
---

# Web Image Sourcing（中文网络图片素材搜集）

用户要"找案例照片 / 参考图 / 素材图 / 图集 / 图文并茂交付"时使用。核心经验：**中文场景下搜索引擎图片结果污染严重，权威源直采 + 批量视觉验证才是可靠路径**。**用户通常要的是清单元素级别的特写照（玛尼堆特写、铺装纹样、标识细部），不是大场景全景**——拿到图先问自己"这张图讲的是清单里的哪一项"，对不上号的果断砍掉。

## ⚠️ 关键词清单是任务参数，不是写死的

本 skill 所有示例关键词（藏式庭院 13 组、玛尼堆、鹅卵石等）**只是演示**。每次任务的关键词/主题由用户当次提供（如"日式枯山水""侘寂风酒店""茶室庭院"），流程完全通用：
- 采集侧：把用户给的关键词清单直接代入"每词一窗口、每词 3-4 篇"循环
- QC 侧：视觉核对的"预期主题"同样随任务变
- 交付侧：图鉴分组/标题/要点随主题变
**不要默认沿用上次任务的词**；用户没给清单时先问，或按用户项目工程量清单拆解（先例：13 组 = 雕塑/水景/景石/铺装/树池/廊架/草阶/标识/照明/假山/围墙/种植等工程项）。

## 三维采集框架（用户方法论，2026-08 确立）

搜集素材/信息必须**三个维度同时开火**，不是单一平台：

| 维度 | 是什么 | 平台示例 | 特点 |
|---|---|---|---|
| **① 搜索平台** | 通用搜索引擎 | Bing（async 直链）、百度、360、搜狗 | 覆盖面广但图片结果污染严重（见 endpoint-matrix）；用来发现线索、验证概念 |
| **② 专业平台** | 垂直领域分享站 | 建筑：gooood 谷德、有方 space、在库言库 ikuku、ArchDaily 中文、十方、ABBS；设计：站酷、花瓣、拓者；建材：gooood 建材区等 | **质量最高、信息密度大**（项目名+设计师+年份+图纸），官方摄影图；适合案例对标与材料选型 |
| **③ 多用户平台** | UGC 内容社区 | 小红书、抖音、B站、微博、知乎 | **真实场景实拍最多**（施工现场、细节特写、本地做法），但需视觉 QC（跑题/广告混入） |

执行顺序建议：**先 ② 专业平台拿权威案例 → 再 ③ UGC 补真实细节特写 → ① 搜索平台查漏补缺**。每平台具体采集模式见 `references/chinese-social-platforms.md`（小红书/抖音/B站/微博）与 `references/professional-platforms.md`（gooood 等建筑站实测）。

## 工作流

1. **先想权威源**（成功率最高，质量最可控）：
   - 官网图片 CDN 通常可 curl 直下（例：松赞 `image.songtsam.com/upload/...`、Dwarika's `dwarikas.com/media/...`）。
   - 媒体报道原文页：正则提取文章 HTML 中**全部**图片 URL——一篇文章常有 20-30 张，比搜索结果干净得多（例：搜狐「建构物语」瑞吉专文 28 张，其中入口标识、木格栅墙特写、酥油灯供品都是稀缺元素图）。
   - 设计站图片 CDN 可直下但站内搜索常无效（gooood 搜索返回招聘页）。
2. **搜索引擎作补充**：首选 Bing async 端点（`cn.bing.com/images/async?q=..&first=0&count=30&relp=30`），一次 30 条干净直链。完整端点实测矩阵见 `references/endpoint-matrix.md`。
3. **批量下载 + 卫生检查**：UA + Referer 头；魔数校验（JPEG `\xff\xd8\xff` / PNG `\x89PNG\r\n\x1a\n`）；大小 <4KB 丢弃；域名黑名单过滤。用 `scripts/batch_download.py`。
4. **蒙太奇拼图批量筛选**：候选图拼 2×2 或 3×2 网格，每格左上角用荧光黄标签标注文件名，一次 vision 调用看 4-6 张，快速淘汰无关图（`scripts/make_montage.py`）。
5. **关键图单张复核**：拼图缩略图 + JPEG 压缩会让视觉模型产生幻觉（脑补内容、编造地点、张冠李戴），最终入选的关键图必须**单张** vision 复核，描述只写画面中确证的元素。
6. **诚实标注缺口**：找不到可靠特写照的元素，用相近做法图 + 明确标注"特写照待补"，绝不拿垃圾图充数，也不把推断写成事实。

## 关键陷阱

- **中文查询词污染**：Bing 图片对"藏 / 玛尼 / 六字"等词返回字典页、丝袜广告、卡通角色等完全无关结果；英文词也会被污染（"mani stones"→电源设备图）。对策：换元素词精确搜，但最终以视觉验证为准。
- **browser 导航部分中文搜索页报 `'utf-8' codec can't decode byte 0xb2`**：浏览器栈对某些站点响应解码失败；改 curl 抓取 + Python 按 utf-8/gb18030 依次解码。
- **murl 提取正则**：Bing HTML 中直链格式为 `murl&quot;:&quot;URL&quot;`（&quot; 是转义引号），用 `re.findall(r'murl&quot;:&quot;(.*?)&quot;', t)`。
- **需登录态的源**（小红书未登录 404、百度 acjson 返 antiFlag、搜狗 napi 返 forbid、DDG 拿不到 vqd、Wikimedia 屏蔽）：不要硬闯，要么换权威源，要么明确请用户扫码/提供权限。**当权威源和免费搜索引擎都失败时，可用 Playwright 启动本地 Chromium（headless:false）弹出浏览器窗口**——用户扫码登录后脚本自动搜索+截图；自带 Chromium 走用户本地网络，不受 Browserbase IP 封锁。**注意**：Playwright profile 复用在部分平台（小红书）会触发自动化指纹风控（错误码 300012「IP 存在风险」），属指纹检测而非真 IP 问题——此时改用**真实浏览器 + cua-driver 桌面通道**路线（见下）。
- **真实浏览器路线（小红书/抖音等需登录平台的高清采集首选）**：用 cua-driver `launch_app` 打开用户本机 Edge 新窗口直达搜索 URL，`get_window_state` 读 UIA 树拿笔记卡片 token，后台 click 进笔记，窗口截图保存。真实指纹无风控、无「暂时无法浏览」；截图拿渲染像素，**防盗链只挡直接下载 URL、不影响截图** → 高清素材无需 App。完整流程、坑位、脚本见 `references/chinese-social-platforms.md` + `scripts/extract_xhs_notes.py`。
- **小红书链接标注（交付物加 🔗原帖 时）**：截图对应的笔记 URL 在 cua-driver 缓存 JSON 的 element `value` 字段（`search_result/{note_id}?xsec_token=...`），可从 hermes-results 的 `call_*.txt` 按 window_id 分组重建 截图→URL 映射（第 N 个卡片 = note{N}）。**但 xsec_token 是会话性的，隔天打开 explore URL 直接 404「你访问的页面不见了」**——交付时标注必须**去掉过期 token、保留永久 note_id 直链**（`xiaohongshu.com/explore/{note_id}`），并注明"失效可按标题站内搜索"。重建/注入全流程见 `references/xhs-url-annotation.md`。⚠️ 注入 HTML 链接时勿用模糊正则（patch 的 fuzzy match 会把相似 img 行当成 10 处匹配）——用 Python 精确 `str.replace` 锚定完整 URL。
- **防盗链**：部分 CDN 需要 Referer（如 huaban 的 gd-hbimg 需带来源站或 `https://cn.bing.com/`）；原图失败回退 thumb 缩略图直链。
- **360 图片接口限流**：`image.so.com/j?q=..&src=srp` 返回 JSON（`list[].img/thumb/width/height`）但限流严重（每词仅 2-4 条），只能作补充。
- **视觉模型拼图幻觉**：拼图缩略图 + JPEG 压缩会让视觉模型脑补内容、编造地点、张冠李戴；最终入选的关键图必须**单张** vision 复核。
- **browser 工具编码错误时用 Playwright 兜底**：部分中文站点在 Hermes browser 工具中报 `'utf-8' codec can't decode byte 0xb2`（响应解码 bug）；此时改用 Playwright 本地 Chromium（`chromium.launchPersistentContext`，headless:false）走用户本地网络，不受 Browserbase IP 封锁。需登录的社交平台（小红书/抖音）也可走此通道：扫码一次，cookie 持久化到 `userDataDir`，后续复用。详见 `references/chinese-social-platforms.md`。

## 脚本
- `scripts/bing_async_search.py` — Bing async 图片搜索（30 条直链/查询，含黑名单过滤）
- `scripts/batch_download.py` — 带魔数/大小卫生检查的批量下载
- `scripts/make_montage.py` — 文件名标注拼图生成器（供 vision 批量筛选）
- `scripts/extract_xhs_notes.py` — 从 cua-driver get_window_state 落盘 JSON 提取小红书笔记卡片 element_token（真实浏览器截图路线用）
- `scripts/compress_for_casebook.py` — 批量压缩采集截图（720px JPEG q82，~15:1）供 HTML casebook/PPT 嵌入
- `scripts/verify_casebook.py` — casebook 交付前全量校验（html.parser 结构 + 引用完整性 + 页码 + 素材墙 tile 数 + `--banned` 问题图黑名单零残留）；npm 项目可挂 `"test": "node verify_casebook.js"`（同逻辑 node 版）使 `npm run test` 成为真实回归门

## 参考
- `references/github-publish.md` — 本 skill 发布/更新到 GitHub 的完整路径（大陆网络：代理诊断、gh 安装与授权三坑、建仓推送、日常更新；用户偏好开源分享，仓库 danzey0425-lgtm/web-image-sourcing）
- `references/endpoint-matrix.md` — 图片搜索端点实测矩阵 + 污染案例 + 下载卫生细则
- `references/chinese-social-platforms.md` — 小红书/抖音网页端抓取模式、登录态保持、防盗链限制、真实浏览器 + cua-driver 桌面通道高清截图工作流（2026-08 实测，含全部坑位与踩坑记录）
- `references/xhs-url-annotation.md` — 截图→笔记 URL 映射重建（cua-driver 缓存 JSON 按 window_id 分组）、xsec_token 会话性过期（404 实测）、永久 note_id 直链标注、HTML 交付物注入 🔗原帖 链接的完整脚本流程
- `references/html-casebook-integration.md` — 素材整合进 HTML 交付物管线：压缩 → 嵌入（保留设计 tokens）→ 结构校验 → file:// 真实渲染验证（含 img void-element 误报、stage scale transform 测量陷阱等坑）；**含"图片-说明一致性审核"章节**（旧素材 caption 绝不可信，逐张 vision 复核、水印三档判定、问题图黑名单残留检查、自己采集素材也要读图内标题核实——用户 QC 红线）与**"要点文字核查"章节**（换图后要点孤儿、无法核实术语删/软化、统计数字一致性、素材墙废图如实标注；用户"你自己核查一遍内容"触发）与 **1920×1080 排版最小字号/图片尺寸最终定稿**（正文 ≥20px、要点标题 ≥28px、图注 ≥16px、主图 ≥335px、素材墙 10 列 tile ≥150px；用户三次纠正"文字太小"后定格）
- **联用技能**: `reference-case-research`（标案报告撰写）——本技能负责"找到并验证图片"，该技能负责"组织成图文报告"；两者联用覆盖从搜集到交付的全链路。
