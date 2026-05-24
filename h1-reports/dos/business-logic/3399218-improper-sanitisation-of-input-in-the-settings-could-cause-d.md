# Stored XSS in Email Settings (email_fromName/email_fromCompany) Leading to DOM-DoS

## Metadata
- **Source:** HackerOne
- **Report:** 3399218 | https://hackerone.com/reports/3399218
- **Submitted:** 2025-10-25
- **Reporter:** lu3ky-13
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding, Denial of Service (DOM-level)
- **CVEs:** CVE-2025-52666
- **Category:** business-logic

## Summary
An authenticated attacker can inject arbitrary JavaScript via email_fromName and email_fromCompany fields in account-settings-email.php. The payload is persisted in storage and rendered without proper output encoding, causing arbitrary script execution in viewers' browsers. This enables DOM-level denial-of-service by disabling page UI and functionality for all users viewing affected pages.

## Attack scenario
1. Attacker authenticates to the application or exploits weak access controls to reach the email settings page
2. Attacker navigates to /admin/account-settings-email.php and submits a POST request with JavaScript payload in email_fromName or email_fromCompany fields (e.g., '<img src=x onerror="alert(1)">')
3. Application saves the unsanitized payload to persistent storage (database/configuration) without encoding
4. When any user (including admins) views pages that render these settings, the stored JavaScript executes in their browser context
5. Attacker's script can manipulate DOM, hide/disable UI elements, replace page content, or redirect users, effectively disabling the site
6. If admin users are affected, attacker gains ability to perform privileged actions under admin context or escalate access

## Root cause
The application fails to apply output encoding (HTML entity encoding) when rendering email_fromName and email_fromCompany values on pages. Input validation during save is either absent or insufficient, and no Content Security Policy (CSP) or other XSS mitigations are in place.

## Attacker mindset
An insider or low-privileged user seeks to disrupt service availability for other users, particularly administrators. By injecting DOM-manipulation scripts, they achieve denial-of-service without network-level access. If they can influence admin activities, they maximize impact by triggering script execution in high-privilege contexts.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data rendered in HTML context (use framework-provided escaping functions like htmlspecialchars())
- Apply input validation to reject or sanitize scripts at submission time (whitelist approach for email metadata fields)
- Enforce Content Security Policy (CSP) headers with script-src restrictions to prevent inline script execution
- Use templating engines with automatic escaping enabled by default
- Implement stored XSS testing in security QA pipeline, especially for settings/configuration pages
- Apply principle of least privilege: restrict who can modify email settings; audit changes
- Consider using a library like DOMPurify for client-side sanitization as defense-in-depth
- Implement rate limiting and account lockout on repeated settings modifications to detect abuse

## Variant hunting
Search for other settings pages (admin, user profile, system config) that persist and render user-supplied text fields without encoding
Identify all database/config value reads that are directly output to HTML templates without escaping
Test email-related fields: email_signature, email_template, reply_to_name, sender_address, subject_prefix
Check for similar patterns in plugin configuration, system settings, and user profile pages
Review any form field that accepts free-text input and is displayed on dashboards or admin panels
Test for mutation XSS (mXSS) by injecting payloads that survive HTML parsing and trigger on re-rendering

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (unauthenticated variant if access controls weak)
- T1598 - Phishing: Spearphishing Link (if combined with malicious redirects in injected script)
- T1566 - Phishing: Phishing (if used to deliver secondary payload)
- T1539 - Steal Web Session Cookie (if script exfiltrates admin session tokens)
- T1561 - Disk Wipe (if script performs destructive DOM manipulations simulating data loss)

## Notes
The PoC demonstrates a straightforward injection; the actual payload was not explicitly shown but the impact description confirms DoS capability. Requires authentication/authorization to exploit, reducing severity slightly but not eliminating risk if user roles are poorly segregated. The vulnerability affects any user viewing pages that render these settings, making admins high-value targets. Consider this a critical finding if Revive Adserver is used in production ad-serving environments where availability is essential.

## Full report
<details><summary>Expand</summary>

h1 team

I found an input sanitization/encoding issue in account-settings-email.php where attacker-controlled values saved in email_fromName and email_fromCompany are persisted and later rendered to pages without proper output encoding. Because arbitrary JavaScript can be persisted and executed in viewers’ browsers, an attacker can run scripts that disrupt or replace the page UI — effectively disabling the site for victims (DOM-level denial-of-service). This is a stored/script injection vulnerability with high impact when rendered to admin or privileged users.

Safe Proof-of-Concept
1 go to http://localhost/test2/revive-adserver-6.0.1/www/admin/account-settings-email.php
2 add payload email_fromName and email_fromCompany  
3 the will disable all website you cant use it
http request

```
POST /test2/revive-adserver-6.0.1/www/admin/account-settings-email.php HTTP/1.1
Host: localhost
Content-Length: 1122
Cache-Control: max-age=0
sec-ch-ua: "Not=A?Brand";v="24", "Chromium";v="140"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Accept-Language: en-US,en;q=0.9
Origin: http://localhost
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAFTySI5FcKHdgQSw
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost/test2/revive-adserver-6.0.1/www/admin/account-settings-email.php
Accept-Encoding: gzip, deflate, br
Cookie: sessionID=44958de8497392e940916ecd332da541; ox_install_session_id=ln1aq7d4aopg1511andp5oocji
Connection: keep-alive

------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="submitok"

true
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="email_fromAddress"

1@aa.com
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="email_fromName"

1@aa.com
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="email_fromCompany"

1@aa.com
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="submitok"

true
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="email_logOutgoing"

true
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="submitok"

true
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="email_pluginType"


------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="token"

62f4ed819fb1ccc904033105a8d567ad
------WebKitFormBoundaryAFTySI5FcKHdgQSw
Content-Disposition: form-data; name="submitsettings"

Save Changes
------WebKitFormBoundaryAFTySI5FcKHdgQSw--

```

{F4931193}

{F4931194}

test url
http://localhost/test2/revive-adserver-6.0.1/www/admin/account-settings-email.php

## Impact

Arbitrary script execution in the application origin when persisted value is rendered to any page viewed by users.

Possible attacker actions include:

Replace page content or remove UI controls (rendering site unusable for the victim).

Block interaction with the app (disable buttons, hide forms) — effectively a targeted denial-of-service for users who view the infected page.

Phishing overlays, forced actions, or other client-side attacks against the user (exfiltration only possible if cookies/session not hardened).

If admin users view affected pages, the impact is high (site disruption; potential for privileged actions performed under admin context).

Severity: High — depends on which roles see the persisted values and cookie/session protections in place.

</details>

---
*Analysed by Claude on 2026-05-24*
