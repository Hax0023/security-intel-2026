# Open Redirect via Triple-Slash Bypass in Third-Party Authentication 'next' Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 223326 | https://hackerone.com/reports/223326
- **Submitted:** 2017-04-24
- **Reporter:** ysx
- **Program:** Weblate
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Authentication Bypass (Redirect), URL Validation Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Weblate authentication system fails to properly validate the 'next' parameter used for post-login redirects, allowing attackers to bypass validation by using a triple-slash prefix (///) to redirect users to arbitrary external domains. This vulnerability affects all third-party authentication providers including GitHub and potentially others.

## Attack scenario
1. Attacker crafts a malicious login URL with next parameter containing ///google.com
2. Attacker sends phishing email to Weblate users with the crafted URL
3. Victim clicks link and authenticates via GitHub or other third-party provider
4. Validation logic fails to recognize ///google.com as external URL due to triple-slash bypass
5. User is redirected to attacker-controlled domain (google.com in PoC)
6. Attacker can perform credential harvesting, malware distribution, or social engineering on the redirected page

## Root cause
Insufficient URL validation in the redirect handler. The application likely uses a simple check for '//' prefix to detect external URLs, but the triple-slash prefix (///) bypasses this check. The parser may strip one slash, leaving //google.com which is treated as a relative protocol-relative URL that resolves to the attacker's domain.

## Attacker mindset
Focused on chaining authentication flows with open redirects for phishing campaigns. Attacker discovered that common validation patterns (checking for '//' or 'http') can be bypassed with alternative syntax like '///' or other URL encoding tricks. This is a reconnaissance-level finding seeking to establish post-authentication redirect abuse.

## Defensive takeaways
- Implement whitelist-based URL validation for redirect parameters rather than blacklist approaches
- Use URL parsing libraries to normalize and validate URLs before redirecting (urllib.parse, URL() constructor)
- Reject any redirect URL unless it matches an explicit whitelist of allowed domains or is a relative path without protocol
- Validate the parsed scheme is empty or 'http'/'https' only, not 'javascript:', 'data:', or protocol-relative
- Test with multiple bypass techniques: ///, ////, encoded slashes, backslashes, mixed case, null bytes
- Log all redirect attempts with mismatched domains for security monitoring
- Consider not using 'next' parameter at all; instead use a redirect token mapped to allowed destinations

## Variant hunting
Test with backslash variants: \\\google.com or mixed \/\/\google.com
Try encoded variations: %2F%2F%2Fgoogle.com or %252F%252F%252Fgoogle.com
Test protocol-relative URLs: //google.com, ////google.com
Try javascript protocol: javascript:alert(1) or variations with slashes
Check if data: URIs are accepted: data:text/html,<img src=x onerror=alert(1)>
Test with null bytes or whitespace: ///google.com%00 or ///google.com	
Check other redirect parameters: redirect, return_to, goto, continue, back, referrer
Test with unicode/IDN domains that resolve to attacker IP
Try localhost bypass: ///localhost@google.com

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1187 - Forced Authentication
- T1583.001 - Acquire Infrastructure: Domains

## Notes
This is a classic open redirect in a high-value context (authentication flow). The triple-slash bypass suggests the application used a naive string check rather than proper URL parsing. The vulnerability is particularly dangerous because it follows successful authentication, making victims more likely to trust the redirected domain. The report is well-structured but lacks detail on impact assessment and affected versions. Weblate's response and patch timeline would be valuable for determining if this was a known bypass technique they hadn't considered.

## Full report
<details><summary>Expand</summary>

Hi,

It is currently possible to execute an open redirection attack via the `next` parameter with the inclusion of a triple-slash prefix.

## Proof of Concept
### Redirect URL
```
https://demo.weblate.org/accounts/login/github/?next=///google.com
```

After authenticating, the user will be immediately redirected to the attacker-specified target.  I believe this affects all third-party authentication providers on the Weblate platform.

Please let me know if you require any additional details regarding this vulnerability.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
