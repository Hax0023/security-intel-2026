# Registered Users Contact Information Disclosure on Salesforce Lightning Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1443654 | https://hackerone.com/reports/1443654
- **Submitted:** 2022-01-07
- **Reporter:** rptl
- **Program:** GSA (General Services Administration) - https://disposal.gsa.gov
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Improper Access Control, Insecure Direct Object References (IDOR), API Abuse
- **CVEs:** None
- **Category:** web-api

## Summary
A Salesforce Lightning endpoint at https://disposal.gsa.gov failed to properly validate authorization on the SelectableListDataProvider controller, allowing authenticated users to retrieve sensitive contact information of all registered users in the system. By manipulating the message parameter in POST requests to /s/sfsites/aura, an attacker could enumerate and extract PII including names, email addresses, phone numbers, and internal Salesforce IDs.

## Attack scenario
1. Attacker creates a legitimate user account on disposal.gsa.gov and completes email verification
2. Upon login, attacker monitors HTTP traffic and identifies POST requests to /s/sfsites/aura endpoint used for Aura framework communication
3. Attacker crafts a malicious POST request targeting the SelectableListDataProviderController with descriptor 'serviceComponent://ui.force.components.controllers.lists.selectableListDataProvider.SelectableListDataProviderController/ACTION$getItems'
4. Attacker modifies the message parameter to request Contact entity data with pageSize of 1000 records, while preserving valid aura.context and aura.token from legitimate session
5. Endpoint processes request without verifying user authorization to access Contact records and returns full Contact object details including LastName, FullName, Email, Phone, and system IDs
6. Attacker iterates through multiple pages or adjusts parameters to extract complete contact database of all users

## Root cause
Insufficient authorization checks in the Salesforce Lightning Aura framework component. The SelectableListDataProviderController's getItems action failed to validate whether the authenticated user had proper permissions to access Contact record data. The framework accepted any authenticated session token without enforcing field-level security (FLS) or record-level security (RLS), allowing the controller to return sensitive PII that should have been restricted.

## Attacker mindset
An insider threat or low-privilege user seeking to harvest contact information from the government disposal system. The attacker recognized that Salesforce Aura endpoints are often overlooked in security testing and that component-level authorization is frequently misconfigured. By leveraging a valid authentication token, the attacker bypassed frontend restrictions to directly query backend data APIs.

## Defensive takeaways
- Implement strict authorization checks at the Aura component controller level for all data retrieval methods, not relying solely on frontend security
- Enforce Salesforce Field-Level Security (FLS) and Record-Level Security (RLS) policies at the API layer to prevent unauthorized data access
- Validate that authenticated users have explicit permissions to access the requested entity (Contact) and its fields before returning data
- Implement rate limiting and request throttling on Aura endpoints to detect and block enumeration attempts
- Audit all custom Aura controllers and service components for authorization bypass vulnerabilities
- Apply principle of least privilege - authenticated users should only access data required for their specific role
- Monitor and log all Aura framework API calls for suspicious patterns such as large page sizes or repeated entity queries
- Disable direct access to sensitive entities through generic data provider controllers; use purpose-built endpoints with explicit authorization logic

## Variant hunting
Test other Aura service components for similar authorization bypass (e.g., RecordService, ListService, DataService)
Attempt to access other sensitive entities beyond Contact (Account, Opportunity, User, CustomObjects with PII)
Check if attackers can modify the layoutType, currentPage, or pageSize parameters to extract larger datasets or different data formats
Test with callingDescriptor parameter set to different values to bypass origin validation
Investigate if the vulnerability exists in other Salesforce Lightning Experience endpoints on the same domain
Examine whether unauthenticated users can access the same endpoints if CSRF protections are weak
Test if object-level or field-level filtering parameters can be bypassed through encoding or parameter manipulation

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Enumerate External Targets
- T1592: Gather Victim Identity Information
- T1087: Account Discovery
- T1078: Valid Accounts
- T1538: SaaS Enumeration

## Notes
This vulnerability affects a government system (GSA disposal.gsa.gov) handling potentially sensitive information about property disposal transactions. The Salesforce Lightning framework's Aura component architecture has been a source of similar authorization bypass vulnerabilities. The report demonstrates that even authenticated-required endpoints must implement granular authorization. The attacker required valid account credentials, limiting exposure but still representing a significant information disclosure risk for insider threats or accounts compromised through other means. Salesforce orgs should regularly audit custom Aura controllers as part of their security program.

## Full report
<details><summary>Expand</summary>

Hi, 

Sample of the Information Disclosure is below.  More records are attached -███

"LastName":"████","FullName__c":"█████████","Id":"██████████","MailingStreet":null,"Active__c":false,"Email__c":null,"LastModifiedBy":{"Id":"00530000009KyDqAAK","Name":"SNA █████████","sobjectType":"User"},"UserPassword__c":null,"Office__c":null,"BIA_Coordinator__c":false,"Contact_Type__c":null,"MailingCountry":null,"Salutation":null,"MailingState":null,"OwnerId":"005t0000002H5O6AAK","RecordType":{"Name__l":"Non-Federal Contact","Id":"████","Name":"Non-Federal Contact","sobjectType":"RecordType"},"Phone":"███"

User","sobjectType":"User"},"AccountId":"█████████","Email":"█████","Subscription_Type__c":null,"THPO_Coordinator__c":false,"MobilePhone":null,"Do_Not_Call__c":false,**Name":"█████████**,"Region__c":null,"LastModifiedDate__f":"5/12/2019 8:49 AM","CreatedById":"005t0000001FpB7AAK","Subscriber__c":false,"State__c":null,"CreatedBy":{"Id":"005t0000001FpB7AAK","Name":"Property Disposal Site Guest User","sobjectType":"User"},"Section_7_Coordinator__c":false,"Environmental_Assessor__c":false,"MailingCity":null,"Salutation__l":null,"CreatedDate__f":"1/24/2018 1:22 AM","Comments__c":null,"CreatedDate":"2018-01-24T06:22:57.000Z","Division__c":null,"LastName":"████","FullName__c":"████"


## Steps to Reproduce -

1) Create user account on https://disposal.gsa.gov

2) Complete to account verification process.

3) After login, visit the burp history and look for any any POST request having "/s/sfsites/aura" kind of request.

4) Use the POST request like this █████ in repeater and modify "message" parameter as below and leave remaining aura.context and aura.token parameters as it is.

message={"actions":[{"id":"261;a","descriptor":"serviceComponent://ui.force.components.controllers.lists.selectableListDataProvider.SelectableListDataProviderController/ACTION$getItems","callingDescriptor":"UNKNOWN","params":{"entityNameOrId":"Contact","pageSize":1000,"currentPage":1,"getCount":true,"layoutType":"FULL","enableRowActions":true,"useTimeout":false}}]}

5) contact details of users will be returned by the endpoint.

## Impact

Information disclosure.

</details>

---
*Analysed by Claude on 2026-05-24*
