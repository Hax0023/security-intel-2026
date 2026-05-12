# Self XSS in Create New Workspace Screen

## Metadata
- **Source:** HackerOne
- **Report:** 1442017 | https://hackerone.com/reports/1442017
- **Submitted:** 2022-01-05
- **Reporter:** unnamedx
- **Program:** Mattermost
- **Bounty:** No reward requested
- **Severity:** low
- **Vuln:** Cross-Site Scripting (XSS), Self-XSS, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Self-XSS vulnerability exists in the Create New Workspace screen where user-supplied input in the workspace name field is not properly sanitized or encoded before being reflected in the DOM. An attacker can inject malicious JavaScript through the workspace name parameter, though exploitation requires user interaction on the same session.

## Attack scenario
1. Attacker crafts a malicious URL or navigates to https://customers.mattermost.com/cloud/connect-workspace
2. Attacker navigates to the 'Create New Workspace' functionality
3. Attacker enters payload "/><img src=x onerror=alert(document.cookie)> in the workspace name input field
4. The payload is reflected unsanitized into the page DOM, executing JavaScript in the context of the user's browser
5. JavaScript code executes with access to document.cookie and other sensitive session data
6. Attacker could exfiltrate cookies, tokens, or perform actions as the authenticated user

## Root cause
The workspace name input field does not properly escape or encode user-supplied input before reflecting it back in the HTML response or DOM. This allows breaking out of the intended context with a closing tag sequence and injecting arbitrary HTML/JavaScript elements.

## Attacker mindset
A security researcher identifying inadequate input validation and output encoding on a user-controlled field. Notably, the reporter demonstrates ethical disclosure by acknowledging out-of-scope status and requesting no rewards, prioritizing responsible disclosure over bounty incentives.

## Defensive takeaways
- Implement proper output encoding/escaping for all user-supplied input reflected in HTML context (use HTML entity encoding)
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Use templating engines with auto-escaping enabled by default
- Implement input validation to reject or sanitize potentially dangerous characters (< > / quotes)
- Conduct security code review of all input handling in workspace creation workflows
- Test all user input fields with XSS payloads during QA testing

## Variant hunting
Test other workspace-related input fields (description, settings, etc.) for similar XSS issues
Check if the vulnerability persists in workspace editing/update functions
Test for DOM-based XSS in client-side JavaScript processing of workspace names
Investigate if other cloud management features have similar input validation gaps
Look for similar patterns in user profile, team creation, and channel creation screens

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
While classified as Self-XSS due to requiring user action on their own session, the impact could be significant in scenarios involving shared workstations, phishing attacks that trick users into entering malicious workspace names, or combined with CSRF attacks. The out-of-scope status on that particular domain suggests it may be a third-party or customer-facing service, but the underlying vulnerability warrants remediation. The reporter's altruistic approach demonstrates good faith security research practices.

## Full report
<details><summary>Expand</summary>

Hi team,
I have found an vulnerability on your website .
step to reproduce :

1.firstly i want to say sorry for this .please read carefully
when im testing on your website .i was redirected to  : https://customers.mattermost.com/cloud/connect-workspace
2.then navigate to create new workspace 
3.on workspace name input this payload : "/><img src=x onerror=alert(document.cookie)>
4.xss will trigger 

I know this domain is in out of scope ,but attacker can steal user cookies . I dont want any rewards for this i just want to aware you guys for this vulnerability .Hope you can understand .
Thanks for reading my report

## Impact

attacker can steal user cookies

</details>

---
*Analysed by Claude on 2026-05-12*
