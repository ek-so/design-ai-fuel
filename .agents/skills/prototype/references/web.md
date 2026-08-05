# Web prototype

## When to use
Greenfield or isolated web spike. In an existing web app, reuse that stack instead.

## Default
**Vite + React + TypeScript + shadcn/ui + Tailwind**

Why: quick dev server, solid component primitives, agents iterate on UI fast without framework ceremony.

## Confirm before scaffolding
Propose the default (or the user's named alternative). Wait for yes/no.

## Scaffold (after confirm)
1. Create the Vite React-TS app in the agreed directory.
2. Add Tailwind + shadcn per current shadcn Vite docs (don't invent outdated steps from memory — check docs if unsure).
3. Verify `dev` starts.

## First screen (only if scoped)
- One primary view that makes the product idea obvious.
- Fake data in-module or a tiny mock; no API layer.
- Prefer existing design-system pieces if this lives inside a larger monorepo/app.

## Stop
Hand back: how to run, what was mocked, and one suggested next step.
