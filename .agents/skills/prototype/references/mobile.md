# Mobile prototype (iOS / Android)

## When to use
Touch-first product, device APIs matter, or the user explicitly wants mobile.

## Advise a stack
Ask (or infer) whether they need **one codebase** or **native per platform**.

| Goal | Suggest | Why |
|------|---------|-----|
| Both platforms, UI-heavy, fast demo | **React Native (Expo)** | Shared JS/TS, quick preview, agents already strong at RN patterns |
| iOS-only, native feel | **SwiftUI** | Best fit for Apple-only prototypes |
| Android-only | **Jetpack Compose** | Best fit for Android-only prototypes |
| Heavy native modules / existing native app | Stay native or add a thin RN screen — don't rewrite |

Push back if they ask for dual native apps "for a quick prototype" when Expo would get a demo faster — unless native is the point of the spike.

## Confirm before scaffolding
State the recommendation + why. Wait for yes/no.

## Scaffold (after confirm)
- **Expo:** create app with the current Expo template, run on simulator/web preview as available.
- **SwiftUI / Compose:** Xcode or Android Studio project template; keep structure minimal (one screen target).

## First screen (only if scoped)
- One flow that shows the mobile-specific value (gestures, list, camera placeholder, etc.).
- Fake data; stub device permissions with placeholders unless the spike *is* the device API.

## Stop
How to run on simulator/device, what's mocked, one next step.
