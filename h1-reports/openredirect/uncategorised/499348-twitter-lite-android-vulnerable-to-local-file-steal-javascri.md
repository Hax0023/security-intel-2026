# Twitter Lite Android: Local File Theft, JavaScript Injection, and Open Redirect via Exported Activity

## Metadata
- **Source:** HackerOne
- **Report:** 499348 | https://hackerone.com/reports/499348
- **Submitted:** 2019-02-21
- **Reporter:** rahulkankrale
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Exported Component, Intent Data Validation Failure, Local File Access, JavaScript Injection, Open Redirect, Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** uncategorised

## Summary
The TwitterLiteActivity component in Twitter Lite Android is exported without proper intent data validation, allowing external applications to pass arbitrary URIs including file://, javascript://, and malicious HTTP schemes. This enables attackers to steal local files, inject JavaScript code for session token theft, and perform open redirects without user awareness.

## Attack scenario
1. Attacker creates a malicious Android application that requests the device to communicate with the exported TwitterLiteActivity component
2. Attacker crafts an intent with a data URI pointing to a local file path (file:///sdcard/sensitive_data.html) or JavaScript payload
3. The vulnerable activity processes the intent without validating the URI scheme or content
4. JavaScript injection payload executes within the Twitter Lite WebView context, gaining access to sensitive data and authentication tokens
5. Alternatively, attacker passes a javascript:// or malicious HTTP URI causing code execution or redirect to phishing site
6. User's local files are accessed, authentication tokens are exfiltrated, or user is silently redirected to malicious domain

## Root cause
The TwitterLiteActivity component is exported (accessible to other apps) but lacks input validation on the data URI passed through intents. The activity directly processes URIs without whitelisting allowed schemes or validating their safety before loading them in a WebView context.

## Attacker mindset
An attacker would target this vulnerability to create a seemingly innocent app that silently communicates with Twitter Lite to exfiltrate user credentials, steal session tokens, or access sensitive local files without user consent. The ability to inject JavaScript in the Twitter Lite context is particularly valuable for token theft and session hijacking.

## Defensive takeaways
- Never export Android components unless absolutely necessary; if export is required, implement strict input validation
- Validate and whitelist all URI schemes accepted by activities that handle external intents (e.g., only http/https, reject file://, javascript://, etc.)
- Implement URI scheme validation before loading content in WebView or native components
- Use intent-filter restrictions and explicit component targeting instead of relying on exported components
- Sanitize and validate all intent data, including URI parameters and paths, against a whitelist of allowed patterns
- Apply proper Content Security Policy (CSP) headers and disable JavaScript execution when not required
- Use Android's SafeBrowsingHelper and implement URL validation against malicious redirects

## Variant hunting
Check for other exported Activities in Twitter Lite and other Twitter Android apps that might process URIs without validation
Search for exported Services or Broadcast Receivers that accept and process external data
Test other URL schemes (content://, data://, tel://, custom schemes) against the vulnerable activity
Examine WebView configurations for JavaScript enablement and bridge exposure in exported components
Look for similar patterns in other mobile apps that process deep links or custom URI schemes

## MITRE ATT&CK
- T1203
- T1204
- T1190
- T1563
- T1187
- T1566

## Notes
This vulnerability affects the Android manifest's component export configuration combined with WebView data handling. The ability to inject JavaScript in the Twitter Lite context is particularly critical as it could allow attackers to access authentication tokens, user data, and perform unauthorized actions on behalf of the user. The vulnerability requires either an attacker app or user interaction to trigger the malicious intent. POC video was provided demonstrating all three attack vectors.

## Full report
<details><summary>Expand</summary>

**Summary:** com.twitter.android.lite.TwitterLiteActivity is set to exported and doesn't validate data pass to intent due to which this activity vulnerable to steal users local files, javascript injection and open redirect.

**Description:** com.twitter.android.lite.TwitterLiteActivity is set to exported so external app can communicate with it.
As this activity doesn't validate data pass through intent critical uri like javascript and file so malicious app can steal users files as well as inject javascript.
It can leads to many issue like UXSS, Token steal, etc.

## Steps To Reproduce:

  1. To reproduce we use ADB tool

  2. To reproduce local file access use: adb shell am start -n com.twitter.android.lite/com.twitter.android.lite.TwitterLiteActivity -d "file:///sdcard/BugBounty/1.html"

  3. To reproduce javascript injection: adb shell am start -n com.twitter.android.lite/com.twitter.android.lite.TwitterLiteActivity -d "javascript://example.com%0A alert(1);"

  4. To reproduce open redirect: adb shell am start -n com.twitter.android.lite/com.twitter.android.lite.TwitterLiteActivity -d "http://evilzone.org"

 * Video of POC attached.

Thanks

## Impact

As critical uri like javascript & file is not being validate malicious app can steal users session token, users files etc.

</details>

---
*Analysed by Claude on 2026-05-24*
