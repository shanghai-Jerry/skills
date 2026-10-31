---
name: release-publish
description: 整编排型 skill：星愿池/AnyApp 一个版本「发布推广物料全流程」四步走——①更新总览文案（app-promo-texts）→ ②市场介绍图 + 小红书图（zh-intro-images + xhs-promo-images）→ ③16:9 版本更新图（update-banner-images）→ ④官网同步（sync-ghpages-site）。适用于「发布这个版本」「版本发布流程」「发版推广物料」「新版本上推广/上官网」「release 一下」等任务；单步深度操作仍优先用对应专项 skill。
---

# 版本发布推广流程（四步全编排）

一个 App 版本发版时，推广物料的完整生产链路：**文案 → 市场介绍图/小红书图 → 版本更新图 → 官网同步**。本 skill 是**编排层**：定义顺序、口径对齐点与产物清单；每一步的具体执行读并遵循对应专项 skill，不重复其细节。

流程在 v1.6.1（2026-10-31）完整跑通验证过一轮。

## 前置检查（四步开始前）

- 版本号已升级：`starcollection/AppScope/app.json5` 的 `versionName/versionCode`，`constants.ets` 的 `APP_VERSION` 同步
- `starcollection/CHANGELOG.md` 顶部已有本版本段（文案与更新图的取材源）
- 真机新功能截图已在 `starcollection/resources/design/demo/`
- 版本语义已定稿（不要为「先发物料」提前透露未拍板的行为）

**口径总原则：一步取材、步步对齐。** 全流程共用一个取材源——本版本 CHANGELOG 的功能条目 + demo 真机截图的真实界面元素。文案里的数字/天数/界面原文、介绍图上的标语、更新图里的条目清单，三者必须是同一组表述；任何一步想改措辞，回到 CHANGELOG 口径一致改三处。

## 全流程产物清单（发布物盘点用）

| 步骤 | 产物 | 路径（starcollection/resources/design/ 下） |
|---|---|---|
| ① 推广文案 | 版本更新总览篇小红书文案 | `recommend_texts/xhs_v<版本去点>_update.md`（如 v1.6.1 → `xhs_v161_update.md`） |
| ②a 市场介绍图 | 本版本新页面介绍长图（1080×1920） | `zh/intro_<页名>.jpg` |
| ②b 小红书图 | 上图逐张 3:4 顶裁（1080×1440） | `xhs/<同名>.jpg` |
| ③ 版本更新图 | 16:9 更新总览图，双格式 | `updated/intro_v<版本去点>_update.jpg` + `.webp` |
| ④ 官网 | 开发仓物料 + 官网 gh-pages 功能营地/版本区（中英双语） | 跨仓库（见 sync-ghpages-site） |

## 第一步 · 版本更新总览文案（app-promo-texts）

**任务**：为本版本写一篇「版本更新总览篇」文案（区别于单功能种草篇），落盘 `recommend_texts/xhs_v<ver>_update.md`。

- 骨架与合规照 **`app-promo-texts`** skill 的通用方法论执行；星愿池的 CTA 生成规则、tag、合规红线加读 **`xhs-starcollection-texts`** 的专属口径
- 总览篇款式参考已验证先例：`recommend_texts/xhs_v160_update.md` / `xhs_v161_update.md`——痛点钩子 + emoji 功能清单（本版本 5~7 个要点逐条）+ 信任块 + 金句收尾
- **功能清单条目与 CHANGELOG 本版本条目一一对应，不漏大功能、不编造**；截图引用的真机元素（数字/文案/日期）以 demo 截图实际内容为准
- 与后续 ③ 的更新图共版式素材：这一步整理出的「条目名（2~4 字）+ 一句话说明（≤18 字）」清单会被 ③ 直接复用，写时就按这个粒度整理

## 第二步 · 市场介绍图 + 小红书图（zh-intro-images → xhs-promo-images）

**任务**：把 demo 真机截图转成应用市场介绍长图，再转小红书 3:4。两条链在同一个 cv 任务里顺序执行，前一阶段的输出即为后一阶段素材。

1. **zh-intro-images**：每张新页面/demo 截图在 `gen_intro_images_zh.py` 的 `configs` 追加配置（title/subtitle/desc/accent 取页面主色），**单配置运行**（勿全量跑），目检 + 验证 1080×1920；产出 `zh/intro_*.jpg`
2. **xhs-promo-images**：把本版本 zh/ 新图（及本次要发的存量图）批转 3:4 顶裁到 `xhs/`（同文件名，JPEG q90），**逐张验证** 比例 0.75 / ≥750×1000 / ≤3MB，任何一张不达标重跑
3. desc/特性胶囊文案与第一步文案的功能清单用词对齐（同一功能同一说法）

## 第三步 · 版本更新图（update-banner-images）

**任务**：生成应用市场 16:9 版本更新图，产出 `updated/intro_v<ver>_update.jpg` + `.webp`（JPG ≤5MB / WEBP ≤200KB 双达标）。

- 按 **`update-banner-images`** skill 执行：只改 `gen_update_image.py` 顶部 `CONTENT` 配置（version/title/bigline/features/images/output），版本号格式 `intro_v<版本去点>_update`
- 取材即第一步整理的「条目名 + 一句话说明」5~7 条（与 `xhs_v<ver>_update.md` 口径一致），images 取第二步生成的本版本 zh 图（通常 3 张）
- 前置依赖：zh 图未生成先回去跑第二步；目检 + 脚本自动打印的双格式体积验证不可跳过

## 第四步 · 官网同步（sync-ghpages-site）

**任务**：把开发仓本版物料同步到公开官网仓（stars-collection-opensource，线上 www.bigchange.top）。

- 按 **`sync-ghpages-site`** skill 全流程执行：源仓盘点/先提交推送 → 目标仓 main 先行（拷图 + 版本文案 md，`docs:` 提交）→ gh-pages 功能营地 + 版本区（中英双语，`deploy:` 提交）→ 结构校验 → push → 验证部署
- 带走清单即前面三步的全部产物：`xhs/intro_*.jpg` 介绍图、`recommend_texts/xhs_v<ver>_update.md` 版本文案、（视需求）更新图
- 功能营地 `<article class="feature">` 的 lead/`<ul>` 文案从版本文案正文提炼；营地总数 N 与「N 个营地」文案计数保持一致；「最新」徽章只留在新版本

## 收尾

- 源仓提交推送全部物料（`zh/`、`xhs/`、`updated/`、`recommend_texts/`）
- 线上验证：官网营地/版本区/图片可访问、文案链接不 404（md 链接指向目标仓 main）
-小红书发布顺序建议：单功能种草篇逐篇发 → 版本更新图 + 总览篇收尾（更新图 also 可直接传应用市场更新说明）

## 编排要点（踩过的坑）

- **顺序不能颠倒**：④ 的素材（营地文案）来自 ① 的版本文案、④ 的图片来自 ②；③ 依赖 ② 的 zh 图。消阶段依赖只有一条合法捷径：文案草稿可与 ② 并行写，但定稿前必须用真实截图元素回填
- **跨 skill 的「版本去点」格式统一**：v1.6.1 → 文件名一律 `161`（`xhs_v161_update.md` / `intro_v161_update.jpg`），不要出现 `v1_6_1`
- **单配置运行纪律**：zh/update 两个生成脚本都遵守各自 skill 的「只跑当前配置」约定，历史 config 引用的 demo 截图可能已清理，全量跑会 FileNotFoundError
- 每步产物在 CHANGELOG 本版本段的「优化改进/其他变更」如实记录一条（物料生产也留痕），并同步 `APP_VERSION_INTRO.md`
