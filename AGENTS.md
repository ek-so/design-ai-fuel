# AGENTS.md

Project guidance for AI agents working in this repo or consuming its skills.

## Purpose

**design-ai-fuel** is a shared skill pack for product designers and product people who build with AI coding agents. Prefer skills under `.agents/skills/` over ad-hoc one-off prompts.

## Working style

- Be direct. No fluff.
- Challenge assumptions before accepting them; push back when needed.
- Back claims with sources, files, or concrete evidence.
- Prefer existing components, tokens, and patterns in the target project before inventing new ones.

## Skills

Skills live in `.agents/skills/<skill-name>/SKILL.md`.

| Skill | When to use |
|-------|-------------|
| `presentation` | Creating, structuring, or writing a presentation, deck, or talk |

Invoke with `/presentation` or by describing a matching task. The agent loads the skill when the description matches.

## Adding a skill

1. Create `.agents/skills/<skill-name>/SKILL.md`
2. Add YAML frontmatter with `name` and `description`
3. Write methodology, steps, and a quality checklist in the body
4. Keep one domain per skill
