# Web prototype

## When to use
Greenfield or isolated web spike. In an existing web app, reuse that stack instead.

## Default stack
**Vite + React + TypeScript + shadcn/ui + Tailwind**

Why: quick dev server, solid component primitives, agents iterate on UI fast without framework ceremony.

This is the single place to change the web greenfield default. `SKILL.md` points here — keep the default explicit and one line.

## Confirm before scaffolding
Propose the default above (or the user's named alternative). One or two sentences of why is enough. Wait for yes/no.

## Scaffold (after confirm)
1. Create the Vite React-TS app in the agreed directory.
2. Add Tailwind + shadcn per current shadcn Vite docs (don't invent outdated steps from memory — check docs if unsure).
3. Verify `dev` starts.

## First screen (only if scoped)
- One primary view that makes the product idea obvious.
- Fake data in-module or a tiny mock; no API layer.
- Prefer existing design-system pieces if this lives inside a larger monorepo/app.

## Stop
Hand back: how to run, what was mocked, and one suggested next step. If they need to share a demo, offering a minimal static/preview host is a fine optional next step — don't start publish/setup unless they ask.
