# Admin Authentication Bypass via Response Manipulation Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1490470 | https://hackerone.com/reports/1490470
- **Submitted:** 2022-02-24
- **Reporter:** 7odamoo
- **Program:** HackerOne Report #1490470
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Client-Side Validation, Improper Input Validation, Privilege Escalation, Broken Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can bypass admin authentication by intercepting the login API response and modifying the status field from false to true, regardless of credential validity. This allows unauthorized access to admin accounts and subsequent privilege escalation to view/delete sensitive company reports and process returns.

## Attack scenario
1. Attacker navigates to the admin login page at the target subdomain
2. Attacker enters any username (e.g., 'Admin') and incorrect password credentials
3. Attacker intercepts the POST /api/Account/Login/ request in Burp Suite
4. Attacker forwards the request and intercepts the 200 OK response containing {"status":false,...}
5. Attacker modifies the response field status from false to true
6. Attacker forwards the modified response, which the client accepts as successful authentication, granting admin session access

## Root cause
The application relies solely on client-side validation of the login response status field without server-side session validation. The server sends the authentication result to the client but does not enforce server-side checks before granting session tokens or maintaining authentication state. The authentication decision is made on the client side based on the response status rather than server-side session management.

## Attacker mindset
Reconnaissance and exploitation of client-side trust assumptions. The attacker recognized that intercepting HTTP responses is trivial with common proxy tools and that modifying a boolean flag could bypass fundamental authentication controls. No special knowledge of the backend was required—only familiarity with HTTP interception and awareness that many developers incorrectly trust client-supplied authentication decisions.

## Defensive takeaways
- Never trust client-side authentication validation; always enforce authentication and authorization server-side
- Use server-side sessions with secure session tokens (HTTP-only, Secure flags) instead of relying on response status fields
- Implement proper authentication flows with cryptographic session management (e.g., JWT with server validation, session cookies with server-side store)
- Validate all authentication decisions server-side before granting access to protected resources
- Implement rate limiting and account lockout mechanisms on login endpoints to prevent brute force attempts
- Use HTTPS with HSTS to prevent man-in-the-middle response manipulation
- Never expose authentication state directly in API responses; use secure session mechanisms
- Conduct security code review focusing on authentication and session management logic
- Implement comprehensive logging and monitoring of login attempts and authentication failures

## Variant hunting
Check for other boolean response fields that control access (e.g., isAdmin, isAuthenticated, canAccess)
Test if other HTTP response codes (e.g., changing 200 to other codes) affect authentication logic
Examine if response headers contain authentication tokens that can be manipulated
Test password reset/change endpoints for similar client-side validation flaws
Check API endpoints for missing authentication checks entirely
Test if modifying other user accounts in the response affects which account is logged in
Investigate if the client-side code has any observable authentication logic that can be reversed

## MITRE ATT&CK
- T1190
- T1110
- T1199
- T1021
- T1078
- T1566

## Notes
This is a textbook example of improper client-side trust and broken authentication. The vulnerability is trivially exploitable with basic HTTP interception tools (Burp Suite, OWASP ZAP, Fiddler). The impact is severe: full admin account compromise, access to sensitive company data (1066 reports), and destructive capabilities (delete reports, process returns). The writeup contains redacted sensitive information but demonstrates clear reproducible steps. This type of vulnerability should have been caught in basic security code review or penetration testing. The fix requires fundamental architectural changes to implement proper server-side authentication and session management.

## Full report
<details><summary>Expand</summary>

Hello Team

I found that i can bypass the login page of the Admin account by intercepting the respone of the login request of ```█████``` subdomain and change ```status``` from ```false``` to ```true```

## Steps To Reproduce:

  1. Open ```████```
  2. Enter ```Admin``` as a Username  and ```███``` as a password 

█████

  3. Press log in and Intercept the request in Burp
```
POST /api/Account/Login/ HTTP/2
Host: ███████
Cookie: ███
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 38
Origin: ████████
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers

{"UserName":"██████","Password":"██████████"}
```

  4. Intercept the response for this request in Burp by >> ```Do Intercept >>Response to this request``` and then Forward this request
  5. Change ```status``` value from ```false``` to ```true``` and Forward the request

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
Expect-Ct: enforce, max-age=7776000, report-uri='███-Allow-Origin: ██████-Allow-Headers: Accept, Content-Type, Origin
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Date: ████ ██████ GMT
Content-Length: 71

{"status":true,"errorMessage":"Username and Password does not match."}
```


  6. Now open ```Report``` , ```Change Password``` and  ```Process Return``` and then Turn off the intercept of the Burp

██████████
█████████
███████

## Supporting Material/References:

POC Video

█████████

## Impact

The attacker can 
- login as an ██████ by bypassing the authentication  
- change the ███ password to takeove the ███ account
- View the company's reports and delete them [1066 Report]
- View processReturn

</details>

---
*Analysed by Claude on 2026-05-24*
