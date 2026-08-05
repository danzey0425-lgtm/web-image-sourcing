# 复用提示词模板 —— 小红书实拍素材 → 景观图鉴流水线

> 用法：把下面提示词整段粘贴给任何 AI agent（Hermes / Claude Code / ChatGPT 等），替换【】中的内容即可。
> 前置条件：目标机器已装 cua-driver 并注册 MCP（55 个工具），有真实 Edge 且已登录小红书（"个人" profile）。

---

【任务】：我需要采集小红书高清实拍素材，并制作成一份图文并茂的【景观元素图鉴】。

【主题】：藏式/喜马拉雅文化圈酒店景观对标案例，工程量清单元素共 13 组：
01 玛尼堆雕刻/煨桑炉；02 水转经筒/藏式庭院水景；03 玛尼石刻/六字真言石头；
04 经幡藏式/转经筒门；05 藏式铺装地面/卵石庭院；06 庭院树池/石砌花坛藏式；
07 藏式廊架/木构走廊；08 草阶台阶/石缝植草；09 藏文标牌/景区导视藏式；
10 酥油灯/藏式灯笼夜景；11 假山叠水/庭院瀑布藏式；12 藏式围墙白墙/毛石墙肌理；
13 格桑花海/高原花卉庭院

每组 2 个搜索关键词，每个关键词点进 3-4 篇笔记截图，总计约 108 张高清图。

### 执行要求（严格遵守）

1. 采集通道：使用真实 Edge 浏览器 + cua-driver 桌面操控（MCP 工具 mcp__cua_driver__*）。
   禁止用 Playwright/无头浏览器——小红书自动化指纹风控（错误码 300012）必挂。

2. 会话：start_session(capture_scope="window")——必须 window 作用域，desktop 作用域会禁用窗口工具。

3. 导航：每个关键词用 launch_app 带 --new-window + 搜索 URL 打开独立窗口：
   https://www.xiaohongshu.com/search_result?keyword={URL编码}&source=web_search_result_notes
   等 10-12s 加载。

4. 提取卡片：get_window_state(include_screenshot=false, max_elements=400) 抓 UIA 树，
   从 elements 里找 value 含 search_result/ 和 xsec_token= 的链接元素
   （按 element_index 排序、按 note_id 去重），前 N 个就是 note1-N。

5. 进笔记截图：click 卡片 token → sleep 12s（SPA 慢）→
   get_window_state(include_screenshot=true, screenshot_out_file="{组}_{关键词}_note{N}.png") →
   click element 7（返回）→ sleep 7s。截图命名规范：{两位组号}_{关键词}_note{N}.png。

6. 截图即原图：窗口截图 = 高清渲染像素（防盗链只挡直链下载，不挡渲染截图）。每张约 1-2MB 属正常。

7. 霸榜处理：若关键词被店名/广告霸榜（如"卵石庭院"全是餐厅），补搜更精准词（如"鹅卵石 铺装"）补齐数量。

8. 视觉 QC（红线）：所有截图必须用视觉模型逐张核对"图片实际内容"与 caption 一致——
   禁止凭笔记标题写 caption。先例教训：白天客房照片被标"夜景"、佛堂被标"干砌石墙"、
   湖泊被标"玛尼堆"、宗教插画被标"经幡"，全被用户当场抓包。批量核查用 2×2/2×3 拼图法（每张标 IMG 编号）。

9. 链接标注：每张实拍图旁标注原帖链接 https://www.xiaohongshu.com/explore/{note_id}
   （必须去掉 xsec_token——token 会过期，实测过期后打开 404；note_id 永久有效）。失效时提示"按标题站内搜索"。

10. 交付物：
   - HTML 图鉴（1920×1080 横版，可键盘翻页）：封面 + 索引 + 每元素 1 页
     （左侧设计要点 3-4 条 + 右侧 5 图）+ 结尾 + 素材墙（全部截图分 2-3 页网格展示）
   - 可读性硬标准：要点标题 ≥28px、正文 ≥20px、图注 ≥16px、主图 ≥335px 高
   - 先交付 HTML 预览给用户确认，再导出 PDF（每页一张，1920×1080）

11. PDF 导出（若需要）：
   - 生成打印副本：给 stage 和每个 section 写死 inline style
     （position:relative / height:1080px / page-break-after:always），保留原 class
   - 用 Playwright page.pdf({width:'1920px', height:'1080px', printBackground:true})
     （Edge headless 直出会是空白）
   - 封面若空白：屏幕模式单独截图封面，PyMuPDF 合成到第 1 页
   - 最后 save(garbage=4, deflate=True) 压缩

12. 中途自查：每完成 2-3 组，抽查截图确认非空白/非无关内容；发现不对立即修正，不要等全部做完。

【输出】：全部截图保存到指定目录；HTML 图鉴 + PDF；一张"截图文件名 → 原帖链接"映射表。

---

## 使用示例（最小替换）

把上面模板中：【任务】【主题】【13 组清单】按实际替换；其他通用。
换主题时只需改第 4-5 行那种"01 玛尼堆…"格式的组名与关键词。

## 成功案例参考（2026-08 藏式庭院景观图鉴）

- 13 组 × 2 词 × 4 篇 = 108 张高清实拍（1568×832 渲染像素）
- 19 页 HTML 图鉴 + 19 页 PDF（10MB，garbage=4 压缩）
- 全程约 3-4 小时（含 7 轮视觉 QC 与 11 处内容更正）
- 原图 141MB → 压缩 6.6MB 嵌入交付物
