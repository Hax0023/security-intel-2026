# Session Information Disclosure via Browser Back Button

## Metadata
- **Source:** HackerOne
- **Report:** 13939 | https://hackerone.com/reports/13939
- **Submitted:** 2014-05-29
- **Reporter:** niks
- **Program:** Simplenote
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Session Management, Information Disclosure, Client-side Caching
- **CVEs:** None
- **Category:** web-api

## Summary
After logging out from Simplenote, users could press the browser back button to view previously authenticated session data and access sensitive information. This occurs because the application fails to properly invalidate cached pages and verify session validity before rendering content.

## Attack scenario
1. Attacker logs into their legitimate Simplenote account
2. Attacker clicks the logout button to terminate their session
3. Attacker immediately clicks the browser back button
4. Browser serves cached version of the authenticated page from local cache
5. Attacker can now view sensitive note content without an active session
6. Attacker gains unauthorized access to application data despite logout

## Root cause
The application does not set appropriate HTTP cache-control headers (no-cache, no-store, must-revalidate) on authenticated pages, allowing the browser to serve cached content even after session termination. Additionally, there is no client-side session validation or authentication check before rendering protected content on page load.

## Attacker mindset
An opportunistic attacker using the browser back button to exploit predictable caching behavior. This represents a low-effort attack requiring no technical sophistication—just knowledge of basic browser functionality. Attackers targeting shared computers or public terminals would find this particularly valuable.

## Defensive takeaways
- Implement strict HTTP cache-control headers on all authenticated pages: Cache-Control: no-cache, no-store, must-revalidate, Pragma: no-cache, Expires: 0
- Validate session token/authentication status on every page load before rendering sensitive content
- Redirect unauthenticated users to login page immediately if session is invalid or missing
- Implement onunload or beforeunload handlers to clear sensitive data from memory
- Consider using anti-caching techniques specific to sensitive pages (e.g., cache busting with timestamps)
- Test logout flow with browser back/forward navigation regularly
- Use secure session tokens with proper expiration and invalidation mechanisms

## Variant hunting
Check if forward button also exposes cached sessions
Test if browser history can be accessed to view previous authenticated states
Verify if other logout mechanisms (timeout-based, session kill) have similar issues
Check if sensitive data persists in browser storage (localStorage, sessionStorage) after logout
Test on different browsers and versions for inconsistent cache behavior
Examine if pages containing PII or sensitive notes are specifically vulnerable
Test if tab restoration/session restore features expose authenticated content

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
This is a classic web application vulnerability from the early 2010s. The writeup is straightforward and reproducible. The fix is well-understood but often overlooked by developers. This type of vulnerability is particularly impactful on shared computers or public terminals. The reporter provided clear reproduction steps and a reasonable remediation suggestion.

## Full report
<details><summary>Expand</summary>

Use Google chrome  35.0.1916.114m for reproduction  
1. go to https://app.simplenote.com/
2. login into the app.
3. Now press logout, and press back button on browser. You will see the session back.This is the information disclosure vulnerability.

I recommend checking for a valid, authenticated session and if there isn't one redirect to the login page.

</details>

---
*Analysed by Claude on 2026-05-24*
