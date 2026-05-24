# Clickjacking Vulnerability on Web Server

## Metadata
- **Source:** HackerOne
- **Report:** 13550 | https://hackerone.com/reports/13550
- **Submitted:** 2014-05-27
- **Reporter:** dushyantsahu1
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, User Interface Manipulation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A clickjacking vulnerability was identified on the target web server that allows attackers to trick users into clicking on hidden or disguised UI elements. This could lead to unauthorized actions, information disclosure, or compromise of user accounts depending on the affected application's functionality.

## Attack scenario
1. Attacker creates a malicious webpage with legitimate-looking content or interface elements
2. Attacker overlays transparent or invisible frames containing clickable elements from the vulnerable target application
3. User visits the malicious webpage believing they are interacting with innocent content
4. User clicks what appears to be a normal button or link on the attacker's page
5. The click actually triggers an action on the hidden target application (e.g., changing settings, authorizing transfers, deleting content)
6. Application performs the unintended action due to user's authenticated session with the vulnerable web server

## Root cause
The web application lacks proper frame-busting code and does not implement the X-Frame-Options HTTP header to prevent the page from being embedded in iframes on untrusted domains.

## Attacker mindset
An attacker seeks to exploit user trust and clickstream manipulation to perform unauthorized actions without explicit user awareness, leveraging the user's existing authentication to the vulnerable application.

## Defensive takeaways
- Implement X-Frame-Options HTTP header set to 'DENY' or 'SAMEORIGIN' to prevent framing by external sites
- Deploy Content Security Policy (CSP) frame-ancestors directive to control which domains can embed the application
- Implement frame-busting JavaScript code as a fallback defense mechanism
- Use UI security mechanisms like transparency checks and double-click verification for sensitive operations
- Educate users about risks of clicking on suspicious links and provide clear visual indicators of state changes
- Apply CSRF tokens for state-changing operations to add additional verification layers

## Variant hunting
Check for other sensitive endpoints that perform actions without additional verification (password changes, permission grants)
Test for combinations of clickjacking with CSRF vulnerabilities on state-changing operations
Examine admin panels and authenticated areas for frame-busting protections
Test drag-and-drop functionality that could be exploited similarly to clickjacking
Investigate mouse-over and focus-based attacks on form elements

## MITRE ATT&CK
- T1190
- T1566
- T1204.1

## Notes
This report appears to be a template or general vulnerability description rather than a specific instance with technical details. The writeup lacks concrete proof-of-concept evidence, specific affected URLs, or detailed impact demonstration. Effective clickjacking reports should include a working PoC demonstrating the vulnerability chain.

## Full report
<details><summary>Expand</summary>

Vulnerability description
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages. 


Affected items
Web Server 

The impact of this vulnerability
The impact depends on the affected web application. 





</details>

---
*Analysed by Claude on 2026-05-24*
