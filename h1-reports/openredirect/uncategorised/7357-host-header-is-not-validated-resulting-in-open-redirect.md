# Host Header Validation Bypass Leading to Open Redirect

## Metadata
- **Source:** HackerOne
- **Report:** 7357 | https://hackerone.com/reports/7357
- **Submitted:** 2014-04-12
- **Reporter:** anshuman_bh
- **Program:** IRCCloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Host Header Injection, Web Cache Poisoning, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
IRCCloud fails to validate the HTTP Host header, allowing attackers to inject arbitrary domains and trigger redirects to attacker-controlled sites. This vulnerability can be chained with caching mechanisms to perform web cache poisoning attacks against legitimate users, or exploited through alternate channels like password reset emails.

## Attack scenario
1. Attacker crafts an HTTP request to irccloud.com with a malicious Host header pointing to attacker.com
2. The application processes the request without validating the Host header against the expected domain
3. Application generates a redirect response using the unsanitized Host header value
4. If cached by a proxy/CDN, the poisoned response is served to subsequent legitimate users
5. Legitimate users clicking links or being redirected are sent to attacker.com instead of IRCCloud
6. Attacker can harvest credentials, distribute malware, or perform phishing attacks on victims

## Root cause
The application dynamically constructs redirect URLs or uses the Host header without validating it against a whitelist of legitimate hostnames. No server-side verification ensures the Host header matches the actual target domain.

## Attacker mindset
An attacker recognizes that Host header validation is often overlooked despite being a foundational security control. By exploiting this oversight, they can leverage legitimate domain trust to redirect users or poison caches at scale, maximizing impact with minimal effort. The availability of public documentation on Host header attacks increases attack likelihood.

## Defensive takeaways
- Implement strict whitelist validation of Host headers against expected domain(s) before using in any logic
- Reject requests with suspicious or non-matching Host headers (HTTP 400 Bad Request)
- Avoid using Host header for authentication, authorization, or security decisions
- Use absolute URLs in redirects rather than reconstructing from request headers
- Implement proper cache control headers (Vary, Cache-Control) to prevent cache poisoning
- Use Secure, HttpOnly, and SameSite cookie flags to limit exposure from redirects
- Configure CDN/proxy cache policies to account for Host header variations
- Validate Host headers in password reset, email confirmation, and other sensitive workflows
- Implement monitoring to detect unusual Host header patterns in access logs

## Variant hunting
Check if X-Forwarded-Host or X-Original-Host headers bypass validation
Test with duplicate Host headers to identify parsing inconsistencies
Verify behavior with IP addresses, IPv6, or alternate port specifications in Host header
Examine if validation differs between password reset, account recovery, and other sensitive functions
Test interaction with CDN/WAF caching to identify cache poisoning potential
Check if Host header validation is applied to all endpoints or only specific ones
Investigate whether Host header injection affects CORS policies or CSRF token validation
Test with internationalized domain names (IDN) or unicode encoding bypasses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1046

## Notes
The researcher demonstrates awareness of multiple exploitation vectors (cache poisoning vs. alternate channels) but only partially validates impact (password reset not vulnerable, but principle remains). The vulnerability's severity depends on cacheability and whether redirects are used in security-sensitive contexts. This is a classic example of a simple input validation oversight with significant blast radius when combined with caching infrastructure.

## Full report
<details><summary>Expand</summary>

Please see the attached screenshot where I am sending a request to irccloud.com with an invalid HOST header and I am getting redirected to that domain. This is because the HOST header is not validated to ensure that the request is originating from that target host or not.

http://www.skeletonscribe.net/2013/05/practical-http-host-header-attacks.html http://carlos.bueno.org/2008/06/host-header-injection.html 
The above links mention 2 different ways to exploit this issue:
1. web-cache poisoning and/or 
2. Using alternate channels like password reset emails. 

For the first way, it can be exploited by poisoning a cache with the attacker's domain and then serving that poisoned response to legitimate users, causing them to redirect to the attacker's domain. This attack kind of varies depending on different web servers as they interpret duplicate Host headers in different ways. The attack vectors are very well explained in the above blogs so I don't want to re-iterate them here again. 

For the second way, I verified that the password reset functionality on the IRC Cloud website does not retrieve the Host header when sending emails. But, validating the Host header is always a good practice. 

</details>

---
*Analysed by Claude on 2026-05-24*
