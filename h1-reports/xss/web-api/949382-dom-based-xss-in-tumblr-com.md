# DOM-Based XSS in tumblr.com /reblog endpoint via Insufficient CSP

## Metadata
- **Source:** HackerOne
- **Report:** 949382 | https://hackerone.com/reports/949382
- **Submitted:** 2020-08-01
- **Reporter:** keer0k
- **Program:** Tumblr
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-Based XSS, Improper Content Security Policy
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists on Tumblr's /reblog endpoint due to insufficient Content Security Policy rules, allowing attackers to execute arbitrary JavaScript in the victim's browser context. The vulnerability is similar to a previously reported issue (#882546) but exploits weaker CSP enforcement on the specific reblog page.

## Attack scenario
1. Attacker crafts a malicious URL targeting the /reblog/ID/OTHER_ID endpoint containing JavaScript payload in a clickable element or parameter
2. Attacker distributes the malicious URL via social engineering, direct message, or embeds it in a seemingly legitimate reblog
3. Victim visits the URL and interacts with the page (clicks the 'click me' button)
4. DOM manipulation code processes user-controlled input and renders it without proper sanitization
5. JavaScript payload executes in the victim's browser within the Tumblr.com origin
6. Attacker gains access to victim's account, session cookies, or can perform actions on their behalf

## Root cause
The /reblog page endpoint implements an overly permissive or missing Content Security Policy that fails to prevent inline script execution. User-controlled data from URL parameters or DOM manipulation is rendered without proper sanitization or escaping, allowing injected JavaScript to execute.

## Attacker mindset
Opportunistic vulnerability hunter identifying similar patterns from previously disclosed issues and testing if weaker CSP policies exist on related endpoints. The attacker understands that different pages on the same domain may have varying security controls.

## Defensive takeaways
- Implement strict, consistent CSP headers across all endpoints with 'script-src' directive limiting scripts to specific sources only
- Sanitize and validate all user-controlled input before DOM insertion using context-aware encoding
- Use safe DOM manipulation APIs (textContent instead of innerHTML) when handling user data
- Conduct security audits across similar endpoints to identify inconsistent security policies
- Apply input validation and output encoding consistently across the application
- Implement automated CSP testing in CI/CD pipeline to detect regressions

## Variant hunting
Test other reblog-related endpoints (/reblog/*, /reblog/?, /reblog/*/*) for similar CSP weaknesses
Check other Tumblr pages with user-generated content or dynamic routing for insufficient CSP
Examine URL parameters and hash-based routing on reblog pages for XSS vectors
Test interaction flows (click, hover, form submission) that trigger DOM updates
Look for similar issues on related endpoints (#882546 reference suggests this is a pattern)

## MITRE ATT&CK
- T1190
- T1566

## Notes
Report references a previous issue (#882546) indicating this is a recurring vulnerability class on Tumblr. The specific mention of CSP insufficiency suggests the fix from the previous report was not comprehensively applied across all similar endpoints. The attack requires user interaction (clicking elements), reducing severity slightly from reflected/stored XSS. Session-based account compromise is a critical impact requiring immediate remediation.

## Full report
<details><summary>Expand</summary>

# Description

Hi, i would like to report DOM-Based XSS that it's exactly like this one #882546, this one work just because  the page /reblog/ID/OTHER_ID doesn't have a correct CSP rule.

# Steps to reproduce
1. go to `https://www.tumblr.com/reblog/620008931446652928/JBuEvzz5`
2. click in `click me`
3. click in open
4. XSS will be triggered

## Impact

it is possible to perform malicious actions on the victim's account

</details>

---
*Analysed by Claude on 2026-05-12*
