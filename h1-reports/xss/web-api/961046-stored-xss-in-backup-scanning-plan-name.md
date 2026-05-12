# Stored XSS in Backup Scanning Plan Name

## Metadata
- **Source:** HackerOne
- **Report:** 961046 | https://hackerone.com/reports/961046
- **Submitted:** 2020-08-17
- **Reporter:** sbakhour
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Acronis backup console where user input in the backup scanning plan name field is not properly sanitized or encoded before being stored and displayed. An attacker can inject malicious SVG/JavaScript payloads that execute whenever the plan is viewed or edited by any user with access to that plan.

## Attack scenario
1. Attacker authenticates to the Acronis management console with a valid account
2. Attacker navigates to Backup Scanning > Plans > Create Plan
3. Attacker selects a backup location and injects XSS payload in the plan name field: /><svg/onload=prompt(document.domain)>
4. Attacker confirms plan creation, triggering immediate XSS execution
5. Attacker saves the malicious plan; the payload is persisted in the backend database
6. When any user views, edits, or accesses the saved plan, the stored XSS executes in their browser session, allowing session hijacking or further exploitation

## Root cause
The application fails to properly validate and encode user-supplied input in the backup scanning plan name field. Input sanitization is either absent or insufficient, and output encoding is not applied when rendering the plan name in the UI, allowing SVG/HTML injection with event handlers to execute arbitrary JavaScript.

## Attacker mindset
An insider or low-privileged user could inject payloads into shared backup plans to compromise other users' sessions, steal credentials, or perform lateral movement. The ability to inject into plan names suggests the attacker is testing for common injection points in administrative interfaces and exploiting trust in the backup/disaster recovery functionality.

## Defensive takeaways
- Implement strict input validation for all user-supplied fields, rejecting or sanitizing special characters like >, <, /, and quotes
- Apply context-aware output encoding (HTML entity encoding) when rendering user-provided data in web pages
- Use a security-focused templating engine that auto-escapes by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution and SVG event handlers
- Perform security code review of all data input/output flows, especially in administrative consoles
- Add validation on the backend to reject suspicious patterns before storing in the database
- Implement security testing (SAST/DAST) in the development pipeline to catch XSS vulnerabilities early
- Apply the principle of least privilege to limit which users can create/edit plans

## Variant hunting
Search for similar stored XSS in other Acronis console fields: policy names, device names, schedule names, report names, backup location descriptions, and any user-editable metadata fields. Test all create/edit forms for improper input handling. Check for reflected XSS variants in URL parameters related to plan viewing or filtering.

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1555

## Notes
This is a classic stored XSS in an administrative/backup console. The vulnerability is particularly severe because backup systems are critical infrastructure, and users may trust this interface. The self-XSS behavior during creation suggests client-side validation is being bypassed or incomplete. The payload persisting across page reloads confirms server-side storage without sanitization. Mozilla Firefox was tested, but the vulnerability likely affects all browsers. The attacker demonstrated good methodology by showing both immediate and persistent XSS execution.

## Full report
<details><summary>Expand</summary>

Dear Acronis Security Team,

##Summary:

There is a possibility of storing an XSS on the https://mc-beta-cloud.acronis.com/ui/ console.

##Steps To Reproduce:

1. Login to the console with the given account
2. Go to "Backup Scanning" under "PLANS"
3. Click on "Create Plan"
4. Specify the location of the "Backups to scan" (in my case I selected my PC where the agent is installed)
5. Name the plan with this payload "/><svg/onload=prompt(document.domain)>
6. The XSS will fire up many times showing a self XSS alert
7. Keep pressing "OK" till the alert goes away
8. Click on "Create" to create the plan then click on the edit icon then click on "Save Changes"
9. The Self XSS alert may re-pop up several times, just keep pressing the "OK" button
10. Reload the pages by re-visiting  https://mc-beta-cloud.acronis.com/ui/  or going between the tabs
11. Click again on  "Backup Scanning" under "PLANS"
12. Select the plan create with the payload "/><svg/onload=prompt(document.domain)>
13. Try to Edit it and the stored XSS will fire up.

##Supporting Material/References:

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
