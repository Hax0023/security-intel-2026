# Stored XSS in infogram.com via Language Profile Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 430029 | https://hackerone.com/reports/430029
- **Submitted:** 2018-10-28
- **Reporter:** theappsec
- **Program:** Infogram
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Infogram's user profile settings where the language parameter is not properly sanitized or encoded before being stored and displayed on public profile pages. An attacker can inject arbitrary JavaScript code via the language field in the PUT /api/users/me endpoint, which executes when the public profile is viewed by any user.

## Attack scenario
1. Attacker crafts a malicious PUT request to /api/users/me with JavaScript payload in the language parameter
2. Payload bypasses input validation and is stored in the database without sanitization
3. Attacker shares their public profile URL with victims or waits for users to visit it
4. When victim views attacker's public profile, the stored payload executes in victim's browser context
5. JavaScript can steal session cookies, CSRF tokens, or perform actions on behalf of the victim
6. Attacker gains unauthorized access to victim accounts or steals sensitive information

## Root cause
The language parameter from user profile updates is not properly validated, sanitized, or HTML-encoded before being persisted to the database and rendered on the public profile page. The application trusts user input without implementing adequate output encoding defenses.

## Attacker mindset
An attacker would recognize that user profile fields are often overlooked for XSS protection, especially fields that seem 'safe' like language preferences. The public profile visibility makes this particularly valuable for broad impact, and the stored nature means payload execution happens without additional user interaction beyond visiting a profile.

## Defensive takeaways
- Implement strict input validation on all user-controlled fields, including language parameters with whitelist of valid language codes
- Apply HTML entity encoding/escaping to all user-supplied data before rendering in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Implement output encoding at the templating layer using auto-escaping features
- Validate and sanitize input on both client and server side
- Regularly audit profile-related endpoints for XSS vulnerabilities
- Implement security headers like X-XSS-Protection and X-Content-Type-Options

## Variant hunting
Check other user profile fields (first_name, last_name, username, bio, location) for similar XSS
Test the GET /api/users/{id} endpoint to see if it returns unsanitized profile data
Check if the vulnerability exists in other PUT/POST endpoints that accept user input
Test other user settings pages and preference panels
Look for similar vulnerabilities in user profile display across different views (card view, full profile, search results)
Check if the payload persists across different domains if Infogram has subdomains or partner sites

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
This is a classic stored XSS vulnerability with high impact due to public profile visibility. The payload uses script tag closure (></script>) to break out of potential context, followed by img onerror handler for code execution. The use of document.domain in the PoC confirms execution in the victim's browser context with access to sensitive data.

## Full report
<details><summary>Expand</summary>

The stored XSS was found in the language profile parameter.

POC:
Change profile settings with following request:

```http
PUT /api/users/me HTTP/1.1
Host: infogram.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
csrf-token: **your token**
X-Requested-With: XMLHttpRequest
Content-Length: 135
DNT: 1
Connection: close
Cookie: **your cookies**

first_name=name&last_name=name&username=&confirm_password=password&language=></script><img src=x onerror=alert(document.domain)>;//
```
Go to your public profile link.

example: https://infogram.com/dd_ddt7

## Impact

This allows an attacker to inject custom Javascript codes that can be used to steal information from infogram's users.

</details>

---
*Analysed by Claude on 2026-05-12*
