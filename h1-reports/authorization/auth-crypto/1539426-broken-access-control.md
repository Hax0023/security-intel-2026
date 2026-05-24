# Broken Access Control - Unauthorized Admin Panel Access via Response Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1539426 | https://hackerone.com/reports/1539426
- **Submitted:** 2022-04-13
- **Reporter:** nayefhamouda
- **Program:** UPS (United Parcel Service)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control, Improper Authentication, Client-side Security Controls, Response Manipulation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A broken access control vulnerability allows attackers to bypass authentication and gain unauthorized access to the admin panel by manipulating the API response status field. By intercepting the SendTempPassword endpoint response and changing the 'status' field from false to true, attackers can access password reset functionality without proper authorization, leading to complete administrative control.

## Attack scenario
1. Attacker navigates to the target support site and accesses the password reset/account recovery functionality
2. Attacker initiates a SendTempPassword API request with any email address and intercepts it using a proxy tool like Burp Suite
3. Attacker modifies the intercepted HTTP response, changing the 'status' field from 'false' to 'true' despite the error message indicating the username does not exist
4. Attacker bypasses the client-side validation and gains access to the /resetPassword endpoint without proper authentication
5. Attacker navigates to the admin panel where they can view all user reports and sensitive information
6. Attacker gains full control to read, modify, or delete all reports and administrative data

## Root cause
The application relies on client-side response status validation rather than enforcing server-side authorization checks. The backend allows access to sensitive endpoints (resetPassword, admin panel) based on a response field that can be manipulated by the client, indicating the authentication/authorization logic is not properly enforced on the server side.

## Attacker mindset
An attacker would recognize that the application trusts the client's interpretation of the API response status field. By intercepting and modifying this field, they exploit the lack of server-side validation. The attacker understands that if they can trick the client into believing authentication succeeded, the server may grant access without re-verifying credentials.

## Defensive takeaways
- Never rely on client-side status fields for authorization decisions; all access control must be enforced server-side
- Implement proper session management and token-based authentication (JWT, OAuth) that cannot be manipulated by the client
- Always validate user authentication and authorization on every request to sensitive endpoints, regardless of previous responses
- Use HTTP-only and Secure cookies to prevent client-side manipulation of authentication tokens
- Implement server-side checks to verify that users attempting password resets are either logged in or have valid reset tokens
- Add rate limiting and account lockout mechanisms to prevent brute force attempts on password reset endpoints
- Ensure the API returns consistent and secure error messages that don't leak information about account existence
- Conduct thorough security testing of authentication and authorization flows, including response manipulation attacks

## Variant hunting
Check for other endpoints that might rely on response status manipulation for access control
Test if other boolean response fields can be modified to bypass authorization (e.g., 'isAdmin', 'isApproved', 'isVerified')
Examine password reset tokens to see if they can be predicted or brute-forced
Test if the resetPassword endpoint performs server-side validation of the reset token or if it trusts client state
Check if other account recovery mechanisms (security questions, email verification) have similar vulnerabilities
Test if the admin panel access check can be bypassed by directly accessing endpoints with modified headers or session cookies
Investigate if the vulnerability affects other user roles or permission levels

## MITRE ATT&CK
- T1190
- T1589
- T1110
- T1078

## Notes
The report is poorly structured with heavy redactions, making it difficult to fully assess the vulnerability scope. However, the core issue is clear: server-side authorization is missing. The vulnerability likely affects multiple endpoints beyond those mentioned. The report includes a video POC which should be reviewed for complete details. The attacker's ability to access all reports suggests either complete lack of row-level security (RLS) or that session tokens are being improperly validated. This is a critical vulnerability requiring immediate patching.

## Full report
<details><summary>Expand</summary>

## Summary:
hello ups team ,,,
I've found broken access control vulnerability in your sites 
It allows me to access the admin panel of the support team, and I can view all requests within the site

vulnerable domains:**█████**
## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. go to **█████████** 
  2. go to **████████████████** ,put any email address and intercept the request
  
```
POST /api/Account/SendTempPassword/?userName=█████████████ HTTP/2
Host: ██████████████████
Cookie: ████████
Content-Length: 0
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
Accept: application/json, text/plain, */*
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Origin: ██████████████████
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7


```
  3.On the burp site, intercept the response for this request and change this value to 
Then change the **"status"** value of this request from false to true

##response:

```
HTTP/2 200 OK
Cache-Control: no-cache,no-cache,no-store
Pragma: no-cache,no-cache
Content-Type: application/json; charset=utf-8
Expires: -1
Server: 
X-Content-Type-Options: nosniff
X-Xss-Protection: 1; mode=block
Referrer-Policy: no-referrer
Strict-Transport-Security: max-age=31536000; includeSubDomains;preload
X-Frame-Options: DENY
X-Ua-Compatible: IE=Edge
Content-Security-Policy: script-src 'self'; object-src 'self'; frame-ancestors 'none'
Expect-Ct: enforce, max-age=7776000, report-uri='███████████████-Allow-Headers: Accept, Content-Type, Origin
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Date: ██████████████████ ████████████ GMT
Content-Length: 89

{"status":true,"errorMessage":"Username does not exist. Please enter correct Username."}
```

  4. After that, go to this path  **/resetPassword** You will notice that this page has been opened without problems

███████████

Go to user or report and you will notice that it opens normally and you can fully control it

I made a video of the vulnerability that you can watch

##video POC:

███████

## Impact

The attacker can hack the admin control panel and view and modify all reports

</details>

---
*Analysed by Claude on 2026-05-24*
