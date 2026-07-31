---
name: agent-brief
description: Compact the current conversation into a brief so another agent can pick up the work.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Agent Brief

- Write a brief that summarizes this conversation so a fresh agent can continue the work.
- Save it to the OS temp directory — not the current workspace.
- Include a "suggested skills" section listing skills the next agent should invoke.
- Do not repeat content already in specs, plans, ADRs, issues, commits, or diffs — link by path or URL instead.
- Redact secrets and PII (API keys, passwords, personal data).
- If the user passed arguments, treat them as the next session's focus and shape the brief around that.
