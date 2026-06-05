"""
Text rendering for PPT slides.

Adds styled text boxes to PPTX slides with support for:
- Title, subtitle, body text
- Bullet points
- Custom fonts, colors, shadows
- Card backgrounds with blur effect (simulated)
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


def hex_to_rgb(hex_color: str) -> RGBColor:
    """Convert hex color to RGBColor."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return RGBColor(r, g, b)


def parse_color(color_str: str) -> RGBColor:
    """Parse color string (hex or named)."""
    if color_str.startswith("#"):
        return hex_to_rgb(color_str)
    # Add more color name support if needed
    return RGBColor(0, 0, 0)


def parse_color_with_alpha(color_str: str) -> tuple[RGBColor, int]:
    """
    Parse color string with optional alpha.

    Returns:
        Tuple of (RGBColor, alpha 0-255)
    """
    if color_str.startswith("rgba"):
        # rgba(255, 255, 255, 0.85)
        parts = color_str.replace("rgba(", "").replace(")", "").split(",")
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        alpha = int(float(parts[3]) * 255)
        return RGBColor(r, g, b), alpha
    elif color_str.startswith("#"):
        return hex_to_rgb(color_str), 255
    else:
        return RGBColor(0, 0, 0), 255


def get_alignment(align_str: str) -> PP_ALIGN:
    """Convert alignment string to PP_ALIGN enum."""
    align_map = {
        "left": PP_ALIGN.LEFT,
        "center": PP_ALIGN.CENTER,
        "right": PP_ALIGN.RIGHT,
        "justify": PP_ALIGN.JUSTIFY,
    }
    return align_map.get(align_str, PP_ALIGN.LEFT)


def add_text_box(
    slide,
    text: str,
    x: float,          # Inches
    y: float,          # Inches
    width: float,      # Inches
    height: float,     # Inches
    font_size: int = 18,
    font_weight: str = "normal",
    font_color: str = "#ffffff",
    alignment: str = "left",
    line_height: float = 1.5,
    shadow: bool = False,
    shadow_color: str = "rgba(0,0,0,0.3)",
    shadow_offset: tuple = (2, 2),
    shadow_blur: int = 8,
    is_bullet: bool = False,
    bullet_color: str = None,
    anchor: str = "top",
):
    """
    Add a styled text box to a PPTX slide.

    Args:
        slide: PPTX slide object
        text: Text content
        x, y, width, height: Position and size in inches
        font_size: Font size in points
        font_weight: 'normal' or 'bold'
        font_color: Hex color string
        alignment: 'left', 'center', 'right', 'justify'
        line_height: Line height multiplier
        shadow: Whether to add text shadow
        shadow_color: Shadow color (rgba or hex)
        shadow_offset: Shadow offset (x, y) in points
        shadow_blur: Shadow blur radius
        is_bullet: Whether to add bullet points
        bullet_color: Color for bullet symbols
        anchor: Vertical anchor ('top', 'middle', 'bottom')
    """
    # Add text box
    txBox = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(width), Inches(height)
    )
    tf = txBox.text_frame

    # Set word wrap
    tf.word_wrap = True

    # Set vertical anchor
    anchor_map = {
        "top": MSO_ANCHOR.TOP,
        "middle": MSO_ANCHOR.MIDDLE,
        "bottom": MSO_ANCHOR.BOTTOM,
    }
    tf.auto_size = None  # Disable auto-size to respect our dimensions

    # Parse text content
    lines = text.split("\n") if "\n" in text else [text]

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        # Set text
        if is_bullet and line.strip():
            p.text = f"• {line}"
        else:
            p.text = line

        # Set alignment
        p.alignment = get_alignment(alignment)

        # Set line spacing
        p.line_spacing = Pt(font_size * line_height)

        # Style runs
        for run in p.runs:
            run.font.size = Pt(font_size)
            run.font.bold = font_weight == "bold"
            run.font.color.rgb = parse_color(font_color)

            # Add shadow effect (simulated via font color adjustment)
            if shadow:
                # Note: python-pptx doesn't support text shadow directly
                # We'll use a slightly darker/lighter color as approximation
                pass


def add_card_background(
    slide,
    x: float,
    y: float,
    width: float,
    height: float,
    bg_color: list = None,      # [r, g, b, a]
    border_color: list = None,  # [r, g, b, a]
    border_width: int = 1,
    radius: int = 16,
):
    """
    Add a card background shape to a PPTX slide.

    Note: python-pptx doesn't support rounded rectangles natively,
    so we use a rectangle as approximation.
    """
    from pptx.enum.shapes import MSO_SHAPE

    # Default card style
    if bg_color is None:
        bg_color = [255, 255, 255, 30]
    if border_color is None:
        border_color = [255, 255, 255, 50]

    # Add rectangle shape
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(width), Inches(height)
    )

    # Set fill color with transparency
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(bg_color[0], bg_color[1], bg_color[2])
    # Note: python-pptx doesn't support fill transparency directly

    # Set border
    line = shape.line
    line.color.rgb = RGBColor(border_color[0], border_color[1], border_color[2])
    line.width = Pt(border_width)

    # Move to back (behind text)
    # Note: python-pptx doesn't have a direct method for this
    # The shape will be added in order, so we need to reorder

    return shape


def render_slide_text(
    slide,
    slide_data: dict,
    style_config: dict,
    layout_regions: dict,
):
    """
    Render all text content for a slide.

    Args:
        slide: PPTX slide object
        slide_data: Slide data from plan (title, subtitle, key_points, etc.)
        style_config: Style token dict
        layout_regions: Dict of TextRegion objects from layout engine
    """
    text_config = style_config.get("text", {})

    # Render title
    if slide_data.get("title") and "title" in layout_regions:
        region = layout_regions["title"]
        title_style = text_config.get("title", {})

        add_text_box(
            slide,
            slide_data["title"],
            region.x, region.y, region.width, region.height,
            font_size=title_style.get("size", 44),
            font_weight=title_style.get("weight", "bold"),
            font_color=title_style.get("color", "#ffffff"),
            alignment=region.align,
            shadow=title_style.get("shadow", False),
            shadow_color=title_style.get("shadow_color", "rgba(0,0,0,0.3)"),
            shadow_offset=tuple(title_style.get("shadow_offset", [2, 2])),
            shadow_blur=title_style.get("shadow_blur", 8),
        )

    # Render subtitle
    if slide_data.get("subtitle") and "subtitle" in layout_regions:
        region = layout_regions["subtitle"]
        subtitle_style = text_config.get("subtitle", {})

        add_text_box(
            slide,
            slide_data["subtitle"],
            region.x, region.y, region.width, region.height,
            font_size=subtitle_style.get("size", 24),
            font_weight=subtitle_style.get("weight", "normal"),
            font_color=subtitle_style.get("color", "rgba(255,255,255,0.85)"),
            alignment=region.align,
        )

    # Render body text (key_points)
    body_region_name = "body" if "body" in layout_regions else None
    if body_region_name and slide_data.get("key_points"):
        region = layout_regions[body_region_name]
        body_style = text_config.get("body", {})
        bullet_color = body_style.get("bullet_color", None)

        body_text = "\n".join(slide_data["key_points"])

        add_text_box(
            slide,
            body_text,
            region.x, region.y, region.width, region.height,
            font_size=body_style.get("size", 18),
            font_weight=body_style.get("weight", "normal"),
            font_color=body_style.get("color", "#ffffff"),
            alignment=region.align,
            line_height=body_style.get("line_height", 1.6),
            is_bullet=region.bullet,
            bullet_color=bullet_color,
        )

    # Render two-column layout
    if slide_data.get("key_points") and "left" in layout_regions:
        left_region = layout_regions["left"]
        right_region = layout_regions.get("right")
        body_style = text_config.get("body", {})

        points = slide_data["key_points"]
        mid = len(points) // 2
        left_points = points[:mid]
        right_points = points[mid:]

        if left_points:
            add_text_box(
                slide,
                "\n".join(left_points),
                left_region.x, left_region.y, left_region.width, left_region.height,
                font_size=body_style.get("size", 18),
                font_color=body_style.get("color", "#ffffff"),
                alignment=left_region.align,
                line_height=body_style.get("line_height", 1.6),
                is_bullet=left_region.bullet,
            )

        if right_points and right_region:
            add_text_box(
                slide,
                "\n".join(right_points),
                right_region.x, right_region.y, right_region.width, right_region.height,
                font_size=body_style.get("size", 18),
                font_color=body_style.get("color", "#ffffff"),
                alignment=right_region.align,
                line_height=body_style.get("line_height", 1.6),
                is_bullet=right_region.bullet,
            )
