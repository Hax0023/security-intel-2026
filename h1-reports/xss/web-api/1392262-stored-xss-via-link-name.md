# Stored XSS via LINK Name in Templates Page

## Metadata
- **Source:** HackerOne
- **Report:** 1392262 | https://hackerone.com/reports/1392262
- **Submitted:** 2021-11-05
- **Reporter:** xploiterr
- **Program:** Insightly
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The LINK NAME field in Insightly's Templates page fails to properly escape user input, allowing stored XSS injection. An attacker can inject malicious JavaScript that executes in the context of all users viewing the affected template. The vulnerability exists because the link name is reflected directly within a <script> tag without sanitization.

## Attack scenario
1. Attacker authenticates to Insightly marketing platform and navigates to create a new redirect link
2. Attacker enters XSS payload in the Link Name field: '"></script><img src=x onerror=alert(1)>{{'7'*7}}
3. Payload breaks out of the script tag context and injects an img tag with onerror event handler
4. Attacker creates or edits an email template that references the malicious link
5. Any user in the organization who views that email template triggers the stored XSS payload
6. Attacker gains ability to steal session cookies, perform actions as victims, or conduct phishing

## Root cause
The application reflects the LINK NAME parameter directly into a <script> tag without proper HTML entity encoding or output escaping. The lack of input validation and output sanitization allows breaking out of the script context to inject arbitrary HTML/JavaScript.

## Attacker mindset
An internal or authenticated attacker seeks to compromise other users in the organization by poisoning shared email templates with stored XSS. The attack has organizational scope - all users viewing the template become victims. The attacker leverages the trusted nature of internal templates to bypass user suspicion.

## Defensive takeaways
- Implement strict output encoding/escaping for all user-controlled data, especially when reflected in script contexts
- Use Content Security Policy (CSP) to restrict inline script execution and prevent onerror handler exploitation
- Apply input validation and sanitization on the LINK NAME field to reject or escape special characters
- Store template content in a way that separates code from data - avoid embedding user input directly in executable contexts
- Implement server-side XSS filters and HTML sanitization libraries (e.g., DOMPurify, OWASP ESAPI)
- Conduct security testing of all form inputs that are persisted and displayed to other users
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Check all other link configuration fields for similar XSS vulnerabilities (description, URL, metadata)
Test custom field inputs in email templates for stored XSS
Examine other content management features (landing pages, forms) for reflected/stored XSS
Test template tag injection in template names and content
Review any JavaScript context rendering in reports, dashboards, or analytics pages
Test for XSS in campaign name fields or other shared organizational objects

## MITRE ATT&CK
- T1190
- T1598
- T1539
- T1566
- T1187

## Notes
Report demonstrates practical organizational impact - the vulnerability affects all users viewing the poisoned template, not just the attacker. The use of script tag context makes the payload particularly dangerous as it bypasses some browser XSS filters. The Jinja2-like template syntax ({{'7'*7}}) in payload suggests the backend may use template engines, indicating potential for Server-Side Template Injection (SSTI) as well.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi Team,

The `LINK NAME` is not properly escaped at the `Templates` page leading to `Stored XSS` and the name is reflected in the `<script> tag` , due to lack of sanitization the user can break out of the <script> tag and execute the XSS.

See Proof Of Concept below.
Thank You.

---

## Steps To Reproduce:

A. Log into your account at `https://marketing.na1.insightly.com/`

B. Click on `Plus Sign` --> `Add a new redirect Link` 

C. Enter this `'"></script><img src=x onerror=alert(1)>{{'7'*7}}` payload in the `Link Name` and fill all other details.

D. Click on `Save` and click on `Emails Icon` --> `Email Templates` --> `New Email Templates`

E. Enter all the details and click on `Save`

Wait a little bit and you will see the XSS executing.

## Note all the users visiting that page will execute the XSS in the organization.

---

## Proof Of Concept:

See this Video POC:

{F1504350}

POC:

{F1504349}

## Impact

An XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, perform requests in the name of the victim or for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
