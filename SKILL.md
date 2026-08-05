---
name: web-image-sourcing
description: 中文网络图片+信息采集与图鉴交付总纲。三维采集、视觉QC、HTML/PDF交付。Use when 找图/素材/案例/对标报告。
---

# Web Image Sourcing — 中文网络图片+信息采集总纲

用户要"找案例照片 / 参考图 / 素材图 / 对标案例 / 图文并茂交付 / 搜集信息"时使用。
**定位：图片+信息双输出**——不只找图，也采集项目名/设计师/材料/施工做法等信息（B站专栏、有方项目页、建材商名录、搜索线索）。
核心经验：**中文搜索引擎图片污染严重（Bing 中文词→丝袜广告），权威源/专业平台直采 + 批量视觉验证才是可靠路径**。
**用户要的是清单元素级特写照（玛尼堆特写、铺装纹样、标识细部），不是大场景全景**——拿到图先问"这图讲的是清单哪一项"，对不上就砍。

---

## 0. 任务启动器（接到新主题的 SOP）

1. **确认主题与清单**：用户给的词是演示；新主题先确认（用户没给就问，或按项目工程量清单拆解：雕塑/水景/景石/铺装/树池/廊架/草阶/标识/照明/假山/围墙/种植…）。
2. **拆关键词**：每元素 1-2 词，词要"行业语境"（例：藏式酒店+玛尼堆，而非裸词玛尼堆）。
3. **三维开火**（见 §1）：② 专业平台拿权威案例 → ③ UGC 补真实细节 → ① 搜索平台查漏补缺。每平台采 3-4 篇/条。
4. **采集期顺手记录**：窗口标题、平台、URL 映射在采集当下就存（事后从缓存重建是最后手段）——QC 与链接标注都靠它。
5. **采集完立即 QC**（窗口还开着可重截）：MD5 去重 → 大小扫描（23,846B=防盗链废图）→ 拼图批量 vision 核查 → 单张复核关键图。
6. **交付**：HTML 图鉴（先预览再导出 PDF），素材墙全量收录，🔗 溯源标注。
7. **复盘**：新坑/新平台结论写回本 skill（见 §7 更新日志）。

---

## 1. 三维采集层（方法论骨架）

| 维度 | 是什么 | 平台 | 用法与特点 |
|---|---|---|---|
| **① 搜索平台** | 通用搜索引擎 | Bing async、百度、360、搜狗 | **用途是"发现线索"不是"拿图"**：查项目名/设计师/术语/概念验证 → 反查专业站；Bing 图片 async 端点一次 30 条直链可用，但中文词污染严重，图片仅作补充 |
| **② 专业平台** | 垂直分享站 | gooood 谷德、有方 archiposition、在库言库 ikuku、ArchDaily 中文、ABBS、站酷、花瓣、拓者 | **质量最高、信息密度大**（项目名+设计师+年份+官方摄影）；gooood 建材区=材料选型直链；适合案例对标 |
| **③ 多用户平台** | UGC 社区 | 小红书、抖音、B站、微博、知乎 | **真实场景实拍最多**（施工现场/细节特写/本地做法）；跑题与广告混入多，QC 必做 |

**执行顺序**：② 权威案例 → ③ 真实特写 → ① 查漏补缺。**每平台采集模式见 `references/platform-matrix.md`（总表）→ `chinese-social-platforms.md`（UGC 实测）→ `professional-platforms.md`（专业站实测）→ `endpoint-matrix.md`（搜索端点）**。

**通用桌面通道（需登录或反爬平台，真实 Edge + cua-driver）**：
```
launch_app(msedge --new-window + 搜索URL) → sleep 10-12s → get_window_state 抓树
→ 按平台形态提取卡片 token（Hyperlink 直取 / Group 点击）→ click → sleep 10-12s
→ 截图落盘 {组}_{词}_note{N}.png → 返回 → 下一卡片/下一词
```
- 前提：cua-driver MCP 已注册；`start_session(capture_scope="window")`（desktop 作用域禁用窗口工具）
- 真实指纹无风控；**防盗链只挡直接下载 URL、不挡渲染截图** → 窗口截图=高清原图
- 需登录平台（小红书/抖音/微博）：用户扫码一次即可；Playwright profile 复用会触发 300012 指纹风控，勿用
- 页面内容不进 UIA 树的平台（抖音卡片是 Group 非链接）：截图+vision 定位或点 Group token

---

## 2. QC 与处理层（红线）

**图片-说明一致性（用户 QC 红线，凭标题写 caption 必翻车）**：
1. **采集时**：窗口标题含英文哲思/无主题词（impermanent/option/better）→ 当场标可疑；
2. **批量拼图核查**（4-6 张/次，左上角标文件名，vision 读图内标题逐一判定"是/否+实际标题"）→ 7 批查 40+ 张；
3. **关键图单张复核**（拼图+JPEG 会致视觉模型幻觉，入选图必须单张看）；
4. **水印三档**：商业图库水印（摄图网等）→ 必换；来源署名水印（建构物语）→ 可留但 caption 写明出处；无 → 正常；
5. **问题图黑名单零残留**：下架图写黑名单，全文 grep 确认；
6. **要点文字核查**：换图必查同页文字（要点孤儿）；无法核实的术语删/软化；统计数字对实情；废图如实标注。

**批量收尾**：MD5 全量去重 → 大小异常扫描 → vision 抽查关键图 → 写交付清单.md（亮点+需剔除+存疑标注）。

---

## 3. 交付层（HTML 图鉴 / PDF）

完整管线见 `references/html-casebook-integration.md`，要点：
- 压缩先做（720px JPEG q82，~15:1）；嵌入保留设计 tokens；素材墙 10 列全量收录
- **1920×1080 舞台最小字号（用户三次纠正后定稿）**：正文 ≥20px、要点标题 ≥28px、图注 ≥16px、主图 ≥335px、tile ≥150px
- 校验：`scripts/verify_casebook.py`（npm 挂 node 版）→ 真实渲染验证（broken 空数组 + 无 JS 错 + 溢出检查用 offsetHeight 非 getBoundingClientRect——stage scale 陷阱）
- 🔗 溯源：xsec_token 会过期（404 实测），标注用永久 note_id 直链 + "失效可按标题站内搜索"；注入用精确 str.replace 勿用模糊正则（group 错乱毁过整份 HTML）
- PDF：Playwright page.pdf() + 打印副本 inline style（保留 class！）+ 封面单独截图合成（三坑详见 reference）

---

## 4. 边界与诚实规则

- **不做**：绕过登录墙的灰色手段（硬闯只浪费时间——小红书未登录 404、百度 antiFlag、搜狗 forbid）；伪造 token（404 实测）；把推断写成事实
- **做不了就直说**：找不到可靠特写照的元素 → 相近做法图+明确标注"特写照待补"，绝不拿垃圾图充数
- **版权**：素材仅作设计参考；商用需授权（尤其含人脸/品牌/平台 UI 的截图）；来源署名如实
- **登录依赖**：需登录平台先请用户扫码（抖音搜索结果必须登录；小红书已有登录态；B站免登录）

---

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

---

## 6. 脚本与参考索引

**scripts/**：`bing_async_search.py`（Bing 30 条直链）、`batch_download.py`（魔数/大小卫生）、`make_montage.py`（拼图）、`extract_xhs_notes.py`（UIA 树卡片提取）、`compress_for_casebook.py`（720px JPEG）、`verify_casebook.py`（交付校验）
**references/**：`platform-matrix.md`（本表+接入流程）、`chinese-social-platforms.md`（小红书/抖音/B站实测+全部坑位）、`professional-platforms.md`（gooood/有方实测+待测清单）、`endpoint-matrix.md`（搜索端点实测）、`xhs-url-annotation.md`（链接重建与标注）、`html-casebook-integration.md`（交付管线+QC+字号定稿+PDF 三坑）、`github-publish.md`（发布更新流程）、`prompt-template.md`（可复用提示词）
**联用**：`reference-case-research`（图文报告撰写）——本 skill 负责采集验证，该 skill 负责组织成报告。

---

## 7. 更新日志

- 2026-08-05 v3 重构：踩坑史→方法树（任务启动器/三维采集/QC/交付/边界五层）；新增平台能力矩阵总表；定位升级为图片+信息双输出；QC 前置原则；诚实边界成文。原因：反思诊断——旧版是事件驱动堆砌，无导航无 SOP。
- 2026-08-05 v2：三维采集框架（专业平台实测 gooood/有方 + 抖音/B站桌面通道 + 关键词参数化 + GitHub 发布流程）。
- 2026-08-05 v1：小红书 108 张全链路沉淀（桌面通道/QC 红线/HTML 图鉴/PDF 导出/🔗 标注），上传 GitHub。
