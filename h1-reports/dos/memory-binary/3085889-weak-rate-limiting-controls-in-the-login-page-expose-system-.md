# Weak Rate Limiting Controls in Login Page Expose System to Brute Force and DoS Attacks

## Metadata
- **Source:** HackerOne
- **Report:** 3085889 | https://hackerone.com/reports/3085889
- **Submitted:** 2025-04-09
- **Reporter:** hajjaj0x
- **Program:** Lichess.org
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Insufficient Rate Limiting, Brute Force Attack, Broken Authentication, Credential Stuffing
- **CVEs:** None
- **Category:** memory-binary

## Summary
The login page at lichess.org lacks proper rate limiting controls, allowing attackers to bypass per-username rate limiting by distributing brute force attempts across multiple accounts. An attacker can systematically attempt login combinations using tools like Burp Suite Intruder without triggering account lockout or IP-based blocking mechanisms.

## Attack scenario
1. Attacker navigates to the lichess.org login page and captures a login request using Burp Suite proxy
2. Attacker modifies the request by removing the CSRF token and session cookies to bypass client-side protections
3. Attacker imports large username and password wordlists into Burp Suite Intruder with cluster bomb payload type
4. Attacker discovers that rate limiting only applies per-username, so distributing attacks across many usernames avoids 429 responses
5. Attacker launches the brute force attack which systematically tries credential combinations across the entire user base
6. Attack succeeds when valid credentials are found (HTTP 200 response), granting unauthorized account access

## Root cause
Rate limiting implementation uses per-username thresholds without implementing global IP-based or cumulative request throttling. The system fails to account for distributed brute force patterns where attacks target multiple different usernames sequentially or in parallel.

## Attacker mindset
Reconnaissance-focused adversary seeking to gain unauthorized account access for account takeover, privilege escalation, or sensitive data theft. The attacker demonstrates knowledge of HTTP security mechanisms (CSRF tokens, cookies) and exploit automation tools, indicating moderate skill level targeting a high-value platform.

## Defensive takeaways
- Implement multi-layered rate limiting: per-IP, per-username, and global thresholds combined
- Add exponential backoff delays after failed login attempts with progressive delays
- Implement CAPTCHA challenges after 3-5 failed login attempts
- Deploy account lockout mechanisms (temporary 15-30 minute locks) after threshold of failures
- Monitor for brute force patterns: multiple failed attempts across different usernames from same IP
- Log and alert on suspicious login patterns (high volume of failed attempts, credential stuffing indicators)
- Enforce strong password policies and consider passwordless authentication methods
- Implement Web Application Firewall (WAF) rules to detect and block brute force attack signatures
- Use behavioral analytics to detect account takeover attempts based on login patterns

## Variant hunting
Search for similar rate limiting bypasses in: password reset endpoints (per-email instead of per-IP), account enumeration endpoints (username validation without throttling), API authentication endpoints without concurrent request limits, multi-tenant applications with per-tenant rather than per-IP rate limiting, OAuth/SAML endpoints where rate limiting applies to code exchange but not token requests

## MITRE ATT&CK
- T1110.001 Brute Force: Password Guessing
- T1110.004 Brute Force: Credential Stuffing
- T1078.001 Valid Accounts: Default Accounts
- T1190 Exploit Public-Facing Application
- T1133 External Remote Services

## Notes
The report demonstrates sophisticated understanding of rate limiting bypass techniques. Key observation: attacker must use sufficiently large wordlists to stay under IP-based rate limits while distributing username attacks. The removal of CSRF token suggests either token reuse vulnerability or missing token validation. The plaintext credential transmission in multipart form-data is normal but should be protected by HTTPS. The vulnerability rating appears understated given direct path to account takeover of any user account.

## Full report
<details><summary>Expand</summary>

## Summary:

The login page lacks proper rate limiting, allowing an attacker to easily perform a brute-force attack. This vulnerability enables the attacker to systematically try different username and password combinations until they successfully compromise any account, which poses a significant security risk.

## Steps To Reproduce:

1.    Navigate to the login page.

2. Attempt login with any valid credentials.

 3.  Capture the request using a proxy tool (e.g., Burp Suite).

  +  Modify the captured request by deleting the token parameter and the cookies to make the request look like this:
====================================================================
POST /login HTTP/2
Host: lichess.org
Content-Length: 343
Cache-Control: max-age=0
Sec-Ch-Ua-Platform: "Linux"
X-Requested-With: XMLHttpRequest
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryc5GZocBapliqt011
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: */*
Origin: https://lichess.org
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://lichess.org/login
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

------WebKitFormBoundaryc5GZocBapliqt011
Content-Disposition: form-data; name="username"

§username§
------WebKitFormBoundaryc5GZocBapliqt011
Content-Disposition: form-data; name="password"

§password§
------WebKitFormBoundaryc5GZocBapliqt011
Content-Disposition: form-data; name="remember"

true
------WebKitFormBoundaryc5GZocBapliqt011-- 
=================================================================================

5.    Send the request to Burp's Intruder, adding a username wordlist for the "username" field and a password wordlist for the "password" field. Run the attack with the cluster bomb payload type.

    +   The wordlists should be large and realistic, matching common usernames and passwords (this will prevent rate-limiting issues caused by a smaller wordlist).

       + A smaller wordlist will cause the app to respond with 429 Too Many Requests due to insufficient time between attempts.

6.    Launch the attack, and you should eventually find a valid pair of credentials (response code 200 OK).

      + Ensure auto encoding is turned off in Burp Suite, as the credentials in the request are in plaintext.

     +   Note: The valid username will match many incorrect password attempts before the correct password is found and the app will not even feel that or make any reaction

Cause of the Vulnerability:

The vulnerability exists because the rate-limiting mechanism only checks for excessive requests to individual usernames. It does not account for multiple requests being sent to different usernames, allowing an attacker to bypass the rate-limiting by targeting a range of usernames. This creates an opportunity for a brute-force attack across a large set of accounts.

## Supporting Material/References:
{F4234333}
{F4234390}
{F4234544}

  * [attachment / reference]

## Impact

This vulnerability can lead to account takeover, privilege escalation, and the theft of sensitive user data.

</details>

---
*Analysed by Claude on 2026-05-24*
