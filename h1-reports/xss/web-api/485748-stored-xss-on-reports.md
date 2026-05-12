# Stored XSS in MoPub Reports

## Metadata
- **Source:** HackerOne
- **Report:** 485748 | https://hackerone.com/reports/485748
- **Submitted:** 2019-01-25
- **Reporter:** giddsec
- **Program:** MoPub
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the MoPub reports functionality where malicious JavaScript payloads can be injected through the custom report name field. When any user views the infected report, the malicious script executes in their browser context, allowing attackers to steal sensitive data or perform unauthorized actions.

## Attack scenario
1. Attacker navigates to the custom reports creation page (https://app.mopub.com/reports/custom/)
2. Attacker clicks 'New network report' to create a malicious report
3. Attacker injects XSS payload in the report name field: "><img src=x onerror=alert(document.domain)>
4. Attacker clicks 'Run and save' to store the malicious report in the database
5. Any authorized user who accesses and views this report triggers the stored XSS payload
6. Malicious JavaScript executes in the victim's browser, potentially stealing session tokens, credentials, or sensitive report data

## Root cause
The application fails to properly sanitize and encode user input in the report name field before storing it in the database. The output is not HTML-encoded when rendering reports, allowing injected HTML/JavaScript to execute in the user's browser.

## Attacker mindset
An attacker with report creation privileges seeks to create a persistent attack that compromises any user viewing specific reports. By embedding malicious scripts in report metadata, they achieve broad impact with a single submission, making this a high-value attack for data exfiltration or privilege escalation.

## Defensive takeaways
- Implement strict input validation on all report fields, rejecting or sanitizing HTML/script tags
- Apply context-appropriate output encoding (HTML entity encoding) when rendering reports to browsers
- Use a robust HTML sanitization library (e.g., DOMPurify, sanitize-html) for any user-supplied content
- Implement Content Security Policy (CSP) headers to restrict script execution
- Apply the principle of least privilege to report creation and viewing permissions
- Use templating engines that auto-escape output by default
- Implement security headers like X-XSS-Protection and X-Content-Type-Options

## Variant hunting
Check other report fields (description, tags, filters) for similar XSS vulnerabilities
Test stored XSS in other application features that accept user input (dashboards, custom names, annotations)
Investigate if report parameters or configuration options are vulnerable to XSS
Test reflected XSS in report viewing URLs or export functions
Check DOM-based XSS in report filtering or search functionality
Verify if SVG uploads or file attachments in reports can be exploited

## MITRE ATT&CK
- T1190
- T1566
- T1559
- T1555
- T1185

## Notes
This is a classic stored XSS vulnerability with high impact due to the nature of reports being accessed by multiple users. The proof-of-concept uses a simple image onerror payload to demonstrate execution. The vulnerability likely affects all users with report access, making it a critical security issue. The attacker requires at least the ability to create reports, suggesting this could be exploited by low-privileged accounts or escalated from other vulnerabilities.

## Full report
<details><summary>Expand</summary>

**Summary:** 
Stored XSS can be submitted on reports, and anyone who will check the report the XSS will trigger. 

**Description:**
Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application. 

## Steps To Reproduce:

  1. Go to https://app.mopub.com/reports/custom/
  2. Click **New network report**.
  3. On the name, enter payload: **"><img src=x onerror=alert(document.domain)>**
  4. Click **Run and save** then XSS will trigger. 

**Demonstration of the vulnerability:**
PoC: ████


Tested on Firefox and chrome.

## Impact

The attacker can steal data from whoever checks the report.

</details>

---
*Analysed by Claude on 2026-05-12*
