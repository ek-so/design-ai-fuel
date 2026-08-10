---
name: code-review
description: >-
  Senior-engineer review of a codebase for structure, reuse, and long-term
  maintainability. Use when the user asks for a code review, architecture
  cleanup, component reuse check, or sustainability pass on a project.
disable-model-invocation: true
---

# Code Review

Review the target project as a senior engineer building a durable system. Prefer evidence from the codebase over speculation.

## Scope

Ask which path or app to review if unclear. Stay inside that boundary.

## Look for

- **Structure** — clear boundaries, sensible folder layout, coupling/duplication
- **Reuse** — repeated UI/logic that should be shared; dead or near-duplicate components
- **Reliability** — error handling, edge cases, brittle paths, missing types
- **Sustainability** — naming, consistency with existing patterns, hard-to-change spots
- **Tech debt** — leftovers, unused assets, one-off hacks, config/script clutter

Skip style nits unless they hurt clarity or consistency. Don't invent a rewrite.

## Output

1. **Verdict** — 1–2 sentences on overall health
2. **Findings** — grouped by severity (`must fix` / `should fix` / `nice to have`), each with a concrete file/path and why it matters
3. **Reuse opportunities** — specific candidates to extract or consolidate
4. **Suggested next steps** — short, ordered cleanup list (no drive-by refactors unless asked)
