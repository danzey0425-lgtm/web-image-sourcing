# Chinese Social Platforms — Image Sourcing Patterns

## Xiaohongshu (小红书)

### 可靠路线（2026-08 实测）：真实浏览器 + cua-driver 桌面通道 ⭐

**结论**：网页版「防盗链 + 跳 App」两大坑只坑自动化指纹（Playwright/headless），**不坑真实浏览器**。
真实 Edge 浏览器（用户日常 profile、真实 IP、真实指纹）打开小红书搜索页和笔记详情页**完全正常**：
无风控、无「当前笔记暂时无法浏览」、无强制跳 App。截图拿到的是**渲染像素**，防盗链只挡「直接下载图片 URL」
（无 referer 时返回 23KB 缩略图），**完全不影响页面截图质量** → 高清素材直接可截，无需 App。

### 完整工作流（cua-driver MCP）

```text
1. launch_app:  msedge.exe --new-window "https://www.xiaohongshu.com/search_result?keyword=<URL编码>&source=web_search_result_notes"
                → 返回新 window_id（每关键词开新窗口，省去地址栏导航的麻烦）
2. sleep 10s（搜索页加载）
3. get_window_state(include_screenshot=false, max_elements=400)
                → 搜索页 UIA 树暴露 250+ 元素，含全部笔记卡片链接（Hyperlink，value 含 explore/<note_id>?xsec_token=...）
4. 解析树文件 → 拿到卡片 element_token（用 extract_xhs_notes.py）
5. click(element_token)   ← 后台 synthetic click，可靠
6. sleep 10-12s（SPA 过渡 + 图片加载；截图太早会抓到旧页面/过渡帧）
7. get_window_state(include_screenshot=true, screenshot_out_file="<组号>_<关键词>_noteN.png")
                → 窗口标题 = 笔记标题（用于验证打开的是哪篇）
8. click(element 7 = 浏览器「返回」按钮) → sleep 7s → 回到搜索页
9. 重复 5-8 直到每组 3-4 篇；换关键词 → 回到步骤 1（新窗口）
```

每张截图 1568×832 窗口渲染图（1920×1080 显示缩放），图片区清晰可用。
质量快速判断：文件大小（正常笔记页截图 ~100KB+；空白/失败页明显偏小）+ 抽查 vision 复核。

### 关键坑（都踩过）

- **Playwright profile 会被风控**：`launchPersistentContext` 持久登录态复用时返回错误码 **300012「IP 存在风险」**——实际是自动化指纹检测，不是 IP 问题。别死磕 Playwright，改用真实浏览器。
- **set_value 写地址栏后回车不触发导航**：焦点不在地址栏。要么先 click 地址栏元素再 set_value + foreground return，
  要么干脆 launch_app 新窗口带 URL（最省事，推荐）。
- **foreground 按键被 Windows 前景锁拒绝**：cua-driver daemon 不在 UIAccess 级别。需要键盘时先 bring_to_front
  （AttachThreadInput 路径）再 foreground press_key；或直接点坐标让窗口获焦。
- **xsec_token 不可编造**：自造 token 打开的是 404「你访问的页面不见了」页。token 必须从 UIA 树/页面链接里拿真实值。
- **xsec_token 会过期**：采集后数小时/数天，缓存快照里的 token 打开 explore URL 即 404「页面不见了」
  （实测）。要标注原帖链接时去掉 token 只留 `explore/<note_id>` 永久 ID；URL 可从采集期缓存
  （hermes-results/call_*.txt）反查重建，无需重采（详见 html-casebook-integration.md「原帖链接标注」）。
- **搜索词被店名/品牌霸榜**：如「卵石庭院」全被一家墨西哥餐厅占掉。对策：换更精准的行业词补搜（「鹅卵石 铺装」→ 公园鹅卵石铺设工艺、庭院铺贴教程，质量极高）。
- **点击卡片后 UIA 树更新慢**：窗口标题/URL 已变但 Document 元素仍显示旧页面属正常过渡，等 10-12s 再截图，不要急着重试。
- **MCP 偶发不可达**：cua-driver 调用偶尔报 server 不可达，等 ~56s 自动恢复，不要重复轰炸。
- **cua-driver 会话生命周期**：跨长空闲/上下文压缩后 MCP 会话会失效，get_window_state 直接报错——重新 `start_session`（capture_scope='window'）即可恢复，无需重启 Edge 或重开窗口（窗口/pid 都还在）。
- **capture_scope 陷阱（必踩）**：`start_session(capture_scope='desktop')` 会**禁用 window 级工具**（get_window_state 返回"窗口作用域工具被禁用"）。修复：`end_session` → 重新 `start_session(capture_scope='window')`。批量截图流程必须用 **window scope**。
- **UIA 树形态签名**：搜索页 250+ 元素（笔记卡片链接暴露）；笔记详情页只有 ~10 个 chrome 元素（页面内容不进 UIA 树）。**别用元素数判断导航是否成功——用窗口标题（=笔记标题）+ 截图判断**；标题已变但树还小是正常过渡，等 10-12s 再截图。
- **element_token 随 snapshot 失效**：每次返回搜索页后必须重新 get_window_state（snapshot ID 递增，如 s000000d3）再点下一张卡片；用旧 token 点击会落空。模式固定为：返回 → 抓树 → extract 脚本 → 点卡片。
- **广告笔记混入搜索结果**：小红书搜索里混有自推广笔记（如"我们是标识标牌源头工厂"），标题一眼可辨，QC 时剔除。
- **新窗口白屏（18 元素空树）**：launch_app 新窗口偶发深灰空白页，UIA 树只有 ~18 个 chrome 元素——既不是笔记页的 10 个、也不是搜索页的 250+。修复：点 element 7（该树里的「刷新」按钮）或直接关窗重开；实测重开即恢复，无需换词/换 session。
- **标签标题滞后 ≠ 点击失败（判读以地址栏为准）**：点击卡片后标签标题可能仍显示旧搜索页名，但地址栏已变为 explore/<note_id>。以**地址栏 URL + 截图内容**判断导航是否成功，别只看标签标题——曾因此差点误删一张有效截图（标题旧、URL 新、截图实为目标笔记）。
- **长批量窗口堆积**：每词一窗口，13 组 × 2 词 ≈ 26+ 个 Edge 窗口。中途可顺手关掉已完成旧窗口（element 2 = 关闭按钮）减轻资源压力，也避免误点到错误窗口；window_id 映射随时可经 launch_app 返回的 windows 列表核对。

### 旧路线（保留作对照，已证实不可靠）

- Playwright `launchPersistentContext` + 2x deviceScaleFactor 截图：搜索页能截，但**笔记详情页大量显示「暂时无法浏览」**，
  且 profile 复用会触发 300012 风控。仅在没有真实浏览器可用时的最后手段。
- 直接 curl/CDN 下载图片 URL：防盗链 → 全部 23,846 字节缩略图（特征值：恰好 23846 字节 = 防盗链缩略图，可作废图判定）。

## Douyin (抖音)

### Web Access
- Search results require login ("登录后即可搜索更多精彩视频").
- Same `launchPersistentContext` approach works for keeping login state.
- Video cover images appear in search results after login, but resolution is low.
- 实测补充：抖音短视频封面是高清实拍，适合找施工现场、元素特写（配合真实浏览器截图路线同样适用）。

## When These Platforms Are Worth Using
- When **authoritative sources** (hotel official sites, architectural media articles) have no photos for niche elements (e.g., water prayer wheels, tree pits, rockery)
- When user explicitly asks for "小红书 style" real-world photos vs. professional architectural photography
- **Honesty rule**: always tell the user when a search returned no real results (e.g., "藏式树池" had zero tree pit photos on both platforms — only architecture/tourism photos)
- 批量任务（13 组 × 2 词 × 3-4 篇 = 80-100 张截图）时：每词开新窗口的流程已完全定型，逐组推进即可；中间可批量检查已存截图质量。

### 批量收尾 QC 配方（80-100+ 张时）
1. **MD5 全量去重**：execute_code 遍历 `*_note*.png`，按文件 hash 分组，找出完全重复的截图（同一笔记在不同关键词下重复出现的情况）。
2. **大小异常扫描**：正常笔记页截图 0.7-2MB；<200KB 需人工确认（单图笔记 97KB 也可能内容正常）；>2.5MB 罕见。23,846 字节 = 防盗链缩略图特征值，直接判废。
3. **vision 单张抽查 2-3 张关键图**：确认主图清晰、非空白页、非加载失败帧。
4. **写 `交付清单.md`**：逐组列出亮点素材 + 明确标出需剔除的图（广告笔记、被店名/品牌霸榜的跑题图）与真实性存疑的图（如"扎什伦布寺绿松石地板"笔记未经考证，标注"作为灵感素材可用"），供用户裁切使用。
