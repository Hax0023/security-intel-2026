# Stored XSS and Open Redirect in affiliate-preview.php

## Metadata
- **Source:** HackerOne
- **Report:** 819362 | https://hackerone.com/reports/819362
- **Submitted:** 2020-03-14
- **Reporter:** keyurvala
- **Program:** HackerOne (Specific program not disclosed in report)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** CVE-2021-22871
- **Category:** uncategorised

## Summary
A stored XSS vulnerability exists in the Website Properties form where user-supplied input is not properly sanitized before being stored and later displayed in the affiliate-preview.php admin page. An authenticated attacker can inject malicious JavaScript that executes when administrators view the affiliate preview, potentially redirecting them to arbitrary external sites.

## Attack scenario
1. Attacker authenticates with a valid user account
2. Attacker navigates to Inventory > Website > Website Properties
3. Attacker injects a payload like "http://Test"><img src=x onclick=window.location=\"http://evil.com\">" into the Website URL field
4. Attacker saves the malicious payload to the database
5. Administrator visits affiliate-preview.php to view generated affiliate code
6. Malicious JavaScript executes in the admin's browser, redirecting them to attacker-controlled domain

## Root cause
Insufficient input validation and output encoding on the Website URL field in Website Properties. The application fails to sanitize HTML/JavaScript special characters before storing user input in the database, and does not properly escape output when displaying the data in affiliate-preview.php.

## Attacker mindset
An authenticated insider or low-privilege user seeks to compromise administrative accounts or redirect legitimate users to phishing/malware sites by exploiting the trust placed in the affiliate preview feature.

## Defensive takeaways
- Implement strict input validation on all URL fields - validate against whitelist of protocols (http, https only) and reject special characters
- Apply context-aware output encoding - HTML encode all user-supplied data when rendering in HTML context
- Use Content Security Policy (CSP) headers to restrict script execution and prevent inline event handlers
- Implement parameterized queries and prepared statements to prevent injection
- Add server-side validation in addition to client-side validation
- Sanitize HTML/JavaScript special characters using established libraries (e.g., DOMPurify, OWASP ESAPI)
- Apply principle of least privilege - restrict user permissions for modifying critical website properties
- Implement audit logging for changes to website configuration

## Variant hunting
Check other input fields in Website Properties (description, metadata, custom fields) for similar XSS vulnerabilities
Test other admin preview pages and reporting features that display user-controlled data
Search for other instances where Website URL is rendered without encoding across the application
Check if similar vulnerabilities exist in other admin functionality accessible through GET parameters (codetype, block, affiliateid)
Test for reflected XSS in the affiliate-preview.php GET parameters themselves
Examine other inventory management sections (Products, Campaigns) for stored XSS
Test for CSRF attacks combined with stored XSS for higher impact

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1204.001

## Notes
The vulnerability chain includes both stored XSS and open redirect, amplifying impact. The use of img tag with onclick event bypasses basic XSS filters. The payload demonstrates creative bypass of URL validation. The report lacks information about whether the program patched the vulnerability and the actual bounty amount awarded.

## Full report
<details><summary>Expand</summary>

### Summary:
Stored XSS can be submitted on the Website using Default Manager, and anyone who will check the report the XSS and Open Redirect will trigger.

### Description:
Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.

### Steps To Reproduce:
1. Login with valid credentials of the user.
2. Go to inventory > Website > Website Properties
3. Fill the form and Enter Website URL as "http://Test"><img src=x onclick=window.location="http://google.com">". Click Save Changes.
4. Login with an administrator account.
4. Open http://localhost/hackerone/www/admin/affiliate-preview.php?codetype=invocationTags%3AoxInvocationTags%3Aspc&block=0&blockcampaign=0&target=&source=&withtext=0&charset=&noscript=1&ssl=0&comments=0&affiliateid=1&submitbutton=Generate
5. Click on Header Script Banner there is image click on that it will execute xss or open redirect.

## Impact

###Impact
Users can redirect the admin user or any normal user to any other website evil.com.

</details>

---
*Analysed by Claude on 2026-05-24*
