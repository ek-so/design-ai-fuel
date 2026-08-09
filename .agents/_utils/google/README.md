# Google Workspace tools

OAuth-based CLIs for Docs, Sheets, Slides, and Drive.

All local runtime data lives **outside the repo** in `~/.design-ai-fuel/`:

| Path | Purpose |
|------|---------|
| `~/.design-ai-fuel/.venv` | Python virtualenv |
| `~/.design-ai-fuel/output/` | Drafts and exports |
| `~/.design-ai-fuel/client_secret.json` | Your GCP OAuth Desktop client |
| `~/.design-ai-fuel/token.json` | Cached user OAuth token |

Optional env overrides: `DESIGN_AI_FUEL_HOME`, `GOOGLE_CLIENT_SECRETS`, `GOOGLE_TOKEN`.

## 1. Create a Google Cloud OAuth client

1. Open [Google Cloud Console](https://console.cloud.google.com/) and create (or pick) a project.
2. Enable APIs: **Google Drive**, **Google Docs**, **Google Sheets**, **Google Slides**.
3. **APIs & Services → OAuth consent screen**: choose External (or Internal for Workspace). Add yourself as a test user if the app is in Testing.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - Application type: **Desktop app**
   - Download the JSON and save it as:
     `~/.design-ai-fuel/client_secret.json`

## 2. Install Python deps

From the design-ai-fuel repo root:

```bash
.agents/_utils/google/setup.sh
source .agents/_utils/google/activate.sh
```

## 3. First-time authentication

Any CLI opens a browser once for consent (Drive + Docs + Sheets + Slides):

```bash
source .agents/_utils/google/activate.sh
python .agents/_utils/google/gdocs.py create --title "Hello" --open
```

## CLIs

Activate the venv first (`source .agents/_utils/google/activate.sh`).

### Docs — `gdocs.py`

```bash
python .agents/_utils/google/gdocs.py create --title "Brief" --from notes.md --open
python .agents/_utils/google/gdocs.py read "DOC_URL"
python .agents/_utils/google/gdocs.py update "DOC_URL" --from notes.md --mode replace
python .agents/_utils/google/gdocs.py export "DOC_URL" --format md   # also: pdf, docx
```

### Sheets — `gsheets.py`

```bash
python .agents/_utils/google/gsheets.py create --title "Data" --from data.csv --open
python .agents/_utils/google/gsheets.py read "SHEET_URL" --out data.csv
python .agents/_utils/google/gsheets.py update "SHEET_URL" --from data.csv --range A1
python .agents/_utils/google/gsheets.py export "SHEET_URL" --out data.csv
```

### Slides — `gslides.py`

Outline markdown: `# Slide title` plus `- bullet` lines (or a JSON list of `{title, bullets}`).

```bash
python .agents/_utils/google/gslides.py create --title "Review" --from outline.md --open
python .agents/_utils/google/gslides.py read "SLIDES_URL"
python .agents/_utils/google/gslides.py export "SLIDES_URL" --format pdf   # also: pptx
```

### Drive — `gdrive.py`

```bash
python .agents/_utils/google/gdrive.py search "design brief"
python .agents/_utils/google/gdrive.py share "FILE_URL" --email someone@example.com --role reader
python .agents/_utils/google/gdrive.py share "FILE_URL" --anyone
python .agents/_utils/google/gdrive.py mkdir --title "Project folder" --open
python .agents/_utils/google/gdrive.py move "FILE_URL" --folder "FOLDER_ID"
```

Commands that create or mutate files print `kind` / `id` / `url` lines for chaining.

## Layout

| Path | Role |
|------|------|
| `config.py`, `auth.py`, `bootstrap.py`, `cli_common.py` | Shared OAuth and CLI helpers |
| `setup.sh`, `activate.sh`, `requirements.txt` | Venv install |
| `lib/` | Docs / Sheets / Slides / Drive API helpers |
| `gdocs.py`, `gsheets.py`, `gslides.py`, `gdrive.py` | CLIs |
