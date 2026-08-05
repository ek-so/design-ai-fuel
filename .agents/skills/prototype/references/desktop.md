# Desktop prototype

## When to use
Windowed app, OS menus/files, or "works offline as an installable app" matters more than a URL.

## Advise a stack

| Goal | Suggest | Why |
|------|---------|-----|
| Web-like UI, cross-platform, fastest demo | **Electron** or **Tauri + web UI** | Reuse web skills; Tauri if smaller footprint matters |
| Mac-only native | **SwiftUI** | Better OS integration than wrapping a browser |
| Already a web Vite app to wrap | Wrap later — **prototype UI in Vite first** | Avoid Electron ceremony until the UI idea works |

Push back if they want Electron "just to try a layout" — a Vite web prototype is usually enough first.

## Confirm before scaffolding
Recommendation + why; wait for yes/no.

## Scaffold (after confirm)
Keep the shell thin: one window, no auto-updater, no installer polish. Prefer official templates for Electron/Tauri/SwiftUI.

## First screen (only if scoped)
- One primary window/view.
- Fake data; local mock state is fine.
- Skip code signing and distribution.

## Stop
How to run locally, what's mocked, one next step (e.g. file open, tray, packaging).
