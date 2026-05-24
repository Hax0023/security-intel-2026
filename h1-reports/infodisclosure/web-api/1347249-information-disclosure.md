# Information Disclosure via Privileged URIs in Tor Session

## Metadata
- **Source:** HackerOne
- **Report:** 1347249 | https://hackerone.com/reports/1347249
- **Submitted:** 2021-09-21
- **Reporter:** kkarfalcon
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Privilege Escalation, URI Scheme Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
Brave Browser fails to properly restrict access to certain privileged URIs (chrome://downloads, brave://inspect/#devices, brave://device-log/) when using Tor, allowing sensitive information disclosure within the Tor session. While Brave correctly blocks access to chrome://wallet and chrome://history in Tor by redirecting to a normal session, it inconsistently allows access to debugging and log URIs that should not be accessible within anonymized Tor sessions.

## Attack scenario
1. Attacker uses Brave Browser with Tor enabled for anonymous browsing
2. Attacker navigates to brave://inspect/#devices or chrome://downloads within the Tor session
3. Privileged URI loads within the Tor session instead of triggering redirect to normal Brave session
4. If UXSS vulnerability exists on these pages, attacker can exfiltrate sensitive data (download history, device information, logs) over Tor
5. Device logs and debugging information leak into the Tor session, potentially revealing local network topology
6. Attacker gains unintended access to personal information that should be isolated from Tor

## Root cause
Inconsistent URI scheme validation and filtering logic in Brave. While chrome://history and chrome://wallet are properly blocked/redirected in Tor sessions, the blocking logic fails to include chrome://downloads, brave://inspect/#devices, and brave://device-log/. These privileged URIs are accessible within Tor when they should trigger a redirect to a normal session.

## Attacker mindset
An attacker leverages Brave's oversight in restricting privileged URIs to gain information about the victim's system while maintaining Tor anonymity. Combined with potential UXSS vulnerabilities, this provides a vector to exfiltrate sensitive data (downloads, device logs, debugging info) through the supposedly isolated Tor environment.

## Defensive takeaways
- Implement centralized URI scheme validation that applies consistently across all chrome:// and brave:// privileged URIs
- Maintain an explicit allowlist of URIs that can be accessed in Tor mode; default-deny all privileged URIs
- Redirect all debugging, logging, and device inspection URIs to normal sessions when accessed from Tor
- Regular security audit of URI handling to catch inconsistencies in filtering logic
- Add integration tests verifying that new privileged URIs respect Tor session restrictions
- Implement URI validation at browser initialization and navigation events
- Consider hardening UXSS protections on all privileged pages as defense-in-depth

## Variant hunting
Enumerate other brave:// and chrome:// URIs not yet tested for Tor bypass (brave://settings, brave://extensions, etc.)
Test data: URIs and blob: URIs in Tor mode for similar bypasses
Check if extensions can register privileged schemes that bypass Tor restrictions
Investigate whether chrome://blob and chrome://sandbox expose information in Tor
Test file:// URI access in Tor with different path traversal techniques
Look for other debugging interfaces (DevTools, Inspector) accessible in Tor

## MITRE ATT&CK
- T1020 - Automated Exfiltration
- T1005 - Data from Local System
- T1113 - Screen Capture
- T1213 - Data from Information Repositories

## Notes
Report demonstrates good security research methodology by identifying inconsistent security controls. Brave's selective blocking of privileged URIs suggests framework exists but implementation is incomplete. The mention of potential UXSS on these pages elevates severity if combined with this bypass. Reporter appropriately suggests remediation aligned with existing Brave patterns (redirect to normal session). No evidence of actual exploitation with UXSS provided, keeping impact to information disclosure category.

## Full report
<details><summary>Expand</summary>

Vulnerability tested on:- Brave	1.29.81 Chromium: 93.0.4577.82 (Official Build) (64-bit)
Vulnerability description:- For security measures and for privacy purposes, Brave has the ability to open a normal tab of the Brave when we navigate to: `chrome://wallet`, `chrome://history` etc. due to the reason that Tor should be blocking privileged URIs like `file:///`, `chrome://` etc. When we open local storage URIs or the Data URIs, it is blocking. So, we can say that TOR in Brave protects users from opening anything privileged in the browser.
But there is some weird case for: `chrome://downloads` and `brave://inspect/#devices`. Both can be dangerous when there is a UXSS present there because it can get to know about the data. The `brave://device-log/` looks interesting too, why do we see the device log of brave in the TOR Network in the Brave? 

Steps to reproduce:
1. Open Brave with TOR
2. Navigate to `brave://inspect/#devices`

Expected behavior?
--> When we are doing device debugging, it should have opened normal Brave and shouldn't open the privileged URI in the TOR session itself. Open `chrome://bookmarks` and `chrome://history`

Actual behavior?
--> It opens the debugging session inside the protected tor session.

Suggestions?
--> We should block `chrome://downloads`,  `brave://inspect/#devices`, `brave://device-log/` etc. and when somebody tries to navigate to those URIs, a normal Brave session should be started like we do for `chrome://history` as it keeps TOR away from personal information inside the brave URIs.

## Impact

Information disclosure.

</details>

---
*Analysed by Claude on 2026-05-24*
