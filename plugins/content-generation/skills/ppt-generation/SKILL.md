---
name: ppt-generation
description: "Generate professional PowerPoint presentations with editable text. Creates gradient backgrounds (no API needed) or AI-generated backgrounds (with Gemini API), overlays styled text with multiple layout options. Use when user asks for PPT, presentation, slides, slideshow, or slide deck."
---

# PPT Generation Skill

## Overview

Generate professional PowerPoint presentations with **editable text overlays**. Supports two modes:

- **Template Mode** (no API): Pillow-generated gradient backgrounds, instant
- **API Mode** (with GEMINI_API_KEY): Gemini-generated custom backgrounds, richer visuals

**Key Features:**
- Editable text (not baked into images)
- 5 style presets with consistent design tokens
- 6 layout types (title, content, two-column, etc.)
- Parallel background generation for speed
- Retry logic for stability

## Architecture

```
ppt-generation/
├── SKILL.md                      ← You are here
└── scripts/
    ├── generate.py               ← Main orchestrator
    ├── background.py             ← Background generation (template + API)
    ├── layout.py                 ← Layout engine (percentage → inches)
    ├── text_render.py            ← Text overlay (fonts, colors, bullets)
    └── styles/
        ├── glassmorphism.json    ← Purple-cyan gradient
        ├── dark-premium.json     ← Black + glow
        ├── gradient-modern.json  ← Warm gradient
        ├── minimal-light.json    ← Clean light
        └── vibrant.json          ← Bold multi-color
```

## Quick Start

### Step 1: Create Presentation Plan

Create a JSON file with your presentation structure:

```json
{
  "title": "My Presentation",
  "style": "glassmorphism",
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Main Title",
      "subtitle": "Subtitle or tagline",
      "layout": "title_center"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Key Features",
      "key_points": [
        "Feature one with details",
        "Feature two with details",
        "Feature three with details"
      ],
      "layout": "content"
    }
  ]
}
```

### Step 2: Generate Presentation

```bash
python ./scripts/generate.py \
  --plan-file /path/to/plan.json \
  --output-file /path/to/output.pptx \
  --style glassmorphism
```

**Options:**
- `--style STYLE`: Override plan's style (glassmorphism|dark-premium|gradient-modern|minimal-light|vibrant)
- `--use-api`: Use Gemini API for backgrounds (requires GEMINI_API_KEY)
- `--preview N`: Only generate first N slides
- `--list-styles`: Show available styles

## Workflow

### Step 1: Understand Requirements

When user requests PPT generation, ask:

1. **Topic**: What is the presentation about?
2. **Slides**: How many slides? (default: 5-8)
3. **Style**: Which visual style? (recommend based on topic)
4. **Content**: Key points for each slide

### Step 2: Style Recommendation

Based on topic, recommend 2 styles:

| Topic | Recommended Styles |
|-------|-------------------|
| Tech product / AI / SaaS | glassmorphism, gradient-modern |
| Executive / premium | dark-premium, minimal-light |
| Startup / brand launch | gradient-modern, vibrant |
| Consulting / academic | minimal-light |
| Marketing / creative | vibrant, gradient-modern |

Show style descriptions and let user choose.

### Step 3: Create Plan

Generate the JSON plan with:

```json
{
  "title": "Presentation Title",
  "style": "glassmorphism",
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Main Title",
      "subtitle": "Tagline",
      "layout": "title_center"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Slide Title",
      "key_points": ["Point 1", "Point 2", "Point 3"],
      "layout": "content"
    }
  ]
}
```

**Layout auto-assignment:**
- `type: "title"` → `layout: "title_center"`
- `type: "content"` → `layout: "content"`
- `type: "section"` → `layout: "section_divider"`
- `type: "two_column"` → `layout: "two_column"`

### Step 4: Generate

```bash
# Template mode (fast, no API)
python ./scripts/generate.py \
  --plan-file plan.json \
  --output-file presentation.pptx

# API mode (richer backgrounds)
python ./scripts/generate.py \
  --plan-file plan.json \
  --output-file presentation.pptx \
  --use-api

# Preview first 3 slides
python ./scripts/generate.py \
  --plan-file plan.json \
  --output-file preview.pptx \
  --preview 3
```

### Step 5: Review & Iterate

After generation:
1. Show the PPTX to user
2. Ask for feedback
3. Modify specific slides if needed
4. Re-generate only changed slides

## Style Tokens Reference

Each style defines: background, text, card, and layouts.

### glassmorphism
- **Background**: Purple (#667eea) → Cyan (#00d4ff) diagonal gradient
- **Text**: White, bold titles, subtle shadows
- **Card**: Frosted glass effect (semi-transparent white)
- **Best for**: Tech products, AI/SaaS, futuristic pitches

### dark-premium
- **Background**: Black (#0a0a0a) → Dark navy (#1a1a2e) vertical gradient
- **Text**: White with cyan glow on titles
- **Card**: Dark with cyan border (optional)
- **Best for**: Premium products, executive presentations

### gradient-modern
- **Background**: Purple (#7c3aed) → Pink (#ec4899) → Orange (#f97316) mesh
- **Text**: White, extra bold titles
- **Card**: Semi-transparent with rounded corners
- **Best for**: Startups, creative agencies, brand launches

### minimal-light
- **Background**: Light gray (#f5f5f5) → Gray (#e8e8e8) vertical gradient
- **Text**: Dark gray (#1a1a1a), clean typography
- **Card**: White with subtle border
- **Best for**: Consulting, academic, formal reports

### vibrant
- **Background**: Pink (#f43f5e) → Purple (#8b5cf6) → Cyan (#06b6d4) mesh
- **Text**: White, bold with yellow bullets
- **Card**: Semi-transparent with white border
- **Best for**: Marketing, social media, creative campaigns

## Layout Types

| Layout | Use Case | Regions |
|--------|----------|---------|
| `title_center` | Title slide, centered | title, subtitle |
| `title_left` | Title slide, left-aligned | title, subtitle |
| `content` | Standard content slide | title, body |
| `two_column` | Split content | title, left, right |
| `section_divider` | Chapter break | title, subtitle |
| `image_text` | Image + text (placeholder) | title, image, text |

## API Mode Setup

If you want richer AI-generated backgrounds:

1. Get a Gemini API key from https://aistudio.google.com/apikey
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
3. Use `--use-api` flag when generating

**Note:** Template mode works perfectly without any API key.

## Complete Example

User request: "Create a 5-slide presentation about our AI product launch"

### Plan

```json
{
  "title": "Nova AI Launch",
  "style": "glassmorphism",
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Introducing Nova AI",
      "subtitle": "Intelligence, Reimagined",
      "layout": "title_center"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Why Nova?",
      "key_points": [
        "10x faster processing",
        "Human-like understanding",
        "Enterprise-grade security"
      ],
      "layout": "content"
    },
    {
      "slide_number": 3,
      "type": "two_column",
      "title": "Key Features",
      "key_points": [
        "Natural language input",
        "Multi-modal processing",
        "Real-time insights",
        "Seamless integration",
        "99.9% uptime",
        "Global deployment"
      ],
      "layout": "two_column"
    },
    {
      "slide_number": 4,
      "type": "content",
      "title": "Built for Scale",
      "key_points": [
        "1M+ concurrent users",
        "99.99% uptime SLA",
        "Global CDN infrastructure"
      ],
      "layout": "content"
    },
    {
      "slide_number": 5,
      "type": "section",
      "title": "Get Started Today",
      "subtitle": "nova-ai.com",
      "layout": "section_divider"
    }
  ]
}
```

### Generate

```bash
python ./scripts/generate.py \
  --plan-file nova-plan.json \
  --output-file nova-presentation.pptx \
  --style glassmorphism
```

## Notes

### Quality Guidelines

**Text Content:**
- Keep titles short (5-8 words)
- Limit key points to 3-5 per slide
- Use parallel structure in bullet points
- Avoid walls of text

**Layout Selection:**
- Title slides: Use `title_center` or `title_left`
- Content slides: Use `content` or `two_column`
- Section breaks: Use `section_divider`
- When unsure, use `content`

**Style Consistency:**
- All slides use the same style (defined in plan)
- Style tokens ensure consistent colors, fonts, spacing
- No need for reference images between slides

### Performance

| Mode | 10-slide time | Notes |
|------|---------------|-------|
| Template (parallel) | ~15s | Recommended default |
| Template (sequential) | ~30s | Use `--no-parallel` |
| API (parallel) | ~50s | Requires GEMINI_API_KEY |

### Troubleshooting

**Issue: Text overlapping**
- Check layout regions in style JSON
- Reduce text content or use different layout

**Issue: Background not生成**
- Check Pillow is installed: `pip install Pillow`
- For API mode, verify GEMINI_API_KEY is set

**Issue: Wrong style applied**
- Use `--list-styles` to see available options
- Ensure style name matches exactly (case-sensitive)
