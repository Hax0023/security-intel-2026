# Browser cross-site scripting filter misconfiguration

## Metadata
- **Source:** HackerOne
- **Report:** 12454 | https://hackerone.com/reports/12454
- **Submitted:** 2014-05-18
- **Reporter:** yourdarkshadow
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
Issue detail :-
No X-XSS-Protection header was set in the response. This means that the browser uses default behaviour that detection of a cross-site scripting attack never prevents rendering.

Remediation detail
The following header should be set:

X-XSS-Protection: 1; mode=block

Issue background :-
Cross-site scripting (XSS) filters in browsers check if the URL contains possible harmfu

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Issue detail :-
No X-XSS-Protection header was set in the response. This means that the browser uses default behaviour that detection of a cross-site scripting attack never prevents rendering.

Remediation detail
The following header should be set:

X-XSS-Protection: 1; mode=block

Issue background :-
Cross-site scripting (XSS) filters in browsers check if the URL contains possible harmful XSS payloads and if they are reflected in the response page. If such a condition is recognized, the injected code is changed in a way, that it is not executed anymore to prevent a succesful XSS attack. The downside of these filters is, that the browser has no possibility to distinguish between code fragments which were reflected by a vulnerable web application in an XSS attack and these which are already present on the page. In the past, these filters were used by attackers to deactivate JavaScript code on the attacked web page. Sometimes the XSS filters itself are vulnerable in a way, that web applications which were protected properly against XSS attacks became vulnerable under certain conditions.

Remediation background :-
It is considered as better practice to instruct the browser XSS filter to never render the web page if an XSS attack is detected.

</details>

---
*Analysed by Claude on 2026-05-24*
