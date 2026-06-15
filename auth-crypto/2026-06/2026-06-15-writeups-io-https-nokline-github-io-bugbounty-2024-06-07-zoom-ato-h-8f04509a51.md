# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cookie XSS, Cookie Tossing, OAuth Authorization Code Theft, Browser Permission Hijacking, Content Security Policy Bypass, Session Hijacking
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable Cookie XSS vulnerabilities through cookie tossing techniques to achieve persistent session hijacking on Zoom. By exploiting CSP nonce cookie parsing, OAuth dirty dancing attacks, and hijacking browser permissions, attackers could steal authorization codes and gain unauthorized access to user webcams and microphones on web-based Zoom.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce parameter by exploiting cookie string parsing behavior
2. Attacker uses cookie tossing to set malicious cookies on parent domain affecting multiple subdomains
3. XSS payload executes in user's browser and initiates OAuth flow to steal authorization codes
4. Stolen authorization code is used to obtain valid OAuth tokens via dirty dancing technique
5. Attacker uses tokens to hijack browser permissions and enable webcam/microphone without user interaction
6. Session is fully compromised allowing persistent access to Zoom account and resources

## Root cause
Inadequate cookie value sanitization combined with improper cookie string parsing logic in CSP nonce handling. The application failed to properly escape special characters in cookie values before reflecting them in CSP headers and script nonce attributes, allowing attackers to break out of intended parsing contexts.

## Attacker mindset
Sophisticated attacker leveraging deep understanding of cookie mechanics, OAuth flows, and CSP bypass techniques. Rather than pursuing quick wins, the attacker demonstrated patience in finding seemingly useless vulnerabilities and creatively chaining them into a devastating attack chain affecting core authentication and device access mechanisms.

## Defensive takeaways
- Implement strict input validation and output encoding for all cookie values before reflection in HTTP headers or HTML attributes
- Use context-aware encoding (HTML entity encoding, URL encoding, JavaScript escaping) based on where data is reflected
- Validate and regenerate CSP nonces server-side rather than relying on client-controlled cookie values
- Implement SameSite cookie attributes to mitigate cookie tossing attacks across subdomains
- Apply additional OAuth security measures such as PKCE (Proof Key for Code Exchange) to prevent authorization code theft
- Require explicit user interaction and confirmation before granting sensitive browser permissions
- Conduct security review of cookie parsing logic which may have unexpected behavior with quoted strings and escape sequences
- Perform regular security audits on high-value targets even when vulnerabilities appear unexploitable in isolation

## Variant hunting
Look for similar cookie parsing issues in other CSP-protected applications, particularly those using cookies to store nonce values. Investigate other security-sensitive cookies that are reflected in HTTP headers without proper sanitization. Test for cookie tossing vulnerabilities on applications with multiple subdomains sharing parent domain cookies. Search for OAuth implementations that lack PKCE or other authorization code protection mechanisms.

## MITRE ATT&CK
- T1190
- T1539
- T1110
- T1656
- T1187
- T1563
- T1528

## Notes
This vulnerability demonstrates the importance of treating seemingly minor issues like cookie XSS seriously, especially on high-value targets. The combination of cookie tossing, OAuth exploitation, and browser permission hijacking created a perfect storm for account takeover. The six-month patch timeline highlights the complexity of fixing such deeply embedded issues. The $15k bounty reflects the critical nature and exploitability of the chained vulnerabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
