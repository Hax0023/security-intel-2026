# access to profile & reset password page without authentication

## Metadata
- **Source:** HackerOne
- **Report:** 2213337 | https://hackerone.com/reports/2213337
- **Submitted:** 2023-10-17
- **Reporter:** mohs3n
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary:
Hi team,
when i checking https://valleyconnect.tva.gov i see we are login! and in top of page see : Hello, null. and we can access to some internal page like  Reset Password.
                       

## Steps To Reproduce:
1. go to https://valleyconnect.tva.gov
2. click on [reset passwod menu](https://valleyconnect.tva.gov/password-rules)

## Tips
by default we are login in portal and 

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

## Summary:
Hi team,
when i checking https://valleyconnect.tva.gov i see we are login! and in top of page see : Hello, null. and we can access to some internal page like  Reset Password.
                       

## Steps To Reproduce:
1. go to https://valleyconnect.tva.gov
2. click on [reset passwod menu](https://valleyconnect.tva.gov/password-rules)

## Tips
by default we are login in portal and we can get status code 200 from below  Api :
```
GET /customapi/v1/user/getbasicprofileinfo HTTP/2
Host: valleyconnect.tva.gov
```

response is :
```
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8

"{\"username\":null,\"email\":null,\"orgId\":null,\"hasRemoteAssistanceGrant\":false}"
```
we can access to favorites too:
```
GET /customapi/v1/user/getuserfavorites 
```

response is :
```
HTTP/2 200 OK
Date: Tue, 17 Oct 2023 14:45:02 GMT

""
```

## Supporting Material/References:

  * {F2780981}
  * {F2780983}

## Impact

Improper Authentication leads to access to internal page like reset password and profile page.

</details>

---
*Analysed by Claude on 2026-05-24*
