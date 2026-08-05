---
name: prototype
description: Guide prototyping from idea to a scoped first build. Use whenever the user wants a prototype, MVP mock, clickable demo, spike, or "just something to try" — including vague asks like "let's build a quick version" or "can we mock this up". Prefer this skill over jumping straight into scaffolding. Covers web, mobile, desktop, and CLI; works for greenfield and existing repos.
---

# Prototype

Help the user go from an idea to a **scoped** prototype without overbuilding. Intake and stack choice matter more than clever scaffolding — a wrong platform or a too-big first turn wastes more time than a slow setup.

## Workflow

Follow these steps in order. Ask one decision at a time when something is missing. If the user's message already answered a step, don't re-ask — confirm briefly and move on.

### 1. Intent first

Clarify **what** we're prototyping and **who it's for** (even one sentence). If the idea is already clear from the request, restate it in a line and proceed.

Do not scaffold yet.

### 2. Platform and stack

If the user hasn't specified a platform, **advise one** that fits the product — don't only ask blankly. If they named a platform that fights the idea (e.g. native iOS for a content site meant for sharing links), **push back once** with a better fit and why, then let them decide.

**Greenfield defaults** — read the matching playbook, propose its default stack (short why), wait for yes/no:

| Platform | Playbook |
|----------|----------|
| Typical web app | `references/web.md` |
| iOS / Android | `references/mobile.md` |
| Desktop | `references/desktop.md` |
| CLI | `references/cli.md` |

Stack defaults live in those files so they can change without editing this workflow. For web, use whatever `references/web.md` names as the default unless the user already picked another stack.

**Existing repo:** Prefer the project's existing stack, design system, and patterns. Only use a greenfield default from the playbooks when starting a new app or an isolated spike outside the main UI.

Read the matching file under `references/` once the platform is agreed (or while advising, if you need the default stack).

### 3. Scope this turn

Ask explicitly:

- **Scaffold only** — project/bootstrapping, then stop
- **Scaffold + one first screen** — recommended when the idea is clear enough to draw one UI

Default recommendation: scaffold + one first screen. Do not add more screens, real auth, APIs, or persistence in this turn unless the user asks.

### 4. Build only what was agreed

- **Fidelity default:** UI-only with fake/mock data. No real backend unless requested.
- Reuse existing components and tokens when in a repo that has them.
- After finishing the agreed scope, stop and offer a sensible next step (another screen, wiring, or polish) — don't silently continue.

## Principles

- **Ask before expanding.** Extra features feel helpful and usually aren't for a first prototype.
- **Advise, don't only interview.** Users often want a recommendation more than a menu.
- **Push back on bad platform fits** once, with an alternative — then respect the choice.
- **One composition at a time.** First screen should show the product idea, not a dashboard of everything.

## Out of scope for this skill

Production hardening, full design systems from scratch, multi-platform parity in one go, or shipping/release pipelines — unless the user explicitly pivots there.
