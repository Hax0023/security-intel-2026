# Open Redirection in fabric.io Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 39631 | https://hackerone.com/reports/39631
- **Submitted:** 2014-12-17
- **Reporter:** avicoder_
- **Program:** Fabric.io
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The fabric.io login page contains an open redirection vulnerability in the redirect_url parameter that allows attackers to redirect authenticated users to arbitrary external websites. By manipulating the redirect_url parameter with a payload like @google.com, an attacker can bypass URL validation and redirect users after successful authentication.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.fabric.io/login?redirect_url=@evil.com
2. Attacker shares this link via phishing email, social media, or other social engineering channels
3. Victim clicks the link and is presented with the legitimate fabric.io login page
4. Victim logs in with their credentials, trusting the fabric.io domain
5. After successful authentication, victim is automatically redirected to evil.com
6. Attacker can now harvest credentials, distribute malware, or conduct credential harvesting attacks

## Root cause
The redirect_url parameter is not properly validated against a whitelist of allowed domains. The application likely uses a simple string matching or protocol check that fails to account for the '@' character bypass technique, which is interpreted differently by URL parsing mechanisms.

## Attacker mindset
Attackers exploit this to craft convincing phishing campaigns targeting fabric.io users. The vulnerability is attractive because users trust the legitimate login page and are more likely to enter credentials, then be seamlessly redirected to attacker infrastructure for credential harvesting, malware distribution, or account compromise.

## Defensive takeaways
- Implement strict whitelist validation for redirect_url parameters using URL parsing libraries
- Validate that redirect URLs match expected domain patterns before redirecting
- Use allowlist of permitted redirect domains rather than blacklist approaches
- Implement URL parsing that correctly handles edge cases like '@' character in URLs
- Log and monitor redirect parameters for suspicious patterns
- Consider using relative URLs or POST-based redirect mechanisms instead of query parameters
- Educate users about verifying URLs in address bar after login flows

## Variant hunting
Check for similar redirect_url parameters in other endpoints (logout, password reset, settings)
Test with various bypass techniques: //evil.com, \\evil.com, %00evil.com, javascript: protocols
Look for redirect parameters with different names: return_url, back, next, continue, destination
Test POST-based redirects and hidden form fields
Check mobile app endpoints for similar vulnerabilities
Test cross-domain redirects via parameter injection in other query parameters

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Spearphishing Link with Attachment
- T1566.002 - Phishing: Phishing - Spearphishing Link

## Notes
The use of '@' character as bypass is particularly interesting as it leverages URL parsing differences. This is a classic open redirect vulnerability likely resulting from insufficient input validation. The simplicity of the report suggests this was caught early in deployment. Fabric.io (now part of Google/Firebase) should have implemented proper URL validation frameworks in their authentication flow.

## Full report
<details><summary>Expand</summary>

Hi dear, 
Once the person is logged into his account he can be redirected to any website .

https://www.fabric.io/login?redirect_url=@<payload>

for example : https://www.fabric.io/login?redirect_url=@google.com

Tested on updated firefox and chrome.

</details>

---
*Analysed by Claude on 2026-05-24*
