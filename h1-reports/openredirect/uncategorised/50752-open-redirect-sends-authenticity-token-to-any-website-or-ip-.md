# Open Redirect via Double Slash Path Traversal Sends CSRF Token to Attacker-Controlled Domains

## Metadata
- **Source:** HackerOne
- **Report:** 50752 | https://hackerone.com/reports/50752
- **Submitted:** 2015-03-10
- **Reporter:** seifelsallamy
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, CSRF Token Leakage, Path Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
A double slash (//example) in the URL path on mobile.twitter.com causes the authenticity_token to be sent to arbitrary domains via HTTP POST. The attacker bypasses domain validation by converting IP addresses to single-number notation (e.g., 93.184.216.34 = 1572395042), allowing redirection to any website or IP address.

## Attack scenario
1. Attacker crafts a malicious URL: https://mobile.twitter.com//[attacker-ip-as-number]/messages
2. Attacker converts target IP (e.g., example.com → 93.184.216.34) to integer notation (1572395042)
3. Victim clicks the attacker's link while authenticated to Twitter
4. Browser processes double slash path and redirects POST request to attacker's server
5. Authenticity_token and other sensitive form data is transmitted to attacker-controlled endpoint
6. Attacker can perform CSRF attacks or session hijacking using the leaked token

## Root cause
Insufficient URL path normalization on mobile.twitter.com. The application fails to properly validate and canonicalize URL paths before processing redirects. Double slashes (//path) bypass domain whitelist validation, and the application accepts numeric IP representations in place of hostnames.

## Attacker mindset
The researcher demonstrates clever social engineering awareness—understanding that typical open redirect filters block dot-notation domains. By converting IPs to integer format, they bypass simplistic regex/whitelist filters that only check for domain patterns. This reflects understanding of how path parsing and numeric IP representations work in browsers and servers.

## Defensive takeaways
- Implement strict URL parsing and canonicalization before any redirect operations
- Normalize double slashes and other path traversal patterns in the request handler
- Whitelist redirect destinations explicitly; reject any redirect not matching known-safe patterns
- Reject numeric IP addresses and non-standard IP notations in redirect URLs
- Use a dedicated URL validation library rather than custom regex
- Implement server-side redirect validation independent of client-side checks
- Log and alert on suspicious redirect patterns (double slashes, numeric IPs, unusual encodings)
- Consider preventing CSRF token inclusion in redirects; use SameSite cookie attributes

## Variant hunting
Test triple slashes (///) and other path traversal techniques on other endpoints
Check if hexadecimal IP notation (0x5db82c22) also bypasses validation
Test octal IP notation (0335.0270.0330.0042) on different services
Attempt localhost redirects using 127.1, 127.0.0.1, or numeric variants (2130706433)
Test Unicode normalization and other encoding bypass techniques (%2f%2f)
Check if fragment identifiers (#) can bypass redirect validation
Test on other mobile platforms and endpoints that accept form submissions
Investigate if other sensitive tokens (CSRF, session, API keys) are similarly exposed

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a well-researched vulnerability showing the importance of input validation and understanding browser behavior around URL parsing. The researcher's use of IP conversion tools demonstrates how attackers research and engineer bypass techniques. The vulnerability chains together path traversal (double slash), open redirect, and CSRF token leakage into a complete attack. The mobile endpoint appears to have less rigorous validation than the main desktop version, suggesting inconsistent security implementations across platforms.

## Full report
<details><summary>Expand</summary>

Hi,
URL: https://mobile.twitter.com//example/messages (there is double slash before "example" word)
when you click "send" after writing a message the authenticity_token will send to https://example
this URL doesn't allow any dots in it, so i can not write //example.com 
but when i write a number it will redirect me to an ip, 
EG:
https://mobile.twitter.com//0/messages
>> 0.0.0.0
when i write a longer number it will redirect me to another ip
i fount this website that can change server or a website to ip
https://www.site24x7.com/find-ip-address-of-web-site.html
then i fount this website that can change any ip to a single number (without dots)
http://www.smartconversion.com/unit_conversion/IP_Address_Converter.aspx
so i'll change http://example.com to an ip by the first website
http://example.com = 93.184.216.34
now i'll change 93.184.216.34 to a single number without dots by the second website
93.184.216.34 = 1572395042
now to redirect from twitter to example.com
https://mobile.twitter.com//1572395042/messages
Thank you!


</details>

---
*Analysed by Claude on 2026-05-24*
