# Open Redirect via URL Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 504751 | https://hackerone.com/reports/504751
- **Submitted:** 2019-03-04
- **Reporter:** jishnu_sudhakaran
- **Program:** Omise
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Validation Bypass, Path Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in omise.co due to improper URL validation in the request path. By encoding forward slashes and question marks (%2f%2f%2f and %3f), an attacker can bypass validation and redirect users to arbitrary external domains like bing.com. This allows attackers to redirect legitimate users to malicious sites for phishing campaigns.

## Attack scenario
1. Attacker identifies that omise.co processes URL paths and may have insufficient redirect validation
2. Attacker crafts a malicious URL using URL encoding to bypass basic validation: /%2f%2f%2fbing.com%2f%3fwww.omise.co/?category=interview&page=2
3. Attacker sends phishing email or advertisement to victims with the crafted URL appearing to come from omise.co
4. Victim clicks the link, which displays omise.co in the address bar initially due to the legitimate host
5. Application processes the encoded path traversal sequence and redirects to bing.com
6. Attacker has successfully redirected victim to malicious site for credential harvesting or malware distribution

## Root cause
The application fails to properly validate redirect destinations before performing the redirect. The validation logic likely checks for unencoded redirect patterns but does not decode URL-encoded sequences (%2f for '/', %3f for '?') before validation, allowing bypassing of security checks through encoding.

## Attacker mindset
An attacker would leverage this to conduct phishing campaigns by creating seemingly legitimate omise.co links that redirect to credential harvesting sites. This is particularly effective because the initial URL contains the legitimate domain, bypassing user trust indicators. The attacker could also use this for SEO poisoning or malware distribution.

## Defensive takeaways
- Decode all URL-encoded characters before validation - never validate on encoded input
- Implement a whitelist of allowed redirect destinations rather than blacklist approach
- Use absolute URL validation and reject any redirect to different domains
- Consider disallowing redirects entirely if not core functionality
- Validate against double-encoded patterns and other bypass techniques
- Log all redirect attempts for security monitoring
- Use security headers like X-Frame-Options and Content-Security-Policy to limit redirect impact

## Variant hunting
Search for similar patterns in other endpoints that accept URL parameters. Look for other parameter types that might construct URLs (return_url, redirect_to, next, destination, callback, etc.). Test encoding variations: double encoding (%252f), unicode encoding (\u002f), case variations (%2F), mixed encoding schemes. Check other Omise properties and subdomains for the same vulnerability.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Email
- T1187 - Forced Authentication
- T1021.005 - Remote Services: VNC

## Notes
The vulnerability demonstrates a common validation bypass technique where encoding defeats string matching. The attacker pattern shows sophisticated understanding of how web frameworks parse paths. The writeup could be improved by clarifying whether this is a path-based redirect or query parameter redirect, and whether the application actually performs an HTTP redirect or client-side navigation. The impact is moderated to Medium because modern browsers show URL changes and users may notice the redirect.

## Full report
<details><summary>Expand</summary>

Open Redirect Vulnerability

URL  : https://www.omise.co////bing.com/?www.omise.co/?category=interview&page=2  
 
Parameter Type  : URL Rewrite  

Attack Pattern  : %2f%2f%2fr87.com%2f%3fwww.omise.co%2f  


How to Reproduce

1. Intercept the below url using Burpsuite & send it to repeater

https://www.omise.co/?category=interview&page=2

2. Use this attack pattern 

/%2f%2f%2fbing.com%2f%3fwww.omise.co

3. Now it will redirect to bing.com



Below i will give u the Rquest body & also attaching the screenshots


GET /%2f%2f%2fbing.com%2f%3fwww.omise.co/?category=interview&page=2 HTTP/1.1
Host: www.omise.co
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _omise-website_session=OHdwcEpSZVUvVXRqS3F3bUVyUUhaZ2pVY00wVWJ1c042RWZZNHdOendwUEkzS0dnaTJPb1hub3ZxcGhkUk5FNy96blpiNjJPL0hhMUZBdS9Jb2ZFY25BcWxzcXNjbTAyclJLTlo0VGUvbzBsa085MXhNUG9uZFpzRnBBeEp4a2MtLU9ONHdIWVBZdWZlS3VIVXVYTVNkOVE9PQ%3D%3D--cf8f4d43247d9eb5aa162a3f00fabc02bbda3b34
Upgrade-Insecure-Requests: 1

## Impact

An attacker can use this vulnerability to redirect users to other malicious websites, which can be used for phishing and similar attacks

</details>

---
*Analysed by Claude on 2026-05-24*
