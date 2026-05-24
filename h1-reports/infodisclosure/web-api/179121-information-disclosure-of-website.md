# Information Disclosure of Browsed URLs via Logcat in Brave Browser for Android

## Metadata
- **Source:** HackerOne
- **Report:** 179121 | https://hackerone.com/reports/179121
- **Submitted:** 2016-10-31
- **Reporter:** 1_1_1
- **Program:** Brave Browser
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Information Disclosure, Insufficient Data Protection, Insecure Logging, Local Information Leak
- **CVEs:** None
- **Category:** web-api

## Summary
Brave Browser for Android logs all visited URLs to the system logcat with debug-level verbosity, allowing any application with access to logcat (which is accessible to unprivileged apps on Android 4.4) to enumerate browsing history. This vulnerability exposes sensitive user activity without requiring elevated privileges or user interaction.

## Attack scenario
1. Attacker installs a malicious application on victim's Android device with READ_LOGS permission
2. Malicious app runs 'adb shell logcat' or uses Android's logging APIs to read system logs
3. App filters logs by Brave browser process ID to isolate browser-related messages
4. All visited URLs are extracted from debug-level log output in plain text
5. Attacker exfiltrates browsing history to remote server for analysis
6. Attacker gains complete visibility into victim's web browsing behavior without their knowledge

## Root cause
Brave Browser logs sensitive information (complete URLs with query parameters and navigation data) at DEBUG log level that gets written to system logcat. The application failed to: (1) restrict verbose logging in production builds, (2) implement access controls on log output, or (3) sanitize URLs before logging. On Android 4.4, logcat was readable by any application, making this a critical design flaw.

## Attacker mindset
An attacker would recognize that browser logging is often overlooked in security reviews. By targeting the system logging layer rather than the application's protected storage, they bypass application-level security controls. The attacker understands that debug logs are frequently left enabled in production and that many users run unpatched Android 4.4 devices where logcat is world-readable.

## Defensive takeaways
- Never log sensitive user data (URLs, credentials, tokens) regardless of log level
- Disable or minimize debug logging in production builds; use build variants to control verbosity
- Implement a privacy-aware logging policy that sanitizes or redacts sensitive data before logging
- Use ProGuard/R8 to strip debug logging calls from release APKs
- Store sensitive browsing history only in encrypted application-specific storage, never in system logs
- Implement log-level controls that respect user privacy settings
- Conduct regular security audits of all logging statements, especially in browser/privacy-focused apps
- Test on multiple Android versions to understand log accessibility differences

## Variant hunting
Check if other sensitive URLs or paths are logged (search URLs, visited domains, HTTP headers)
Test if authentication tokens, session IDs, or cookies appear in logcat
Verify if this affects other Brave versions or related browsers (Chromium variants)
Determine if HTTPS URLs with query parameters containing PII are logged
Check if WebSocket connections or private browsing mode URLs are also logged
Test accessibility on different Android versions where logcat permissions vary
Look for similar logging issues in other privacy-focused applications

## MITRE ATT&CK
- T1123 - Audio Capture (information gathering from logs)
- T1513 - System Information Discovery (discovering user activity via logs)
- T1414 - Gather Victim Device Information
- T1001.003 - Obfuscated Files or Information (URL logging without sanitization)

## Notes
This vulnerability is particularly severe for a privacy-focused browser like Brave, which explicitly markets privacy protection. The attack requires minimal privileges on Android 4.4 (where logcat is world-readable) but requires READ_LOGS permission on later versions. The reporter provided clear reproduction steps using standard ADB tools. This is a classic example of how security-critical applications can leak sensitive data through overlooked logging channels that bypass application-level security controls.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please fill all sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty.

## Summary:
Malicious application can see what the user is browsing
[add summary of the vulnerability]

## Products affected: 
BRave browser for android
 * operating system, Brave version or Brave website page, etc.
Android Version Os : 4.4, App version:1.9.56
## Steps To Reproduce:
1)Open adb shell
2)ps | grep "app process id"
3)logcat *:D | grep "process id of app"

YOu will see all the url that the user is browsing 

 * List the steps needed to reproduce the vulnerability

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)
http://www.androidsecurity.guru/category/logging/


</details>

---
*Analysed by Claude on 2026-05-24*
