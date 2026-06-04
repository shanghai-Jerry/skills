---
name: video-generation
description: Use this skill when the user requests to generate, create, or imagine videos or images. Supports Volcengine Ark (Seedance/Doubao) providers.
---

# Video & Image Generation Skill

## Overview

This skill generates high-quality videos and images using structured prompts and Python scripts. It supports:

- **Volcengine Ark (Seedance)** — Video generation (text-to-video, image-to-video)
- **Volcengine Ark (Doubao Seedream)** — Image generation (text-to-image)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ARK_API_KEY` | Yes | — | Volcengine Ark API key. Must be set before running any generation commands. |
| `VOLCENGINE_API_BASE` | No | `https://ark.cn-beijing.volces.com/api/v3` | Volcengine Ark API base URL (for different regions). |
| `VOLCENGINE_IMAGE_MODEL` | No | `doubao-seedream-4-5-251128` | Default model for image generation. |
| `VOLCENGINE_IMAGE_SIZE` | No | `2K` | Default image size (e.g. `2K`, `4K`, `1024x1024`). |
| `VOLCENGINE_VIDEO_MODEL` | No | `doubao-seedance-1-5-pro-251215` | Default model for video generation. |
| `VOLCENGINE_VIDEO_DURATION` | No | `5` | Default video duration in seconds. |
| `VOLCENGINE_VIDEO_RATIO` | No | `16:9` | Default aspect ratio for video. |
| `VOLCENGINE_POLL_INTERVAL` | No | `5` | Polling interval (seconds) for async video task status. |
| `VOLCENGINE_WATERMARK` | No | `false` | Whether to add watermark to generated content. |

> These variables must be available in the environment when the agent executes the Python scripts. The agent should ensure they are set before proceeding.

## Path Conventions

This skill uses a **sandboxed temporary directory** to avoid polluting the user's workspace:

| Base | Meaning |
|---|---|
| `./scripts/` | Relative to SKILL.md directory (skill root) — contains Python scripts |
| `<sandbox-dir>` | Temporary directory for this skill session (auto-created, auto-cleaned) |
| `<sandbox-dir>/workspace/` | Stores status files and prompts |
| `<sandbox-dir>/outputs/` | Stores generated videos and images |

> **Important**: All temporary files are stored in `<sandbox-dir>`. The agent should create this directory at session start and clean it up at session end (unless the user wants to keep the outputs).

### Sandbox Directory Setup

At the start of each skill session, the agent should:

```bash
# Create sandbox directory with unique session ID
SANDBOX_DIR="/tmp/skill-sessions/video-gen-$(date +%s)"
mkdir -p "$SANDBOX_DIR/workspace" "$SANDBOX_DIR/outputs"
```

### Cleanup

At the end of the session (or when the user confirms), clean up:

```bash
# Remove sandbox directory (keeping outputs if user wants)
rm -rf "$SANDBOX_DIR"
```

---

## Task Status Tracking

The skill uses JSON status files in a `<sandbox-dir>/workspace` directory to track whether image or video generation tasks are currently running. These files enable the Agent (and users) to check task status at any time.

### Status Files

| File | Purpose |
|---|---|
| `<sandbox-dir>/workspace/image_generation_status.json` | Tracks image generation task status |
| `<sandbox-dir>/workspace/video_generation_status.json` | Tracks video generation task status |

### Status File Format

Both status files share the same JSON structure:

```json
{
  "status": "idle",
  "prompt": "the prompt used for generation",
  "output_path": "<sandbox-dir>/outputs/xxx.png",
  "image_url": null,
  "video_url": null,
  "task_id": null,
  "started_at": null,
  "completed_at": null,
  "error": null
}
```

> - `task_id` is only used by the video generation status file.
> - `image_url` is set after image generation completes; it is the HTTP URL returned by the API.
> - `video_url` is set after video generation completes; it is the HTTP URL returned by the API.

**Possible `status` values:**

| Status | Meaning |
|---|---|
| `idle` | No task running, no previous result |
| `running` | A generation task is currently in progress |
| `completed` | Task finished successfully, output file is ready |
| `failed` | Task ended with an error, check `error` field for details |

### Checking Status

To check whether any generation task is running, read the status files:

```bash
cat <sandbox-dir>/workspace/image_generation_status.json
cat <sandbox-dir>/workspace/video_generation_status.json
```

**Decision rules based on status:**

- `running` — A task is in progress. Wait for it to complete, or inform the user that a task is already running.
- `completed` — The previous task succeeded. The output file path is in `output_path`. You may reuse the result or start a new task.
- `failed` — The previous task failed. Check `error` for details. You may retry or inform the user.
- `idle` — No task has been executed yet. Safe to proceed.

---

## Automated Execution Workflow

**CRITICAL**: When this skill is triggered, execute the full pipeline immediately without asking the user for confirmation. Do not stop to ask "shall I proceed?" or "is this OK?" — just run the pipeline directly.

The standard pipeline for video generation has 3 phases:

### Phase 1: Check Status & Generate Prompt

1. Read both status files. If either shows `running`, inform the user and wait.
2. Analyze the user's request and identify: subject, style, mood, composition, aspect ratio, lighting.
3. Generate a detailed English prompt (always use English for prompts regardless of user language).
4. Save the prompt as a JSON file: `<sandbox-dir>/workspace/{descriptive-name}.json`
5. Update `<sandbox-dir>/workspace/image_generation_status.json`:

```json
{
  "status": "idle",
  "prompt": "the generated prompt text",
  "output_path": null,
  "started_at": null,
  "completed_at": null,
  "error": null
}
```

### Phase 2: Generate Image

Generate a reference image to guide video generation (reference images significantly enhance quality and visual consistency).

1. Update `<sandbox-dir>/workspace/image_generation_status.json` to `running`:

```json
{
  "status": "running",
  "prompt": "the prompt text",
  "output_path": "<sandbox-dir>/outputs/{descriptive-name}_reference.png",
  "image_url": null,
  "started_at": "<current ISO timestamp>",
  "completed_at": null,
  "error": null
}
```

2. Execute the image generation script:

```bash
python ./scripts/generate_volcengine_image.py \
  --prompt "<the generated prompt>" \
  --output-file <sandbox-dir>/outputs/{descriptive-name}_reference.png \
  --size 2K
```

3. On success, the script outputs both the local path and the image URL. Extract the `Image URL: xxx` from the output and update the status file:

```json
{
  "status": "completed",
  "prompt": "the prompt text",
  "output_path": "<sandbox-dir>/outputs/{descriptive-name}_reference.png",
  "image_url": "<the extracted image URL from script output>",
  "started_at": "<start timestamp>",
  "completed_at": "<current ISO timestamp>",
  "error": null
}
```

4. On failure, update the status file:

```json
{
  "status": "failed",
  "prompt": "the prompt text",
  "output_path": null,
  "image_url": null,
  "started_at": "<start timestamp>",
  "completed_at": "<current ISO timestamp>",
  "error": "<error message from script output>"
}
```

5. If image generation fails, **stop the pipeline** and inform the user. Do not proceed to video generation without a reference image.

### Phase 3: Generate Video

Use the reference image from Phase 2 to generate the video.

1. Update `<sandbox-dir>/workspace/video_generation_status.json` to `running`:

```json
{
  "status": "running",
  "prompt": "the prompt text",
  "output_path": "<sandbox-dir>/outputs/{descriptive-name}.mp4",
  "reference_image": "<image URL or local path>",
  "image_url": null,
  "video_url": null,
  "task_id": null,
  "started_at": "<current ISO timestamp>",
  "completed_at": null,
  "error": null
}
```

2. Execute the video generation script. **IMPORTANT**: Use the `image_url` from `image_generation_status.json` (the HTTP URL returned by the API) as the `--reference-images` parameter. This is preferred over local file paths because it avoids unnecessary re-uploading and ensures better quality:

```bash
python ./scripts/generate_volcengine_video.py \
  --prompt "<the generated prompt>" \
  --reference-images <image_url from image_generation_status.json> \
  --output-file <sandbox-dir>/outputs/{descriptive-name}.mp4 \
  --duration 5 \
  --ratio 16:9
```

> If for any reason `image_url` is not available (e.g., the API returned only base64 data), fall back to using the local file path from `output_path` in `image_generation_status.json`.

**IMPORTANT**: The script submits an async task first, then polls for completion. As soon as the script outputs `Task submitted: {task_id}` (via stderr), extract the task_id and **immediately reply to the user** with the task_id before the polling completes. Also update `<sandbox-dir>/workspace/video_generation_status.json` to include the task_id:

```json
{
  "status": "running",
  "prompt": "the prompt text",
  "output_path": "<sandbox-dir>/outputs/{descriptive-name}.mp4",
  "reference_image": "<image URL>",
  "image_url": null,
  "video_url": null,
  "task_id": "<the extracted task_id>",
  "started_at": "<start timestamp>",
  "completed_at": null,
  "error": null
}
```

3. On success, the script outputs both the local path and the video URL. Extract the `Video URL: xxx` from the output and update the status file:

```json
{
  "status": "completed",
  "prompt": "the prompt text",
  "output_path": "<sandbox-dir>/outputs/{descriptive-name}.mp4",
  "reference_image": "<image URL>",
  "image_url": null,
  "video_url": "<the extracted video URL from script output>",
  "task_id": "<the task_id>",
  "started_at": "<start timestamp>",
  "completed_at": "<current ISO timestamp>",
  "error": null
}
```

4. On failure, update the status file:

```json
{
  "status": "failed",
  "prompt": "the prompt text",
  "output_path": null,
  "reference_image": "<image URL>",
  "image_url": null,
  "video_url": null,
  "task_id": "<the task_id or null>",
  "started_at": "<start timestamp>",
  "completed_at": "<current ISO timestamp>",
  "error": "<error message from script output>"
}
```

### Phase 4: Present Results

After the pipeline completes:

1. Present the generated video to the user using the appropriate presentation tool.
2. Then present the reference image.
3. Provide a brief description of the generation result.
4. If the pipeline failed at any phase, clearly explain what went wrong and offer to retry.

---

## Script Reference

### Volcengine Image Generation

**Script**: `./scripts/generate_volcengine_image.py`
**Model**: `doubao-seedream-4-5-251128` (default)

```bash
python ./scripts/generate_volcengine_image.py \
  --prompt "<prompt>" \
  --output-file <sandbox-dir>/outputs/output.png \
  --size 2K
```

Parameters:

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--prompt` | Yes | — | Text prompt for image generation |
| `--output-file` | Yes | — | Absolute path to save the generated image |
| `--model` | No | doubao-seedream-4-5-251128 | Volcengine Ark model identifier |
| `--size` | No | 2K | Image size (2K, 4K, or WxH format like 1024x1024) |
| `--num` | No | 1 | Number of images to generate (1-4) |
| `--seed` | No | — | Optional seed for reproducibility |

**Flow**: Synchronous API call → Download image(s) from returned URL(s) → Output local path and image URL.

### Volcengine Video Generation

**Script**: `./scripts/generate_volcengine_video.py`
**Model**: `doubao-seedance-1-5-pro-251215` (default)

```bash
python ./scripts/generate_volcengine_video.py \
  --prompt "<prompt>" \
  --reference-images <reference-image-path> \
  --output-file <sandbox-dir>/outputs/output.mp4 \
  --duration 5 \
  --ratio 16:9
```

Parameters:

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--prompt` | No* | — | Text prompt (use `--prompt-file` instead for file-based prompts) |
| `--prompt-file` | No* | — | Path to a text file containing the prompt |
| `--reference-images` | No | — | Paths to reference images or HTTP URLs (space-separated) |
| `--output-file` | Yes | — | Absolute path to save the generated video (.mp4) |
| `--model` | No | doubao-seedance-1-5-pro-251215 | Volcengine Ark model identifier |
| `--duration` | No | 5 | Video duration in seconds (5 or 10) |
| `--ratio` | No | 16:9 | Aspect ratio (16:9, 9:16, or 1:1) |
| `--generate-audio` | No | false | Generate audio for the video |

*One of `--prompt` or `--prompt-file` is required.

**Flow**: Submit async task → **Extract task_id from stderr output and reply to user immediately** → Poll status (5s interval) → Download video on completion → Output local path and video URL.

> Do NOT read the Python scripts. Just call them with the appropriate parameters.

---

## Image-Only Generation

If the user explicitly requests **only an image** (not a video), skip Phase 3 (video generation) and go directly to Phase 4 after image generation completes.

---

## Notes

- **Always use English for prompts** regardless of the user's language
- Detailed, descriptive prompts produce significantly better results
- Reference images enhance generation quality, especially for visual consistency
- Video generation is async and may take several minutes — inform the user about estimated wait time
- Volcengine Ark video/image URLs are temporary; files are automatically downloaded to the specified output path
- **Do NOT ask the user for confirmation before executing** — run the pipeline immediately when triggered
