# Google Drive / Docs ↔ IDE setup

How agents in this repo should talk to Google Drive and Docs: through **Cursor’s Google Drive MCP plugin** (OAuth in the browser). No local Python scripts, no GCP project, no `client_secret.json`.

Official / product context:

- [Cursor MCP docs](https://cursor.com/docs/mcp) — Marketplace plugins install with OAuth
- Cursor Marketplace → **Google Drive** (also Gmail / Calendar under Google Workspace plugins)
- Google’s Workspace MCP endpoints are used by those plugins (Developer Preview; capabilities can change)

## Why MCP (not custom scripts)

| Approach | What the user does |
|----------|--------------------|
| **Google Drive MCP (this guide)** | Install plugin → Connect → log into Google once |
| Local OAuth CLIs / Desktop client | Create a GCP project, OAuth client, embed secrets, run venv scripts |

For design-ai-fuel, prefer MCP so anyone who clones only signs into their own Google account.

## Cursor (preferred path)

1. Open **Cursor Settings → Tools & MCP** (or **Customize** / Marketplace).
2. Install the **Google Drive** plugin (Google Workspace).
3. Click **Connect** next to Google Drive and finish the browser Google login / Allow access flow.
4. Confirm the server shows as connected (not “needs auth”).

Optional related plugins if a skill needs them: **Gmail**, **Google Calendar** — same Connect + OAuth pattern.

## How agents should use it here

Once Google Drive MCP is connected:

1. Ask the agent to create, search, read, or share Drive/Docs files in plain language.
2. Prefer MCP tools over inventing local scripts.
3. Created files live in **the signed-in user’s** Google Drive.
4. If a tool is missing or auth fails, reconnect under **Tools & MCP** (Google’s preview servers evolve).

## Quick verify

In chat:

```text
Using Google Drive MCP, create a short Google Doc titled "design-ai-fuel smoke test" with one paragraph of placeholder text, then give me the link.
```

If Cursor prompts to authenticate, complete Connect / Allow access, then retry.

## If MCP cannot create Docs in your build

Some preview builds expose read/search more reliably than create. If create is unavailable:

1. Reconnect the Google Drive plugin and check the consent scopes include Drive write access.
2. Update Cursor / reinstall the plugin from the Marketplace.
3. As a last resort, create the Doc in the Google UI and use MCP to read/update/share it.

Do **not** fall back to custom GCP OAuth scripts in this repo — keep setup MCP-only.
