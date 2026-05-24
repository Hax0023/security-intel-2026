# Open Redirection Vulnerability in JetBlue Domain

## Metadata
- **Source:** HackerOne
- **Report:** 1267176 | https://hackerone.com/reports/1267176
- **Submitted:** 2021-07-17
- **Reporter:** 0xjackal
- **Program:** JetBlue
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Open Redirection, URL Parsing
- **CVEs:** None
- **Category:** uncategorised

## Summary
A JetBlue URL is vulnerable to open redirection, allowing attackers to redirect users to arbitrary external domains like google.com. The vulnerability leverages improper parsing of URL credentials in the authority component, enabling attackers to craft deceptive links for phishing campaigns while maintaining the appearance of a legitimate JetBlue domain.

## Attack scenario
1. Attacker identifies that JetBlue's domain improperly parses URLs with embedded credentials
2. Attacker crafts a malicious URL using the format: https://[credentials]_https@google.com targeting JetBlue's domain
3. Attacker distributes the URL via phishing emails, social media, or other channels to JetBlue users
4. User clicks the link believing it's a legitimate JetBlue URL due to domain visibility in browser address bar
5. Browser redirects user to attacker-controlled domain (google.com in PoC, but could be phishing site)
6. Attacker captures credentials or installs malware on victim's system

## Root cause
Improper URL parsing in the application's redirect mechanism. The application fails to properly validate and sanitize the target URL before performing a redirect. The use of credentials in the URL authority component (username:password@host format) allows attackers to obscure the true redirect destination.

## Attacker mindset
The attacker is leveraging browser URL parsing behavior differences across browsers (Chrome vs Firefox) to craft URLs that appear legitimate in the address bar while redirecting to malicious destinations. This is a classic phishing enablement technique that exploits user trust in authentic application domains.

## Defensive takeaways
- Implement strict whitelist validation for all redirect destinations - only allow redirects to known, trusted domains
- Never trust user-supplied redirect parameters without extensive validation
- Use relative redirects instead of absolute URLs when possible
- Validate redirect URLs against a whitelist of allowed domains before processing
- Implement Content Security Policy (CSP) headers to restrict redirect capabilities
- Log and monitor redirect requests for anomalous patterns
- Educate users about verifying actual destination URLs before clicking redirects
- Test URL parsing behavior across different browsers and URL formats

## Variant hunting
Test other credential-based URL injection patterns: https://user:pass@attacker.com, https://user@attacker.com
Check for reflected redirects in other parameters (return_url, next, redirect_to, callback)
Test URL encoding bypasses: %2f%2f (//), %3f (?), %23 (#)
Test javascript: protocol handlers and data: URIs
Check for open redirects in logout, password reset, OAuth callback flows
Test double encoding and nested URL schemes
Look for redirects in API endpoints and mobile app communication

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1583.005 - Acquire Infrastructure: Domains

## Notes
This report demonstrates a relatively low-impact vulnerability as it requires user interaction and browsers like Firefox mitigate the risk by warning users. However, the phishing potential elevates concern. The redacted nature of the actual vulnerable parameter limits full technical analysis. The reporter correctly identified this as an open redirect but the writeup lacks depth regarding the exploitation chain beyond phishing. No evidence of actual exploitation or account compromise was provided. This appears to be a proof-of-concept report rather than evidence of active abuse.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi jetblue Security Team.

The following URL is vulnerable to an open redirect (it will redirect to google.com):
- https://█████_https@google.com

Work at Google Chrome & Other Browser 
Except Firefox will ask you first if you want to redirect to that page , See:-

█████████
  
##What is Open Redirect:-
Open redirection vulnerabilities arise when an application incorporates user-controllable data into the target of a redirection in an unsafe way. An attacker can construct a URL within the application that causes a redirection to an arbitrary external domain. This behavior can be leveraged to facilitate phishing attacks against users of the application. The ability to use an authentic application URL

Supporting Material/References:
-https://blog.detectify.com/2019/05/16/the-real-impact-of-an-open-redirect/
-https://medium.com/@0xrishabh/open-redirect-to-account-takeover-e939006a9f24

## Steps To Reproduce:
1. Go to  https://████_https@google.com
2. Redirect to google.com

## Impact

Open Redirection

</details>

---
*Analysed by Claude on 2026-05-24*
