# Cookie Injection and DoS via create_user Parameter in Periscope.tv Login

## Metadata
- **Source:** HackerOne
- **Report:** 583819 | https://hackerone.com/reports/583819
- **Submitted:** 2019-05-18
- **Reporter:** protostar0
- **Program:** Twitter/Periscope (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** HTTP Response Splitting, Cookie Injection, Denial of Service, CRLF Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
The create_user parameter in Periscope.tv's OAuth login flow is vulnerable to CRLF injection, allowing attackers to inject arbitrary HTTP headers and cookies into the response. This can be exploited to either manipulate cookie attributes (domain, max-age) for session hijacking or trigger a 504 Gateway Timeout denial of service condition.

## Attack scenario
1. Attacker navigates to Periscope.tv login page and initiates OAuth signup (Twitter/Google/Facebook)
2. Attacker identifies the vulnerable create_user parameter in the redirect URL
3. Attacker crafts payload with CRLF characters (%0d%0a) to inject additional HTTP headers/response content
4. Attacker modifies legitimate login URL with injected payload (e.g., create_user=dosattack%0d%0ahakou)
5. Social engineering victim to click malicious login link or automatic redirect
6. Server processes CRLF injection, either corrupting session cookies or crashing with 504 timeout, disrupting service

## Root cause
Insufficient input validation and sanitization of the create_user parameter before incorporating it into Set-Cookie headers or HTTP response generation. The application fails to filter CRLF characters that can break HTTP header boundaries.

## Attacker mindset
Opportunistic security researcher discovering low-hanging fruit in OAuth implementation. Motivation includes demonstrating impact of input validation gaps to establish credibility. Dual exploitation paths (cookie manipulation + DoS) show thorough testing methodology.

## Defensive takeaways
- Implement strict input validation on all OAuth callback parameters, rejecting CRLF characters and special header delimiters
- Use security libraries that properly encode Set-Cookie values to prevent header injection
- Apply allowlist validation for create_user parameter (e.g., only accept 'true'/'false' boolean values)
- Implement rate limiting on login endpoints to mitigate DoS exploitation
- Use HTTP-only, Secure, and SameSite cookie flags to limit injection impact
- Conduct regular security testing of OAuth flows with OWASP testing methodologies

## Variant hunting
Similar CRLF injection patterns may exist in other OAuth parameters (csrf, redirect_uri, state). Test other social login providers (Google, Facebook) documented as vulnerable. Check for header injection in response headers (Location, Set-Cookie, X-Custom-Headers).

## MITRE ATT&CK
- T1190
- T1499

## Notes
Report demonstrates classic HTTP response splitting vulnerability in OAuth context. PoC evidence (F492114, F492115) provided but not included in writeup. Vulnerability affects authentication critical functionality with moderate complexity (requires user interaction). The 504 timeout response indicates backend processing of malformed headers, suggesting improper header parsing in application or upstream proxy.

## Full report
<details><summary>Expand</summary>

**Description:** i find in  periscope.tv  a parameter "create_user" allow to inject "loginissignup" cookie,
when tested with crlf payload get response "**HTTP/1.1 504 GATEWAY_TIMEOUT**"
** Link Vulnerable:** https://www.periscope.tv/i/twitter/login?create_user=*payload*&csrf=*your_csrf_token*
## Steps To Reproduce:
  1. go to https://www.periscope.tv/
  2. click to login 
  3. click create new account
  4. choose twitter [ google & facebook also vulnerable]

  5-get link like https://www.periscope.tv/i/twitter/login?create_user=true&csrf=*your_csrf_token*

  6-edit create_user parameter 

**example : edit domain & max-age of loginissignup cookie **
payload="exploit;Domain=hakou.com;Max-Age=1000000000000000000000"
link=https://www.periscope.tv/i/twitter/login?create_user=exploit;Domain=hakou.com;Max-Age=1000000000000000000000&csrf=*your_csrf_token*
poc F492114

**example2: dos attack **
payload="dosattack%0d%0ahakou"
link=https://www.periscope.tv/i/twitter/login?create_user=dosattack%0d%0ahakou&csrf=*your_csrf_token*
get this response 
>HTTP/1.1 504 GATEWAY_TIMEOUT
Content-Length: 0
Connection: Close

poc 
F492115

## Impact

inject cookie & dos attack

</details>

---
*Analysed by Claude on 2026-05-24*
