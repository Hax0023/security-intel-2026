# Stored Cross-Site Scripting (XSS) in User Profile City Field

## Metadata
- **Source:** HackerOne
- **Report:** 1122513 | https://hackerone.com/reports/1122513
- **Submitted:** 2021-03-10
- **Reporter:** h4x0r_dz
- **Program:** Acronis (devicelock.com)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the user profile editing functionality where the City field on the admin user edit page fails to properly validate and encode user input. An attacker can inject arbitrary JavaScript code through the City field that executes when other users view the attacker's profile page.

## Attack scenario
1. Attacker creates a new account on devicelock.com/forum/
2. Attacker navigates to the admin user edit page and accesses the Personal Information section
3. Attacker injects malicious JavaScript payload (e.g., <img src=x onerror=alert(document.cookie)>) in the City field
4. Attacker saves the changes, which stores the unvalidated payload in the database
5. Legitimate users visit the attacker's profile page (view_profile.php?UID=<id>)
6. The stored payload executes in the context of the victim's browser, allowing session hijacking, credential theft, or malware distribution

## Root cause
The City field input is not properly sanitized or validated before storage, and the output is not properly HTML-encoded when rendered on the profile page. The application likely trusts user input and renders it directly in the DOM without escaping special characters.

## Attacker mindset
An attacker would exploit this to gain persistent access to victim accounts, steal session cookies, redirect users to phishing pages, or leverage the trusted domain to distribute malware. The profile page view likely has high exposure, making this an effective attack vector.

## Defensive takeaways
- Implement strict input validation on all user-editable fields, especially those displayed publicly
- Apply context-aware output encoding (HTML entity encoding) for all user-controlled data rendered in HTML context
- Use a whitelist approach for City field input (alphanumeric, spaces, hyphens only)
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Sanitize data using established libraries (e.g., DOMPurify, OWASP ESAPI)
- Apply principle of least privilege to admin user edit endpoints
- Regular security testing including automated XSS scanning and manual code review

## Variant hunting
Search for similar patterns in other profile fields (Name, About, Bio, etc.), comment sections, forum posts, product reviews, admin configuration pages, and any user-generated content fields. Check if other Bitrix installations (common CMS) have similar issues in user profile modules.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1185 - Browser Session Hijacking

## Notes
This vulnerability is particularly dangerous because it affects an admin-accessible endpoint, suggesting possible privilege issues. The Bitrix CMS platform used here is known to have legacy code patterns; organizations should audit all user input fields in Bitrix installations for similar encoding issues.

## Full report
<details><summary>Expand</summary>

## Summary

Hello, @acronis Team I hope you all doing well.

I just found A Stored Cross-site Scripting on devicelock.com/forum/ by changing the ***City*** value on https://www.devicelock.com/bitrix/admin/user_edit.php? to HTML/javascript code and lead to Stored Cross-site Scripting.


  1. go to https://www.devicelock.com/forum/view_profile.php?register=yes  and create a new account 
  1. go to https://www.devicelock.com/bitrix/admin/user_edit.php? and click on **Personal information** and in `City` input put and xss payload like: `<img src=x onerror=alert(document.cookie)>` and click on apply.
  1. Go to https://www.devicelock.com/forum/view_profile.php?UID=<your_user_id> and change `<your_user_id>` to your id 

## POC
https://www.devicelock.com/forum/view_profile.php?UID=28349

{F1225664}

## Impact

Stored XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
