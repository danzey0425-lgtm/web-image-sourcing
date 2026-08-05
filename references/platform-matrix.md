# 平台能力矩阵（总表 + 新平台接入流程）

三维采集框架中所有已验证平台的速查表。**新增平台先看底部接入流程**，实测结论写回本表。

## 总表

| 平台 | 维度 | 登录 | UIA 形态 | 卡片提取 | 截图内容 | 坑 |
|---|---|---|---|---|---|---|
| 小红书 | ③ UGC | 需（Edge 已登录） | 250+ 元素，卡片=Hyperlink | value 含 `search_result/{note_id}` | 笔记图文页 | xsec_token 会话级过期；插画蹭标签；店名/品牌霸榜（换精准词补搜） |
| 抖音 | ③ UGC | 需（扫码一次） | 未登录仅 16 元素空树；登录后 286 元素，卡片=**Group** | Group token 点击 | 视频帧（正在播放，暂停可截封面） | 未登录硬拦截；泛内容混入（游戏/广告）；视频帧含人物 |
| B站 | ③ UGC | 免 | 211 元素，卡片=Hyperlink | value 含 `/video/BV` | 视频页/专栏页 | 游戏内容混入；广告标签；播放器 UI 占画面（用暂停帧） |
| gooood 谷德 | ② 专业 | 免 | 147 元素，卡片=Hyperlink | value 含 `.htm` + Image 子元素 | 项目页多图+设计说明 | 招聘/广告混入；建材区是 mike-x.com 短链需验证；站内搜索无效（返回招聘页） |
| 有方 archiposition | ② 专业 | 免 | 138 元素，卡片=Hyperlink | value 含 `/items/{id}` | 项目页多图+信息（label 含项目名/设计师/日期） | 轮播卡片 label 重复；商城/招聘噪音 |
| Bing 图片 | ① 搜索 | 免 | curl async JSON | `murl&quot;` 直链 | 原图下载 | 中文词污染严重（藏/玛尼→丝袜广告）；<4KB 丢；360 限流每词 2-4 条 |
| 官网/媒体 | ② 权威 | 免 | curl 直下 | 正则提文章全部图 URL | 官方摄影图 | CDN 防盗链需 Referer（huaban 需带来源站）；原图失败回退 thumb |

## 待测专业站（按需启用）

在库言库 ikuku（建筑/景观案例库）、ArchDaily 中文、ABBS 论坛（施工/材料讨论）、站酷 ZCOOL（表现图/插画）、花瓣 huaban（采集图库）、拓者设计吧（室内/景观论坛）。

## 新平台接入流程

1. **真实 Edge 打开目标站**（launch_app --new-window，URL 编码关键词），sleep 10-12s；
2. **抓树判形态**（get_window_state max_elements=400）：
   - 卡片是 Hyperlink（value 含 URL）→ **extract 模式**：正则提 token，click 进详情截图（小红书/B站/gooood/有方同构）；
   - 卡片是 Group/Text（无 URL）→ **点击模式**：click Group token 或截图+vision 定位坐标（抖音）；
   - 树只有 chrome 元素（10-20 个）→ **登录墙**：请用户扫码，登录后重抓（抖音未登录 16 元素→登录后 286）；
3. **实测 1 卡片**：click → 截图 → vision 确认内容清晰、非空白；
4. **结论写回**：本表加一行 + 平台细节（坑位/提取正则/登录依赖）写进 `chinese-social-platforms.md`（UGC）或 `professional-platforms.md`（专业站）。

## 提取模式速判

- **Hyperlink 模式**（小红书/B站/gooood/有方）：`scripts/extract_xhs_notes.py` 改正则即可复用（匹配 value 含平台特征串：`search_result/`、`/video/BV`、`.htm`、`/items/`）
- **Group 模式**（抖音）：直接 click Group token，靠地址栏 `modal_id=`/标签标题变化确认导航成功
- **curl 模式**（Bing/官网/媒体）：直链下载 + 魔数/大小卫生检查
