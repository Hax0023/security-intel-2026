# Limited Open Redirection using SSO-SAML - Bypass via Double Slash

## Metadata
- **Source:** HackerOne
- **Report:** 178345 | https://hackerone.com/reports/178345
- **Submitted:** 2016-10-27
- **Reporter:** shailesh4594
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirection, Authentication Bypass, Regex Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A bypass of a previously patched open redirection vulnerability was discovered in the SAML SSO sign-in endpoint. By using a double slash (`//`) in the URL path, attackers could bypass the External Link Warning security control that was implemented in the previous patch. This allowed direct redirection to external SSO URLs without user notification.

## Attack scenario
1. Attacker identifies that HackerOne patched an open redirection issue in the SSO-SAML endpoint
2. Attacker discovers that path normalization isn't properly handled by testing variations with double slashes (`/users//saml`)
3. Attacker crafts a malicious link using the double-slash bypass: `https://hackerone.com/users//saml/sign_in?email=attacker@evil.com`
4. Attacker posts this link in comments or reports where users are likely to click
5. Users click the link expecting it leads to a legitimate HackerOne page, bypassing the external warning
6. Users are silently redirected to attacker-controlled SSO endpoint, potentially capturing credentials or session tokens

## Root cause
The patch for the previous open redirection vulnerability (CVE #171398) used a regular expression or validation logic that did not account for path normalization techniques. Specifically, duplicate slashes in URL paths can be normalized differently across web servers and frameworks, allowing the validation to be bypassed while the underlying routing still processes the request correctly.

## Attacker mindset
An attacker demonstrating good security research methodology by finding a bypass to a previous patch. The use of path manipulation (double slashes) suggests understanding of how URL parsers and normalizers work differently than security filters. The attacker is likely motivated by improving security awareness or bounty rewards.

## Defensive takeaways
- Validate and normalize URLs before applying security filters (remove duplicate slashes, resolve relative paths)
- Use whitelist-based approach for allowed redirects rather than blacklist/regex-based filtering
- Implement URL parsing using standard library functions that handle normalization consistently
- Apply security checks after URL normalization, not before
- Use HTTP status code 307/308 with POST-only redirects for sensitive operations instead of GET parameters
- Implement security controls at multiple layers (URL validation, routing, and final redirect)
- Test security patches with path traversal and normalization techniques (double slashes, dots, Unicode encoding)
- Consider using strict redirect whitelisting with exact domain matching rather than path-based rules

## Variant hunting
Test other path normalization techniques: `https://hackerison.com/users/./saml/...`, `https://hackerone.com/users/%2f/saml/`, URL encoded slashes
Test case variations and encoding: `https://hackerone.com/users//SAML/`, mixed case paths
Test semicolon separators: `https://hackerone.com/users/;/saml/`
Test backslash on Windows systems: `https://hackerone.com/users\saml\`
Fuzz the email parameter and other query params for injection points
Test other authentication endpoints that may use similar patterns
Check if `remember_me` parameter is also vulnerable to manipulation

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1187

## Notes
This is a classic example of how security patches can be bypassed when they target the symptom rather than the root cause. The original vulnerability likely validated against the final URL without normalizing it first. The reporter provided clear PoC evidence distinguishing between the patched and unpatched versions. The vulnerability is classified as 'Limited' because it requires user interaction (clicking a link) and the impact is redirection to SSO, not complete account takeover, though it could facilitate credential theft or social engineering attacks.

## Full report
<details><summary>Expand</summary>

Hello,

**Endpoint:** https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true

Recently, you have patched an open redirection issue which was reported as #171398. 
I found a bypass of that patch. 

**Steps to reproduce:** 
1. Add following in comment/report : 
```https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true``` 
2. Click on link. 
3. You will redirected on SSO URL without going through **External Link Warning** page. 
4. Done.

PoC  : 
https://hackerone.com/users/saml/sign_in?email=teste@snapchat.com&remember_me=true (Through external warning page)
https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true (Without external warning page)

**Suggested Fix:** Use more stronger regular expression and filtration at this endpoint.

Best regards,
Shailesh


</details>

---
*Analysed by Claude on 2026-05-24*
