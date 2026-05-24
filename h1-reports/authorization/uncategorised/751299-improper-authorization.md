# Improper Authorization - Admin Can Demote Organization Owner

## Metadata
- **Source:** HackerOne
- **Report:** 751299 | https://hackerone.com/reports/751299
- **Submitted:** 2019-12-04
- **Reporter:** abdellah29
- **Program:** Stripo
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Authorization, Broken Access Control, Insufficient Input Validation, Client-Side Security Control Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An authenticated admin user can bypass disabled UI controls by manipulating the DOM to change the organization owner's role to admin, effectively removing the owner from their privileged position. Once demoted, the original owner loses access to the account and cannot regain control of the organization.

## Attack scenario
1. Attacker creates or is invited to an organization as an admin user
2. Attacker navigates to the user management endpoint and inspects the role input field which is disabled for the owner
3. Attacker uses browser developer tools (F12) to enable the disabled input field and change the owner's role from 'owner' to 'admin'
4. Attacker sends a PUT request to /cabinet/stripeapi/v1/organizations/{orgId}/users with the modified role parameter
5. Backend server accepts the request without proper authorization checks and demotes the owner to admin
6. Original owner discovers they are no longer the owner and cannot log back into their account or regain control

## Root cause
The backend API endpoint /cabinet/stripeapi/v1/organizations/{orgId}/users fails to validate authorization rules on the server-side. While the frontend UI disables role modification controls for the owner (relying on client-side security), the backend does not enforce that only certain roles (or none) can modify an owner's role. The server trusts client-provided input without verifying the requester's permissions and role hierarchy constraints.

## Attacker mindset
An admin user with legitimate access seeks to take control of the organization by removing the owner. They recognize that UI controls (disabled input fields) are merely client-side restrictions and can be bypassed using developer tools. They exploit the trust the backend places in client-side security controls and the lack of server-side authorization validation.

## Defensive takeaways
- Implement server-side authorization checks for all sensitive operations, never rely solely on client-side UI restrictions
- Enforce role-based access control (RBAC) rules at the API level - validate that the requester has permission to modify user roles before processing requests
- Protect the owner role with special rules that prevent any user (including admins) from demoting the owner without additional verification
- Implement audit logging for role changes and account modifications to detect suspicious activity
- Add multi-factor confirmation or approval workflow for critical operations like owner role changes
- Validate that role changes maintain at least one owner in the organization at all times
- Implement proper input validation and sanitization on all API endpoints
- Use security headers and implement Content Security Policy to prevent DOM manipulation attacks

## Variant hunting
Check if other sensitive user attributes (suspension status, permissions, email) can be modified through similar authorization bypass
Test if other privileged operations (project deletion, organization settings changes) have the same server-side validation weakness
Investigate if other role types (editor, viewer) can be granted owner-equivalent permissions through role modification
Check if the authorization check is missing for batch user management operations
Test if organization admins can modify their own roles or other admin roles in ways that shouldn't be allowed
Verify if the same vulnerability exists in other endpoints that manage organizational hierarchy or permissions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (DOM manipulation of disabled controls)
- T1548 - Abuse Elevation Control Mechanism (bypassing role restrictions)
- T1078 - Valid Accounts (using legitimate admin account to escalate privileges)
- T1556 - Modify Authentication Process (effectively locking out owner from account)

## Notes
The vulnerability demonstrates a classic security mistake where developers implement access controls on the client-side but fail to enforce them server-side. The disabled input field was security through obscurity - easily bypassed with developer tools. The impact is severe as it results in account takeover and denial of access to the legitimate owner. This is a critical control bypass that should have been caught during security code review. The attack requires prior admin access, making it a privilege escalation vulnerability.

## Full report
<details><summary>Expand</summary>

hi there ,

i found an vulnerability on  https://my.stripo.email/cabinet/#/users/orog_id ,

generally every user have an organisation and the organisation contain projects , 

lets suppose : test@gmail.com is the owner of the project

and test2@gmail.com was invited to his project as admin , in normal situation the owner can not be removed even if second account is admin

the issue is i can removed the owned from hi position to admin , and the big problem once the owner is removed he can not login again to his account


## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. you must have 2 account , one owner , the second got invited as admin

  2. log in with your second account and go to https://my.stripo.email/cabinet/#/users/xxxx

       you will see that the input of role is disabled , enable it via inspect element ( f12) , 

then change the role of owner for it to admin , an PUT request will be sent

##http request

PUT /cabinet/stripeapi/v1/organizations/135428/users HTTP/1.1
Host: my.stripo.email
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Bearer null
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache
Pragma: no-cache
Expires: Sat, 01 Jan 2000 00:00:00 GMT
Content-Length: 231
Origin: https://my.stripo.email
Connection: close
Referer: https://my.stripo.email/cabinet/
Cookie: __stripe_mid=f1a62f3d-2ba4-4742-a1ae-97c309223fec; __stripe_sid=20155b5b-e547-4e52-9c4c-53fd4b08ed8a; _ga=GA1.2.472610903.1575449565; _gid=GA1.2.1705021668.1575449565; _fbp=fb.1.1575449579810.16963820; token=eyJhbGciOiJIUzI1NiJ9.eyJzZWN1cml0eUNvbnRleHQiOiJ7XCJ1c2VySW5mb1wiOntcImlkXCI6MTMwODUxLFwiZW1haWxcIjpcImFiZGVsbGFobmFkaTNAZ21haWwuY29tXCIsXCJsb2NhbGVLZXlcIjpcImVuXCIsXCJmaXJzdE5hbWVcIjpcInRlc3Q0NVwiLFwibGFzdE5hbWVcIjpcIm5cIixcImdhSWRcIjpcImJiYzBkNGExLWI5NDYtNDIwMy1iOTNmLTcxNjhmYmEyMWI5ZVwiLFwicGhvbmVzXCI6W10sXCJhY3RpdmVcIjpmYWxzZSxcImFjdGl2ZVByb2plY3RJZFwiOjEzNzg3NyxcImlzU3VwZXJVc2VyXCI6ZmFsc2UsXCJzdXBlclVzZXJWMlwiOmZhbHNlLFwib25seUZiQ3JlZGVudGlhbHNcIjpmYWxzZSxcInNldHRpbmdzRW1haWxTb3J0QnlcIjpcImNyZWF0ZWRUaW1lXCIsXCJzZXR0aW5nc0VtYWlsU29ydEFzY1wiOmZhbHNlLFwic2V0dGluZ3NUZW1wbGF0ZVNvcnRCeVwiOlwidXBkYXRlZFRpbWVcIixcInNldHRpbmdzVGVtcGxhdGVTb3J0QXNjXCI6ZmFsc2UsXCJjb2xvclwiOlwiI2ZiYTc2ZlwiLFwib3JnYW5pemF0aW9uSWRcIjoxMzA2NjUsXCJzdWJzY3JpcHRpb25UeXBlXCI6XCJGUkVFXCIsXCJjb25zZW50UmVjZWl2ZWRcIjp0cnVlLFwidGVtcGxhdGVDcmVhdGVkT25Mb2dpblwiOmZhbHNlLFwiZmlyc3RMb2dpblwiOmZhbHNlfSxcImlzc3VlZEF0XCI6MTU3NTQ1MDIzMDMxOH0ifQ.GidxPLc4Wu80JWxScUjLrq4nmLr2lEamONcWsATBQfY; intercom-session-b1m243ec=Tlk4aHpydmFMOTc5SlZRaGRabE43WUIwanoxdXAyNlowR3FWbE9oaXNDRm5mYlhRRHNBNjlyLzJOOWQybmtYQi0tZzUrdnd1enBReWhPM0J3M1N2SFIzUT09--a917964bb8221fad0a6d3e38fab8cde2af1efed4

{"repository":{},"idField":"id","entityType":"USER","id":135628,"role":"admin","organizationId":135428,"firstName":"TESt","lastName":"account","color":"#cc90e2","email":"pain45@wearehackerone.com","projectIds":[],"suspended":false} 

##http response :


HTTP/1.1 200 
Server: nginx
Date: Wed, 04 Dec 2019 09:56:41 GMT
Content-Type: application/json;charset=UTF-8
Connection: close
Vary: Accept-Encoding
█████████
████
X-Frame-Options: sameorigin
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Length: 180

█████cc90e2","email":"pain45@wearehackerone.com","projectIds":[],"suspended":false}

i hope it is clear , 

thanks

## Impact

an attacker ( already admin ) can remove the owner from his role , and the last one can not login any more to his account

</details>

---
*Analysed by Claude on 2026-05-24*
