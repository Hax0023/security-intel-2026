# Open Redirect via Parameter Bypass in Khan Academy Login

## Metadata
- **Source:** HackerOne
- **Report:** 6357 | https://hackerone.com/reports/6357
- **Submitted:** 2014-04-07
- **Reporter:** smiegles
- **Program:** Khan Academy
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Khan Academy's login page contained an open redirect vulnerability in the 'continue' parameter that could be bypassed by using a malformed URL with a single slash instead of double slashes. An attacker could craft a redirect to an external site by exploiting incomplete URL validation logic that failed to properly sanitize malformed protocol specifications.

## Attack scenario
1. Attacker identifies that the 'continue' parameter on /login accepts redirect URLs
2. Attacker discovers that standard URL validation rejects 'http://example.com' format
3. Attacker realizes the validation can be bypassed using 'http:/example.com' (single slash)
4. Attacker crafts malicious URL: https://www.khanacademy.org/login?continue=http:/www.olivierbeg.nl
5. Victim clicks the link and is redirected to attacker's domain after login
6. Attacker can harvest credentials, perform phishing, or distribute malware via trusted Khan Academy domain

## Root cause
The application implemented URL validation that checked for properly formatted protocol schemes (http://) but failed to account for malformed variations (http:/). The validation likely used a blacklist or regex pattern that didn't comprehensively cover edge cases in URL formatting, allowing single-slash variants to bypass the protection.

## Attacker mindset
An attacker would systematically test variations of URL schemes and delimiters to find gaps in validation logic. The discovery of the single-slash bypass demonstrates fuzzing of protocol separators and understanding that developers often test 'normal' cases but miss edge cases in URL parsing.

## Defensive takeaways
- Implement strict URL validation using robust parsing libraries rather than regex patterns
- Whitelist allowed redirect domains instead of trying to blacklist malicious patterns
- Use language-native URL parsing functions that handle edge cases and malformed URLs consistently
- Test redirect validation against common bypass techniques: single slashes, missing slashes, mixed protocols, relative paths
- Validate that parsed URLs match expected scheme and domain after parsing, not before
- Log and alert on redirect attempts to external domains for security monitoring
- Consider implementing redirect allowlists or requiring explicit user confirmation for cross-origin redirects

## Variant hunting
Test other malformed protocol variations: http:/, http://, http:///, http: (no slashes)
Check for JavaScript URI schemes: javascript:alert(1) in continue parameter
Test data URIs: data:text/html,<script>alert(1)</script>
Try protocol-relative URLs: //attacker.com
Test with backslashes instead of forward slashes on Windows-based parsing
Check for encoding bypasses: %2f%2f or other URL encoding variations
Test case sensitivity in validation: HTTP:// vs http://
Look for similar redirect vulnerabilities in other parameter names or endpoints

## MITRE ATT&CK
- T1598.003 - Phishing: Links in Live Chat (weaponized open redirect for social engineering)
- T1566.002 - Phishing: Spearphishing Link (malicious link via trusted Khan Academy domain)
- T1598 - Phishing (credential harvesting via redirect to fake login)

## Notes
This is a classic example of how URL parsing can have subtle edge cases. The researcher's finding is elegant - demonstrating that insufficient validation logic creates exploitable gaps. The 'continue' parameter is a common feature in authentication flows, making this vulnerability class particularly valuable for bug bounties. The writeup is minimal but effective in proving the bypass with clear examples.

## Full report
<details><summary>Expand</summary>

Hi,

I found a bypass in the redirects :
`https://www.khanacademy.org/login?continue=http://www.olivierbeg.nl` won't work.
`https://www.khanacademy.org/login?continue=http:/www.olivierbeg.nl` will work :-)

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
