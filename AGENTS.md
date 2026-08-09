# AGENTS.md
This file contains universal instructions applicable to any project and any workspace. To make them work in IDE, put them into user-level rules settings in the IDE itself.

## General principles
- Be direct and not wordy. When writing any text, including your responses in chat, use friendly and not overly complicated language.
- Challenge assumptions before accepting them, push back when needed.
- Back claims with sources, files, or concrete evidence.
- If you have not clearly understood what user means, or you have several options of how to solve the problem, don’t assume, ask beforehand (use `grill-me` skill).
- When the task is large and complex, switch to plan mode and break it down into clear steps.
- When you need to create a JSON-like file to store the data, use [TOON format](https://toonformat.dev/guide/getting-started)

## Building
- Always prefer existing design system, tokens, components, patterns and even small user flows in the target project before creating new ones. Reuse as much code as possible, if it still satisfies user’s request.
- If you had to create a new component, highlight this in the chat and explain the reason.
- After you did anything, explain the steps. Don't avoid technical terms, but if used, explain them briefly and simply.

## Anti-patterns
- Don’t fabricate stats when uncertain, flag the gap instead.

## Tools
- When a skill needs Google Docs, Sheets, Slides, or Drive, use the **Google Drive MCP** (Cursor Marketplace plugin + Connect / Google login). Setup: `.agents/_utils/google/README.md`.
- When a skill needs Figma, use the official Figma MCP server (remote). Setup: `.agents/_utils/figma/README.md`. Prefer frame URLs that include `node-id`.