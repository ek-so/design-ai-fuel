<p align="center">
  <img src="assets/cover.png" alt="design-ai-fuel cover" width="100%" />
</p>

# design-ai-fuel

Shared agent skills for product designers and product people who build with Cursor (and other agents that read `AGENTS.md` / `.agents/skills`).

## Layout

```text
AGENTS.md                 # Project agent guidance
.agents/
  skills/
    presentation/
      SKILL.md            # Presentation dramaturgy skill
assets/
  cover.png
```

## What's inside

### `AGENTS.md`
How agents should behave in this project: tone, evidence standards, and how skills are organized.

### Skills (`.agents/skills/`)
Domain methodology agents load automatically or via `/skill-name`.

| Skill | Description |
|-------|-------------|
| `presentation` | Kapterev dramaturgy — brief, slide content, speaker notes, quality checklist |

## How to use

1. Clone this repo
2. Copy `AGENTS.md` and `.agents/` into your project root (merge with any existing `.agents/skills/` you already have)

> **Can't see the `.agents/` folder?** Folders starting with `.` are hidden by default. On Mac, press `⇧⌘.` (Shift + Cmd + dot) in Finder to reveal them.

**Skills** — invoke with `/presentation`, or describe a matching task and let the agent pick it up from the skill description.
