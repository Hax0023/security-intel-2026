# Open Redirection at smartreports.mtncameroon.net

## Metadata
- **Source:** HackerOne
- **Report:** 1530396 | https://hackerone.com/reports/1530396
- **Submitted:** 2022-04-04
- **Reporter:** vulnera
- **Program:** MTN Cameroon
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirection, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists at smartreports.mtncameroon.net that allows attackers to craft malicious URLs using path traversal sequences to redirect users to arbitrary external domains. The vulnerability can be exploited through a simple URL manipulation technique using double slashes and path traversal notation.

## Attack scenario
1. Attacker crafts a malicious URL: https://smartreports.mtncameroon.net//example.com/..;/css
2. Attacker sends the URL to victim via phishing email or social engineering
3. Victim clicks the link, trusting the MTN Cameroon domain in the URL
4. Browser renders the legitimate smartreports domain in the address bar initially
5. Application processes the redirect parameter and sends user to attacker-controlled example.com
6. Attacker harvests credentials or distributes malware from the redirected site

## Root cause
Insufficient input validation on the redirect parameter. The application likely uses string-based redirect logic without properly validating whether the target URL is internal or external, and does not account for path traversal bypass techniques using double slashes (//) and semicolon notation (;).

## Attacker mindset
Attackers exploit this to perform credential harvesting, malware distribution, or phishing campaigns by leveraging the legitimate domain's trust. The bypass technique (//example.com/..;/) is used to evade simple prefix-based validation that only checks if URLs start with a slash.

## Defensive takeaways
- Implement whitelist-based URL validation for redirects; only allow redirects to explicitly approved internal paths
- Use URL parsing libraries rather than string manipulation to normalize and validate redirect targets
- Validate that redirect destinations are relative URLs (starting with /) or from a whitelist of allowed domains
- Implement proper canonicalization of URLs before validation to handle bypasses like //, ;, and ../ sequences
- Add security headers like X-Content-Type-Options and implement CSP to mitigate redirect-based attacks
- Log all redirect attempts and monitor for suspicious patterns
- Use HTTPS-only redirects and implement HSTS

## Variant hunting
Search for similar open redirection patterns in other MTN services and applications. Test for variations: single slash bypass, backslash usage (\example.com), URL encoding bypasses (%2F%2Fexample.com), protocol-relative URLs (//example.com), and javascript: protocol handlers. Check for redirect parameters with common names: redirect, return, url, goto, next, dest, target, continue.

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1566.002
- T1102.001

## Notes
The report is minimal with limited detail on validation logic or bypass techniques. The path traversal bypass using (..;) suggests the application may be attempting some level of filtering but not accounting for all bypass variations. This is a classic open redirection vulnerability commonly found in legacy applications. The double slash notation (//) is a well-known bypass for applications checking if redirect URLs start with a single slash.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, 
I found open redirection on https://smartreports.mtncameroon.net

## Steps To Reproduce:
1. Go to https://smartreports.mtncameroon.net//example.com/..;/css

2. Redirection to example.com

## Impact

Open redirection vulnerability can redirect users to malicious sites that harm users

</details>

---
*Analysed by Claude on 2026-05-24*
