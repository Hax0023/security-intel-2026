# Open Redirection in index.php

## Metadata
- **Source:** HackerOne
- **Report:** 320376 | https://hackerone.com/reports/320376
- **Submitted:** 2018-02-27
- **Reporter:** prashantkumar96
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Manipulation, Path Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
The index.php page performs unsafe redirection based on user-supplied path parameters without proper validation. An attacker can craft URLs that bypass domain validation by manipulating the path structure, allowing redirection to attacker-controlled domains that appear similar to the legitimate domain.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.hackerone.com/index.php/index.php.attacker.com
2. Attacker shares this URL via phishing email or social engineering, appearing legitimate as it starts with hackerone.com
3. Victim clicks the link, which is displayed in browser as hackerone.com in initial address bar view
4. Application processes the path parameter and constructs redirect to https://www.hackerone.com.attacker.com
5. Browser resolves this to attacker-controlled domain (due to DNS or attacker infrastructure)
6. Victim is now on attacker's phishing page believing they are on HackerOne

## Root cause
The redirection logic strips 'index.php' from the path without proper validation of the remaining path structure. It fails to verify that the constructed redirect URL remains within the same domain, allowing path manipulation to create lookalike domains through DNS resolution or substring matching attacks.

## Attacker mindset
Leverage trust in established brand (HackerOne) to create convincing phishing attacks. The vulnerability allows creating URLs that appear legitimate at first glance but redirect to attacker infrastructure. This is particularly effective for stealing credentials from security researchers or bug bounty hunters.

## Defensive takeaways
- Implement strict whitelist-based URL validation for all redirect destinations
- Verify that redirect targets are absolute URLs or relative paths that remain on the same domain
- Use URL parsing libraries to properly validate domain ownership before redirecting
- Implement redirect destination allowlists rather than blacklists
- Log and monitor unusual redirect patterns for detection
- Consider removing index.php handling if not necessary, or use proper routing frameworks
- Test redirect functionality with malicious payloads including domain confusion attempts

## Variant hunting
Check other PHP entry points (admin.php, api.php, etc.) for similar redirect vulnerabilities
Test redirect parameters in other endpoints that may accept URL parameters
Attempt path traversal variations: index.php/../, index.php//, index.php%2F
Test protocol confusion: index.php/javascript:, index.php/data:, index.php//attacker.com
Check if redirect validation differs for authenticated vs unauthenticated users
Test relative URL handling with multiple slashes and dots: index.php/...//attacker.com

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1040

## Notes
The vulnerability demonstrates how parameter manipulation in URL path parsing can bypass simple string replacement logic. The attack is particularly effective because the malicious URL retains the legitimate domain prefix, making it appear trustworthy. This is a common pattern in open redirect vulnerabilities where domain validation relies on substring matching rather than proper URL parsing.

## Full report
<details><summary>Expand</summary>

**Summary:**
Redirection is performed by HackerOne website when **index.php** page is visited. The parameter to **index.php** is used in redirection. By manipulating this parameter, an attacker can redirect victim outside www.hackerone.com

**Description:**
When a user visit www.hackerone.com/index.php/xyz, he/she is redirected to www.hackerone.com/xyz. However, when visiting www.hackerone.com/index.php/index.phpxyz, user will be redirected to www.hackerone.comxyz (without a slash between **com** and **xyz**).

Further, when visiting www.hackerone.com/index.php/index.php.hacker0ne.com, user will be redirected to www.hackerone.com.hacker0ne.com, a domain **hacker0ne.com**

### Steps To Reproduce

1. Visit https://www.hackerone.com/index.php/index.php.hacker0ne.com
2. Notice that the site redirects to https://www.hackerone.com.hacker0ne.com/

## Impact

Attacker can phish users

</details>

---
*Analysed by Claude on 2026-05-24*
