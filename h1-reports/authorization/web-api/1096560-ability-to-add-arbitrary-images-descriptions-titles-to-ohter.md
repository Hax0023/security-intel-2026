# Insecure Direct Object Reference (IDOR) on Issue Media Upload - getrevue.co

## Metadata
- **Source:** HackerOne
- **Report:** 1096560 | https://hackerone.com/reports/1096560
- **Submitted:** 2021-02-05
- **Reporter:** mirhat
- **Program:** getrevue.co
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Missing Authorization Check, Horizontal Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability exists in the `/app/items` endpoint that allows authenticated attackers to add images, descriptions, and titles to other users' issues by manipulating the 'issue' parameter in the request. This enables unauthorized modification of arbitrary issues and potential account hijacking or data manipulation.

## Attack scenario
1. Attacker authenticates to getrevue.co and creates their own issue to understand the media upload workflow
2. Attacker navigates to their issue and attempts to upload an image via the Media section
3. Attacker intercepts the POST request to `/app/items` containing their issue ID
4. Attacker modifies the 'issue' parameter to a victim's issue ID (e.g., 347976) while keeping other malicious payloads (title, description, author fields)
5. Attacker sends the modified request, successfully adding content to the victim's issue
6. Victim's issue is now modified with attacker-controlled content (images, descriptions, titles), potentially hijacking the issue or spreading misinformation

## Root cause
The backend endpoint `/app/items` performs insufficient authorization checks. The application validates that the user is authenticated but fails to verify that the user owns or has permission to modify the target issue identified by the 'issue' parameter. The endpoint trusts the client-supplied issue ID without server-side ownership validation.

## Attacker mindset
An attacker with valid credentials could systematically enumerate issue IDs and modify other users' content. The ease of exploitation (simple parameter modification) combined with high impact (content hijacking) makes this an attractive target. The attacker could deface issues, inject malicious links/descriptions, or damage user reputation.

## Defensive takeaways
- Implement explicit authorization checks on all endpoints - verify the authenticated user owns/has permission for the resource before allowing modifications
- Use indirect references (UUIDs, hashed tokens) instead of sequential numeric IDs to make enumeration harder
- Apply principle of least privilege - extract resource ownership from server-side session context rather than trusting client input
- Validate all request parameters server-side, especially resource identifiers
- Implement comprehensive logging and alerting for unauthorized access attempts
- Add rate limiting on resource enumeration attempts
- Conduct authorization testing across all CRUD endpoints during security reviews

## Variant hunting
Check other endpoints accepting 'issue' or similar resource identifiers - likely vulnerable to same IDOR pattern
Test comment/reply endpoints for IDOR on issues and other collaborative features
Examine user profile modification endpoints for similar authorization bypass
Check publication/collection endpoints for IDOR vulnerabilities
Review all API endpoints that accept numeric IDs to identify sequential enumeration opportunities
Test batch operations that might accept multiple resource IDs
Check for IDOR in sharing/permission endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force (for ID enumeration)
- T1566 - Phishing (using modified issue content to inject malicious links)
- T1195 - Supply Chain Compromise (content injection into trusted issues)

## Notes
The vulnerability demonstrates a common authorization pattern failure where authentication is properly implemented but authorization is missing. The sequential numeric issue ID (347976) makes enumeration trivial. The lack of CSRF protection validation on the IDOR itself (though CSRF token is present) suggests layered security failures. The video POC confirms practical exploitability. This is a clear example of horizontal privilege escalation affecting data integrity across the platform.

## Full report
<details><summary>Expand</summary>

**Summary:** 

Hi team,
I discovered a vulnerability that allows an attacker to add arbitrary images/descriptions/titles to other people's issues via IDOR

**Description:**

It's possible to perform a IDOR attacker on `getrevue.co`when adding a image to your issue it's also possible to add descriptions and more to other people's issue

## Steps To Reproduce:

   1. Go to `getrevue.co` and Sign In
   2. Click on Issues then Click on Add new issue
   3. Go to the Issue that you created and from the bottom of the page Click on Media
   4. Turn on the Intercept and Upload image
   5. On the request change the ID to your other account's issue ID

Request:

```
POST /app/items HTTP/1.1
Host: www.getrevue.co
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://www.getrevue.co/app/issues/current
X-CSRF-Token: qbWPNjfb12c1Plj7WrYDYgQFgWl2IaZr6/Qr/Vf5WyaDGyf68jn1mzx3xwtgFxBBX19RkHs/YHiREA7Ae6PGqg==
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 519
Origin: https://www.getrevue.co
Connection: close
Cookie: [YOUR_COOKIE]

{"item_type":"image","issue":347976,"id":null,"title":"Your account has been hacked","url":"","description":"Your account has been hacked","author":"Your account has been hacked","publication":"Your account has been hacked","section":"Your account has been hacked","image":"https://revue-direct-production.s3.amazonaws.com/cache/30fd80f79ad919f1e310aa97e0ab7940/7dc308f18b70ba627eb954d2d5376bea.png","image_file_name":"","created_at":"","tweet_handle":"","tweet_profile_image":"","tweet_description":"","tweet_lang":""}
```

POC video:

{F1185366}

## Impact

Ability to add arbitrary images/descriptions/titles to other people's issues
It's possible to hijack other people's issues

</details>

---
*Analysed by Claude on 2026-05-24*
