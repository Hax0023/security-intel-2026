# User Can Upload Files After Account Closure

## Metadata
- **Source:** HackerOne
- **Report:** 1020371 | https://hackerone.com/reports/1020371
- **Submitted:** 2020-10-27
- **Reporter:** h4x0r_dz
- **Program:** Basecamp (Hey.com)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Improper Authentication, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A closed account user retains the ability to upload files via the Active Storage direct upload endpoint, bypassing account status validation. The application fails to check whether a user's account is active before processing upload requests, allowing closed account users to upload files to S3 storage using valid session cookies and CSRF tokens.

## Attack scenario
1. Attacker creates a Hey.com account and uploads a test file to learn the upload endpoint structure
2. Attacker records the POST request to /rails/active_storage/direct_uploads in Burp Suite
3. Attacker intentionally closes their account, triggering the deactivation workflow
4. Attacker logs back in and captures a valid CSRF token and active session cookie from the closed account session
5. Attacker replays the recorded upload request using the new CSRF token and session cookie
6. Application accepts the upload request and returns signed S3 URLs allowing file persistence despite account closure

## Root cause
The Active Storage direct upload endpoint lacks authentication state validation. The application only validates CSRF tokens and session cookies but fails to verify that the authenticated user's account is in an active state. This allows users with valid credentials but closed accounts to continue uploading files to cloud storage.

## Attacker mindset
An attacker with a closed account seeks to continue uploading files, potentially to exfiltrate data, upload malicious content, or maintain persistence. The attacker leverages Burp Suite to intercept and replay requests, demonstrating that account closure status is not enforced server-side at the upload endpoint.

## Defensive takeaways
- Implement account status validation on all authenticated endpoints, particularly file upload operations
- Check account.active? or equivalent status flag before processing any user requests
- Audit Active Storage integration to ensure all upload endpoints enforce proper authorization checks
- Consider invalidating all active sessions upon account closure rather than relying on endpoint-level checks
- Implement rate limiting and anomaly detection on upload endpoints to catch replayed requests
- Add logging and alerts for upload attempts by closed accounts
- Periodically audit authorization logic across all API endpoints that modify state or create resources

## Variant hunting
Check if other file operations (delete, download, share) are also accessible by closed accounts
Test if closed accounts can access other authenticated endpoints beyond uploads
Verify if closing an account properly revokes all associated API tokens and sessions
Test if closed accounts can still attach files to existing messages or emails
Check if the signed S3 URLs from closed account uploads are valid after long periods
Test account reactivation workflows to see if they properly reset upload permissions

## MITRE ATT&CK
- T1190
- T1199
- T1550.001

## Notes
This vulnerability demonstrates a common authorization bypass pattern where application-level access control is insufficient. While CSRF and session validation are present, the absence of business logic validation (account active status) creates a critical gap. The use of signed S3 URLs with 300-second expiration extends the attack window. The reporter provided clear reproducible steps with request/response examples, suggesting this was a straightforward authorization bypass rather than a complex exploitation chain.

## Full report
<details><summary>Expand</summary>

Summary:
===========================

Hello @basecamp This is my first report on your program and I hope to end well :) .

I was testing https://app.hey.com/ and I my account has been closed, so I back to the requests history, and I tried to send these requests even my account closed.

and I found that the user can still upload files even his account closed.

 Steps To Reproduce:
================ 
I have already a closed account. to Reproduce this bug you can create a new account and closed.


1.run burp suite and go to https://app.hey.com and create a new account 
2. upload any file  and send the `POST app.hey.com/rails/active_storage/direct_uploads` request to the repeater  
3. close the account 

4.  login to the closed account on https://app.hey.com/ and you will find this page :

{F1054506}


5. intercept the page and find `csrf-token` and put it on `X-CSRF-Token:` header in `POST app.hey.com/rails/active_storage/direct_uploads` request.
and change the Cookie for the new one.

6. back to burp history , you will find ths PUT request (send it to repater )`https://haystack-production-storage-us-east-1.s3.amazonaws.com/<key>?x-amz-storage-class=<>&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<>&X-Amz-Date=<>&X-Amz-Expires=300&X-Amz-SignedHeaders=content-length%3Bcontent-md5%3Bcontent-type%3Bhost&X-Amz-Signature=<>`

it contains the file content that you uploaded .

7. send this request :

```
POST /rails/active_storage/direct_uploads HTTP/1.1
Host: app.hey.com
Connection: close
Content-Length: 116
Accept: application/json
X-CSRF-Token:<your_CSRF-Token>
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36
Content-Type: application/json
Origin: https://app.hey.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://app.hey.com/messages/support/new
Accept-Encoding: gzip, deflate
Accept-Language: ar,en-US;q=0.9,en;q=0.8
Cookie: <your_Cookie>

{"blob":{"filename":"<filename>","content_type":"<content_type>","byte_size":338,"checksum":"<checksum>"}}`
```

in the response you will find something like THis :

```
HTTP/1.1 200 OK
Date: Tue, 27 Oct 2020 22:40:16 GMT
Content-Type: application/json; charset=utf-8
Connection: close
Server: openresty
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: strict-origin-when-cross-origin
Vary: Accept
Set-Cookie: force-primary-dc=1; path=/; max-age=3; secure
Set-Cookie: authenticity_token=ie9Iq%2By2%2B8dqEzgfYEgCWcFvD0jJ3DGH999TM8ObvceSNnk%2Beb79Myae2rImhpXVn%2F%2BD1nz3onYUawGbYZVicA%3D%3D; path=/; expires=Sat, 27 Oct 2040 22:40:16 GMT; SameSite=Lax; secure
Set-Cookie: _haystack_session=ErWRGp2IIXTWN2OcrubqWOK9GYsf1M4J%2BEQEboc%2BsTyF3Crrc8fOxS5QFq6DnhptMAqsHuToydbTzRnobqBtiR2sLiYetn4rNSit80siXqea7l0OE6fadEjpE4pA8wpHYN71HCSiJPtC%2FX0Ft9svU8xN0ybaczRDjWJi5I%2F3Qz4rPyuAdFSwHpoPrSOOC%2BYXIqeE55OBpI0VBH6IhAggK4dFiRb1Cs8jiaXVXqD%2Bi7A81ZFIw%2BLwZng0187SHY4SEaU5raCFkXuRJ6BDoq0wK8Sr5haLjTvUxFzdYdYLmsnDcslKzGb5QVNV62d9NbcmAJ6O7ZQh0vK8LxrEFA%3D%3D--pKSAzE6vGEr77yCg--R9MNGFlyj98MLnbKaX5h0Q%3D%3D; path=/; secure; HttpOnly
ETag: W/"9101e50c2c6269212bb817279c93a1e6"
Cache-Control: max-age=0, private, must-revalidate
X-Request-Id: 42cb6125062852dd41f9ae7d
X-Runtime: 0.021788
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Region: us-east-1
Content-Length: 1283

{"id":165504432,"key":"fyeem62eqa2ipopoty6c5j0aye3t","filename":"xss.svg","content_type":"image/svg+xml","metadata":{},"byte_size":338,"checksum":"QvuRT8WQtAGYrfSb+pmYdQ==","created_at":"2020-10-27T22:40:16.000000Z","service_name":"production","signed_id":"eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCTEJsM1FrPSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--4c4a7ab7c81958dee84da90fd0e5d2f759d5330f","attachable_sgid":"BAh7CEkiCGdpZAY6BkVUSSI8Z2lkOi8vaGF5c3RhY2svQWN0aXZlU3RvcmFnZTo6QmxvYi8xNjU1MDQ0MzI_ZXhwaXJlc19pbgY7AFRJIgxwdXJwb3NlBjsAVEkiD2F0dGFjaGFibGUGOwBUSSIPZXhwaXJlc19hdAY7AFQw--ee2d9e3be264f7c2628062c9d0bfd3260dbd1377","direct_upload":{"url":"https://haystack-production-storage-us-east-1.s3.amazonaws.com/fyeem62eqa2ipopoty6c5j0aye3t?x-amz-storage-class=INTELLIGENT_TIERING\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\u0026X-Amz-Credential=AKIAQ742G4ISOGL5I25G%2F20201027%2Fus-east-1%2Fs3%2Faws4_request\u0026X-Amz-Date=20201027T224016Z\u0026X-Amz-Expires=300\u0026X-Amz-SignedHeaders=content-length%3Bcontent-md5%3Bcontent-type%3Bhost\u0026X-Amz-Signature=4c158a4ecc84191abb75e4a5670dff3979cfd1e5e06cf3006c8492260b5a4f96","headers":{"Content-Type":"image/svg+xml","Content-MD5":"QvuRT8WQtAGYrfSb+pmYdQ==","Content-Disposition":"inline; filename=\"xss.svg\"; filename*=UTF-8''xss.svg"}}}
```

back to PUT request in haystack-production-storage-us-east-1.s3.amazonaws.com and change the AWS keys with the new one that you got in the Response. and in the body, you can put anything.

send the PUT request, and back to the previous response and copy `signed_id` value and put it here with the filename.

`https://app.hey.com/rails/active_storage/blobs/redirect/<signed_id>/<filename>`

and you can see you able to upload files even your account is closed.



 ### POC

## Impact

Unauthenticated users at https://app.hey.com/ can upload files after close his account.

</details>

---
*Analysed by Claude on 2026-05-24*
