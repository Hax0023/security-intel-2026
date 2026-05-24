# Open Redirect in eb9f.pivcac.prod.login.gov

## Metadata
- **Source:** HackerOne
- **Report:** 798742 | https://hackerone.com/reports/798742
- **Submitted:** 2020-02-18
- **Reporter:** timwhite
- **Program:** login.gov
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, Unsafe URL Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the PIV CAC authentication endpoint where the redirect_uri parameter is not properly validated, allowing attackers to redirect authenticated users to arbitrary external domains. This can be exploited for phishing attacks by crafting malicious links that appear to originate from the legitimate login.gov domain.

## Attack scenario
1. Attacker crafts a malicious URL containing redirect_uri parameter pointing to attacker-controlled phishing domain (e.g., https://google.com)
2. Attacker sends phishing email to government employees containing the malicious login.gov link with fragment identifier (#@secure.login.gov) for obfuscation
3. Victim clicks the link believing it's legitimate login.gov domain in the URL bar
4. Victim successfully authenticates with PIV CAC credentials on the legitimate login.gov endpoint
5. After authentication, the endpoint redirects victim to the attacker's phishing site (google.com) which mimics login.gov
6. Victim unknowingly enters credentials or sensitive information on the phishing page, exposing PIV CAC-related credentials

## Root cause
The redirect_uri parameter is not validated against a whitelist of allowed redirect destinations. The application trusts user-supplied redirect_uri values without verifying they point to authorized internal or partner domains. The fragment identifier (#@secure.login.gov) is used as a bypass technique since URL parsing may treat the fragment as navigation metadata rather than part of the hostname.

## Attacker mindset
An attacker would target government employees or contractors who use PIV CAC authentication. The goal is to harvest credentials or perform account takeover by creating a deceptive phishing page that appears legitimate due to the login.gov domain in the initial URL. This is particularly effective for government workers who may be less suspicious of links from official-looking domains.

## Defensive takeaways
- Implement strict whitelist validation for all redirect_uri parameters against a pre-approved list of internal domains and trusted partners
- Never trust user-supplied redirect destinations; validate against registered callback URLs stored server-side
- Parse URLs carefully to prevent bypass techniques using fragments (#), query parameters, or other encoding schemes
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Log all redirect attempts and alert on suspicious patterns or unusual destinations
- Use absolute URL validation rather than string matching or regex that may be bypassed
- Consider implementing POST-Redirect-GET pattern with server-side session storage of intended redirect instead of client-supplied parameters
- Perform security code review of all authentication and authorization endpoints

## Variant hunting
Check other authentication endpoints for similar redirect_uri validation issues (OAuth, SAML, OIDC implementations)
Test other query parameters that might accept URLs (callback, return_to, next, goto, success_url, continue)
Attempt to bypass validation using URL encoding, double encoding, or internationalized domain names (IDN)
Test redirect validation with data: URIs, javascript: protocols, or file: URIs
Examine partner/federation login pages for similar open redirect issues
Check mobile applications or API endpoints for redirect parameter handling
Test redirect chains (redirect to a page that redirects again) to evade validation

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1566.002

## Notes
This vulnerability affects a critical government authentication service (login.gov) used by federal employees. The severity is elevated due to the high-value targets and potential for credential theft. The use of fragment identifiers as a bypass technique suggests the validation may rely on simple string parsing. PIV CAC credentials are particularly valuable targets due to their use in accessing secure government systems. The fix should include comprehensive validation logic that accounts for known bypass techniques.

## Full report
<details><summary>Expand</summary>

poc:
```
https://eb9f.pivcac.prod.login.gov/?nonce=wI0UglN84A06Q4z4JnkZVc3i1V8%3D&redirect_uri=https%3A%2F%2Fgoogle.com%23%40secure.login.gov%2Flogin%2Fpiv_cac
```
visit this and will redirect to google.com

## Impact

phishing

</details>

---
*Analysed by Claude on 2026-05-24*
