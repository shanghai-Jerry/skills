---
name: sync-ghpages-site
description: 把一个仓库（stars-collection，项目开发仓）的已提交变动同步到另一个仓库（stars-collection-opensource，公开官网仓）：介绍图/版本文案先进目标仓库 main，再到 gh-pages 增改功能营地与版本区（中英双语），结构校验后提交推送，验证部署。适用于「同步官网」「更新 gh-pages 网站」「新版本上官网」「把开发仓的新功能挂到官网」「官网内容同步」「跨仓库同步推广物料」等任务。
---

# 官网同步（stars-collection → stars-collection-opensource）

推广官网是**跨仓库**同步：物料产出于开发仓，站点维护在公开仓，两端是两个独立 clone，不能混用同一套 git 命令。中英文内容**必须同步改**。本流程 2026-10-30 完整验证过一轮（v1.6.0/v1.6.1，八个营地 → 十二个营地）。

## 仓库角色（改动前先认清在哪一边）

| 角色 | 仓库 | 承担的内容 |
|---|---|---|
| **源仓库** | `stars-collection`（项目开发仓，本 skill 通常在这个仓里被触发） | 介绍图（`starcollection/resources/design/xhs/intro_*.jpg`）、版本文案（`starcollection/resources/design/recommend_texts/xhs_v*_update.md`、`v*_update.md`） |
| **目标仓库** | `stars-collection-opensource`（公开官网仓） | 官网站点（`gh-pages` 分支：`index.html`、`en/index.html`、`images/`）+ 版本文案 md 与介绍图素材（`main` 分支，版本区链接指向这里） |

### 目标仓库本地路径发现规则（按顺序找，不写死）

1. **同级目录**：源仓库 cwd 的同级（`../stars-collection-opensource/`），存在 `index.html` 分支 `gh-pages` 即命中——这台机器上就是这么 clone 的；
2. **工作区配置**：在源仓库的 `MEMORY.md` / `AGENTS.md`「Tool Setup」节搜 `stars-collection-opensource`，machine-specific 本地路径记在这里，不记在 skill 里；
3. **远程兜底**：以上都没有时，`git remote -v` 判断远端是 `shanghai-Jerry/stars-collection-opensource` 即为正确仓库，clone 到源仓库同级目录再继续；
4. **找不到就问用户**，确认后把结论写回「Tool Setup」节，下次不再问。

**跨仓库取素材不用 `git show`**：两个 clone 都在本地，介绍图/文案直接 `cp <源仓库路径>/... <目标仓库路径>/...`；`git show` 只用于目标仓库自己的 main ↔ gh-pages 两分支之间（见下）。

## 目标仓库事实（gh-pages 相关硬约束）

| 事实 | 值 |
|---|---|
| 线上地址 | www.bigchange.top（CNAME，push gh-pages 后 GitHub Pages 自动部署，1–2 分钟生效） |
| 分支关系 | 目标仓库内 **gh-pages 与 main 历史独立（orphan 分支，无共同祖先）**——不能 merge/rebase，不能直接 checkout main 的已跟踪文件 |
| 目标仓库内取 main 文件 | 在 gh-pages 工作区执行 `git show main:<path> > <path>` |
| 页面 | 中文 `index.html`、英文 `en/index.html`、共用 `images/`（en 页引用路径是 `../images/`） |
| 提交规范 | 目标 main 提交前缀 `docs:`，gh-pages 提交前缀 `deploy:` |

页面上 **「星路上的 N 个营地」**（英文 "N camps along the trail"）的 N 要跟 `<article class="feature">` 实际数量一致。

## 内容映射表

| 源仓库的改动 | 目标仓库动作 |
|---|---|
| 新增 `resources/design/xhs/intro_*.jpg` 介绍图 | ① 拷入目标 main `images/`（docs 提交）② 建功能营地 `<article class="feature">`（中英各一），或替换既有营地配图 |
| 新增/更新 `xhs_v*_update.md`、`v*_update.md` 版本文案 | ① 拷入目标 main 仓库根（docs 提交，版本区链接才能指向 `blob/main/<md>`）② 版本区新增 `<div class="ver">` 块，并把「最新/Latest」徽章 `<em>最新</em>` 从旧版本摘下（只能有一个） |
| 版本文案正文 | 营地 lead/`<ul>` 文案的素材库：痛点 → 每个功能一条 `<li>`（短句、用词贴合原文案） |
| 站点级事实（域名、下载链接、隐私口径） | 中英两页逐处同步改 |

## 同步步骤

### 阶段一 · 源仓库盘点

1. **盘点开发仓改动**：`git log --oneline -n 10` + `git status`（未跟踪文件也常是本次要同步的内容）。源仓库有未提交的物料**先在源仓库提交推送**，保证素材可追溯，再开始跨仓同步。
2. 列出本次要带走的清单：新介绍图 x 张、版本文案 y 篇、版本号 vN.N.N。

### 阶段二 · 目标仓库 main（素材与文案先行）

3. **切到目标仓库 main**（需工作区干净）：`git checkout main`。动作永远是「先 main 后 gh-pages」——版本区「完整更新说明」链接指向目标 main 的 md，md 落地并推送前先改 gh-pages 会让链接 404。
4. **拷入物料**：`cp` 源仓库的新介绍图到目标 `images/`、新版本文案 md 到目标仓库根。图片先目检一眼，确认内容再写文案。
5. **提交推送**：`docs: 摘要（ vX.Y.Z 介绍图/版本文案）` → `git push origin main`。

### 阶段三 · 目标仓库 gh-pages（站点更新）

6. **切到 gh-pages**（需工作区干净）：`git checkout gh-pages`。素材已在目标 main，可用 `git show main:images/intro_x.jpg > images/intro_x.jpg` 自取（或阶段二拷入的文件在切分支前就用 `git stash`/直接重新 cp）。
7. **中文版 `index.html`**：
   - 新营地结构：`<article class="feature"><div class="feature-inner"><div class="feature-body">` + `h3>标题<small>短标语</small>` + `p.feature-lead` + 3–4 条 `<li>` + `.feature-media` 里的 `.phone>img`；
   - 新营地插在语义相邻的位置（如「子项清单」插在「目标管理」后，「星星时刻/宝贝回应」插在「星愿兑换」后，成对出现；「成长日记」插在「成长档案」后）；`feature:nth-child(even)` 左右轮换按 DOM 位置自动交替，**无需手动调样式**；
   - 版本区：新 ver 块插在最前，h3 用一句标题式概括（从文案金句取），链接指向目标仓库 `blob/main/<md>`。
8. **英文版 `en/index.html`**：同结构镜像翻译，注意三点——图片路径 `../images/`；标题计数同步（"Twelve camps along the trail"）；ver 链接文字是 "Full release notes (中文)"。
9. **两处 H2 计数**：营地数变化时更新「星路上的 N 个营地」和 "N camps along the trail"。
10. **校验**（必须中英两份都跑）：
   ```bash
   grep -c '<article class="feature"' index.html en/index.html   # 应=营地数
   grep -c 'class="ver reveal"' index.html en/index.html         # 应=展示版本数
   grep -o 'images/[a-z_]*\.jpg' index.html | sort -u             # 与 images/ 目录比对
   grep -o '\.\./images/[a-z_]*\.jpg' en/index.html | sort -u
   python3 -c "
   from html.parser import HTMLParser
   class P(HTMLParser):
       def __init__(self):
           super().__init__(); self.stack=[]; self.err=[]
       def handle_starttag(self,t,a):
           if t not in ('meta','link','img','br','input','hr','path'): self.stack.append(t)
       def handle_endtag(self,t):
           if self.stack and self.stack[-1]==t: self.stack.pop()
           elif t in self.stack:
               self.err.append('mismatch '+t)
               while self.stack and self.stack[-1]!=t: self.stack.pop()
               if self.stack: self.stack.pop()
   for f in ('index.html','en/index.html'):
       p=P(); p.feed(open(f).read())
       print(f,'unclosed:',p.stack,'errors:',p.err)
   "
   ```
11. **提交推送**：`deploy: 摘要（含改动范围与双语说明）` → `git push origin gh-pages` → 切回 main `git checkout main`。
12. **验证部署**：1–2 分钟后 `curl -sI https://www.bigchange.top/` 看 200，浏览器复查新段落。

## 已知坑

- **两个仓库是两个 clone**：能力完全不互通——不能在源仓库里 checkout 目标仓库的分支，也不能用 `git show main:` 取源仓库的文件（那是目标仓库内部的用法）。跨仓一律 `cp`，路径以「仓库角色」表为准。
- **同一仓库内 main ↔ gh-pages 也无法合并**：orphan 历史，任何时候都用手工作业或 `git show main:` 提取，别想着 `git merge`。
- **顺序红线：源仓库 → 目标 main → gh-pages**：跨三段乱序会 404 或丢素材；先 gh-pages 后 main 是最常犯的错。
- **「最新/Latest」徽章唯一性**：新版本入列时必须把旧版本的 `<em>` 摘掉，用户报过「页面最新版本标错」这类问题会很难看。
- **en 页图片路径**：demo 中曾差点写成 `images/`，en 页必须是 `../images/`。
- **营地配图只允许一张**：一个营地一个 `.phone>img`；同一版本出多张图时拆成多个营地，而不是往一个 article 里塞图。
- **校验脚本对空白行数敏感**：counts 以实际结构和 images/ 目录为准，别死记上次的数字。
- **push 后立刻看页面看到旧内容**：GitHub Pages 有 1–2 分钟部署延迟，别误判同步失败。

## 与 CI 的配合

目标仓库 main 已配置 `.github/workflows/site-sync-reminder.yml`：push 目标 main 时检测「目标 main 有而 gh-pages 没有的 intro 介绍图 / 未被官网版本区链接的更新文案」，自动开带 `site-sync` 标签的 issue 提醒（存在未关闭同名 issue 则不重复开）。**注意它只能监控目标仓库内部的一致性**——源仓库的新增物料不会触发它，所以阶段三是否完成要靠本 skill 流程推进；同步完成后可关闭 issue（CI 只提醒，不做编辑性内容）。
