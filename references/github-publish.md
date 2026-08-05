# 发布 / 更新本 skill 到 GitHub（大陆网络全路径，2026-08 实测）

用户偏好把沉淀的 skill 开源分享到 GitHub。本机（C:\Users\ASUS，大陆网络）完整路径：

## 0. 前置事实
- GitHub 账号：`danzey0425-lgtm`；仓库：`web-image-sourcing`（public）
- gh CLI 已装在 `C:\Users\ASUS\bin\gh.exe`（无需重装）
- **GitHub 直连被墙**（443 超时、镜像 gh-proxy/mirror.ghproxy/ghfast.top 全挂）——所有 gh/curl 操作必须走代理

## 1. 代理检查（每次先做）
用户有代理软件（日本节点，端口 `127.0.0.1:15490`），但**需手动开启**（系统 ProxyEnable 默认 0）。
```bash
# 探测代理是否可用（端口列表含 15490 及其他常见代理端口）
for port in 15490 7890 7891 7897 1080 10809 8889; do
  curl -sI --max-time 4 -x http://127.0.0.1:$port https://api.github.com 2>&1 | grep -q HTTP && echo "✅ 端口 $port 可用"
done
```
若全不通：请用户开启代理软件，再探一次（等 20-30s）。

## 2. gh 操作统一带代理
```bash
export HTTPS_PROXY=http://127.0.0.1:15490 HTTP_PROXY=http://127.0.0.1:15490
export PATH="/c/Users/ASUS/bin:$PATH"
```

## 3. 未安装 gh 时的安装路径（勿重蹈）
1. **先查最新版本号**（猜版本号会 404「Not Found」——2.63.2 不存在，实际 2.97.0）：
   `curl -s -x $PROXY https://api.github.com/repos/cli/cli/releases/latest | grep browser_download_url`
2. 代理下载 zip → python zipfile 解压 → `cp gh_extract/bin/gh.exe ~/bin/`
3. winget 不可用（源更新失败 0x80072eff）、GitHub 直连/镜像均不可用——只有代理路径可行

## 4. 授权（gh auth login --web 三坑）
- ⚠️ **必须 background 运行**：前台跑 90s 超时被杀，授权码作废
- ⚠️ **不能接 `| head -N` 管道**：管道缓冲会吞掉授权码输出（进程"在跑"但看不到码）
- 后台跑后 poll 拿一次性码（如 `C608-D645`），把码 + `https://github.com/login/device` 给用户浏览器授权
- 完成后 `gh auth status` 验证（Token scopes 需含 repo）

## 5. 建仓推送（首次）
```bash
cd <skill-upload-dir> && git init -b main && git add -A
git -c user.name="danzey0425-lgtm" -c user.email="danzey0425-lgtm@users.noreply.github.com" commit -m "..."
gh repo create web-image-sourcing --public --source=. --push --description "..."
```

## 6. 日常更新（用户说"更新 GitHub 的 skill"时）
```bash
export HTTPS_PROXY=http://127.0.0.1:15490 && export PATH="/c/Users/ASUS/bin:$PATH"
cd "C:/Users/ASUS/Documents/Codex/2026-08-04/bang/web-image-sourcing-upload"
# 从 skills 目录同步最新内容（SKILL.md references scripts）
cp -r "$HERMES_PROFILE/skills/research/web-image-sourcing/." . && git add -A && git commit -m "update" && git push
```

## 7. 仓库结构（与 skill 目录同构）
SKILL.md + README.md（项目介绍/安装/核心结论）+ LICENSE（MIT）+ references/（5 个）+ scripts/（6 个）
