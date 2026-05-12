# Stored XSS in Acronis Cyber Protect Console via Protection Plan Names

## Metadata
- **Source:** HackerOne
- **Report:** 1064095 | https://hackerone.com/reports/1064095
- **Submitted:** 2020-12-22
- **Reporter:** sbakhour
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Acronis Cyber Protect Console where protection plan names are not properly sanitized or validated, allowing attackers to inject malicious JavaScript payloads. The injected payload persists in the application and executes whenever the protection plan is viewed or interacted with, affecting all users who access that plan.

## Attack scenario
1. Attacker authenticates to the Acronis Cyber Protect Console with a valid account
2. Attacker navigates to Protection > Plans and creates a new protection plan
3. Attacker adds devices to the plan and assigns it a malicious name containing HTML/JavaScript payload (e.g., <video><source onerror="javascript:alert(document.domain)">)
4. Attacker confirms plan creation and performs an action triggering a confirmation dialog that displays the plan name
5. The XSS payload executes in the confirmation dialog context, demonstrating code execution
6. The payload persists in the database; any user or the same attacker accessing this plan later will trigger the XSS again, leading to session theft, credential harvesting, or malware distribution

## Root cause
The application fails to implement proper input validation and output encoding when handling protection plan names. User-supplied input is stored directly in the database without sanitization and rendered in the DOM without HTML entity encoding, allowing arbitrary script injection.

## Attacker mindset
An authenticated attacker with legitimate console access seeks to escalate privileges or compromise other users by injecting persistent malicious scripts. The attack targets administrative or operational users who manage protection plans, potentially leading to lateral movement within an enterprise environment.

## Defensive takeaways
- Implement strict input validation: reject or sanitize special characters and HTML tags in plan names using allowlist-based validation
- Apply context-aware output encoding: use HTML entity encoding (e.g., &lt;, &gt;) when rendering user-supplied data in HTML contexts
- Deploy a Content Security Policy (CSP) with strict directives to prevent inline script execution
- Use security libraries (e.g., DOMPurify) to sanitize user input before storage and rendering
- Implement automated security testing (SAST/DAST) to detect XSS vulnerabilities in user input handling
- Enforce code review processes focusing on data flow and encoding practices
- Consider implementing a Web Application Firewall (WAF) to detect and block XSS payloads
- Conduct security awareness training for developers on secure coding practices

## Variant hunting
Search for similar stored XSS vulnerabilities in other user-supplied field names throughout the Acronis console: device names, user profile names, policy descriptions, report titles, backup job names, and any custom naming fields in configuration panels. Test all CRUD operations and state transitions that display user input.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This vulnerability affects a beta environment (mc-beta-cloud.acronis.com) but likely impacts production systems using the same codebase. The vulnerability is particularly dangerous in enterprise contexts where multiple users access shared protection plans. The reproduction steps are clear and easily repeatable, indicating a straightforward implementation flaw. The attacker requires authentication, reducing the attack surface but increasing insider threat risk.

## Full report
<details><summary>Expand</summary>

Dear Acronis Security Team,

## Summary
There is a possibility of storing an XSS on the https://mc-beta-cloud.acronis.com/ui/ console.

## Steps To Reproduce
[add details for how we can reproduce the issue]

  1. Login to the console with the given account
  2. Go to "Protection" under "PLANS"
  3. Click on "Create Plan"
  4. Click on "Add devices" and select the device to add (in my case I selected my PC where the agent is installed)
  5. Name the new created protection plan with this payload  <video><source onerror="javascript:alert(document.domain)">
  6. Click on "Create" button and wait till the plan is created
  7. Once the plan is created go back to the "Protection" under "Plans" and select the created plan by selecting the checkbox
  8. On the "Actions" pane at the right side, click on the "Stop" button
  9. A confirmation box will appear to stop the plan
  10. Click on the red "Confirm" button and the XSS will fire up
  11. Reload the pages by re-visiting https://mc-beta-cloud.acronis.com/ui/
  12. Click again on "Protection" under "Plans"
  13. Select the plan created with this payload name <video><source onerror="javascript:alert(document.domain)">
  14. Repeat steps 8,9,10 and the XSS will fire up again confirming that it is a stored XSS.

## Recommendations
You can prevent XSS by escaping, validating inputs in fields and sanitizing. Plan names are not supposed to contain special characters or payloads.

##Supporting Material/References::
Please refer to the attached screenshot & video for reference.

##Browser Tested:
Mozilla Firefox 68.9.0esr (64-bit)

##Operating System Tested:
Windows 10 Professional 64-bit
Kali Linux 2020 32-bit

## Impact

An XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, perform requests in the name of the victim or for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
