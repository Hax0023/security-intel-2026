# Inadequate Access Controls in Vote Functionality - Unauthorized Voting on Reports

## Metadata
- **Source:** HackerOne
- **Report:** 137503 | https://hackerone.com/reports/137503
- **Submitted:** 2016-05-10
- **Reporter:** apok
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Client-Side Validation Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HackerOne's voting feature on the Hacktivity page lacked server-side access controls, allowing unauthorized users to vote on reports by sending POST requests to /reports/[Report_ID]/votes and delete votes via DELETE requests to /reports/[Report_ID]/votes/[VOTE_ID]. The vulnerability was discovered through client-side control manipulation (removing 'disabled' attributes and modifying JSON values), indicating reliance on client-side validation alone.

## Attack scenario
1. Attacker identifies the vote functionality on HackerOne's Hacktivity page is disabled in the UI
2. Attacker removes HTML 'disabled' attributes from vote buttons and modifies JSON boolean values from false to true using browser developer tools
3. Vote buttons become functional in the client-side interface
4. Attacker clicks vote button, which sends POST request to /reports/[Report_ID]/votes endpoint
5. Server accepts the vote without validating if the user has permission to vote
6. Attacker can subsequently delete votes by sending DELETE requests to /reports/[Report_ID]/votes/[VOTE_ID]

## Root cause
Server-side access control checks were not implemented for the voting endpoints. Authorization validation relied entirely on client-side UI controls (disabled buttons, hidden form fields) rather than server-side verification of user permissions.

## Attacker mindset
Security researcher performing comprehensive client-side validation testing by systematically removing disabled attributes and modifying boolean values to identify hidden or restricted functionality. The attacker was methodical and responsible, testing the impact and immediately removing the test vote to avoid data manipulation.

## Defensive takeaways
- Never rely on client-side controls (disabled attributes, hidden fields, UI restrictions) for security enforcement
- Implement server-side authorization checks on every endpoint that modifies data, regardless of UI presentation
- Validate user permissions before processing POST/DELETE requests to vote endpoints
- Use role-based access control (RBAC) to determine which users can vote on specific resources
- Log all voting activity for audit trails and anomaly detection
- Implement rate limiting on voting endpoints to prevent abuse
- Conduct security reviews for all hidden or feature-flagged functionality before release

## Variant hunting
Check other endpoints that modify user-contributed data (comments, ratings, flags) for similar access control gaps
Review all endpoints with feature flags or disabled UI elements for client-side validation-only implementations
Test authorization bypass on other sensitive operations (report creation, metadata modification, bounty award)
Examine API endpoints for consistent authorization checks across similar functionality

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force (enumeration of report IDs)
- T1021.001 - Remote Services (web application access)

## Notes
The researcher demonstrated good security hygiene by notifying the program immediately and removing test data. The vulnerability highlights the importance of defense-in-depth - UI controls are not security boundaries. The report references a Pornhub bounty program inclusion in a somewhat joking manner, suggesting this is a historical HackerOne report. The attacker's methodology of systematically testing disabled controls is a valid security testing technique that can reveal unintended functionality exposure.

## Full report
<details><summary>Expand</summary>

Hello there,
First of all let me congratulate you for including pornhub in the list of bug bounty programs, me and my colleagues will have a lot of fun with it hahahahahah. Awesome...

Anyways, I stumbled upon something whilst testing hackerone's main site. I don't know if it's a feature that it's going to be implemented soon or if it's something internal, I also have no idea if there are any risks involved in this, I'm confident you'll be accurate in your evaluation.

I started just for fun removing every "disabled" from every control on the web page and changing every "false" for a "true" on every json request, just to see what popped up, I've still have to cover the whole page and try everything to see that there are no client-side only reliant validations on the web page and/or info disclosure, but suddenly on the "Hacktivity" page this "vote buttons" appeared, and to my suprise, when I clicked one of them to go through as a request and assign a "vote id". I of course deleted my vote afterwards, I have no idea what I'm affecting.

Anyways, the endpoint seems to be in https://hackerone.com/reports/[Report_ID]/votes, which accepts the POST method and https://hackerone.com/reports/[Report_ID]/votes/[VOTE_ID] which accepts the DELETE method.

The fix would be fairily easy, implement server-side controls in order to prevent unauthorized users from using this feature.

Please let me know if this is something you would be interested in and we'll work together to fix it if necessary. Otherwise, please just mark it as informational.

I'm also including screenshots with both requests and responses.

Kind Regards,
Apok.

</details>

---
*Analysed by Claude on 2026-05-24*
