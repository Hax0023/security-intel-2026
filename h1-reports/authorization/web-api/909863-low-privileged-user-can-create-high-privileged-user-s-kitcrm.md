# Low Privileged User Can Create High Privileged User's KITCRM Authorization Token and Perform Unauthorized Actions

## Metadata
- **Source:** HackerOne
- **Report:** 909863 | https://hackerone.com/reports/909863
- **Submitted:** 2020-06-27
- **Reporter:** sandeep_rj49
- **Program:** Shopify/KIT CRM
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Privilege Escalation, Insecure Direct Object Reference (IDOR), Token Generation Flaw, Insufficient Authorization Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A low-privileged user without access to Shopify Ping can exploit a flawed token generation API endpoint to create authorization tokens for any high-privileged user by specifying their staff member ID. This allows unauthorized access to view and send messages impersonating senior users in the KIT integration.

## Attack scenario
1. Attacker creates a low-privileged user account in target Shopify store with minimal permissions
2. Attacker authenticates to Shopify Ping using low-privileged credentials to obtain an access_token
3. Attacker identifies target high-privileged user's staff member ID through enumeration or store information
4. Attacker sends POST request to /api/v1/arro_token with low-privileged token and high-privileged user's ID parameter
5. Attacker receives high-privileged user's KITCRM authorization token in response without proper authorization check
6. Attacker uses stolen token to read confidential KIT conversations and send unauthorized instructions impersonating the high-privileged user

## Root cause
The /api/v1/arro_token endpoint performs insufficient authorization validation. It trusts the user-supplied 'id' parameter to generate tokens for ANY user without verifying if the requesting user has permission to access that user's credentials. The application fails to enforce that a user can only generate tokens for their own account, not arbitrary users.

## Attacker mindset
An internal threat actor or compromised low-privileged account seeking to escalate privileges and perform malicious actions (create discounts, send phishing emails, modify campaigns) while maintaining attribution to high-privileged users to avoid detection and accountability.

## Defensive takeaways
- Implement strict authorization checks: Verify that users can only generate tokens for their own account, not arbitrary user IDs
- Apply principle of least privilege: Token generation endpoints should reference the authenticated user context, not accept user IDs as parameters
- Validate permission scope: Cross-reference the requested user ID against the requester's actual permissions before token generation
- Implement comprehensive audit logging: Log all token generation requests with user context to detect privilege escalation attempts
- Use scoped tokens: Limit token scope and validity period rather than generating full-access tokens for other users
- Rate limit token generation: Detect enumeration attempts of user IDs through API request throttling
- Separate token generation APIs: Maintain distinct, properly gated endpoints for generating personal vs. administrative tokens

## Variant hunting
Check other Shopify integration endpoints for user ID parameter acceptance without proper authorization (e.g., /api/v1/user, /api/v1/settings)
Test if low-privileged users can generate tokens for other business entities or stores
Verify if the vulnerability extends to API keys generation endpoints
Check if user enumeration is possible through error message differentiation in token generation responses
Test if the 'myshopify_domain' parameter can be manipulated to access other stores' users
Investigate if the same flaw exists in other Shopify Ping-integrated applications

## MITRE ATT&CK
- T1190
- T1548
- T1548.002
- T1087
- T1078
- T1078.001
- T1556

## Notes
This is a critical privilege escalation chain requiring minimal user interaction. The vulnerability's severity is amplified by the difficulty in attribution—actions performed under stolen high-privileged tokens create accountability ambiguity. The fact that token generation lacks basic authorization checks suggests systemic security issues in the API design. The vulnerability chain demonstrates the danger of trusting user-supplied identifiers without proper authorization validation. Shopify Ping's mobile app context may have increased the likelihood of this oversight during development.

## Full report
<details><summary>Expand</summary>

Using the Shopify ping application a user can communicate with the kit. The kit is an application that creates tasks based on the information supplied through the Shopify ping app by a user. With a few quick messages to Kit using Shopify Ping,  a user can create a discount code and promote it, start a retargeting campaign to bring visitors back to your store, send thank you emails to customers, and much more!

###Who has access to the Shopify PING application?
Full permission users have access to the Shopify ping application. And they can communicate with KIT also using the Shopify ping application.

Low privileged user having no or very low permission is not allowed to log in to the Shopify ping application and thus not allowed to communicate with the kit application.

### What is the bug?
Low privileged who do not have access to the Shopify ping application can create a Shopify ping access token using the login API. Using the Shopify ping access token, a low privileged user can create any user's  KITCRM authorization token. 

While creating the KITCRM authorization token, the vulnerable request asks for user id (staff member id). A low privileged user can create the high privileged user's   KITCRM authorization token by supplying the high privileged user's id in the id parameter of the vulnerable request 1. The response will disclose the high privileged user's KITCRM authorization token. Using the high privileged user's KITCRM authorization token, a low privileged user can read the conversation between high role user and kit and can also send the new instructions to kit using high privileged user token.

###Vulnerable request 1:

Request 1: Generate a high role user's KITCRM authorization token using low privileged user's Shopify ping access token.

```
POST /api/v1/arro_token?access_token=███████&myshopify_domain=alwayzhack.myshopify.com&id=42668326968 HTTP/1.1
Host: www.kitcrm.com
Content-Type: application/json
Cookie: 
Connection: close
Accept: application/json
X-DeviceID: 
User-Agent: Shopify Ping/iOS/2.5.4 (iPhone12,3/com.shopify.ping/13.1.1) - Build 3006
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Content-Length: 0
```
Supply low privileged user's Shopify ping access token in `access_token` parameter value. Change `myshopify_domain ` with yours and `id` parameter value with high privileged user's staff memberid. The response will disclose high privileged user's KITCRM authorization token.

Response:
████████

Request 2: Display high privileged user's communication with kit

```
GET /api/v2/messages HTTP/1.1
Host: www.kitcrm.com
Content-Type: application/json
Cookie: 
Connection: close
Accept: application/json
User-Agent: Shopify Ping/2.5.4 (com.shopify.ping; build:3006; iOS 13.1.1) Alamofire/4.8.2
Authorization: Bearer ████████
Accept-Encoding: gzip, deflate
Accept-Language: en-IN;q=1.0, hi-IN;q=0.9
```

Request 3: Send message to kit using high privileged user's chatbox

```
POST /api/v2/messages HTTP/1.1
Host: www.kitcrm.com
Accept: application/json
Authorization: Bearer 1fbb7a0ebb0dd18c2f3697f51fde49a541a30608255d9a1a258XXXXXXXX
Accept-Encoding: gzip, deflate
Accept-Language: en-us
Content-Type: application/json
Content-Length: 40
X-Shopify-Access-Token: 
Connection: close
X-DeviceID: 
User-Agent: Shopify Ping/iOS/2.5.4 (iPhone12,3/com.shopify.ping/13.1.1) - Build 3006

{
  "incoming_message" : "testtesthai"
}
```

Steps to reproduce:
1. login to the Shopify ping application using high privileged user account credentials.
2. Do some chat with the kit in Shopify ping.
3. Add a low privileged user in your Shopify test account and assign no or very low permission to the low privileged user.
3. Use Shopify ping login API - `POST /admin/api/xauth HTTP/1.1` to create a low privileged user's access token using low privileged user account credentials. 
4. Use low privileged user's Shopify ping access token in the vulnerable request 1. 
5. Input high privileged user's staff member id in the `id` parameter of the vulnerable request 1. 
6. Replay the vulnerable request 1 in the burp suite proxy. The response will disclose high privileged user's KITCRM authorization token.
7. Use high privileged user's authorization token in vulnerable request 2 to view  high privileged user's chat with the kit.
8. To send the command to the kit, replay the vulnerable request 3 with high privileged user's KITCRM authorization token. Instruction will be sent to the kit.

## Impact

A low privileged user can create high privileged user's KITCRM authorization token and can view high privileged user's communication with kit. Also, low privileged users can give new instructions to kit using the discovered high privileged user authorization token. 

When all the communication will be done using a high privileged user account, so tracking the attacker will be difficult.

</details>

---
*Analysed by Claude on 2026-05-24*
