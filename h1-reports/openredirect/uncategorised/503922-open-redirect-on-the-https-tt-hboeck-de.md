# Open Redirect via 'return' Parameter in tt.hboeck.de

## Metadata
- **Source:** HackerOne
- **Report:** 503922 | https://hackerone.com/reports/503922
- **Submitted:** 2019-03-01
- **Reporter:** zophi
- **Program:** HackerOne (tt.hboeck.de)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The 'return' parameter in /public.php accepts arbitrary external URLs without validation, allowing attackers to redirect authenticated users to malicious sites. The vulnerability exists in both POST and GET request methods, making it exploitable through various attack vectors.

## Attack scenario
1. Attacker crafts a malicious URL containing return=http://evil.com/ parameter pointing to /public.php
2. Attacker sends this URL to a target user via email, chat, or embeds it in a webpage
3. User clicks the link and is taken to the legitimate tt.hboeck.de login page
4. User logs in with their credentials, completing authentication
5. Application processes the login and redirects to the URL specified in 'return' parameter (evil.com)
6. User is redirected to attacker's malicious site where credentials or session can be harvested or malware distributed

## Root cause
The application fails to validate or sanitize the 'return' parameter before using it for HTTP redirects. No whitelist validation, domain checking, or relative URL enforcement is implemented.

## Attacker mindset
Leverage the login flow to create a seemingly legitimate entry point. Users trust the initial domain (tt.hboeck.de), making them more likely to log in and trust the subsequent redirect. This is a classic phishing amplification technique using legitimate services.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs - only allow internal paths or pre-approved domains
- Use relative URLs instead of absolute URLs when possible
- Validate that redirect destinations begin with '/' or match the application's domain
- Reject any URL containing protocol schemes (http://, https://) unless explicitly whitelisted
- Log all redirect operations for security monitoring
- Implement Content Security Policy (CSP) headers to restrict external redirects
- Use framework-level redirect functions that enforce URL safety by default
- Test redirect functionality with external domain payloads in security testing

## Variant hunting
Search for other parameters used for redirection (redirect, next, forward, destination, callback, continue, url, target)
Test POST-only endpoints for similar unvalidated redirect parameters
Check password reset flows which commonly use return/redirect parameters
Look for base64-encoded or URL-encoded redirect parameters that bypass basic filters
Test methods like POST to POST, OPTIONS, HEAD for bypass opportunities
Examine error pages and exception handlers for potential redirect vectors
Check for double-encoding bypasses (e.g., %252f instead of %2f)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598 - Phishing
- T1566.002 - Phishing: Phishing - Email
- T1589 - Gather Victim Identity Information

## Notes
Open redirects are frequently underestimated but highly effective in phishing campaigns. The fact that this works across both POST and GET methods increases exploitability. No explicit bounty amount was disclosed in the report. The vulnerability is straightforward to exploit and requires no authentication bypass or complex interaction.

## Full report
<details><summary>Expand</summary>

Hi Team!

Testing request:
`POST /public.php?return=%2F HTTP/1.1
Host: tt.hboeck.de
...........
op=login&login={….}&password={...}&profile=0`

Vulnerable parameter: `return`

Method: `POST` -> `GET` -> OK

POC:
`https://tt.hboeck.de/public.php?return=http%3a%2f%2fevil.com%2f&op=login&login=password=&profile=0`

## Impact

User can be redirect to malicious site.

</details>

---
*Analysed by Claude on 2026-05-24*
