# skills

A curated Claude Code marketplace of 32+ Agent Skills for AI-assisted development.

## Installation

Add this marketplace to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "extraKnownMarketplaces": {
    "skills-most-common-used": {
      "source": {
        "source": "git",
        "url": "https://github.com/shanghai-Jerry/skills-most-common-used.git"
      }
    }
  }
}
```

Then enable individual plugins via the Claude Code marketplace UI or by adding them to `enabledPlugins`:

```json
{
  "enabledPlugins": {
    "superpowers@skills-most-common-used": true,
    "content-generation@skills-most-common-used": true,
    "research-analysis@skills-most-common-used": true,
    "design-deploy@skills-most-common-used": true,
    "skill-development@skills-most-common-used": true,
    "extras@skills-most-common-used": true
  }
}
```

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| **superpowers** | 12 | Core dev workflow: planning, TDD, debugging, code review, git |
| **content-generation** | 5 | Images, video, podcasts, presentations, charts |
| **research-analysis** | 5 | Web research, GitHub analysis, data analysis, reports |
| **design-deploy** | 3 | Frontend design, web audit, Vercel deployment |
| **skill-development** | 4 | Create/evaluate skills, onboarding, discovery |
| **extras** | 3 | Brainstorming, Mac setup, creative surprises |

### superpowers

Core development workflow skills based on [obra/superpowers](https://github.com/obra/superpowers):

- **using-superpowers** - Meta-skill for skill discovery
- **writing-plans** - Create implementation plans
- **executing-plans** - Execute written plans
- **test-driven-development** - TDD workflow
- **systematic-debugging** - Bug investigation
- **requesting-code-review** - Request code review
- **receiving-code-review** - Handle review feedback
- **verification-before-completion** - Verify before claiming done
- **finishing-a-development-branch** - Branch integration
- **using-git-worktrees** - Workspace isolation
- **dispatching-parallel-agents** - Parallel task execution
- **subagent-driven-development** - Implementation with subagents

### content-generation

Media and content creation skills:

- **image-generation** - AI image generation
- **video-generation** - AI video generation
- **podcast-generation** - Audio podcast from text
- **ppt-generation** - PowerPoint presentations
- **chart-visualization** - Data visualization charts

### research-analysis

Research and data analysis skills:

- **deep-research** - Web research methodology
- **github-deep-research** - GitHub repo deep analysis
- **data-analysis** - Excel/CSV data analysis with DuckDB
- **consulting-analysis** - Consulting-grade reports
- **claude-to-deerflow** - DeerFlow AI platform integration

### design-deploy

Frontend design and deployment skills:

- **frontend-design** - Production-grade UI creation
- **web-design-guidelines** - UI audit and compliance
- **vercel-deploy-claimable** - Vercel deployment

### skill-development

Tools for creating and managing skills:

- **skill-creator** - Create/modify/evaluate skills
- **writing-skills** - Write effective skills
- **find-skills** - Discover installable skills
- **bootstrap** - Onboard AI partner identity

### extras

Miscellaneous skills:

- **brainstorming** - Pre-implementation design
- **surprise-me** - Creative showcase
- **mac-setup** - Mac development environment setup

## Credits

- 14 skills from [obra/superpowers](https://github.com/obra/superpowers)
- 18 original skills by shanghai-Jerry
- MIT License
