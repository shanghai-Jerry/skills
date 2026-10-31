---
name: update-banner-images
description: 用 gen_update_image.py 把某版本的更新内容与 zh/ 介绍图统一排版成一张「版本更新图」——1920×1080（16:9）横版，左列文字更新清单 + 右列 zh 长图扇形样机的两列不同版式。适用于「生成版本更新图」「把 changelog 和 zh 图合成一张更新图」「1920x1080 16:9 更新图」「PNG/JPEG 5M 以内或 WEBP 200KB 以内」等任务。zh 图未生成前先跑 zh-intro-images skill。
---

# 版本更新图生成（1920×1080，两列版式）

把一个版本的更新要点 + 三张 zh/ 介绍长图合成**一张 16:9 横版更新图**：左列是「文字版式」（更新条目清单），右列是「图片版式」（zh 竖图扇形样机）——两列格式刻意不同，文字讲清改了什么，图片让人看到长什么样。源于 stars-collection 项目（2026-10-31 生成 v1.6.1 更新图，真机素材已验证）。

**产出硬指标**（应用市场/发布页要求）：分辨率 1920×1080（16:9）；PNG/JPG/JPEG 均 ≤5MB；WEBP ≤200KB。脚本同时输出 JPG（q90，约 230KB）与 WEBP（自动降质到 ≤200KB）双格式。

**脚本**：`starcollection/resources/design/gen_update_image.py`
**素材**：`resources/design/zh/intro_*.jpg`（1080×1920 竖版介绍图，由 zh-intro-images skill / gen_intro_images_zh.py 生成）
**输出**：`resources/design/updated/intro_v<版本>_update.jpg` + 同名 `.webp`

## 版式规格（改动前先读）

| 区域 | 规格 |
|---|---|
| 画布 | 1920×1080，底 NIGHT_SOFT `#101A3E`，顶部 420px 夜空青调渐变 + 固定种子星野（70 点，可复现） |
| 中缝 | x=948 分区线（白 30 alpha，overlay 合成，克制分隔两列） |
| 左列徽章 | y=80 玻璃胶囊（白 34 alpha 底 + teal 描边，overlay 层合成） |
| 左列标题 | y=150 字号 88 白色「<版本> 版本更新」；+104 字号 56 金色主功能句；+190 字号 30 次级副标 |
| 左列条目 | 「名 + 说明」两行式：teal 四芒星点 + 青亮色条目名（30px）+ 次级灰蓝说明（24px），行高 82，7 条封顶（7×82+头部 ≈ 正好排到底部金句） |
| 左列金句 | 底部金色短句 + 64px 金色短线起点，y 兜底 min(计算值, 1006) 防越界 |
| 右列样机 | 3 张 zh 竖图 → 面板宽 330（9:16），扇形微转 [-6°, 0°, +6°]，中心 x=1170/1430/1690，先贴左右、中图最后置顶；圆角 22 + teal 细描边 + 投影（alpha 提取 + blur 18 + y 16 偏移） |
| 右列胶囊 | y=906 三枚实色步骤胶囊「1 · 家长发布」等，对齐各面板中心 |
| 字体 | STHeiti Medium.ttc → PingFang.ttc → Hiragino Sans GB.ttc 顺次查找，缺失打印 WARN |
| 配色 | NIGHT `#0B1026` / NIGHT_SOFT `#101A3E` / TEAL `(45,212,191)` / GOLD `(251,191,36)`，与 zh-intro-images 同体系 |

## 换一个版本的流程

1. **取材**：从 `CHANGELOG.md` 对应版本段提炼 5~7 条「条目名（2~4 字）+ 一句话说明（≤18 字）」，与 `recommend_texts/xhs_v<ver>_update.md` 文案口径对齐；确认 zh/ 下该版本的介绍图已生成（通常 3 张，先跑 zh-intro-images skill）。
2. **改配置**：只改脚本顶部 `CONTENT` dict——`version/badge/title/bigline/subtitle/quote/features/images/output`，`output` 命名 `intro_v<版本下划线格式>_update`（如 v1.6.2 → `intro_v162_update`）。`CONTENT` 是易变配置，版式函数是稳定骨架，勿混着改。
3. **运行**（当前 CONTENT 即当前版本，直接跑即可；不要保留多版本配置全量跑）：
   ```bash
   cd starcollection/resources/design && python3 gen_update_image.py
   ```
4. **目检**：打开输出的 jpg 看——左列文案不越界、金句完整可见（底部安全线 1006）、右列三图大标题不被中间图压死、胶囊与面板对齐、描边阴影正常。
5. **验证**：脚本自动打印像素与体积，JPG ≤5MB、WEBP ≤200KB 两个 OK；WEBP 超 200KB 时脚本会自动降质重存（q 每次 −4，下限 40）。

## 已知坑

- **ImageDraw 是像素替换不是 alpha 合成**：在 RGBA 画布上用 `fill=(r,g,b,a<255)` 画胶囊/分隔线，导出 RGB 时 alpha 被丢弃、整块变实心怪色（首版徽章胶囊变成白块就是它）。半透明玻璃件必须画在独立 overlay 层再用 `canvas.alpha_composite()` 合上去；想要「弱化文字」直接给预混实色（如 `(184,196,222)`）。
- **内容条目越多越容易底部越界**：条目 >7 或说明过长时金句会挤出画面——先压缩条目数，不要硬塞；脚本里金句 y 已有 `min(…, 1006)` 兜底，但兜底之后条目仍可能和金句打架。
- **右列固定三张扇形**：`images` 配置数量不是 3 时版式会错——换版本时默认该版本产出 3 张 zh 图；确实只有 2 张/4 张需手改 `centers` 与胶囊循环，别硬套。
- **面板大标题被中间图压住**：说明重叠过多（三个中心的间距 < 面板宽 − 90px 左右），先收窄 `panel_w` 再拉开 `centers` 间距，右缘别超过 ~1900（旋转展开会外扩约 ±20px）。
- **WEBP 降质下限**：q=40 仍超 200KB 时会以 OVER 打印——通常说明底图过碎（照片噪点大），优先压缩素材而不是继续砍质量。
- **无中文字体环境**：打印 `WARN: No CJK font found` 并跳过文字绘制；macOS 之外环境先确认字体路径。
- **无 PIL**：`python3 -m pip install --user pillow`。

## 参考：CONTENT 模板

```python
CONTENT = {
    'version': '1.6.1',
    'badge': '鸿蒙 · 星愿池',
    'title': '1.6.1 版本更新',
    'bigline': '星星时刻，来了',          # 金色主功能句（本版本最大卖点）
    'subtitle': '评完之后，把感受说给彼此',
    'quote': '别人记录习惯，我们记录在一起。',
    'features': [                        # 5~7 条：(条目名, 一句话说明)
        ('星星时刻', '评完自动弹出：家长写一句感受、录段语音留言'),
        ('递给宝贝', '宝贝视角选心情、回一句话，不识字也能参与'),
        # ...
    ],
    'images': [                          # 恰好 3 张：(zh 文件名, 底部胶囊文案, 旋转角)
        ('intro_starmoment.jpg', '家长发布', -6),
        ('intro_replies.jpg', '宝贝回应', 0),
        ('intro_diary_moment.jpg', '日记收藏', 6),
    ],
    'output': 'intro_v161_update',       # v1.6.2 → intro_v162_update
}
```
