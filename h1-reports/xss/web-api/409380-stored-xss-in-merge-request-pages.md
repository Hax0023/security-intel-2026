# Stored XSS in Merge Request Pages via source_branch Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 409380 | https://hackerone.com/reports/409380
- **Submitted:** 2018-09-13
- **Reporter:** 8ayac
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in GitLab's merge request creation functionality where the source_branch parameter is not properly sanitized or encoded before being stored and displayed. An authenticated attacker can inject malicious JavaScript code via the merge_request[source_branch] parameter that will execute in the browsers of other users viewing the merge request page.

## Attack scenario
1. Attacker authenticates to GitLab and creates a test project with a test branch
2. Attacker navigates to the merge request creation page
3. Attacker intercepts the HTTP request when submitting the merge request form
4. Attacker modifies the merge_request[source_branch] parameter to contain malicious JavaScript payload (e.g., <img/src=x onerror=alert(1)>)
5. Attacker sends the modified request, causing the payload to be stored in the database
6. Other users viewing the merge request page trigger the stored XSS payload, executing arbitrary JavaScript in their session context

## Root cause
The source_branch parameter value is not properly HTML-encoded or sanitized before being stored in the database and rendered in the merge request page HTML response. The application fails to implement output encoding for user-controlled input displayed in the DOM.

## Attacker mindset
A malicious authenticated user seeks to compromise other users on the platform by injecting persistent JavaScript that could steal session tokens, perform unauthorized actions, or harvest credentials. The attacker recognizes that merge request pages are frequently viewed by project collaborators, making this an effective vector for propagating the attack.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data before rendering in HTML context (use context-aware encoding libraries)
- Apply input validation to reject or sanitize unexpected characters in branch names (alphanumeric, hyphens, underscores only)
- Use Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Implement a Web Application Firewall (WAF) to detect and block common XSS payloads
- Conduct security code review of all form handling and parameter processing logic
- Perform regular security testing including automated XSS scanning on all user input fields
- Maintain up-to-date dependency versions and security patches for templating engines

## Variant hunting
Test other branch-related parameters (target_branch, branch names in comparison views)
Check for XSS in merge request title, description, and comment fields
Examine branch selection dropdowns and autocomplete functionality for DOM-based XSS
Test commit message and tag name parameters in related features
Investigate webhook payload parameters that may be displayed to users
Review git reference handling in other parts of the application (tags, commits)

## MITRE ATT&CK
- T1190
- T1583.001
- T1589.001
- T1566.002

## Notes
This is a classic stored XSS vulnerability in a web application. The attack requires authentication but once exploited affects all users viewing the compromised merge request. The vulnerability demonstrates the importance of validating and encoding all user inputs, even those that seem innocuous like branch names. The step-by-step reproduction provided is clear and actionable, making this a straightforward security issue to remediate.

## Full report
<details><summary>Expand</summary>

**Summary:**
I found a Stored XSS in merge request pages. 

**Description:**
The exploit is via the parameter `merge_request[source_branch]` of the request to create a New Merge Request.

## Steps To Reproduce:
1. Sign ikn to GitLab.
2. Click the "[+]" icon.
3. Click "New Project".
4. Fill out "Project name" form with "test-project".
5. Check the radio button of "Public".
6. Check the "Initialize repository with a README".
7. Click "Create project" button.
8. Go to "http(s)://{GitLab host}/{user id}/test-project/branches/new".
9. Fill out each form as follows:
  - Branch name: test-branch
  - Create from: master
10. Click "Create branch" button.
11.  Go to "http://{GitLab host}/{user id}/test-project/merge_requests".
12. Click "Create merge request" button.
13. Click "Submit merge request" button.
14. Intercept the request.
15. Change the `merge_request[source_branch]` parameter's value to `<img/src=x onerror=alert(1)>`
16. Send the request.

Result: poc.png

Note: This behavior can be reproduced on all modern browsers.

## Impact

The security impact is the same as any typical Stored XSS.

Thank you.

</details>

---
*Analysed by Claude on 2026-05-12*
