# Open Redirection Vulnerability in users.whisper.sh

## Metadata
- **Source:** HackerOne
- **Report:** 261592 | https://hackerone.com/reports/261592
- **Submitted:** 2017-08-19
- **Reporter:** hackedbrain
- **Program:** Whisper Systems
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirection, URL Manipulation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The users.whisper.sh subdomain is vulnerable to open redirection, allowing attackers to craft malicious URLs that redirect users to arbitrary external domains. The vulnerability exploits insufficient validation of redirect parameters, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker crafts a malicious URL: http://users.whisper.sh//google.com/%2f.. or similar variant
2. Attacker sends the link to target users via email, social media, or chat (appears legitimate due to whisper.sh domain)
3. Unsuspecting user clicks the link trusting the Whisper domain
4. Application processes the redirect parameter without proper validation
5. User is redirected to attacker-controlled domain (e.g., phishing site mimicking Google login)
6. Attacker captures credentials or performs further social engineering attacks

## Root cause
Insufficient input validation and sanitization of redirect parameters. The application likely uses unsanitized user input directly in Location header without verifying the target is a safe/internal URL. Double-slash (//), percent-encoding (%2f), and path traversal (..) techniques bypass basic checks.

## Attacker mindset
An attacker seeks to leverage the trust users have in legitimate domains (whisper.sh) to redirect them to malicious sites. This is a classic phishing enabler where the legitimate domain provides credibility while the open redirection provides flexibility to target any external URL.

## Defensive takeaways
- Implement strict URL validation: whitelist allowed redirect domains or require relative URLs only
- Use URL parsing libraries to normalize and validate redirect targets before applying redirects
- Avoid client-side redirects from user-controlled parameters; use server-side validation
- Implement Content Security Policy (CSP) with appropriate directives to restrict frame navigation
- Sanitize and validate all user inputs, including those in query parameters and POST data
- Maintain a whitelist of internal/allowed domains and reject any redirect attempts to external domains
- Log redirect attempts and monitor for suspicious patterns indicating attack attempts
- Use frameworks that provide built-in CSRF and redirect protections

## Variant hunting
Test other subdomains (.whisper.sh, api.whisper.sh, etc.) for similar issues
Check for open redirection in other parameters: returnUrl, redirect, next, callback, returnTo, goto, forward
Test with alternative encoding: %252f, unicode escapes, double-encoding, mixed case
Attempt protocol-relative URLs (//), javascript:, data: URIs if reflected in headers
Check POST-based redirects and POST parameters for redirect vulnerabilities
Test chained redirects and multi-stage redirections

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004

## Notes
This is a straightforward open redirection discovered via manual testing. The POC demonstrates the vulnerability clearly with a 303 redirect response. The fix requires implementing proper URL validation whitelist/allowlist mechanisms. No CVSS score provided in original report. The vulnerability has real-world impact in phishing campaigns targeting Whisper users.

## Full report
<details><summary>Expand</summary>

I found that one of your subdomains users.whisper.sh is vulnerable to open redirection.

POC: `http://users.whisper.sh//google.com/%2f..`

Response:
```
HTTP/1.1 303 See Other
X-Powered-By: Express
Location: //google.com/%2f../
Set-Cookie: 
CM; Path=/; HttpOnly
Date: Sat, 19 Aug 2017 14:22:50 GMT
Content-Length: 34
Via: 1.1 google

Redirecting to //google.com/%2f../
```



</details>

---
*Analysed by Claude on 2026-05-24*
