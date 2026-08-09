# Figma ↔ IDE setup

How agents in this repo should talk to Figma today: through the **Figma MCP server** (Model Context Protocol), not a local REST-token script pack.

Official sources:

- [Set up the remote server (recommended)](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)
- [Cursor and Figma: Set up the MCP server](https://help.figma.com/hc/en-us/articles/39889260656407-Cursor-and-Figma-Set-up-the-MCP-server)
- [VS Code and Figma: Set up the MCP server](https://help.figma.com/hc/en-us/articles/39890361040535-VS-Code-and-Figma-Set-up-the-MCP-server)
- [Guide to the Figma MCP server](https://developers.figma.com/docs/figma-mcp-server/)

## Prefer remote MCP

Figma ships two servers:

| Server | When to use |
|--------|-------------|
| **Remote** (`https://mcp.figma.com/mcp`) | Default. Broadest features; no desktop app required; OAuth in the browser |
| **Desktop** (`http://127.0.0.1:3845/mcp`) | Niche org/enterprise cases; needs the Figma desktop app + Dev Mode toggle |

Figma’s docs recommend **remote** for almost everyone.

## Cursor (preferred path)

1. In agent chat, run:

   ```text
   /add-plugin figma
   ```

   That installs Figma’s Cursor plugin: MCP config, workflow skills, and asset-handling rules.

2. Open **Cursor Settings → Tools & MCP**.
3. Next to **Figma**, click **Connect** and finish the browser OAuth “Allow access” flow.

Manual alternative (same remote endpoint): add a global MCP server pointing at `https://mcp.figma.com/mcp`, then Connect / OAuth. Details: [remote server installation → Cursor](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/).

## Other IDEs (short)

| Client | Preferred setup |
|--------|-----------------|
| **VS Code** | MCP HTTP server at `https://mcp.figma.com/mcp` (GitHub Copilot required per Figma’s VS Code guide) |
| **Claude Code** | `claude plugin install figma@claude-plugins-official`, then authenticate via `/mcp` |
| **Codex** | Install the Figma plugin in the Codex app, or `codex mcp add figma --url https://mcp.figma.com/mcp` |

## How agents should use it here

Once MCP is connected:

1. Pass a Figma **frame or layer URL that includes `node-id`** (copy link from Figma).
2. Prefer design-context tools (e.g. `get_design_context`) over guessing from screenshots alone.
3. For design → code, load the Figma skills the plugin ships (design-to-code, Code Connect, etc.) before calling write/generate tools.
4. Treat MCP output as a **reference** to adapt to the target project’s components and tokens — not paste-as-final code.

## Quick verify

Ask in chat:

```text
Who am I in Figma MCP, and list available Figma tools?
```

Then paste a real frame URL with `node-id` and ask for design context.

## Desktop MCP (only if you need it)

1. Figma desktop app → Design file → Dev Mode → enable MCP in the sidebar → copy URL.
2. Point the IDE at `http://127.0.0.1:3845/mcp`.

Skip this unless remote MCP is blocked in your environment; remote stays the default.
