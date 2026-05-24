# Clickjacking lead to remove review

## Metadata
- **Source:** HackerOne
- **Report:** 965141 | https://hackerone.com/reports/965141
- **Submitted:** 2020-08-23
- **Reporter:** mralaayousef
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** clickjacking, UI redressing, missing X-Frame-Options header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application is vulnerable to clickjacking attacks, allowing an attacker to trick users into removing reviews through a transparent iframe overlay. The absence of proper X-Frame-Options headers and clickjacking protections enables UI redressing attacks that can deceive users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious webpage and embeds the vulnerable review removal page in a transparent iframe
2. Attacker overlays a fake interactive element (button, link) on top of the iframe that visually appears harmless
3. User visits the attacker's page and interacts with what appears to be a legitimate element
4. The user's click is actually directed to the hidden iframe, triggering the review removal action
5. Since the user is authenticated to the target application, the review removal request succeeds without user awareness
6. The attacker successfully removes reviews using the victim's authenticated session

## Root cause
The application fails to implement clickjacking defenses: missing X-Frame-Options header, lack of frame-busting JavaScript, and absence of Content-Security-Policy directives that would prevent embedding the application in iframes from different origins.

## Attacker mindset
An attacker seeks to manipulate user interactions without explicit consent, leveraging the victim's existing authentication to perform destructive actions (review removal). This could be motivated by reputation management, competitive advantage, or malicious content moderation.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN headers to prevent framing
- Deploy Content-Security-Policy with frame-ancestors directive restricting embedding
- Add frame-busting JavaScript code as a secondary defense mechanism
- Require explicit user confirmation (CSRF token + additional action verification) for destructive operations like review deletion
- Implement SameSite cookie attributes to limit cross-site request scenarios
- Use visual security indicators when performing sensitive actions

## Variant hunting
Check other review/comment removal endpoints for similar clickjacking vulnerabilities
Test user profile editing, account deletion, and permission changes for clickjacking
Examine all state-changing operations (POST/PUT/DELETE) for missing clickjacking defenses
Test X-Frame-Options bypass techniques and CSP policy weaknesses
Verify clickjacking protections across different endpoints and user roles

## MITRE ATT&CK
- T1190
- T1566

## Notes
Clickjacking is often overlooked despite being a critical UI-based attack vector. The vulnerability's impact is significant because it leverages user trust and existing authentication. The fix is straightforward (adding headers) but must be comprehensive across all sensitive endpoints. The report demonstrates importance of testing framing protections as part of security assessment.

## Full report
<details><summary>Expand</summary>

## Steps To Reproduce:

  1. Open iframe {F960017}
  2. You can remove reviews from this iframe

## Impact

Clickjacking  lead to remove reviews

</details>

---
*Analysed by Claude on 2026-05-24*
