<p align="center">
  <img src="assets/cover.png" alt="design-ai-fuel cover" width="100%" />
</p>

# design-ai-fuel

Shared agent skills for product designers and product people to make any AI agent more efficient.

## How to use

You can copy `AGENTS.md` and `.agents/` into your project root (merge with any existing `.agents/skills/` you already have) or you can fork the repo and open it alongside other projects in your workspace.

**Skills** — each folder under `.agents/skills/` is one skill. Invoke with `/skill-name`, or describe a matching task and let the agent pick it up from the skill description.

**AGENTS.md** — directional rules for how agents should behave.

**Utils** — `.agents/_utils/` holds setup guides for external tools:
- [Figma](.agents/_utils/figma/) — official Figma MCP
- [Google](.agents/_utils/google/) — Cursor Google Drive MCP (Docs / Drive via Google login)