# Internal Path Disclosure via Registration Error Message

## Metadata
- **Source:** HackerOne
- **Report:** 2213381 | https://hackerone.com/reports/2213381
- **Submitted:** 2023-10-17
- **Reporter:** mohs3n
- **Program:** Valley Connect (TVA)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Error Message Information Disclosure, SQL Query Structure Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The registration endpoint at valleyconnect.tva.gov discloses sensitive internal information including server file paths, database schema details, and SQL query structures when rate-limited or concurrent requests trigger validation errors. An attacker can enumerate internal system architecture by sending multiple rapid registration requests and observing detailed error responses.

## Attack scenario
1. Attacker navigates to the registration form at https://valleyconnect.tva.gov/registration
2. Attacker intercepts the POST request with a proxy tool (Burp Suite)
3. Attacker uses the Intruder tool to send multiple rapid registration requests, modifying the email parameter for each request to bypass duplicate checks
4. Application detects race condition or concurrency violation and triggers an OptimisticVerificationException
5. Error handler returns detailed stack trace including file path (D:\Agent\_work\1825\s\Code\DataAccessLayer\Classes\RegistrationRequestService.cs:line 193), database table names (sf_dynamic_content), and SQL query structure (UPDATE with WHERE clauses)
6. Attacker extracts internal infrastructure information for further reconnaissance and attack planning

## Root cause
Insufficient error handling and overly verbose exception messages in the registration service. The application uses Telerik OpenAccess ORM which throws detailed exceptions that are not properly caught and sanitized before returning to the client. The error response includes raw stack traces, file system paths, database schema information, and SQL query structures intended only for server-side logging.

## Attacker mindset
Information gathering reconnaissance. The attacker seeks to map the internal application architecture, identify technology stack (Telerik Sitefinity), discover database schema structure, and locate source code file paths. This intelligence supports further attacks such as SQL injection exploitation, targeted exploitation of known vulnerabilities in identified components, or social engineering based on discovered organizational structure.

## Defensive takeaways
- Implement comprehensive error handling that catches all exceptions and returns generic error messages to users
- Never expose stack traces, file paths, database names, or SQL query structures in client-facing error responses
- Use custom error pages that log detailed technical information server-side only while displaying user-friendly messages to clients
- Implement rate limiting and request throttling on registration endpoints to prevent brute force and race condition attacks
- Disable Telerik Sitefinity debug mode in production environments
- Configure proper exception handling middleware to intercept ORM-level exceptions
- Implement input validation and idempotency checks to prevent race condition scenarios
- Use Web Application Firewall (WAF) rules to detect and block automated registration attacks
- Conduct security code review of DataAccessLayer classes handling database operations

## Variant hunting
Search for similar patterns across other endpoints: password reset, login failures, profile updates, and any endpoints with database write operations that may trigger OptimisticVerificationException. Test error conditions like: concurrent submissions, rate limiting triggers, database constraint violations, and transaction rollbacks. Check for similar issues in other Telerik Sitefinity applications using identical error handling patterns.

## MITRE ATT&CK
- T1590.002 - Gather Victim Organization Information: Identify Cloud Infrastructure
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1217 - Browser Bookmark Discovery (reconnaissance)
- T1592 - Gather Victim Identity Information
- T1046 - Network Service Discovery (via error messages)

## Notes
This vulnerability demonstrates a classic information disclosure flaw where detailed error messages aid reconnaissance. The use of concurrent requests to trigger race conditions is a clever technique to force application errors. The Telerik Sitefinity framework and OpenAccess ORM are specifically identified. The file path structure (D:\Agent\_work\) suggests Azure DevOps or similar CI/CD pipeline. Reporter properly identified the need for 'fast and continuous' requests to trigger the condition. This is a Low-to-Medium severity issue as it enables reconnaissance but doesn't directly compromise data; however, in defense-in-depth scenarios, it could facilitate chaining with other vulnerabilities.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi team,
when we call too many register query, we get  error, in this error we can see internal path and sql query structure

## Steps To Reproduce:
1. go to register form https://valleyconnect.tva.gov/registration 
2. complete form and click on submit registration, then intercept request with burp
3. use intruder for call multiple request, we should replace email in every request.

```
POST /registration HTTP/2
Host: valleyconnect.tva.gov

UserName=admin&Password=jgn%25%5EThgf%23rfvHRESdy56tef&ConfirmPassword=jgn%25%5EThgf%23rfvHRESdy56tef&EmailAddress=Z%40jetamooz.com&EmailAddressVerify=Z%40jetamooz.com&FirstName=alex&LastName=jane&Initials=&Suffix=&JobTitle=it&OrganizationType=Business+Partner&OrganizationName=sarv&Country=792&StreetAddress=sary&City=katy&Province=titi&State=AL&ZipCode=&PhoneNumber=%28934%29+734-4364&MobilePhoneNumber=%28957%29+363-4655&TimeZone=America%2FLos_Angeles&CapAnswer=U4YIQ&CapKey=XXTxVOUWZrCz6buVtsgF2cFaPHLSCKVSRQc4z4My13Bee8JiTYVZXmiPd8zLSbMc&BeCheck=
```

response :
```
 Failed to request registration. Please try again or contact support. Error: Telerik.OpenAccess.Exceptions.OptimisticVerificationException: Row not found: GenericOID@b5128f1e RegistrationRequest base_id=1f499ef7-83fa-4a77-8fd9-693b52c4db9b
UPDATE [sf_dynamic_content] SET [last_modified] = @p0, [voa_version] = @p1 WHERE [base_id] = @p2 AND [voa_version] = @p3
Batch Entry 0 (set event logging to all to see parameter data)
   at Telerik.Sitefinity.Data.TransactionManager.CommitTransaction(String transactionName)
   at DataAccessLayer.Classes.RegistrationRequestService.AddRegistrationRequest(RegistrationRequestEntry model) in D:\Agent\_work\1825\s\Code\DataAccessLayer\Classes\RegistrationRequestService.cs:line 193
```

## Tips:
we should insert fast and continuous for geting error

## Supporting Material/References:
{F2781135}
{F2781143}

## Impact

Impact

</details>

---
*Analysed by Claude on 2026-05-24*
