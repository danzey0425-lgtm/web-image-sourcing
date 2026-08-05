# HTML Casebook 素材整合管线（采集 → 交付物）

适用：把批量采集的截图（小红书/官网/媒体图，单张 1-2MB PNG）整合进 HTML 图鉴/PPT/案例报告。
2026-08 实测：108 张 141MB → 6MB，浏览器秒开。

## 步骤

1. **批量压缩（必须先做）**：1-2MB 截图 × 100+ 张直接嵌入 HTML 会让文件上百 MB、浏览器卡死。
   `scripts/compress_for_casebook.py`：PIL LANCZOS 缩到 720px 宽 + JPEG q82 → 每张 50-70KB，约 15:1。
   输出到 `deck_assets/xhs_web/`（或同类资产子目录），文件名保留原语义（`{组}_{词}_noteN.jpg`）。
2. **整合进 HTML（保留设计 tokens）**：重写/扩展已有 casebook 时**不要动 CSS 变量与设计语言**——
   保留 `:root` tokens（品牌色、线框、字体栈）与 reveal 动画，只新增布局类。
   本类元素页通用布局：右侧图片区改 2 列 grid，主图跨 2 列 + 4 张小图 = 每页 5 图，密度翻倍且不溢出 1080 舞台。
   新增"实拍"角标（红底 xhs-tag）区分实拍与官方图；结尾附 2-3 页**素材墙附录**（10 列 tile 网格，
   每 tile 编号 + 文件名 caption）把剩余素材全量收录——正文精选 + 附录全量，无图遗漏。
   **排版可读性最小尺寸（用户 QC 红线，第三次纠正"文字还是太小"后最终定稿 2026-08）**：
   - 1920×1080 舞台下：正文 ≥20px（line-height 1.6）、要点标题 ≥28px、图注 caption ≥16px、
     页眉 sym ≥29px、页面大标题 h2 ≥70px、case-flag ≥16px——**16.5px/23px/14px 那版仍被用户判太小**，
     宁可大不可小，13.5px/11.5px 更是直接翻车；
   - 图片高度：元素页主图 ≥335px（350px 会挤爆底部 9px）、小图 ≥205px；
   - 素材墙 tile 图 ≥150px 高、tile 标签字 ≥11.5px（10 列 5 行是 44 张的极限排布，图片再大就放不下）；
   - 小图是 1.88:1 笔记页截图，裁成宽条会丢主图——`object-fit:cover` + `object-position:center`，
     布局比例越接近原图越好（素材墙用 10 列而非 6/8 列，图更高、裁切更少）。
   - 放大后空间核算：headH + bodyTop + bodyH（全用 offsetHeight 实测）应 ≤ 1080 - paddingBottom，
     留 ≥100px 余量；正文 20px 时 4 个要点 + 5 图（335+2×205+2×14 gap=773）正好放下。
3. **静态校验（execute_code 一步到位）**：
   - 正则提取全部 `src="..."`，逐一 `os.path.exists` 核对（173 引用 0 缺失）；
   - slide 总数 == 页码总数、页码顺序连续（`(\d+) / (\d+)` 正则核对）；
   - 元素页图片数一致（每页 == 5）、素材墙 tile 数求和 == 素材总数（44+40+24=108）；
   - ⚠️ 朴素标签配对脚本会把 `<img>` 报成"开173闭0"——img 是 void element 本无闭合标签，属误报，
     不要为它加 `</img>`，也别据此判失败。
4. **真实渲染验证（最重要一步）**：`browser_navigate("file:///.../xxx.html")` 后
   `browser_console` 执行：
   `JSON.stringify({slides: document.querySelectorAll('.slide').length, imgs: document.querySelectorAll('img').length, broken: [...document.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')).slice(0,10), active: document.querySelector('.slide.active').className})`
   broken 为空数组 + 无 console/js_errors = 通过。
   **溢出检查（改大尺寸后必做）**：素材墙/图片放大后目测不可靠，用 JS 量每个 grid 的底边是否超出
   1080 舞台：`[...document.querySelectorAll('.wall')].map(w=>{var g=w.querySelector('.grid'),r=g.getBoundingClientRect(),s=w.getBoundingClientRect();return {tiles:g.querySelectorAll('.tile').length, rows:Math.ceil(g.querySelectorAll('.tile').length/10), overflowPx:Math.round(r.bottom-s.top-1080)}})`，
   overflowPx ≤ 0 即无溢出；6 列 tile 网格放 44 张会溢出（8 行 > 舞台高），10 列 5 行才放得下。
   **⚠️ stage scale transform 测量陷阱（真实事故）**：`fit()` 会给 stage 加 `transform: scale(s)`（s<1 缩窗），
   `getBoundingClientRect()` 返回的是**缩放后的视口坐标**——把 178.9px 高的 tile 量成 103px、行距量成 110px，
   会误判"图被裁切/行重叠"。判据必须用**未缩放值**：`offsetHeight`（tile/img 元素）或
   `getComputedStyle(...).height/gridTemplateRows`；`getBoundingClientRect` 数值只能与窗口高度比、不能与 1080 比。
   本次事故链：缩放坐标 → 疑重叠 → 截图+vision 说"正常" → 查 computedStyle 才确认 img 150px/tile 178.9px 完全正常，
   白耗 3 轮排查。经验：**布局尺寸一律 offsetHeight/computedStyle，getBoundingClientRect 只用于视觉定位**。
5. **交付清单**：`交付清单.md` 逐组列亮点 + 标注需剔除图（广告/店名霸榜跑题图）与真实性存疑图。

## 图片-说明一致性审核（发布前必做，用户 QC 红线）

**教训（2026-08 实测被用户当场抓到）**：旧素材/旧 caption **绝不可信**。上一会话遗留的 deck_assets
里 6 张图 caption 与内容不符，用户一眼看出草阶页主图是「摄图网」水印市政大楼梯，跟草阶毫无关系。
触发全量审核后陆续实锤：
- `s10_laigu`：**白天客房室内**（雪山湖景落地窗）被标成"夜景·暖色光盒"；
- `s12_pianshi`：**藏传佛教室内佛堂**（佛像+供桌+软包墙）被标成"干砌片石墙·乱石工艺+佛龛"；
- `s6_yading`：实为松赞梅里冬季建筑群，被标成"亚丁村"；
- `s5_ditan`：现代酒店走廊地毯（非藏式）被放进藏式铺装页；
- `s8_lvgu`：藏式建筑庭院，无草阶内容却放在草阶页；
- 另有三张旧小红书截图与新采集实拍主题重复、树池页复用了煨桑炉图。

**流程（写入交付前检查单）**：
1. **批量拼图核查（首选，比逐张快 4-6 倍）**：PIL 把 4-6 张候选图拼成 2×2/2×3 网格（每格 560-600px 宽，
   左上角标注 `IMG N: 文件名`），一次 vision 调用读**图内标题文字**逐一判断每张是否匹配预期主题，
   问句写成"逐一判断 IMG1..N 是否为 X 主题？回答：是/否+实际标题"。7 批可查完 40+ 张。
   关键存疑图（判定为否、或标题读不清）再单张复核。
2. **逐张 vision 复核 caption 与画面是否一致**——先复核每页 main 主图，再抽 all 存疑小图；
   问法固定："这张图的内容是什么？是否与 [主题] 相关？有没有水印？"；
3. **水印三档判定**：商业图库水印（摄图网/图虫/视觉中国）→ 必须替换；来源署名水印
   （建构物语/澎湃等公众号水印）→ 可保留但 caption 必须写明出处；无可见水印 → 正常；
4. **替换优先用本会话已采集并验证的实拍图**（xhs_web 高清图），保证主题精准 + 无水印；
5. **问题图黑名单残留检查**：把已下架文件名写进黑名单，全文 grep 确认零残留；
6. 修完重跑静态校验 + 真实渲染验证（见上）。

**自己采集的素材同样要核（第二次用户纠错的核心教训）**：笔记窗口标题/搜索词 ≠ 笔记实际内容。
2026-08 实测：`04_经幡藏式_note2/3/4` 窗口标题看似正常（搜索词是"经幡 藏式"），点开后实际是
"All is impermanent / World's impermanent" 藏传佛教骷髅护法**插画/哲思笔记**（标签蹭了 #经幡 #风马旗），
凭标题写 caption 放进经幡页直接翻车，用户当场抓到"对不上"。对策：
- 采集时窗口标题含英文哲思句、无主题关键词（impermanent/option/better 等）→ 当场标记可疑；
- 整合前对每张 xhs 图读图内标题核实（拼图批量核查即可覆盖）；
- 素材墙全量收录跑题图时，tile caption 如实标注（如"04 经幡·藏式插画(非常规)"），不沿用组名。
- 反面案例清单：湖水风光被标"林间玛尼堆"、建筑概念图被标"玛尼堆与经幡"、门廊被标"凹龛煨桑炉"、
  中英双语标牌被标"藏汉双语"——旧图 caption 全是猜的，必须逐张核。

### 要点文字核查（第三层审核：图片之外的文字，用户"你自己核查一遍内容"触发）

图片 caption 核完后，还要全量通读**要素点（.point）、页眉 sym、出处 case-flag、封面/索引/结尾统计**——
2026-08 实测一轮查出 11 处问题，五类规律：

1. **换图后要点孤儿**：某页换下问题图后，同一页的 要点/sym/出处 可能还在讲已下架的图
   （如要点④"青铜雕塑"图被换走、要点②"凹龛煨桑炉"对应图实为门廊、要点③"瑞吉范本·藏文译名"
   图已删且描述本身不实——中英双语被写成藏汉双语）。**换图必查同页文字**，要么把图放回
   （已核实内容正确的旧图可复用，如 s1_qingtong 青铜雕塑回归），要么改文字对应新图。
2. **无法核实的具体名词 → 删或软化**：经搜索/常识无法确证的术语直接去掉，不硬留
   （"贝玛白带"——贝玛=padma 莲花≠白，与主题无关；"片石鱼背墙（敏珠林寺）"无处可考）。
   地名/机构名补规范全称（"安缦廷布"→"安缦不丹·廷布（Amankora Thimphu）"）。
3. **统计数字与实情一致**：封面/索引/结尾的量化表述要对着实际内容核
   （索引写"每页新增实拍 2 张"实际 3-4 张 → 改"每页配实拍参考"）。
4. **素材墙 tcap 对跑题废图如实标注**：店名霸榜废图（墨西哥餐厅）tcap 标"餐厅探店(非景观)"，
   不沿用含糊的组名。
5. **方法**：execute_code 正则提取全部 `.point` 标题+正文、sym、case-flag、cap 一次性通读；
   对 caption 具体但未单独核实的图再补 1 批 montage（读图内标题）；修完跑结构校验 + 渲染验证。
   设计理念类文字（五色体系、转经动线）按专业常识核对即可；具体项目细节（松赞马灯、亚丁广场五色铺装）
   注明来源为公开报道，落地前建议用户对原项目资料再确认。

## 原帖链接标注（交付物溯源，用户常要求）

用户要求"把相关的 xhs 网址标注"时，**无需重新采集**——采集期的 cua-driver 快照缓存里能反查每张截图对应的笔记 URL：

1. **重建映射**：遍历 `~/AppData/Local/hermes/profiles/<profile>/cache/terminal/hermes-results/call_*.txt`
   （get_window_state 落盘 JSON），element 的 `value` 字段含 `search_result/<note_id>?xsec_token=...`；
   按 `window_id` 分组（=每个关键词窗口），取 URL 最多的快照 = 搜索页；窗口标题（tree_markdown 首行
   `- Window "关键词 - 小红书搜索"`）匹配关键词 → 截图前缀；第 N 个 URL = 该词 `note{N}`。108 张 27 词一次全重建。
2. **⚠️ xsec_token 已过期（实测）**：采集数小时/数天后，带 token 的 explore URL 打开即 404
   「你访问的页面不见了」。标注时**去掉 token，只留永久笔记 ID 直链** `https://www.xiaohongshu.com/explore/<note_id>`
   （ID 永久有效，token 反正会过期）；结尾页注明"🔗 为原笔记直链，token 过期时可按标题站内搜索"。
3. **注入方式**：元素页 caption 尾部加 `<a href="URL" target="_blank" title="小红书原笔记">🔗原帖</a>`；
   素材墙 tile 的 tcap 里加 `<a class="xlink" ...>🔗</a>`；CSS 用黄色/蓝色高亮 + hover 下划线。
   映射表落盘 `shot_urls.json`（截图文件名 → URL）供复用。

## PDF 导出（HTML → 每页一页 PDF，三坑连环，2026-08 实测）

用户要 PDF/PPTX 时给 PDF（体积最小：108 图 19 页 ≈ 10MB，PPTX 会 20-30MB+）。**Edge headless `--print-to-pdf` 直出全空白（5.5KB 1 页）不可用；必须 Playwright page.pdf()**。

1. **生成打印副本**：inline style 直接写死布局（不依赖 `@media print` 是否能生效）：
   - stage: `style="position:static;height:auto;overflow:visible;transform:none!important"`
   - 每个 `<section class="slide ...">`：`style="position:relative;visibility:visible;opacity:1;width:1920px;height:1080px;overflow:hidden;page-break-after:always;break-after:page"`（最后一张去掉分页）
   - ⚠️ **注入时必须保留原 class**：只把 style 插到标签结束 `>` 前。曾用 `tag.replace('<section class="slide', '<section class="slide" style=...')` 把 class 破坏成只剩 "slide"（`.cover/.el/.wall` 全丢）→ 全部 grid 布局崩溃、素材墙 108 图只剩 3 张、元素页 5 图只剩 2 张——整本 PDF 内容缺失。修复后 get_image_info 每页 44/40/24 图齐。
2. **Playwright 渲染**（node，项目已有 playwright 依赖时）：
   ```js
   page.pdf({ width:'1920px', height:'1080px', printBackground:true,
              margin:{top:0,bottom:0,left:0,right:0}, preferCSSPageSize:false })
   ```
   打印前 `waitUntil:'networkidle'` + `Promise.all([...document.images].map(...img.complete))` 等全部图片解码；先 `evaluate` 数 `broken images` 与素材墙 tile 数再打。
3. **封面空白坑**：封面（首个 .active 页）在打印布局里内容被推到视口上方（文档被 19×1080 撑开时 absolute 定位干扰），PDF 第 1 页纯米白。修复：屏幕模式单独截图封面（原始 HTML + viewport 1920×1080 时 fit() scale=1 即原尺寸），PyMuPDF 合成：`new_page(1440,810)` 插封面图 + `insert_pdf(src, from_page=1)` 追加其余页。
4. **体积**：`out.save(tmp, garbage=4, deflate=True)` 压缩；封面转 JPEG q88 再插入（PNG 无损会让 PDF 到 34MB）；最终 19 页 ≈ 10MB。
5. **验证**：`pypdf` 数页数（==slide 数）；`fitz page.get_image_info()` 数每页图片（素材墙页 44/40/24）；逐页像素抽样非背景占比（<3% 判空白，注意封面 12%、索引 15% 属正常文字页）；**勿信视觉模型看渲染 PNG**（密集小图上会幻觉出不存在的内容——曾把素材墙页描述成"三个浏览器窗口拼接"），以 fitz/pypdf 客观数据为准。

## 坑位

- **`npm run test` 常是占位脚本**（`echo "Error: no test specified" && exit 1`）——项目无测试时这是预期失败，
  用它当验证会误判；对 HTML/图片类改动做上述结构校验 + 真实渲染验证即可。
  **升级做法（2026-08 落地）**：与其每次解释占位失败，不如把占位脚本替换为真实校验器并挂接
  `package.json`：写 `verify_casebook.js`（node：栈式标签配对 + img src 存在性 + 页码/slide 一致性 +
  元素页每页 5 图 + 素材墙 108 tile），`"scripts": {"test": "node verify_casebook.js"}`——
  `npm run test` 从此成为真实回归门（exit=0 通过）。若项目是 Python 型则挂 `verify_casebook.py` 同理。
- 压缩后保持 720px 宽足够 PPT 卡片展示（1920 舞台下小图 ~300px 宽）；素材墙 tile 用原 720px 图即可，
  不必再压一套缩略图（6MB 总量可接受）。
- 若 HTML 由之前会话产出，先 read_file 全量读一遍再覆盖写（write_file 会警告 last-read 是分页视图）。
- **视觉模型数网格格子不可靠**（把 10 列数成 8 列、漏数行）：tile 列数/行数以 JS 测量为准，截图+vision 只做
  "图是否清晰、有无裁切"的定性确认。
- **正则批量注入/修改 HTML 时，回调参数 group 顺序错乱会整页损坏（真实事故）**：Python `re.sub` 回调里
  把 `m.group(1)` 与 `m.group(2)` 互换，导致 26 处 `<img>` 结构错乱（`src` 变 `alt` 值）+ 素材墙 108 处
  tno/tcap 互换，文件当场写坏。防法：① 正则 group 编号与回调取值一一对照后再写替换模板；
  ② 注入后立即用 `html.parser` 全量验证（未闭合/错配即报），并 grep 损坏特征串（如 `<img src=" alt=`、
  tno 非纯数字）；③ 修复用反向正则精确重建原结构（损坏串 → 原串映射），修完再验证。
- 临时核查拼图（_chk*.png）与一次性脚本用后即删（rm），只留可复用资产（压缩脚本、URL 映射 json、校验脚本）。
