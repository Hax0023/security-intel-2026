# Improper Input Validation in Exported Deep-link Handler Causes FileDisplayActivity Crash (DoS)

## Metadata
- **Source:** HackerOne
- **Report:** 3399016 | https://hackerone.com/reports/3399016
- **Submitted:** 2025-10-24
- **Reporter:** khoof
- **Program:** Nextcloud Android Client (com.nextcloud.client)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Input Validation, Null Pointer Dereference, Exported Component Misuse, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
The FileDisplayActivity component exports a deep-link handler with wildcard host intent-filters that fails to validate external input or check for a valid user context before processing. This causes a null pointer dereference when onStart() attempts to call getAccountName() on a null User object, crashing the application.

## Attack scenario
1. Attacker crafts a malicious deep-link URL (e.g., https://attacker.example.com/f/abcdef) or embeds it in a malicious app
2. Attacker tricks user into clicking the link or installs an app that triggers the deep-link via intent
3. Android's intent router matches the URL against FileDisplayActivity's wildcard host intent-filter
4. Activity is launched without proper account context; no user is logged in or account validation skipped
5. onStart() executes and calls getCurrentUser().blockingGet() which returns null
6. Null User object causes NullPointerException when getAccountName() is invoked, crashing the app

## Root cause
FileDisplayActivity assumes a non-null User object exists when processing external deep-link intents without performing null checks or validating that account context is available. The exported component uses wildcard host matching in intent-filters, allowing any URL scheme to trigger the handler. Input validation and error handling are absent before accessing User interface methods.

## Attacker mindset
Attacker recognizes that exporting an activity with broad intent-filters and insufficient input validation creates a DoS vector. By crafting a simple external URL or embedding it in a malicious app, the attacker can reliably crash the Nextcloud client without user interaction beyond clicking a link. This degrades user experience and could be chained with social engineering for broader impact.

## Defensive takeaways
- Always null-check objects retrieved from dependency injection or blocking calls before dereferencing them
- Replace wildcard hosts in intent-filters with explicit allowlists of trusted domains only
- Validate and sanitize all intent data (uri, extras) at activity entry points before use
- Implement early-return or defensive guards if preconditions (e.g., logged-in user) are not met
- Log and gracefully handle missing context (e.g., no active account) instead of crashing
- Consider making deep-link handlers non-exported if they require authenticated context, or add runtime permission checks
- Use try-catch blocks around blocking operations or migrate to reactive patterns with proper error handling

## Variant hunting
Search for other exported activities that call getCurrentUser() or access account state without null checks
Audit all intent-filters using wildcard hosts or broad action/scheme patterns; validate inputs at all entry points
Check for similar null dereferences on User, Account, or Server objects in onCreate/onStart/onResume lifecycle methods
Identify other blocking calls (blockingGet, blockingFirst) that may return null if observable fails or completes empty
Review deep-link URI parsing for path traversal, injection, or malformed data handling
Test whether other crafted URLs can trigger authenticated requests to external hosts (SSRF risk mentioned in report)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (malicious deep-link delivery)
- T1499 - Endpoint Denial of Service (application crash via crafted input)
- T1204 - User Execution (social engineering to click malicious link)

## Notes
Report identifies medium severity DoS but hints at potential higher-impact variants (SSRF, authenticated fetches on other code paths) due to wildcard intent-filters. The null pointer dereference is straightforward to exploit and crash occurs consistently and early in onStart(). Remediation requires both null-safety fixes and architectural changes to intent-filter scope. The vulnerability is reproducible with a single adb shell command, making it trivial for malware or third-party apps to trigger.

## Full report
<details><summary>Expand</summary>

**Product / Package**
`com.nextcloud.client`

**Component**
`com.owncloud.android.ui.activity.FileDisplayActivity` (exported, multiple `VIEW` intent-filters with wildcard host)

**Severity**
Medium — Denial of Service (app crash). Potential for higher impact if authenticated fetch occurs on other codepaths.

**Summary**
Improper input validation of external deep-link data causes a null dereference in `FileDisplayActivity`. This results in an unhandled `NullPointerException` and application crash when the exported deep-link is invoked. An attacker-controlled link or malicious app can trigger this behavior.

**PoC (repro steps)**

1. On a device with the app installed:

```bash
adb shell am start -a android.intent.action.VIEW \
  -d "https://attacker.example.com/f/abcdef" \
  -n com.nextcloud.client/com.owncloud.android.ui.activity.FileDisplayActivity
```

2. Observe that the app crashes ("App has stopped").  And Show this logs.

**Observed logs (excerpt)**

```
Java

Exception in thread "main" java.lang.RuntimeException: Unable to start activity ComponentInfo{com.nextcloud.client/com.owncloud.android.ui.activity.FileDisplayActivity}: java.lang.NullPointerException: Attempt to invoke interface method 'java.lang.String com.nextcloud.client.account.User.getAccountName()' on a null object reference
    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2974)
    at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:3059)
    at android.app.ActivityThread.-wrap11(Unknown Source:0)
    at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1724)
    at android.os.Handler.dispatchMessage(Handler.java:106)
    at android.os.Looper.loop(Looper.java:164)
    at android.app.ActivityThread.main(ActivityThread.java:7000)
    at java.lang.reflect.Method.invoke(Native Method)
    at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:441)
    at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1408)
Caused by: Exception in thread "main" java.lang.NullPointerException: Attempt to invoke interface method 'java.lang.String com.nextcloud.client.account.User.getAccountName()' on a null object reference
    at com.owncloud.android.ui.activity.FileDisplayActivity.onStart(FileDisplayActivity.kt:2784)
    at android.app.Instrumentation.callActivityOnStart(Instrumentation.java:1342)
    at android.app.Activity.performStart(Activity.java:7278)
    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2937)
    at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:3059)
    at android.app.ActivityThread.-wrap11(Unknown Source:0)
    at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1724)
    at android.os.Handler.dispatchMessage(Handler.java:106)
    at android.os.Looper.loop(Looper.java:164)
    at android.app.ActivityThread.main(ActivityThread.java:7000)
    at java.lang.reflect.Method.invoke(Native Method)
    at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:441)
    at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1408)


### App information
* ID: com.nextcloud.client
* Version: 30340090
* Build flavor: generic

### Device information
* Brand: samsung
* Device: gtaxllte
* Model: Model
* Id: M1AJQ
* Product: gtaxlltexx

### Firmware
* SDK: 27
* Release: 8.1.0
* Incremental: Number
```

**Device / App details**

* App ID: `com.nextcloud.client`
* Version: 30340090 (reported)
* Device: Samsung SM-T585 (Android 8.1.0)


{F4930729}

**Impact**

* Any app or web link can trigger an exported deep-link handler which dereferences a null user object → application crash (Denial-of-Service).
* Because intent-filters allow wildcard hosts, there is additional risk that other crafted URLs could cause authenticated requests, SSRF, or content injection in other codepaths. (Not observed in this PoC — crash occurs early.)

**Root cause**
Improper input handling: the activity assumes a non-null `User` object when processing an external intent and does not validate inputs or the presence of account context before calling `getAccountName()`. This leads to improper error handling and application crash.

**Reproduction checklist**

* Reproducible on device with app installed.
* Command above reproduces crash consistently.
* Attach full `adb logcat -d` output for triage.

**Recommended remediation (developer text)**

1. **Null-check the current user before using it**:

```kotlin
val user = getCurrentUserProvider().getCurrentUser().blockingGet()
if (user == null) {
    Log.w(TAG, "Deep link received but no user logged in; ignoring deep link or prompting login")
    return
}
```

2. **Validate and sanitize deep-link input**: remove `host="*"` and use an explicit allowlist of domains. Validate `intent.data` and path patterns before processing.
3. **Avoid automatic authenticated fetches** of arbitrary external URLs. If fetch is required, only fetch from allowlisted hosts, do not forward user credentials to arbitrary domains, and prevent redirects to internal addresses (RFC1918 / link-local / metadata endpoints).
4. **Fail gracefully** on malformed/unexpected intents (log and return instead of throwing).


</details>

---
*Analysed by Claude on 2026-05-31*
