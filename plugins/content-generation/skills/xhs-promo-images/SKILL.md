---
name: xhs-promo-images
description: 将 App 推广截图（应用市场 9:16 竖版介绍图等）批量处理为符合小红书发布要求的图片：3:4 顶裁、JPEG 压缩、逐张验证比例/像素/体积。适用于「把 zh/ 或任意目录的推广图转到 xhs/ 目录」「小红书发 App 介绍图前的图片处理」等任务。
---

# 小红书 App 推广图处理工具

把 App 的介绍截图（通常是应用市场用的 1080×1920 竖版长图）批量处理成符合小红书图片要求的文件。源于 stars-collection 项目 2026-10-11 的真实需求，流程与脚本已在真机验证。

## 小红书图片要求（硬性，发布方提供）

发布方要求「至少 1 张图片」同时满足：

- **比例**：1:1（正方形）或 3:4
- **像素**：≥800×800px（对应 1:1），或 ≥750×1000px（对应 3:4）
- **大小**：≤3MB

目标：批量处理后**每一张**都达标（优于「至少 1 张」的底线），并逐张打印验证数据。

## 处理流程

1. **盘点输入**：列出源目录（如 `resources/design/zh/`）所有 jpg/png，打印每张的像素尺寸与体积。
   - 应用市场竖版图典型为 1080×1920（9:16）。
2. **选裁切比**：默认 **3:4**（竖版内容信息量保留最多）。目标高 = `round(宽 × 4 / 3)`。
3. **顶裁，不居中裁**：推广图的构图是「顶部标题头部 + 下方手机样机」，从顶部裁 `0 → 目标高` 能保住标题、副标题、特性胶囊和样机上半部；居中裁会把标题切掉。内容比目标比例矮时直接用原图（**绝不放大**）。
4. **输出**：写入目标目录（约定 `resources/design/xhs/`），**同文件名**；JPEG `quality=90, optimize=True`（推广图 1080 宽下约 110–140KB，远低于 3M 上限）。
5. **验证（必须逐张）**：打印每张的 `宽x高 / ratio / 字节数`，核对三项：
   - `ratio ≈ 0.7500`（3:4）或 `1.0000`（1:1）
   - 宽 ≥750 且 高 ≥1000（3:4 口径）
   - 字节 ≤ 3×1024×1024
   任何一张不达标就调整后重跑，不许只口头断言。

## 参考实现

```python
#!/usr/bin/env python3
"""推广图 zh(9:16) -> xhs(3:4) 批量转换。用法: python3 zh_to_xhs.py [src] [dst]"""
import os, sys
from PIL import Image

base = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "zh")
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, "xhs")
os.makedirs(dst, exist_ok=True)

for name in sorted(os.listdir(src)):
    if not name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    im = Image.open(os.path.join(src, name)).convert("RGB")
    w, h = im.size
    # 3:4 顶裁：保住标题头部 + 手机样机上半部；内容不足比例时用原图（不放大）
    target_h = int(round(w * 4 / 3))
    out = im.crop((0, 0, w, min(target_h, h))) if h > target_h else im
    path = os.path.join(dst, name)
    out.save(path, "JPEG", quality=90, optimize=True)
    size = os.path.getsize(path)
    print(f"{name}: {out.size[0]}x{out.size[1]} "
          f"ratio={out.size[0]/out.size[1]:.4f} "
          f"{size/1024/1024:.2f} MB")
```

## 决策记录（为什么是顶裁 3:4）

- 1:1 从 9:16 裁要丢掉 44% 高度，3:4 只丢 25% → 选 3:4。
- 顶部是营销信息（标题/卖点），底部是样机的重复界面区域 → 顶裁。
- 原图为 RGB jpg、体量小（~200KB），q90 输出后体积反降，无画质争议。

## 边界与注意

- **源图不是 1080×1920 时**：公式通用（`目标高 = 宽×4/3`），但仍需逐张验证像素下限；源图太小（宽 <750）需先确认能否接受整体放大或换更宽的源图（推广图不建议放大）。
- **1:1 需求**：裁 `min(w, h)` 见方，同样顶锚 `crop((0, 0, s, s))`，验证 `≥800×800`。
- **透明 PNG 源**：先 `.convert("RGB")` 再存 jpg（本工具默认 jpg 输出；需要保留透明时改存 png 并复核体积）。
- 中文环境 macOS 无 PIL 时：`python3 -m pip install --user pillow`。
- 本 skill 只做位图裁切压缩；若还要生成「带标题头部+样机」的市场长图本体，用 `resources/design/gen_intro_images*.py` 一类的生成脚本先出图，再走本流程。
