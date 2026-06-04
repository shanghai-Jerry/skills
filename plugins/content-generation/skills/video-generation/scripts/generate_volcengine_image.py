"""Generate images using Volcengine Ark (Doubao) API.

Supports text-to-image generation via the synchronous API.

Usage:
    python generate_volcengine_image.py --prompt "A sunset over mountains" --output-file /tmp/image.png
    python generate_volcengine_image.py --prompt "..." --size 1024x1024 --num 2 --output-dir /tmp/images/
"""

import argparse
import os
import sys

import requests

API_BASE = os.getenv("VOLCENGINE_API_BASE", "https://ark.cn-beijing.volces.com/api/v3")
DEFAULT_MODEL = os.getenv("VOLCENGINE_IMAGE_MODEL", "doubao-seedream-4-5-251128")
DEFAULT_SIZE = os.getenv("VOLCENGINE_IMAGE_SIZE", "2K")


def generate_image(
    prompt: str,
    output_file: str,
    model: str = DEFAULT_MODEL,
    size: str = DEFAULT_SIZE,
    num: int = 1,
    seed: int | None = None,
) -> str:
    """Generate images and download to local files.

    Args:
        prompt: Text prompt describing the desired image.
        output_file: Output path for the generated image.
                     If num > 1, this is used as a prefix (e.g. /tmp/img.png -> /tmp/img_0.png).
        model: Model identifier.
        size: Image size in WxH format (e.g. "1024x1024", "1536x1024").
        num: Number of images to generate (1-4).
        seed: Optional seed for reproducibility.

    Returns:
        Success message with output path(s), or error message.
    """
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        return "ARK_API_KEY is not set"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    watermark = os.getenv("VOLCENGINE_WATERMARK", "false").lower() in ("true", "1", "yes")
    body: dict = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "watermark": watermark,
    }
    if seed is not None:
        body["seed"] = seed

    # Submit generation request
    resp = requests.post(
        f"{API_BASE}/images/generations",
        headers=headers,
        json=body,
    )
    data = resp.json()

    # Extract image URLs — defensive parsing for different response formats
    images = data.get("data", [])
    if not images:
        return f"No images in response: {data}"

    downloaded: list[str] = []
    img_urls: list[str] = []
    for idx, img_item in enumerate(images):
        # Try common URL fields
        url = (
            img_item.get("url", "")
            or img_item.get("b64_json", "")
        )
        if not url:
            continue

        # Record HTTP URL for reference
        if url.startswith("http://") or url.startswith("https://"):
            img_urls.append(url)

        # Build output path for multiple images
        if num > 1:
            base, ext = os.path.splitext(output_file)
            out_path = f"{base}_{idx}{ext}"
        else:
            out_path = output_file

        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

        if url.startswith("http://") or url.startswith("https://"):
            # Download from URL
            img_resp = requests.get(url, stream=True)
            img_resp.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in img_resp.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            # Assume base64 encoded data
            import base64
            img_data = base64.b64decode(url)
            with open(out_path, "wb") as f:
                f.write(img_data)

        downloaded.append(out_path)

    if not downloaded:
        return f"Failed to download any images from response: {data}"

    if len(downloaded) == 1:
        msg = f"The image has been generated successfully to {downloaded[0]}"
        if img_urls:
            msg += f"\nImage URL: {img_urls[0]}"
        return msg
    msg = f"{len(downloaded)} images have been generated successfully to: {', '.join(downloaded)}"
    if img_urls:
        msg += f"\nImage URLs: {', '.join(img_urls)}"
    return msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using Volcengine Ark (Doubao) API")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Text prompt for image generation",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Output path for the generated image (e.g. /tmp/image.png)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model identifier (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--size",
        default=DEFAULT_SIZE,
        help=f"Image size in WxH format (default: {DEFAULT_SIZE})",
    )
    parser.add_argument(
        "--num",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Number of images to generate (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for reproducibility",
    )

    args = parser.parse_args()

    try:
        print(
            generate_image(
                prompt=args.prompt,
                output_file=args.output_file,
                model=args.model,
                size=args.size,
                num=args.num,
                seed=args.seed,
            )
        )
    except Exception as e:
        print(f"Error while generating image: {e}", file=sys.stderr)
        sys.exit(1)
