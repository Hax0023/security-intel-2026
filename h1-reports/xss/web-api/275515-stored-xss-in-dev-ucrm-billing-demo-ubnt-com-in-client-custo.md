# Stored XSS in Client Custom Attribute - dev-ucrm-billing-demo.ubnt.com

## Metadata
- **Source:** HackerOne
- **Report:** 275515 | https://hackerone.com/reports/275515
- **Submitted:** 2017-10-08
- **Reporter:** khizer47
- **Program:** Ubiquiti
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Client Custom Attribute field of the UCRM Billing demo application. An authenticated administrator can inject malicious JavaScript code that executes when any user views the custom attributes section, potentially leading to account compromise and privilege escalation.

## Attack scenario
1. Attacker authenticates as an administrator to dev-ucrm-billing-demo.ubnt.com
2. Attacker adds or edits a client and injects XSS payload in the Custom Attribute 1 field (e.g., "><IMG src=x onerror=prompt(1)>")
3. Attacker saves the client, storing the malicious payload in the database
4. Victim administrator or user navigates to the affected client's page
5. Victim clicks 'Show more' to expand custom attributes section
6. JavaScript payload executes in victim's browser session, allowing session hijacking, credential theft, or further malicious actions

## Root cause
The application fails to properly sanitize and encode user-supplied input in the Custom Attribute field before storing and rendering it. The output is not HTML-encoded when displayed, allowing injected script tags and event handlers to execute in the victim's browser context.

## Attacker mindset
An insider threat or compromised administrative account could exploit this to escalate privileges, steal session tokens, or pivot to other administrator accounts. The 'Show more' click trigger suggests the attacker identified this as a less-monitored action, making it suitable for persistent compromise.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, particularly custom attributes
- Use context-aware output encoding (HTML entity encoding) for all dynamic content rendered in HTML context
- Apply Content Security Policy (CSP) headers to restrict inline script execution
- Implement server-side HTML sanitization libraries (e.g., DOMPurify, bleach) for any rich text fields
- Use templating engines with auto-escaping enabled by default
- Conduct security code review of all user input handling and output rendering logic
- Implement automated security testing (SAST/DAST) in CI/CD pipeline to catch XSS vulnerabilities
- Apply principle of least privilege to limit admin account capabilities
- Monitor and log access to sensitive customer data and custom attributes

## Variant hunting
Test other custom attribute fields (Custom Attribute 2, 3, etc.) for similar XSS vulnerabilities
Check if other client fields accept and execute JavaScript (notes, descriptions, tags)
Test user profile custom attributes and organization custom attributes for same vulnerability
Investigate if stored XSS exists in service/invoice custom attributes
Test DOM-based XSS variants using different event handlers (onload, onmouseover, etc.)
Check if the vulnerability exists in exported/downloaded client data formats
Test if administrative logs or audit trails properly encode stored XSS payloads

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1021
- T1105

## Notes
This vulnerability affects a demo/development environment but indicates the vulnerability likely exists in production. The report demonstrates persistence of XSS payload and potential for privilege escalation through session hijacking. The use of external tools like XSSHunter shows attacker awareness of exploit infrastructure. The vulnerability requires administrative privileges to inject but affects any user viewing the data, making it a significant insider threat vector.

## Full report
<details><summary>Expand</summary>

Hey,

Was Testing the subdomins when I came Accross the subdomain https://dev-ucrm-billing-demo.ubnt.com/ I logged in as an Administrator and while testing i added a User and In Client Custom Attribute 1 i added the Payload: `"><IMG src=x onerror=prompt(1);>"">><marquee><img src=x onerror=confirm(3)></marquee>"/` and Save the Client and Then on client page i.e: https://dev-ucrm-billing-demo.ubnt.com/client/24 When User click on Show more (under Custom Attribute 1) The XSS payload executes :) 

{F227283}

{F227284}

If another Admin or A user will perform the steps to see the custo atributes his/her account can be takenover By Such Pentest XSS By using tools like https://xsshunter.com/app etc :) 


</details>

---
*Analysed by Claude on 2026-05-12*
