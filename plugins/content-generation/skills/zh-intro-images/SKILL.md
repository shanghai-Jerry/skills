---
name: zh-intro-images
description: 用 gen_intro_images_zh.py 把 App 真机截图生成为应用市场介绍长图（夜空星愿主题，1080×1920，9:16）：新增页面配置、配色/文案规范、单配置运行、已知坑修复与验证。适用于「生成/更新 zh/ 介绍图」「加一张新页面的市场截图」「demo 截图转介绍长图」等任务。生成后可接 xhs-promo-images 转小红书 3:4。
---

# zh 应用市场介绍长图生成

把一张 App 真机截图包成「渐变头部 + 标题/副标题/特性胶囊 + 圆角样机 + 阴影」的 1080×1920 竖版介绍图（9:16，应用市场/小红书底图）。源于 stars-collection 项目，流程已在真机验证（2026-10-18 生成「成长档案」页）。

**脚本**：`starcollection/resources/design/gen_intro_images_zh.py`
**素材**：`resources/design/demo/`（真机截图 jpg）
**输出**：`resources/design/zh/intro_*.jpg`（1080×1920，JPEG q93，约 200KB）

## 版式规格（夜空星愿主题，改动前先读）

| 元素 | 规格 |
|---|---|
| 画布 | 1080×1920 RGBA，底色 NIGHT_SOFT `#101A3E` |
| 头部渐变 | 高 480px，从 NIGHT `#0B1026` 渐变到 `lerp(NIGHT, accent, 0.42)`，再 100px 渐隐入正文底色 |
| 标题 | y=100，字号 80，白色，居中，两侧各一颗主题色发光星点 |
| 副标题 | y=210，字号 38，白色 alpha 200 |
| 特性胶囊 | y=300，字号 30，白色 alpha 40 玻璃底 + accent 描边，圆角=半高 |
| 装饰线 | y=380，60×4 圆角条，accent 色 |
| 样机 | phone_top=420，宽 = 1080×0.84，超过剩余高度时按 max_h 反算收窄（**不裁切、不放大**），圆角 40，下方 8px 偏移阴影（alpha 110，blur 20） |
| 字体 | 依次找 `/System/Library/Fonts/` 下 STHeiti Medium.ttc → PingFang.ttc → Hiragino Sans GB.ttc，找不到则跳过并打印 WARN |

**各页签 accent 主题色**（对应应用内页签）：teal `(45,212,191)`、紫 `(167,139,250)`、粉 `(244,114,182)`、金 `(251,191,36)`、靛 `(129,140,248)`。

## 新增一张介绍图的流程

1. **看图定文案**：读 demo 截图，确定页面名。四个字段都用中文：
   - `title` 页面名（2–4 字，如「成长档案」）
   - `subtitle` 一句话价值（如「记录身高 · 体重 · 视力」）
   - `desc` 特性胶囊，3–4 个短词用 ` · ` 连接（如「身高记录 · 体重记录 · 视力记录 · 同龄参考对比」），总宽需 < 1080 - 60
   - `accent` 取页面主色（按钮/选中态颜色）
2. **加配置**：在 `configs` 列表末尾追加 dict，`output` 命名 `intro_<英文页名>.jpg`。
3. **单配置运行**（不要直接 `python3 gen_intro_images_zh.py` 全量跑）：历史 demo 截图会被清理，全量跑会因缺文件中途崩。用 import 只跑新配置：
   ```bash
   cd starcollection/resources/design && python3 -c "
   import gen_intro_images_zh as g
   g.generate(g.configs[-1])
   "
   ```
4. **目检**：缩小到 270×480 存临时 png 看一眼——标题不裁切、胶囊不溢出、样机圆角和阴影正常、accent 与页面主色一致。
5. **验证**：打印像素与体积（1080×1920、<3MB 即市场合格）。
6. **（可选）转小红书**：接着用 `xhs-promo-images` skill 顶裁 3:4 到 `xhs/`，同文件名。

## 已知坑

- **`NIGHT` 未定义（NameError）**：脚本曾丢失 `NIGHT = (11, 16, 38)` 常量定义，只有 `NIGHT_SOFT`。2026-10-18 已修复补回；若再现同类 NameError，按头部渐变语义补常量，并可用已有 zh 图顶部像素 `(11,16,38)` 校验取值。
- **旧配置指向已删除的 demo 截图**：`configs` 前 4 项引用的截图可能已从 `demo/` 清走，全量运行会 `FileNotFoundError`——这是预期，按上面单配置方式跑即可，勿删旧配置（保留历史文案记录）。
- **超长截图（如 1280×2832）**：会被 max_h 反算收窄到约 660px 宽，属正常表现，样机会变窄但不裁切。
- **无中文字体环境**：脚本打印 `WARN: No CJK font found` 并跳过；macOS 自带字体路径不存在时先确认系统版本。
- **无 PIL**：`python3 -m pip install --user pillow`。

## 参考：配置模板

```python
{
    'screenshot': 'Weixin Image_20261018210359_64_1.jpg',  # demo/ 下真机截图文件名
    'title': '成长档案',
    'subtitle': '记录身高 · 体重 · 视力',
    'desc': '身高记录 · 体重记录 · 视力记录 · 同龄参考对比',
    'accent': (45, 212, 191),   # 青（页面主色）
    'output': 'intro_growth.jpg',
},
```
