# Reflected XSS Vulnerability in linkpop.com User Profile

## Metadata
- **Source:** HackerOne
- **Report:** 1569940 | https://hackerone.com/reports/1569940
- **Submitted:** 2022-05-13
- **Reporter:** nagli
- **Program:** linkpop.com (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in linkpop.com that allows attackers to inject arbitrary JavaScript code through user profile URLs. The vulnerability appears to have resurfaced after changes were made to the linkpop feature, indicating incomplete patching of a previously identified issue.

## Attack scenario
1. Attacker identifies that linkpop.com accepts unsanitized input in URL parameters or user profile pages
2. Attacker crafts a malicious URL containing JavaScript payload (e.g., testnaglinagli profile with XSS payload)
3. Attacker sends the crafted URL to a victim via social engineering, email, or forum post
4. Victim clicks the malicious link and visits the vulnerable linkpop.com page
5. Attacker's JavaScript executes in the victim's browser with their session privileges
6. Attacker can steal session cookies, perform actions as the victim, or redirect to phishing sites

## Root cause
Insufficient input sanitization and output encoding of user-supplied data in profile pages. Recent code changes may have removed previous XSS protections or introduced new reflection points without proper validation.

## Attacker mindset
Opportunistic researcher identifying that a previously patched vulnerability has regressed. Demonstrates persistence in vulnerability hunting and awareness that code changes can reintroduce old security issues.

## Defensive takeaways
- Implement comprehensive input validation and output encoding on all user-controlled inputs
- Use security-focused templating engines with automatic escaping enabled by default
- Maintain regression testing suite that includes previously identified XSS test cases
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Conduct security review of all recent code changes, especially those touching user profile or display logic
- Implement automated security scanning in CI/CD pipeline to catch XSS before deployment

## Variant hunting
Search for similar reflection points in other linkpop features, user bio sections, custom link descriptions, and any user-generated content display areas. Check for DOM-based XSS in JavaScript that processes profile data.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application

## Notes
This is a minimal report with limited technical details. The researcher provided a URL exhibiting the vulnerability but no payload or proof of concept. The mention of 'seems to work again' strongly suggests this is a regression of a previously reported and supposedly patched vulnerability, indicating inadequate version control, testing, or code review processes during the recent changes to linkpop.

## Full report
<details><summary>Expand</summary>

## Summary

My XSS seems to work again at

https://linkpop.com/testnaglinagli

Best Regards

@nagli

## Impact

XSS

</details>

---
*Analysed by Claude on 2026-05-12*
