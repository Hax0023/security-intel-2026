# Sensitive PII Data Disclosure - Mobile Numbers and Personal Information Leaked via Waitlist API

## Metadata
- **Source:** HackerOne
- **Report:** 902733 | https://hackerone.com/reports/902733
- **Submitted:** 2020-06-19
- **Reporter:** praseudo7
- **Program:** Curve
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Sensitive Data Exposure, Information Disclosure, Inadequate Access Controls, Lack of Input Validation, Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Curve USA waitlist tracking endpoint at /api/waitlist/us returns sensitive personally identifiable information (PII) including full mobile numbers, addresses, user IDs, and referral codes when queried with only an email address. An attacker can enumerate all waitlisted users by brute-forcing email addresses and collecting their complete personal details without any authentication or authorization checks.

## Attack scenario
1. Attacker identifies the vulnerable /api/waitlist/us endpoint through JavaScript file analysis on curve.com
2. Attacker discovers the endpoint accepts a POST request with only an email parameter: {"email":"target@gmail.com"}
3. Attacker crafts a wordlist or uses common email patterns to systematically enumerate valid email addresses
4. Attacker uses Burp Intruder or similar tools to brute-force the email parameter against the API endpoint
5. For each valid email, the API returns complete user profile including phoneNumber, zipcode, position, referralCode, and _id without requiring authentication
6. Attacker harvests PII data for thousands of users including phone numbers and addresses for potential phishing, SIM swapping, or social engineering attacks

## Root cause
The API endpoint implements no authentication or authorization mechanisms and returns sensitive user data in response to unauthenticated requests. The response payload includes PII that should never be exposed through an enumeration attack. The 'Track my Position' feature was designed to show only position number but the backend exposes all user fields regardless of intended UI constraints.

## Attacker mindset
An attacker would recognize that the UI/UX intentionally limits information display but the underlying API has no corresponding server-side restrictions. By intercepting the actual API request, the attacker realizes they can query user data with minimal information (just email) and systematically enumerate the entire user database. This is a classic case of trusting client-side filtering instead of enforcing server-side authorization.

## Defensive takeaways
- Implement authentication and authorization checks on all API endpoints - never rely on obscurity or frontend restrictions
- Apply principle of least privilege: response payloads should only include data necessary for the specific use case (e.g., position number only for 'track position' feature)
- Implement rate limiting and request throttling on enumeration-prone endpoints to prevent brute-force attacks
- Add logging and anomaly detection for suspicious patterns (multiple rapid requests from single IP, sequential email enumeration)
- Validate that API responses don't leak unintended PII; implement response filtering based on user context and permissions
- Use field-level authorization controls to exclude sensitive fields (phoneNumber, address, referralCode) from unauthenticated or non-owner contexts
- Implement CORS restrictions appropriately - the endpoint had unrestricted access-control-allow-origin: *

## Variant hunting
Check other endpoints in /api/waitlist/* for similar unauthenticated PII exposure (e.g., /api/waitlist/eu, /api/waitlist/uk)
Probe for user enumeration in password reset, registration confirmation, or account lookup endpoints
Investigate whether referralCode field can be used to enumerate or impersonate users in referral systems
Test if _id field can be used to directly query user profiles through other endpoints like /api/users/{id}
Check historical API versions or deprecated endpoints that might have similar enumeration vulnerabilities
Verify if email-based lookups exist in other features (support tickets, contact forms, help desk) with similar issues

## MITRE ATT&CK
- T1190
- T1592
- T1588
- T1589
- T1598
- T1040

## Notes
This is a straightforward but high-impact information disclosure vulnerability. The reporter demonstrated excellent methodology by intercepting the actual request and showing how client-side UI constraints can be bypassed. The CORS header allowing all origins (access-control-allow-origin: *) exacerbates the risk by enabling cross-origin enumeration attacks. The response includes referralCode which could potentially be abused in referral manipulation attacks. The vulnerability affects all users in the waitlist indiscriminately and requires minimal attacker sophistication to exploit at scale.

## Full report
<details><summary>Expand</summary>

Hi,

When am going through all the JS files in curve.com I found a link called "/usa" is used to create Curve USA Waitlists by entering your name, email address, mobile number and address details. 

{F874173}

Then there is a functionality called "Track my Position" by using which joined users can view their position in the waiting lists. 

{F874174}

Well, in UI the application only shows the position number but not any other sensitive details. 

{F874175}

But by using the below reported endpoint an attacker can retrieve all the joined users mobile numbers and the other details by just entering the victims email address.

Steps to Reproduce:
=================
1] Navigate to https://curve.com/usa and click on "Track my position"
2] Enter any email address and click on "Submit"
3] Make sure to intercept the request using Burp intercept
4] You'll be presented with the below vulnerable request

Vulnerable Request:
=================
```
POST /api/waitlist/us HTTP/1.1
Host: website-api.production.curve.app
Connection: close
Content-Length: 30
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
Content-Type: application/json;charset=UTF-8
Origin: https://www.curve.com
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.curve.com/credit?rc=
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

{"email":"praseudo@gmail.com"}
```

5] Now send the above vulnerable request to Burp intruder and brute force the email parameter
6] You'll now be able to retrieve all the waitlisted users mobile numbers, ID's, address and other sensitive information in the response.

Response:
=========
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 268
Connection: close
access-control-allow-origin: *
x-dns-prefetch-control: off
x-frame-options: SAMEORIGIN
strict-transport-security: max-age=15552000; includeSubDomains
x-download-options: noopen
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
etag: W/"10c-Qj52/PIteKYG+1CbKaOCNpKyiDo"
date: Fri, 19 Jun 2020 09:41:26 GMT
x-envoy-upstream-service-time: 3
x-envoy-peer-metadata: Ch4KDElOU1RBTkNFX0lQUxIOGgwxMC4wLjE1Mi4yMDEK0AEKBkxBQkVMUxLFASrCAQoUCgNhcHASDRoLd2Vic2l0ZS1hcGkKIQoRcG9kLXRlbXBsYXRlLWhhc2gSDBoKN2Q5NzRmNTQ3NQokChlzZWN1cml0eS5pc3Rpby5pby90bHNNb2RlEgcaBWlzdGlvCjAKH3NlcnZpY2UuaXN0aW8uaW8vY2Fub25pY2FsLW5hbWUSDRoLd2Vic2l0ZS1hcGkKLwojc2VydmljZS5pc3Rpby5pby9jYW5vbmljYWwtcmV2aXNpb24SCBoGbGF0ZXN0ChoKB01FU0hfSUQSDxoNY2x1c3Rlci5sb2NhbAomCgROQU1FEh4aHHdlYnNpdGUtYXBpLTdkOTc0ZjU0NzUtZHRuZzgKGQoJTkFNRVNQQUNFEgwaCnByb2R1Y3Rpb24KUgoFT1dORVISSRpHa3ViZXJuZXRlczovL2FwaXMvYXBwcy92MS9uYW1lc3BhY2VzL3Byb2R1Y3Rpb24vZGVwbG95bWVudHMvd2Vic2l0ZS1hcGkKHwoPU0VSVklDRV9BQ0NPVU5UEgwaCnZhdWx0LWF1dGgKHgoNV09SS0xPQURfTkFNRRINGgt3ZWJzaXRlLWFwaQ==
x-envoy-peer-metadata-id: sidecar~10.0.152.201~website-api-7d974f5475-dtng8.production~production.svc.cluster.local
server: envoy
X-Cache: Miss from cloudfront
Via: 1.1 1671dd64160321b1f8979341944a5b14.cloudfront.net (CloudFront)
X-Amz-Cf-Pop: MAA50-C2
X-Amz-Cf-Id: kUgxzRYYQ9rJw0zP7oR4PnDz6Rz4bCc6r30M25JrfmOyzp_xuMEHyA==

{"_id":"5eec6b1a958666b5141063e3","name":"Cxvvc","email":"praseudo@gmail.com","phoneNumber":"7013899887","zipcode":"10001","position":4379,"referralCode":"BCeE8mzI","createdAt":"2020-06-19T07:36:58.460Z","updatedAt":"2020-06-19T07:36:58.460Z","__v":0,"status":"EXIST"}
```

Below is the video POC for better understanding:

{F874205}

## Impact

An attacker can retrieve all the joined users PII data (like mobile numbers, address, ID's, etc) by just entering the mail address at "Track my position" at https://curve.com/usa.

Mitigation:
=========
Make sure to remove sensitive response parameters which discloses users PII data.


Regards,
Praseudo

</details>

---
*Analysed by Claude on 2026-05-24*
