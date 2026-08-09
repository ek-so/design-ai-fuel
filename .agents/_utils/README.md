# `_utils` — shared tooling for skills

Toolkits that skills (and agents) can call. Each integration lives in its own folder.

| Folder | Purpose |
|--------|---------|
| [`google/`](google/) | Google Docs, Sheets, Slides, Drive CLIs |

## Google Workspace

```bash
.agents/_utils/google/setup.sh
# Place OAuth Desktop client at ~/.design-ai-fuel/client_secret.json
# See google/README.md for Google Cloud Console steps
source .agents/_utils/google/activate.sh
```

```bash
python .agents/_utils/google/gdocs.py create --title "Brief" --from notes.md --open
python .agents/_utils/google/gsheets.py create --title "Data" --from data.csv --open
python .agents/_utils/google/gslides.py create --title "Review" --from outline.md --open
python .agents/_utils/google/gdrive.py search "design brief"
```

Full command list: [`google/README.md`](google/README.md).
