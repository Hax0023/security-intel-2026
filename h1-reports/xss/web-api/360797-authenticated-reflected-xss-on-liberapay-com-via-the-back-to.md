# Authenticated Reflected XSS on liberapay.com via back_to Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 360797 | https://hackerone.com/reports/360797
- **Submitted:** 2018-06-01
- **Reporter:** techguynoob
- **Program:** Liberapay
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Reflected XSS, Client-side redirect manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
The back_to parameter in the team membership leave endpoint (/jio/membership/leave) fails to validate redirect destinations, allowing attackers to redirect authenticated users to arbitrary external websites. This can be leveraged for phishing attacks by tricking users into clicking a cancel button that redirects to attacker-controlled domains.

## Attack scenario
1. Attacker crafts a malicious URL containing back_to parameter pointing to phishing site: https://en.liberapay.com/jio/membership/leave?back_to=http://attacker-phishing.com/
2. Attacker sends the link to a Liberapay user via email or social engineering
3. Victim clicks the link while authenticated on Liberapay
4. Victim is presented with the leave team confirmation page
5. Victim clicks the cancel button expecting to return to safe location
6. Victim is instead redirected to attacker's phishing site which mimics Liberapay login to steal credentials

## Root cause
The back_to parameter is not validated to ensure it redirects only to same-origin URLs. The application trusts user-supplied input for redirect destinations without whitelist validation or URL scheme verification.

## Attacker mindset
Attacker seeks to exploit user trust in Liberapay platform context by leveraging legitimate application URLs for credential theft. The cancel button creates false sense of safety, making victims more likely to interact with phishing content.

## Defensive takeaways
- Implement strict URL validation for all redirect parameters - whitelist allowed domains or use relative URLs only
- Validate that back_to parameter contains only same-origin URLs (match against current domain)
- Use URL parsing libraries to prevent bypasses (e.g., scheme validation to block javascript: or data: URIs)
- Implement Content Security Policy (CSP) with strict frame-ancestors to prevent clickjacking variants
- Add user warnings when redirecting to external sites or require explicit confirmation
- Use server-side redirect handler that validates destination before issuing HTTP redirect
- Log and monitor suspicious redirect patterns for security analytics

## Variant hunting
Check other endpoints with redirect parameters: back, return_to, redirect, next, url, callback, continue
Test all authentication flows (login, logout, password reset) for open redirect vulnerabilities
Examine API endpoints that may accept redirect parameters in POST/JSON payloads
Search for similar patterns in team management, donation flows, and user settings pages
Test with encoded variations: %2f%2f, %5c%5c, ///, @-prefixed URLs to bypass basic filters
Check if XSS is possible by injecting JavaScript in back_to: javascript:alert(), data:text/html schemes

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1566.002

## Notes
This is technically an open redirect vulnerability rather than reflected XSS, though phishing impact overlaps with XSS consequences. The authentication requirement adds context - attacker must trick authenticated users but can use social engineering. The 'Cancel' button UX makes this particularly effective for phishing as users expect it to return them safely.

## Full report
<details><summary>Expand</summary>

###Poc :

<https://en.liberapay.com/jio/membership/leave?back_to=http://example.com/>

Click the cancel button its redirect to 3rd party site.


Regards,
techguy

## Impact

This vulnerability could redirect users to the attackers websites for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
