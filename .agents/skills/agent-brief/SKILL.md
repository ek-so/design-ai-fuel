---
name: agent-brief
description: Compact the current conversation into a brief so another agent can pick up the work.
---

# Agent Brief

- Write a brief that summarizes this conversation so a fresh agent can continue the work.
- Output it in chat as a single copy-pasteable prompt — do not save it to any file or directory.
- Include a "suggested skills" section listing skills the next agent should invoke.
- Do not repeat content already in specs, plans, ADRs, issues, commits, or diffs — link by path or URL instead.
- Redact secrets and PII (API keys, passwords, personal data).
- If the user states a focus for the next session, shape the brief around that.
