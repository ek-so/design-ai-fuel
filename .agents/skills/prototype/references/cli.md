# CLI prototype

## When to use
Developer/ops workflows, scripts, or the product *is* a command-line tool.

## Advise a stack

| Goal | Suggest | Why |
|------|---------|-----|
| Quick scriptable tool in a JS/TS repo | **Node + TypeScript** (e.g. `tsx` / small bin entry) | Matches most agent and web repos |
| Python-heavy environment / data | **Python + argparse or typer** | Natural fit for data/ML contexts |
| Single static binary later | Prototype in TS/Python first; Rust/Go only if that's the point |

Push back if they ask for a full TUI framework before a single command that prints useful output.

## Confirm before scaffolding
Recommendation + why; wait for yes/no.

## Scaffold (after confirm)
- One entry command, `--help`, and a happy-path invocation.
- No plugin system, config layers, or installers unless asked.

## First "screen" (only if scoped)
- One command path that demonstrates the idea (stdin/args → clear stdout).
- Fake/sample input fixtures instead of live integrations.

## Stop
Exact command to run, sample input used, one next step (flags, second command, or real I/O).
