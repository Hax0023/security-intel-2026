# Stored XSS on promo.indrive.com via Unvalidated activationDate Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2051085 | https://hackerone.com/reports/2051085
- **Submitted:** 2023-07-05
- **Reporter:** kristoferent
- **Program:** inDrive
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The promocode activation API endpoint at /api/spreadsheet/promocodes fails to validate and sanitize the activationDate parameter, allowing attackers to inject arbitrary JavaScript payloads that persist in the backend database. When legitimate users query their driver ID through the promo.indrive.com interface, the stored XSS payload executes in their browsers, enabling session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker identifies valid driver IDs through enumeration or social engineering (e.g., ID '4')
2. Attacker crafts malicious POST request to /api/spreadsheet/promocodes with JavaScript payload in activationDate field (e.g., '<script>alert(1)</script>' or more sophisticated payload like fetch-based credential exfiltration)
3. Backend API stores unvalidated payload in database associated with the driver ID without sanitization
4. Attacker tricks victim or victim independently visits https://promo.indrive.com/promocodes to check their promotional status
5. Victim enters their driver ID and clicks 'Проверить ID' (Check ID), triggering API query that retrieves stored payload
6. Malicious script executes in victim's browser context with full access to session cookies, local storage, and ability to perform actions on behalf of the user

## Root cause
The backend API endpoint lacks input validation and output encoding. The activationDate parameter is stored directly in the database without HTML/JavaScript escaping. The frontend then renders this data without proper Content Security Policy or output encoding, allowing script execution.

## Attacker mindset
Low-effort, high-impact attack. Attacker recognizes that promotional features often bypass security scrutiny, especially if marked as 'retired.' The ability to enumerate driver IDs and inject payloads once affects all future queries of those IDs. Secondary exploitation potential: abuse the API to infinitely renew promotional codes for monetary gain.

## Defensive takeaways
- Implement strict input validation on all API parameters—validate activationDate as an actual date format (ISO 8601), reject any non-conforming input
- Apply output encoding context-appropriately: HTML entity encoding for any data rendered in HTML context, JSON encoding for JSON responses
- Enforce Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Use parameterized queries/prepared statements to prevent injection attacks at database level
- Implement rate limiting and authentication checks on API endpoints to prevent unauthorized bulk enumeration of driver IDs
- Deprecate and completely remove retired functionality rather than leaving it accessible and potentially unmaintained
- Perform security testing on all API endpoints, not just user-facing features; treat internal APIs with same rigor as public ones
- Sanitize user-controlled data before storage using libraries like DOMPurify or OWASP Sanitizer; never trust client-side validation

## Variant hunting
Search for similar patterns in inDrive applications: (1) Other date/timestamp parameters in API endpoints that might accept arbitrary values; (2) Any field accepting 'activation', 'expiration', or 'timestamp' data without validation; (3) Frontend pages rendering API responses without encoding; (4) Other subdomains (id.*, api.*, etc.) with similar CORS-enabled endpoints; (5) Promotional or user preference endpoints that store user-supplied strings; (6) Any parameter that accepts strings but is displayed back to users without sanitization

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing for Information
- T1566: Phishing
- T1059: Command and Scripting Interpreter
- T1041: Exfiltration Over C2 Channel

## Notes
The report notes this is 'retired functionality,' which may have contributed to security oversight. The attacker can enumerate driver IDs to infect multiple users. Secondary attack vectors mentioned (infinite promotional code renewal) suggest the API lacks proper state management and replay protection. Requires no authentication to POST to the API, indicating authorization bypass alongside the XSS issue.

## Full report
<details><summary>Expand</summary>

## Summary:
The functionality on https://promo.indrive.com/promocodes allows drivers to find and activate promocodes. It requires a driver ID. When user activates their promocode, the browser makes a POST request to https://id.indrive.com/api/spreadsheet/promocodes with parameters **id** (driver id) and **activationDate** (the date of the promocode activation). It is possible for an attacker to set parameter **activationDate** value to an XSS payload. When a user inputs the same ID when looking for promocodes, the XSS payload will trigger, executing arbitrary JavaScript code in the victims's browser.

## Steps To Reproduce:
1. Make a POST request to https://id.indrive.com/api/spreadsheet/promocodes with the following body: 
```
{"id":"4","activationDate":"<script>alert(1)</script>"}
```
{F2470829}
The driver ID value of **4** is used, but the attacker can enumerate through valid driver IDs to inject the payload into every user's promocode.
2. Go to https://promo.indrive.com/promocodes
3. Input a driver ID (in my example **4**) and click "Проверить ID". The XSS payload will be triggered
{F2470832}


## Supporting Material/References:
Full POST Request:
```
POST /api/spreadsheet/promocodes HTTP/1.1
Host: id.indrive.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 55
Origin: https://promo.indrive.com
Referer: https://promo.indrive.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Te: trailers
Connection: close

{"id":"4","activationDate":"<script>alert(1)</script>"}
```

## Impact

This vulnerability allows an attacker to execute arbitrary JavaScript code in any user's browser.
Despite this being a retired functionality, an attacker could trick users to try and get a promocode.
This could also potentially make promocodes usable infinite amount of times by directly making POST requests to renew the code every 24 hours.

</details>

---
*Analysed by Claude on 2026-05-12*
