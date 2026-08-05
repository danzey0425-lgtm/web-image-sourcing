# 图片搜索端点实测矩阵（2026-08，中国大陆网络环境）

| 端点 | 状态 | 备注 |
|---|---|---|
| `cn.bing.com/images/async?q=..&first=0&count=30&relp=30` | ✅ 可用 | curl 抓取，UTF-8；正则 `murl&quot;:&quot;(.*?)&quot;` 提 30 条直链；需 UA |
| `cn.bing.com/images/search`（browser 导航） | ⚠️ 失败 | 报 `'utf-8' codec can't decode byte 0xb2`；curl 可抓但中文词污染严重 |
| `image.so.com/j?q=..&src=srp`（360） | ⚠️ 限流 | 返回 JSON：`list[].img`(原图)/`thumb`(CDN 缓存)/`width`/`height`/`title`；每查询仅 2-4 条，多词 0 结果 |
| `image.baidu.com/search/acjson` | ❌ | 返回 `{"antiFlag": ...}` 反爬 |
| `pic.sogou.com/napi/pc/searchList` | ❌ | 返回 `{"status":1,"info":"forbid"}` |
| DuckDuckGo（vqd + i.js） | ❌ | 拿不到 vqd（拦截/验证页） |
| `www.xiaohongshu.com/search_result` | ❌ | 未登录 404（"你访问的页面不见了"）；需扫码登录态 |
| Wikimedia Commons API | ❌ | 空响应（网络屏蔽） |
| gooood.cn 站内搜索 | ❌ | 对元素词返回默认招聘页 |
| 官网 / 文章 CDN 直采 | ✅✅ 首选 | 松赞 `image.songtsam.com`、搜狐 `*.cdn.sohucs.com`、澎湃 `image.thepaper.cn`、艾景奖 `idea-king.org.cn`、gooood 图片 `oss.gooood.cn`、dwarikas.com 均可 curl 直下 |

## 中文词污染案例（Bing 图片，同批真实返回）

- "玛尼堆 雕塑 景观" → 丝袜广告图
- "六字真言 石刻" → 汉字"六"教学图
- "mani stones closeup tibet"（英文）→ 电源设备产品图
- "water prayer wheel tibet" → 棕熊 / 阿拉斯加 / 水滴摄影
- "藏式铺装 地面" → "藏"字书法 / 字体素材
- 对策：换元素词精确搜 + 权威源兜底 + 蒙太奇视觉筛选（垃圾图几乎必然混入，必须过筛）

## 下载卫生细则

- 必须带 UA；多数 CDN 需 Referer（来源页或 `https://cn.bing.com/`）
- 魔数校验：JPEG `\xff\xd8\xff`、PNG `\x89PNG\r\n\x1a\n`；<4KB 直接丢弃
- 域名黑名单：eaton / chem17 / zidian / bishun / pngsucai / redocn / nipic / zcool / 1688 / taobao / shipin520 等（电商、字典、素材图标站）
- 原图直链失败 → 回退 thumb 缩略图直链（360 qhimgs1、huaban gd-hbimg）

## 权威源直采技巧

- 文章原文页 = 图矿：正则 `https?://[^"' ]+?\.(?:jpe?g|png|webp)[^"' ]*` 提取全部图片 URL，一篇长文常有 20-30 张且主题高度相关（案例：搜狐瑞吉专文 28 张 → 入口标识、木格栅墙、酥油灯供品等稀缺元素图全在其中）
- 官网 news/酒店页：抓列表页 → 子页 → 图片 CDN 直链；子代理报告的"图片已验证"仍要抽查（自报不可全信）
- 页面编码：新浪旧文 GBK、部分页面 utf-8 带 BOM——按 utf-8 → gb18030 → gbk 依次尝试解码
