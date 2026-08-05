# 专业平台采集模式（建筑/设计垂直站实测）

三维采集框架中的"② 专业平台"维度。质量最高、信息密度大（项目名+设计师+年份+官方摄影图），适合案例对标、材料选型、施工做法研究。

## gooood 谷德设计网（2026-08 实测 ⭐ 首选）

- **无需登录**，真实 Edge 直接访问 `https://www.gooood.cn`（curl 直连/代理可能超时，浏览器正常——以真实 Edge 为准）
- **UIA 树完整暴露**：147+ 元素，**项目卡片是 Hyperlink**（value 含 `.htm` 项目页链接，label = "项目名，地点 / 设计公司"），每个卡片带 Image 缩略图子元素——**与小红书同构，extract 脚本模式直接复用**（正则匹配 `gooood.cn/.*\.htm`）
- **进项目**：click 卡片 Hyperlink → 项目详情页（多图 + 设计说明 + 图纸）→ 截图/滚屏截图
- **分类与搜索**：主导航有"分类"（gooood.cn/search）、"专辑"（专题合集，如"酒店""庭院"类）；站内搜索按钮在顶部（元素 ~27）
- **建材区（对景观设计极有价值）**：首页底部"建材 Materials"栏目，实测含：钢结构廊架/板桁架、泳池系统、户外灯光-景观灯光、景观石材、艺术砖、UHPC 幕墙板等——**材料供应商直链（gooood.mike-x.com/xxx）**，做材料选型/供应商清单时可采
- **坑**：首页混有大量招聘信息（工作/招聘栏）与广告——提取时按"项目卡片"特征（label 含"项目名，地点 / 公司"或 value 含 .htm + Image 子元素）过滤；建材区链接是第三方 mike-x.com 短链，需验证可达性

## 有方 archiposition（2026-08 实测 ⭐ 案例对标首选）

- **无需登录**，`https://www.archiposition.com` 直接访问；UIA 树 138+ 元素
- **项目/文章卡片全是 Hyperlink**：value 含 `archiposition.com/items/{id}`（项目/报道）、`/travels/`（旅行）、`/video?...`（视频），带 Image 缩略图子元素
- **label 信息密度极高**："秦皇岛阿那亚第十一食堂 / 建言建筑 建筑 自然光透过天窗…2026.08.04"——项目名+设计师+分类+简介+日期一次拿全（信息采集价值大）
- **导航分类**：项目 Project（category/1675）、专辑 Series、设计公司库 Companies、竞赛——按需直达
- **坑**：首页混招聘/商城/旅行招募广告（value 含 /recruits/、youzan.com、/travels/ 的按需过滤）；轮播卡 label 重复；页面很长（加载更多分页）

## 其他专业平台（待实测，按需启用）

| 平台 | 网址 | 说明 |
|---|---|---|
| 有方 space | archiposition.com | 建筑媒体，项目/评论/展览 |
| 在库言库 | ikuku.cn | 建筑/景观案例库，中国项目多 |
| ArchDaily 中文 | archdaily.cn | 国际项目中文站 |
| ABBS | abbs.com.cn | 老牌建筑论坛，施工/材料讨论 |
| 十方 | （用户指定，待确认网址） | 用户推荐建筑分享站 |
| 站酷 ZCOOL | zcool.com.cn | 设计作品集（插画/UI/景观表现图） |
| 花瓣 | huaban.com | 采集型图库（图片直链需 Referer） |
| 拓者设计吧 | tuozhe8.com | 室内/景观设计论坛 |

启用原则：**先用真实 Edge 打开测 UIA 树形态**——Hyperlink 暴露 → 走 extract 脚本模式；只有 Group/Text → 走"截图+坐标点击"模式（见抖音）；登录墙 → 请用户扫码。实测结论随时补进本文件。

## 通用流程（专业平台）

1. launch_app --new-window 打开平台首页/搜索页（URL 编码关键词）
2. sleep 10s → get_window_state 抓树
3. 判断形态：Hyperlink（值含 .htm/.html/项目 ID）→ 复用 extract 脚本（改正则）；否则截图 + vision 定位
4. click 卡片 → 项目详情页截图（多图可滚屏分段截）
5. QC 同主流程（vision 核对 caption 与画面、水印三档判定）
6. 信息采集（不只是图）：项目名/设计师/年份/材料可读入 UIA 树 Text 元素，配合截图存档
