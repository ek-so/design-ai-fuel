"""OAuth desktop flow with token cache under ~/.design-ai-fuel/."""

from __future__ import annotations

import sys
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import CLIENT_SECRETS, SCOPES, TOKEN_PATH, ensure_home


def get_credentials() -> Credentials:
    """Load or refresh credentials; open browser on first run."""
    ensure_home()
    creds: Credentials | None = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        return creds

    if not CLIENT_SECRETS.exists():
        print(
            "Missing OAuth client secrets.\n"
            f"  Expected: {CLIENT_SECRETS}\n"
            "Create a Desktop OAuth client in Google Cloud Console, download "
            "client_secret.json, and place it there.\n"
            "See .agents/_utils/google/README.md for steps.",
            file=sys.stderr,
        )
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def build_service(api: str, version: str) -> Any:
    """Build an authenticated Google API service client."""
    from googleapiclient.discovery import build

    return build(api, version, credentials=get_credentials(), cache_discovery=False)
