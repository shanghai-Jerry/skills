"""
Layout engine for PPT slides.

Converts percentage-based layout definitions to absolute positions
for python-pptx text box placement.
"""

from dataclasses import dataclass
from pptx.util import Inches, Pt, Emu


# Slide dimensions (standard 16:9)
SLIDE_WIDTH_INCHES = 13.333
SLIDE_HEIGHT_INCHES = 7.5


@dataclass
class TextRegion:
    """A positioned text region on a slide."""
    x: float          # Inches from left
    y: float          # Inches from top
    width: float      # Inches
    height: float     # Inches
    align: str = "left"
    bullet: bool = False


def resolve_layout(
    layout_name: str,
    style_config: dict,
    slide_width: float = SLIDE_WIDTH_INCHES,
    slide_height: float = SLIDE_HEIGHT_INCHES,
) -> dict[str, TextRegion]:
    """
    Resolve a layout name to absolute positioned TextRegions.

    Args:
        layout_name: Name of layout (e.g., 'content', 'two_column')
        style_config: Style token dict containing 'layouts'
        slide_width: Slide width in inches
        slide_height: Slide height in inches

    Returns:
        Dict mapping region names to TextRegion objects
    """
    layouts = style_config.get("layouts", {})

    if layout_name not in layouts:
        raise ValueError(
            f"Layout '{layout_name}' not found. Available: {list(layouts.keys())}"
        )

    layout_def = layouts[layout_name]
    regions = {}

    for region_name, pos in layout_def.items():
        regions[region_name] = TextRegion(
            x=pos["x"] * slide_width,
            y=pos["y"] * slide_height,
            width=pos["w"] * slide_width,
            height=pos["h"] * slide_height,
            align=pos.get("align", "left"),
            bullet=pos.get("bullet", False),
        )

    return regions


def get_recommended_layout(slide_type: str) -> str:
    """Get recommended layout name based on slide type."""
    layout_map = {
        "title": "title_center",
        "title_left": "title_left",
        "content": "content",
        "two_column": "two_column",
        "section": "section_divider",
        "section_divider": "section_divider",
        "image_text": "image_text",
    }
    return layout_map.get(slide_type, "content")


def validate_plan_layouts(plan: dict, style_config: dict) -> list[str]:
    """
    Validate that all layouts in the plan exist in the style.

    Returns:
        List of warning messages (empty if valid)
    """
    warnings = []
    available_layouts = set(style_config.get("layouts", {}).keys())

    for slide in plan.get("slides", []):
        layout = slide.get("layout", "content")
        if layout not in available_layouts:
            warnings.append(
                f"Slide {slide.get('slide_number', '?')}: "
                f"layout '{layout}' not in style. Available: {list(available_layouts)}"
            )

    return warnings


def auto_assign_layouts(plan: dict) -> dict:
    """
    Auto-assign layouts to slides based on their type if not specified.

    Modifies plan in-place and returns it.
    """
    for slide in plan.get("slides", []):
        if "layout" not in slide:
            slide_type = slide.get("type", "content")
            slide["layout"] = get_recommended_layout(slide_type)

    return plan


# ─── Layout Preview (Text-based) ─────────────────────────────────────────────

def preview_layout(layout_name: str, style_config: dict) -> str:
    """
    Generate a text-based preview of a layout.

    Returns:
        ASCII art representation of the layout
    """
    regions = resolve_layout(layout_name, style_config)

    # Simple ASCII preview
    grid = [["." for _ in range(40)] for _ in range(20)]

    for name, region in regions.items():
        # Convert to grid coordinates
        gx = int(region.x / SLIDE_WIDTH_INCHES * 40)
        gy = int(region.y / SLIDE_HEIGHT_INCHES * 20)
        gw = int(region.width / SLIDE_WIDTH_INCHES * 40)
        gh = int(region.height / SLIDE_HEIGHT_INCHES * 20)

        # Fill region
        label = name[:4]
        for dy in range(min(gh, 20 - gy)):
            for dx in range(min(gw, 40 - gx)):
                if 0 <= gy + dy < 20 and 0 <= gx + dx < 40:
                    if dy == 0 and dx < len(label):
                        grid[gy + dy][gx + dx] = label[dx]
                    elif dy == 0 or dy == gh - 1:
                        grid[gy + dy][gx + dx] = "-"
                    elif dx == 0 or dx == gw - 1:
                        grid[gy + dy][gx + dx] = "|"
                    else:
                        grid[gy + dy][gx + dx] = " "

    return "\n".join("".join(row) for row in grid)
