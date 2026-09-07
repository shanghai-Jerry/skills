"""
Background generation for PPT slides.

Supports two modes:
- Template mode: Generate gradients with Pillow (no API needed)
- API mode: Generate backgrounds via Gemini API (needs GEMINI_API_KEY)
"""

import json
import math
import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFilter


# ─── Color Utilities ──────────────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linearly interpolate between two RGB colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ─── Template Mode: Pillow Gradients ─────────────────────────────────────────

def generate_linear_gradient(
    width: int,
    height: int,
    colors: list[str],
    direction: str = "vertical",
) -> Image.Image:
    """Generate a linear gradient background."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    rgb_colors = [hex_to_rgb(c) for c in colors]

    for y in range(height):
        for x in range(width):
            # Calculate gradient position based on direction
            if direction == "vertical":
                t = y / height
            elif direction == "horizontal":
                t = x / width
            elif direction == "diagonal":
                t = (x / width + y / height) / 2
            elif direction == "diagonal_reverse":
                t = 1 - (x / width + y / height) / 2
            else:
                t = y / height

            # Handle multi-color gradients
            if len(rgb_colors) == 2:
                color = lerp_color(rgb_colors[0], rgb_colors[1], t)
            else:
                # Distribute colors across gradient
                segment = t * (len(rgb_colors) - 1)
                idx = min(int(segment), len(rgb_colors) - 2)
                local_t = segment - idx
                color = lerp_color(rgb_colors[idx], rgb_colors[idx + 1], local_t)

            pixels[x, y] = color

    # Soften gradient
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img


def generate_radial_gradient(
    width: int,
    height: int,
    colors: list[str],
    center: tuple[float, float] = (0.5, 0.5),
) -> Image.Image:
    """Generate a radial gradient background."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    rgb_colors = [hex_to_rgb(c) for c in colors]
    cx, cy = center[0] * width, center[1] * height
    max_dist = math.sqrt(width**2 + height**2) / 2

    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            t = min(dist / max_dist, 1.0)

            if len(rgb_colors) == 2:
                color = lerp_color(rgb_colors[0], rgb_colors[1], t)
            else:
                segment = t * (len(rgb_colors) - 1)
                idx = min(int(segment), len(rgb_colors) - 2)
                local_t = segment - idx
                color = lerp_color(rgb_colors[idx], rgb_colors[idx + 1], local_t)

            pixels[x, y] = color

    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img


def generate_mesh_gradient(
    width: int,
    height: int,
    colors: list[str],
) -> Image.Image:
    """Generate a mesh-like gradient with multiple color points."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Create control points for mesh effect
    points = []
    for i, color in enumerate(rgb_colors):
        angle = (2 * math.pi * i) / len(rgb_colors)
        px = 0.5 + 0.3 * math.cos(angle)
        py = 0.5 + 0.3 * math.sin(angle)
        points.append((px, py, color))

    for y in range(height):
        for x in range(width):
            nx, ny = x / width, y / height

            # Weighted average of all control points
            total_weight = 0
            weighted_r, weighted_g, weighted_b = 0, 0, 0

            for px, py, color in points:
                dist = math.sqrt((nx - px) ** 2 + (ny - py) ** 2)
                weight = 1 / (dist + 0.01)  # Inverse distance weighting
                total_weight += weight
                weighted_r += color[0] * weight
                weighted_g += color[1] * weight
                weighted_b += color[2] * weight

            r = int(weighted_r / total_weight)
            g = int(weighted_g / total_weight)
            b = int(weighted_b / total_weight)
            pixels[x, y] = (r, g, b)

    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    return img


def generate_template_background(
    width: int,
    height: int,
    colors: list[str],
    direction: str = "diagonal",
) -> Image.Image:
    """Generate background using template mode (no API)."""
    if direction == "mesh" or len(colors) > 2:
        return generate_mesh_gradient(width, height, colors)
    elif direction == "radial":
        return generate_radial_gradient(width, height, colors)
    else:
        return generate_linear_gradient(width, height, colors, direction)


# ─── API Mode: Gemini Background ─────────────────────────────────────────────

def generate_api_background(
    prompt: str,
    output_path: str,
    aspect_ratio: str = "16:9",
) -> str:
    """Generate background using Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "generationConfig": {"imageConfig": {"aspectRatio": aspect_ratio}},
            "contents": [{"parts": [{"text": prompt}]}],
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    parts = data["candidates"][0]["content"]["parts"]
    image_parts = [p for p in parts if p.get("inlineData")]

    if not image_parts:
        raise Exception("No image returned from API")

    import base64

    img_data = base64.b64decode(image_parts[0]["inlineData"]["data"])
    with open(output_path, "wb") as f:
        f.write(img_data)

    return output_path


# ─── Unified Interface ────────────────────────────────────────────────────────

def generate_background(
    style_config: dict,
    output_path: str,
    width: int = 1920,
    height: int = 1080,
    use_api: bool = False,
) -> str:
    """
    Generate background based on style config.

    Args:
        style_config: Style token dict with 'background' key
        output_path: Path to save generated background
        width: Image width in pixels
        height: Image height in pixels
        use_api: Whether to use Gemini API (falls back to template if no key)

    Returns:
        Path to generated background image
    """
    bg_config = style_config["background"]
    colors = bg_config["colors"]
    direction = bg_config.get("direction", "diagonal")

    # Try API mode if requested and available
    if use_api and os.getenv("GEMINI_API_KEY"):
        try:
            api_prompt = bg_config.get("api_prompt", "")
            return generate_api_background(api_prompt, output_path)
        except Exception as e:
            print(f"API background failed, falling back to template: {e}")

    # Template mode
    img = generate_template_background(width, height, colors, direction)
    img.save(output_path, "JPEG", quality=95)
    return output_path


def get_available_styles(styles_dir: str) -> dict[str, dict]:
    """Load all available styles from styles directory."""
    styles = {}
    for filename in os.listdir(styles_dir):
        if filename.endswith(".json"):
            name = filename.replace(".json", "")
            with open(os.path.join(styles_dir, filename), "r") as f:
                styles[name] = json.load(f)
    return styles


def get_style_summary(styles: dict) -> str:
    """Get a human-readable summary of available styles."""
    lines = ["Available styles:"]
    for name, style in styles.items():
        lines.append(f"  - {name}: {style['description']} (Best for: {style['best_for']})")
    return "\n".join(lines)
