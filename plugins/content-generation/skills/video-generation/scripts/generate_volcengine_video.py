"""Generate videos using Volcengine Ark (Seedance) API.

Supports text-to-video and image-to-video generation via the async task API.

Usage:
    python generate_volcengine_video.py --prompt "A cat playing piano" --output-file /tmp/video.mp4
    python generate_volcengine_video.py --prompt-file /tmp/prompt.txt --output-file /tmp/video.mp4
    python generate_volcengine_video.py --prompt "..." --reference-image /tmp/ref.jpg --output-file /tmp/video.mp4
"""

import argparse
import base64
import os
import sys
import time

import requests

API_BASE = os.getenv("VOLCENGINE_API_BASE", "https://ark.cn-beijing.volces.com/api/v3")
DEFAULT_MODEL = os.getenv("VOLCENGINE_VIDEO_MODEL", "doubao-seedance-1-5-pro-251215")
POLL_INTERVAL = int(os.getenv("VOLCENGINE_POLL_INTERVAL", "5"))


def generate_video(
    prompt: str,
    output_file: str,
    reference_images: list[str] | None = None,
    model: str = DEFAULT_MODEL,
    duration: int = int(os.getenv("VOLCENGINE_VIDEO_DURATION", "5")),
    ratio: str = os.getenv("VOLCENGINE_VIDEO_RATIO", "16:9"),
    generate_audio: bool = False,
) -> str:
    """Submit a video generation task and poll until complete, then download.

    Args:
        prompt: Text prompt describing the desired video.
        output_file: Absolute path to save the generated video.
        reference_images: Optional list of image paths for image-to-video.
        model: Model identifier (e.g. doubao-seedance-1-5-pro-251215).
        duration: Video duration in seconds ("5" or "10").
        ratio: Aspect ratio ("16:9", "9:16", "1:1").
        generate_audio: Whether to generate audio for the video.

    Returns:
        Success message with output path, or error message.
    """
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        return "ARK_API_KEY is not set"

    # Build content array
    content: list[dict] = [{"type": "text", "text": prompt}]

    if reference_images:
        for img_path in reference_images:
            if img_path.startswith("http://") or img_path.startswith("https://"):
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img_path},
                })
            else:
                with open(img_path, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode("utf-8")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                })

    # Build request body
    watermark = os.getenv("VOLCENGINE_WATERMARK", "false").lower() in ("true", "1", "yes")
    body: dict = {
        "model": model,
        "content": content,
        "duration": duration,
        "ratio": ratio,
        "watermark": watermark,
    }
    if generate_audio:
        body["generate_audio"] = True
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Step 1: Submit task
    resp = requests.post(
        f"{API_BASE}/contents/generations/tasks",
        headers=headers,
        json=body,
    )
    #resp.raise_for_status()
    task_data = resp.json()
    task_id = task_data.get("task_id", "") or task_data.get("id", "")
    if not task_id:
        return f"Failed to submit task: {task_data}"

    print(f"Task submitted: {task_id}", file=sys.stderr)

    # Step 2: Poll until complete
    while True:
        time.sleep(POLL_INTERVAL)
        resp = requests.get(
            f"{API_BASE}/contents/generations/tasks/{task_id}",
            headers=headers,
        )
        poll_data = resp.json()

        task_status = poll_data.get("status", "")
        if task_status == "succeeded":
            # Extract video URL(s)
            content = poll_data.get("content", {})
            if not content:
                return f"Task succeeded but no content returned: {poll_data}"
            video_url = content.get("url", "")
            if not video_url:
                # Some responses nest the url differently
                video_url = content.get("video_url", "")
            if not video_url:
                return f"Cannot find video URL in response: {poll_data}"

            # Step 3: Download video
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            video_resp = requests.get(video_url, stream=True)
            video_resp.raise_for_status()
            with open(output_file, "wb") as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return f"The video has been generated successfully to {output_file}\nVideo URL: {video_url}"

        elif task_status == "failed":
            error_msg = poll_data.get("data", {}).get("error", {}).get("message", "Unknown error")
            return f"Task failed: {error_msg}"

        elif task_status in ("queued", "running", "pending"):
            print(f"  Status: {task_status}...", file=sys.stderr)
            continue

        else:
            print(f"  Unknown status: {task_status}, raw: {poll_data}", file=sys.stderr)
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate videos using Volcengine Ark (Seedance) API")
    parser.add_argument(
        "--prompt",
        help="Text prompt for video generation (use --prompt-file for file-based prompt)",
    )
    parser.add_argument(
        "--prompt-file",
        help="Path to a text file containing the prompt",
    )
    parser.add_argument(
        "--reference-images",
        nargs="*",
        default=[],
        help="Paths to reference images for image-to-video (space-separated, or URLs)",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Output path for the generated video (e.g. /tmp/video.mp4)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model identifier (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=int(os.getenv("VOLCENGINE_VIDEO_DURATION", "5")),
        choices=[5, 10],
        help="Video duration in seconds",
    )
    parser.add_argument(
        "--ratio",
        default=os.getenv("VOLCENGINE_VIDEO_RATIO", "16:9"),
        choices=["16:9", "9:16", "1:1"],
        help="Aspect ratio",
    )
    parser.add_argument(
        "--generate-audio",
        action="store_true",
        help="Generate audio for the video",
    )

    args = parser.parse_args()

    # Resolve prompt
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: --prompt or --prompt-file is required", file=sys.stderr)
        sys.exit(1)

    try:
        print(
            generate_video(
                prompt=prompt,
                output_file=args.output_file,
                reference_images=args.reference_images or None,
                model=args.model,
                duration=args.duration,
                ratio=args.ratio,
                generate_audio=args.generate_audio,
            )
        )
    except Exception as e:
        print(f"Error while generating video: {e}", file=sys.stderr)
        sys.exit(1)
