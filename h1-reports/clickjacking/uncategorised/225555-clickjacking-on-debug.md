# Clickjacking on Debug Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 225555 | https://hackerone.com/reports/225555
- **Submitted:** 2017-05-02
- **Reporter:** bf7e43565d8cf54de3bc5a7
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, Missing X-Frame-Options Header, UI Redressing
- **CVEs:** None
- **Category:** uncategorised

## Summary
The debug.weblate.org endpoint is vulnerable to clickjacking attacks due to missing X-Frame-Options and Content-Security-Policy headers. An attacker can embed the page in an iframe and trick users into clicking on transparent overlay buttons, potentially redirecting them to malicious sites or performing unintended actions.

## Attack scenario
1. Attacker creates a malicious HTML page with an invisible iframe containing debug.weblate.org
2. Attacker overlays transparent clickable elements on top of the framed page, disguising them as legitimate buttons
3. Victim visits the attacker's malicious website unknowingly
4. When victim clicks what appears to be a normal button, they actually interact with hidden elements on the framed debug page
5. Victim is redirected to attacker-controlled domain (MaliciousSite.com) or performs unintended actions on debug.weblate.org
6. Sensitive information or state changes could occur depending on what actions are clickable

## Root cause
The debug.weblate.org endpoint lacks proper HTTP security headers (X-Frame-Options: DENY or SAMEORIGIN, and Content-Security-Policy frame-ancestors directive) that would prevent the page from being embedded in iframes on external domains.

## Attacker mindset
An attacker with moderate capability could exploit this to redirect users to phishing sites, steal credentials through social engineering, or perform actions on behalf of logged-in users. The attacker recognizes that restricted/debug endpoints often have weaker security implementations and targets users who may have legitimate access.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN headers on all endpoints, especially administrative/debug pages
- Deploy Content-Security-Policy header with frame-ancestors directive to prevent framing
- Apply clickjacking protections universally rather than only on production endpoints
- Include frame-busting JavaScript code as defense-in-depth measure
- Regularly audit security headers across all subdomains and endpoints
- Implement stricter access controls and security measures on debug/development endpoints exposed publicly

## Variant hunting
Check for other subdomains (staging.weblate.org, admin.weblate.org, api.weblate.org) for similar header vulnerabilities
Test endpoints with different HTTP methods to find clickjacking-vulnerable state-changing operations
Look for confirmation dialogs that can be obscured and clicked through
Investigate if other Weblate instances or similar applications share this vulnerability pattern
Test for combined vulnerabilities (clickjacking + CSRF) for maximum impact

## MITRE ATT&CK
- T1189 - Drive-by Compromise (via malicious attacker page)
- T1566 - Phishing (email with malicious link)
- T1598 - Phishing for Information
- T1187 - Forced Authentication

## Notes
The writeup is minimal and lacks technical depth. The reference to 'report #225543' suggests related vulnerabilities. The mention of 'user report to CIA' is unclear (may be grammatical error). The actual POC HTML file referenced was uploaded but not shown in this writeup. Debug endpoints require equivalent or higher security than production due to potential information disclosure risks.

## Full report
<details><summary>Expand</summary>

#Proof Of Concept:

Related Issue on report #225543

 1. Navigate to https://debug.weblate.org
 2. As you notice it is forbidden.
 3. just vulnerable by clickjacking.
 3. Now the user report to CIA to open.
 4. Redirect to MaliciousSite.com

I uploaded the poc.html 

Thanks,

</details>

---
*Analysed by Claude on 2026-05-24*
