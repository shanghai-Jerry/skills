---
name: skill-optimizer
description: "Dynamic workflow to optimize existing Agent Skills for better user experience, stability, and performance. Uses parallel agent orchestration for rapid diagnosis and implementation. Use when user wants to improve, optimize, refactor, or enhance an existing skill."
---

# Skill Optimizer

Dynamic workflow for optimizing Agent Skills with parallel agent orchestration. Adapts to the skill's problem profile and runs independent phases concurrently for speed.

## When to Use

- Skill is slow or times out
- Skill output quality doesn't match user expectations
- Skill fails intermittently (stability issues)
- Skill requires external APIs but should work without them
- Skill output is not editable/customizable
- User wants to enhance an existing skill

## Dynamic Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: SCOUT (parallel)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Read    │  │  Map     │  │  Profile │  │  User    │        │
│  │  Skill   │  │  Tools   │  │  Issues  │  │  Ask     │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       └──────────────┴──────────────┴──────────────┘             │
└─────────────────────────────┬───────────────────────────────────┘
                              ↓
┌─────────────────────────────┴───────────────────────────────────┐
│                    PHASE 2: DIAGNOSE (parallel)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │  Root    │  │  Tool    │  │  Pattern │                      │
│  │  Cause   │  │  Audit   │  │  Match   │                      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                      │
│       └──────────────┴──────────────┘                           │
└─────────────────────────────┬───────────────────────────────────┘
                              ↓
┌─────────────────────────────┴───────────────────────────────────┐
│                    PHASE 3: DESIGN (judge panel)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ Approach │  │ Approach │  │ Approach │                      │
│  │    A     │  │    B     │  │    C     │                      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                      │
│       └──────────────┼──────────────┘                           │
│                      ↓                                          │
│              ┌──────────────┐                                   │
│              │   Synthesize │                                   │
│              └──────────────┘                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              ↓
┌─────────────────────────────┴───────────────────────────────────┐
│                    PHASE 4: IMPLEMENT (pipeline)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Config  │→ │  Modules │→ │  Main    │→ │  SKILL   │        │
│  │  Files   │  │          │  │  Script  │  │  .md     │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              ↓
┌─────────────────────────────┴───────────────────────────────────┐
│                    PHASE 5: VERIFY (parallel)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │  Test    │  │  Compare │  │  User    │                      │
│  │  Paths   │  │  Metrics │  │  Review  │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: Full Dynamic Workflow (Recommended)

When you want comprehensive optimization with parallel diagnosis:

```
Use this skill to optimize the [skill-name] skill.
```

The workflow will:
1. Scout in parallel (4 agents)
2. Diagnose issues in parallel (3 agents)
3. Design solutions with judge panel (3 approaches)
4. Implement in pipeline
5. Verify with parallel tests

### Option 2: Targeted Optimization

When you know the specific problem:

```
Optimize [skill-name] for speed / stability / editability / API independence
```

The workflow will skip irrelevant diagnosis and focus on the target.

### Option 3: Quick Audit

When you just want analysis without implementation:

```
Audit [skill-name] and suggest optimizations
```

## Phase Details

### Phase 1: Scout (Parallel Agents)

Spawns 4 parallel agents to gather information simultaneously:

| Agent | Task | Output |
|-------|------|--------|
| **Reader** | Read SKILL.md, scripts, references | Skill structure map |
| **Tool Mapper** | Trace API calls, dependencies, file I/O | Tool chain diagram |
| **Issue Profiler** | Analyze error patterns, bottlenecks | Issue list with severity |
| **User Asker** | Ask user about pain points | User requirements |

```python
# Scout phase runs 4 agents in parallel
parallel(
    agent("Read skill structure", schema=SKILL_STRUCTURE),
    agent("Map tool chain", schema=TOOL_CHAIN),
    agent("Profile issues", schema=ISSUE_PROFILE),
    agent("Ask user about pain points", schema=USER_REQUIREMENTS)
)
```

**Duration:** ~30 seconds (parallel)
**Output:** Consolidated assessment report

### Phase 2: Diagnose (Parallel Analysis)

Spawns 3 parallel agents for root cause analysis:

| Agent | Task | Output |
|-------|------|--------|
| **Root Causer** | 5-Why analysis for each issue | Root causes |
| **Tool Auditor** | Evaluate tool alternatives | Tool recommendations |
| **Pattern Matcher** | Match issues to known solutions | Solution patterns |

```python
# Diagnose phase runs 3 agents in parallel
parallel(
    agent("Root cause analysis", schema=ROOT_CAUSES),
    agent("Tool audit and alternatives", schema=TOOL_AUDIT),
    agent("Match to optimization patterns", schema=PATTERN_MATCH)
)
```

**Duration:** ~30 seconds (parallel)
**Output:** Diagnosis report with root causes and patterns

### Phase 3: Design (Judge Panel)

Generates 3 independent solution approaches, then synthesizes:

```python
# Generate 3 approaches in parallel
approaches = parallel(
    agent("Design approach A: Focus on speed", schema=APPROACH),
    agent("Design approach B: Focus on editability", schema=APPROACH),
    agent("Design approach C: Focus on API independence", schema=APPROACH)
)

# Synthesize best elements
synthesis = agent(
    f"Synthesize the best elements from these 3 approaches: {approaches}",
    schema=SYNTHESIS
)
```

**Duration:** ~45 seconds (parallel generation + synthesis)
**Output:** Optimal architecture with rationale

### Phase 4: Implement (Pipeline)

Sequential implementation with checkpoints:

```python
pipeline(
    [
        {"name": "Create config files", "module": "config"},
        {"name": "Build core modules", "module": "modules"},
        {"name": "Create main orchestrator", "module": "main"},
        {"name": "Update SKILL.md", "module": "docs"}
    ],
    stage1=lambda item: implement(item),
    stage2=lambda result, item: validate_checkpoint(result, item)
)
```

**Duration:** ~2-5 minutes (depends on complexity)
**Output:** Working optimized skill

### Phase 5: Verify (Parallel Tests)

Runs multiple verification paths in parallel:

```python
parallel(
    agent("Test happy path + edge cases", schema=TEST_RESULTS),
    agent("Compare before/after metrics", schema=METRICS),
    agent("Review documentation completeness", schema=DOC_CHECK)
)
```

**Duration:** ~30 seconds (parallel)
**Output:** Validation report

## Problem Profiles

The workflow adapts based on detected problem profile:

### Speed Profile

**Symptoms:** Slow execution, timeouts, sequential bottlenecks
**Focus:** Parallel execution, caching, lazy loading
**Patterns:** Parallel, Pipeline, Checkpoint

### Stability Profile

**Symptoms:** Intermittent failures, API errors, crashes
**Focus:** Error handling, retry logic, fallbacks
**Patterns:** Retry with Backoff, Fallback Mode, Graceful Degradation

### Editability Profile

**Symptoms:** Output baked into images, can't modify
**Focus:** Separate layers, text overlays, modular output
**Patterns:** Layered Output, Text Overlay, Template System

### API Independence Profile

**Symptoms:** Fails without API key, hard dependency
**Focus:** Offline mode, local alternatives, graceful degradation
**Patterns:** Dual Mode, Template Fallback, Local Processing

### Quality Profile

**Symptoms:** Output doesn't match expectations, inconsistent
**Focus:** Style tokens, preview steps, user confirmation
**Patterns:** Style Tokens, Progressive Disclosure, Preview → Confirm

## Optimization Patterns

### Pattern 1: Dual Mode

Add optional API with local fallback:

```python
def execute(input, use_api=False):
    if use_api and os.getenv("API_KEY"):
        return api_mode(input)
    return template_mode(input)  # Always works
```

### Pattern 2: Style Tokens

Config-driven consistency:

```json
{
  "styles": {
    "style1": {
      "colors": ["#667eea", "#00d4ff"],
      "fonts": {"title": 44, "body": 18},
      "layouts": {...}
    }
  }
}
```

### Pattern 3: Parallel Execution

Concurrent independent operations:

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process, item) for item in items]
    results = [f.result() for f in as_completed(futures)]
```

### Pattern 4: Retry with Backoff

Resilient external calls:

```python
for attempt in range(MAX_RETRIES):
    try:
        return api_call()
    except Exception:
        if attempt < MAX_RETRIES - 1:
            time.sleep(2 ** attempt)
```

### Pattern 5: Progressive Disclosure

Preview before full generation:

```
1. Generate preview (1-2 items)
2. User confirms/adjusts
3. Generate remaining
```

### Pattern 6: Layered Output

Separate visual + text layers:

```
Background (image) + Text (editable) = Composite
```

## Example: Optimizing ppt-generation

### Input

```
Optimize ppt-generation skill
```

### Scout Phase (parallel)

| Agent | Finding |
|-------|---------|
| Reader | SKILL.md + 2 scripts, Gemini API dependency |
| Tool Mapper | Sequential: Gemini → python-pptx, ~15s/slide |
| Issue Profiler | Text not editable, requires API, 150s for 10 slides |
| User Asker | Wants editable text, no API dependency, faster |

### Diagnose Phase (parallel)

| Agent | Analysis |
|-------|----------|
| Root Causer | Text baked into images due to single-pass generation |
| Tool Auditor | Pillow can generate gradients locally, python-pptx adds text |
| Pattern Matcher | Matches: Dual Mode, Parallel, Layered Output |

### Design Phase (judge panel)

| Approach | Strategy |
|----------|----------|
| A (Speed) | Parallel background generation, skip text in images |
| B (Editability) | Separate background + text layers, PPTX text boxes |
| C (API Independence) | Pillow gradients + Gemini optional |

**Synthesis:** Combined B + C = Editable text + optional API backgrounds

### Implement Phase (pipeline)

1. Created `background.py` (Pillow gradients + Gemini fallback)
2. Created `layout.py` (percentage-based positioning)
3. Created `text_render.py` (PPTX text boxes)
4. Created `styles/` (5 token presets)
5. Rewrote `generate.py` (orchestrator)
6. Updated `SKILL.md`

### Verify Phase (parallel)

| Test | Result |
|------|--------|
| Happy path | ✓ Generates 10-slide PPTX in ~15s |
| No API | ✓ Works without GEMINI_API_KEY |
| Editable | ✓ Text is editable in PowerPoint |
| Speed | ✓ 150s → 15s (10x faster) |

### Output

```
ppt-generation optimized:
- 10x faster (parallel execution)
- Editable text (PPTX text boxes)
- No API required (Pillow gradients)
- 5 style presets (config-driven)
```

## Configuration

### Workflow Options

| Option | Default | Description |
|--------|---------|-------------|
| `target` | all | Target: speed, stability, editability, api_independence |
| `depth` | full | full, quick (skip design phase) |
| `parallel` | true | Run independent phases in parallel |
| `verify` | true | Run verification phase |

### Adaptation Rules

The workflow adapts based on detected issues:

| If detected | Then focus on |
|-------------|---------------|
| >50% time in API calls | Speed profile |
| >3 error types | Stability profile |
| Output is image-only | Editability profile |
| Hardcoded API key | API Independence profile |
| User mentions "quality" | Quality profile |

## Checklist

- [ ] Problem statement documented
- [ ] Root causes identified (5-Why)
- [ ] Architecture designed (judge panel)
- [ ] Config files created
- [ ] Core modules implemented
- [ ] Error handling added
- [ ] SKILL.md rewritten
- [ ] Before/after metrics compared
- [ ] All test scenarios passed
- [ ] User acceptance confirmed
