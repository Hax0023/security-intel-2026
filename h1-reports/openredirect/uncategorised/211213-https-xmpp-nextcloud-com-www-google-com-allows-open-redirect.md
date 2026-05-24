# Open Redirect via URL Path Traversal on xmpp.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 211213 | https://hackerone.com/reports/211213
- **Submitted:** 2017-03-06
- **Reporter:** todayisnew
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Manipulation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on xmpp.nextcloud.com that allows attackers to redirect users to arbitrary external domains. The vulnerability exploits improper URL parsing by injecting path traversal and URL delimiter characters (///, ;@) to bypass redirect destination validation.

## Attack scenario
1. Attacker crafts a malicious URL using path traversal (///) and authority delimiter (;@) to bypass validation: https://xmpp.nextcloud.com///;@www.google.com
2. Attacker distributes the link via phishing email, social media, or malicious websites to Nextcloud users
3. Victim clicks the link believing it's a legitimate Nextcloud resource
4. Browser parses the URL and the server's redirect logic fails to properly validate the target domain
5. User is redirected to attacker-controlled domain (www.google.com or similar)
6. Attacker can now perform credential harvesting, malware distribution, or other social engineering attacks

## Root cause
Insufficient URL validation in the redirect handling mechanism. The server likely uses basic string matching or incomplete URL parsing that fails to account for RFC 3986 URL delimiter interpretation, allowing attackers to obscure the actual redirect target using path traversal (///) and authority separators (;@).

## Attacker mindset
Opportunistic researcher or malicious actor seeking to exploit trust in Nextcloud infrastructure for phishing attacks. The casual tone suggests a benign security researcher, but the vulnerability is demonstrable and exploitable for credential theft or malware delivery.

## Defensive takeaways
- Implement strict whitelist-based redirect validation using URL parsing libraries that properly handle RFC 3986 compliant URLs
- Use language-native URI parsing functions rather than regex-based validation
- Validate that redirect targets match expected domains/schemes before processing
- Reject URLs containing suspicious characters like ///, ;, or @ in the path component
- Implement Content Security Policy (CSP) headers to limit redirect destinations
- Add logging and monitoring for redirect attempts to suspicious domains
- Conduct security code review of all redirect handling across the application

## Variant hunting
Test other Nextcloud subdomains for similar redirect vulnerabilities
Attempt alternate URL encoding/bypasses: double encoding, Unicode normalization, case variation
Try other path traversal patterns: .., /.//, encoded slashes (%2f%2f)
Test query parameter-based redirects if present
Check for redirect vulnerabilities in login/logout flows and OAuth handlers
Test if the bypass works with other authority delimiters: :, @, ?
Examine if the vulnerability affects redirect chains or multiple hops

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1001.003 - Obfuscation: Steganography
- T1071.001 - Application Layer Protocol

## Notes
Report demonstrates a genuine security vulnerability with minimal technical detail but clear proof-of-concept. The use of path traversal (///) combined with authority separator (;@) is a known bypass technique for URL validation. Low complexity exploit with high impact for phishing campaigns. Reporter's friendly tone suggests collaborative disclosure.

## Full report
<details><summary>Expand</summary>


Good day :)

Hope it goes well, an open redirect exists on the main xmpp.nextcloud.com domain allowing "bad hackers" to do bad things :)

Poc 

https://xmpp.nextcloud.com///;@www.google.com

May you be well on your side of the screen :)

-Eric



</details>

---
*Analysed by Claude on 2026-05-24*
