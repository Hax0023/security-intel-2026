# Email Validation Bypass, Missing Rate Limiting, and Resource Exhaustion on affiliates.nordvpn.com Forgot Password

## Metadata
- **Source:** HackerOne
- **Report:** 798913 | https://hackerone.com/reports/798913
- **Submitted:** 2020-02-18
- **Reporter:** bbece5b1ea2cbb33d0690ad
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Input Validation, Missing Rate Limiting, Denial of Service (Resource Exhaustion), Email Header Injection, Account Enumeration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The forgot password endpoint on affiliates.nordvpn.com lacks proper email validation and rate limiting controls, allowing attackers to bypass validation checks with malformed input (e.g., %0a, %0a%0d). An unauthenticated attacker can submit hundreds of requests with invalid email addresses, triggering backend email processing threads that consume resources without limits, resulting in denial of service.

## Attack scenario
1. Attacker navigates to https://affiliates.nordvpn.com/users/forgot_password endpoint
2. Attacker enters malformed email payloads containing newline characters (%0a, %0a%0d) or special characters that bypass client-side validation
3. Server accepts the malformed input and responds with 'Check your email for instructions on resetting your password' despite email format being invalid
4. Attacker intercepts the POST request using Burp Suite and sends it to the Intruder tool
5. Attacker launches high-velocity attack with 300+ payloads against the endpoint without encountering rate limiting
6. Backend spawns email processing threads for each invalid request, exhausting server resources and causing denial of service

## Root cause
The application fails to implement server-side email validation before processing password reset requests. The validation logic either relies solely on client-side checks or uses insufficient regex patterns that permit special characters. Additionally, no rate limiting mechanism exists on the endpoint to prevent brute-force or resource exhaustion attacks.

## Attacker mindset
An attacker seeks to disrupt service availability and exhaust backend resources. They recognize that password reset endpoints are often overlooked security components. By combining input validation bypass with missing rate limits, they can achieve amplified impact—each request triggers backend processing, multiplying resource consumption without proportional effort.

## Defensive takeaways
- Implement strict server-side email validation using RFC 5322 compliant regex or dedicated email validation libraries
- Enforce rate limiting on password reset endpoints (e.g., 3-5 requests per IP per hour, or per email per 24 hours)
- Validate email format and reject requests with special characters (%0a, %0d, etc.) before database queries
- Implement CAPTCHA or challenge-response mechanisms on repeated failed attempts
- Add request throttling at the application and infrastructure level (WAF rules, API gateway)
- Monitor for anomalous patterns in password reset requests (high volume, malformed inputs)
- Implement async email processing with queue limits to prevent thread exhaustion
- Log and alert on validation failures to detect attack patterns early

## Variant hunting
Search for similar patterns on other NordVPN subdomains and password reset endpoints. Test for email header injection via newline characters in other mail-based functionality (contact forms, newsletter signups). Investigate whether the same validation bypass works with other special characters (%0d%0a, %09, etc.) to identify the root cause of validation logic weakness.

## MITRE ATT&CK
- T1190
- T1836
- T1499
- T1535
- T1589

## Notes
The report title mentions 'RCE' but the actual vulnerability chain demonstrates DoS through resource exhaustion rather than remote code execution. The reference to report #751604 suggests this is a known class of vulnerability at NordVPN. Email newline injection (%0a) can potentially be chained with SMTP header injection for phishing or email spoofing if email sending is not properly sanitized downstream. The incomplete response text suggests the researcher was describing ongoing impact/threads being spawned.

## Full report
<details><summary>Expand</summary>

Go to
https://affiliates.nordvpn.com/users/forgot_password.

Enter arbitrary string like %0a or %0a%0d as email.

It says, No user account was found for the address given, which proves the query are going till the database.

Intercept request using Burp Interceptor, copy to intruder

Copy some 300 payloads, start attack, it keeps on saying

Check your email for instructions on resetting your password



Reference(for RATE limitng part): https://hackerone.com/reports/751604

POST /users/forgot_password HTTP/1.1
Host: affiliates.nordvpn.com
Connection: close
Content-Length: 206
Cache-Control: max-age=0
Origin: https://affiliates.nordvpn.com
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36
Sec-Fetch-User: ?1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Referer: https://affiliates.nordvpn.com/users/forgot_password
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: FirstSession=source%3Dgoogle%26campaign%3D%28direct%29%26medium%3Dorganic%26term%3D%28not%20provided%29%26content%3D%26hostname%3Dnordvpn.com%26pathname%3D/ovpn/%26date%3D20200107; _ga=GA1.2.26932056.1578394187; _gcl_au=1.1.1601631500.1578394190; __ssid=68ca10a8698b7fb327263a8af004e27; __cfduid=d03c846b273cfaf202a9c937242d1e2801581188311; locale=fi; cf_clearance=af23e443418808e03b379a3ba32fb1087149b191-1581964267-0-150; _gid=GA1.2.1712630761.1581964273; fontsCssCache=true; CurrentSession=source%3D%28direct%29%26campaign%3D%28direct%29%26medium%3D%28none%29%26term%3D%26content%3D%26hostname%3Dsupport.nordvpn.com%26pathname%3D/%26date%3D20200217; __zlcmid=wniv8mm0uelBwG; EUcomp=1; PHPSESSID=d53979189f4863cecd9bb69a8e13e8d2; swidth=1366; __utma=98793550.26932056.1578394187.1582038804.1582038804.1; __utmc=98793550; __utmz=98793550.1582038804.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 6bdfac53cbfb648b7ebe7a1fe1b93f4d=%7B%22v%22%3A%225.5%22%2C%22a%22%3A3322107227%2C%22b%22%3A%229da5c861ab1bfdefdfac0f80a32ff41d%22%2C%22c%22%3A1582039359968%2C%22d%22%3A%221e4d8b53d81a31ac7c5b8df209084902%22%2C%22e%22%3A%22%22%7D; __utmb=98793550.56.10.1582038804

_method=POST&data%5B_Token%5D%5Bkey%5D=fa7176462667ccddf68219e7b3a1a821c5bbb3c4&data%5BUser%5D%5Bemail%5D=%0a&data%5B_Token%5D%5Bfields%5D=d772038fc9d0d3adc2959122a9bd4b88c5edf33e%253An%253A0%253A%257B%257D

Response
              <li>No user account was found for the address given.</li>

POST /users/forgot_password HTTP/1.1
Host: affiliates.nordvpn.com
Connection: close
Content-Length: 209
Cache-Control: max-age=0
Origin: https://affiliates.nordvpn.com
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36
Sec-Fetch-User: ?1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Referer: https://affiliates.nordvpn.com/users/forgot_password
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: FirstSession=source%3Dgoogle%26campaign%3D%28direct%29%26medium%3Dorganic%26term%3D%28not%20provided%29%26content%3D%26hostname%3Dnordvpn.com%26pathname%3D/ovpn/%26date%3D20200107; _ga=GA1.2.26932056.1578394187; _gcl_au=1.1.1601631500.1578394190; __ssid=68ca10a8698b7fb327263a8af004e27; __cfduid=d03c846b273cfaf202a9c937242d1e2801581188311; locale=fi; cf_clearance=af23e443418808e03b379a3ba32fb1087149b191-1581964267-0-150; _gid=GA1.2.1712630761.1581964273; fontsCssCache=true; CurrentSession=source%3D%28direct%29%26campaign%3D%28direct%29%26medium%3D%28none%29%26term%3D%26content%3D%26hostname%3Dsupport.nordvpn.com%26pathname%3D/%26date%3D20200217; __zlcmid=wniv8mm0uelBwG; EUcomp=1; PHPSESSID=d53979189f4863cecd9bb69a8e13e8d2; swidth=1366; __utma=98793550.26932056.1578394187.1582038804.1582038804.1; __utmc=98793550; __utmz=98793550.1582038804.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 6bdfac53cbfb648b7ebe7a1fe1b93f4d=%7B%22v%22%3A%225.5%22%2C%22a%22%3A3322107227%2C%22b%22%3A%229da5c861ab1bfdefdfac0f80a32ff41d%22%2C%22c%22%3A1582039359968%2C%22d%22%3A%221e4d8b53d81a31ac7c5b8df209084902%22%2C%22e%22%3A%22%22%7D; __utmb=98793550.56.10.1582038804

_method=POST&data%5B_Token%5D%5Bkey%5D=fa7176462667ccddf68219e7b3a1a821c5bbb3c4&data%5BUser%5D%5Bemail%5D=%26%20&data%5B_Token%5D%5Bfields%5D=d772038fc9d0d3adc2959122a9bd4b88c5edf33e%253An%253A0%253A%257B%257D

Response
            <p>Check your email for instructions on resetting your password.</p>

## Impact

Hundreds of email threads are triggered at back end, since all of these are invalid email address, the threads will keep on RETRYING sending email and bring down NordVPN servers.
Also check

</details>

---
*Analysed by Claude on 2026-05-12*
