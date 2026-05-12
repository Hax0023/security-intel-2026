# HTML Injection and Possible XSS in main nordvpn.com domain

## Metadata
- **Source:** HackerOne
- **Report:** 780632 | https://hackerone.com/reports/780632
- **Submitted:** 2020-01-22
- **Reporter:** kiriknik
- **Program:** NordVPN
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTML Injection, Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
HTML injection vulnerability in nordvpn.com/blog endpoint allows attackers to inject arbitrary HTML and potentially execute JavaScript by bypassing URL encoding filters. The vulnerability enables session hijacking, credential theft, and phishing attacks through crafted URLs that inject malicious links or scripts into the page.

## Attack scenario
1. Attacker crafts a URL with double URL-encoded HTML/JavaScript payload targeting the blog parameter
2. Attacker sends phishing email with malicious link to nordvpn.com/blog endpoint to victims
3. Victim clicks the link, which passes through Cloudflare filter due to encoding obfuscation
4. Page renders injected HTML, redirecting footer links to attacker-controlled domain (e.g., 192.168.1.1)
5. Attacker can inject credential harvesting forms or JavaScript to steal session cookies
6. Attacker potentially gains access to user accounts and sensitive VPN session data

## Root cause
Insufficient input validation and output encoding on the blog parameter. The application fails to properly sanitize or HTML-encode user-controlled input, and relies on client-side or WAF filtering which can be bypassed through URL encoding techniques (double encoding, percent-encoding variation).

## Attacker mindset
Opportunistic abuse of parameter pollution for phishing and credential theft. Attacker recognizes that legitimate domain (nordvpn.com) has high trust value and attempts to exploit it for session stealing and malware distribution.

## Defensive takeaways
- Implement server-side input validation with whitelist approach for all parameters
- Apply proper HTML entity encoding/escaping to all user-controlled output
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Perform output encoding at point of use, not just WAF level
- Implement URL validation to prevent open redirect attacks
- Use security headers like X-XSS-Protection, X-Content-Type-Options
- Conduct security code review of parameter handling in blog functionality
- Test for bypass techniques including double encoding, unicode encoding, case variation

## Variant hunting
Search for similar parameter injection in other endpoints: /news, /press, /articles, /updates. Test other URL parameters for HTML injection: search, redirect, callback, return, next, ref, referrer. Look for reflected parameters in error pages and 404 handlers. Check for similar encoding bypass techniques on other NordVPN subdomains.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056
- T1539

## Notes
The vulnerability demonstrates encoding filter bypass techniques. Cloudflare WAF was insufficient protection indicating need for defense-in-depth. The double URL encoding (%25 = %, %32 = 2, %33 = 3, %36 = 6, etc.) obfuscates the payload structure. Impact is elevated if cookie flags lack HttpOnly/Secure attributes. Reporter notes 'steal cookie' and 'possible XSS' indicating uncertainty about JavaScript execution feasibility, suggesting Cloudflare may have partially mitigated script injection while HTML injection remained viable.

## Full report
<details><summary>Expand</summary>

## Summary:
HTML injection in main domain can allow hackers forward users to any another domain. Also, if anybody can find method to bypass cloudflare filter hackers can steak cookie with with vuln 

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Go to https://nordvpn.com/blog/?1%25%32%32%25%33%65%25%33%63%25%32%66%25%36%31%25%33%65%25%33%63%25%36%31%25%30%63href%25%33%64%25%32%32http://3232235777
  2. Check, that links on the bottom of page goes to 192.168.1.1
   {F692879}

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

The vulnerability allow a malicious user to inject html tags and (possible) execute Javascript which could lead to steal user's session

</details>

---
*Analysed by Claude on 2026-05-12*
