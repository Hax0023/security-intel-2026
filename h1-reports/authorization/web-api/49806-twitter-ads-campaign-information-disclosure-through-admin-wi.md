# Twitter Ads Campaign Information Disclosure via Unauthenticated Admin Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 49806 | https://hackerone.com/reports/49806
- **Submitted:** 2015-03-02
- **Reporter:** avicoder_
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Authentication, Sensitive Data Exposure, Information Disclosure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated endpoint at ads.twitter.com/admin/accounts_typeahead.json exposed sensitive campaign information including associated member details without proper authorization checks. The endpoint allowed querying arbitrary account names to retrieve campaign metadata and user information normally restricted to authorized campaign members.

## Attack scenario
1. Attacker logs into any Twitter account (including low-privilege accounts)
2. Attacker navigates to ads.twitter.com/admin/accounts_typeahead.json?query=targetaccount
3. Attacker modifies the query parameter to target competitor, celebrity, or high-profile account names
4. Endpoint returns JSON response containing sensitive campaign information including member names, roles, and associations
5. Attacker extracts user_name_info element revealing campaign members without authorization
6. Attacker can enumerate multiple accounts to build intelligence about campaign structures and organizational affiliations

## Root cause
The typeahead/autocomplete endpoint lacked proper authorization validation before returning sensitive campaign data. The endpoint appears to have been designed for admin use but was either publicly accessible or had insufficient authentication checks, allowing any logged-in user to access information restricted to authorized campaign members.

## Attacker mindset
An attacker would seek competitive intelligence, targeting high-profile brands and campaigns to understand organizational structure, team composition, and advertising strategies. The ease of exploitation and information harvesting potential make this attractive for corporate espionage, competitive analysis, or social engineering attacks against campaign members.

## Defensive takeaways
- Implement proper authorization checks on all admin endpoints, not just authentication
- Require explicit role/permission verification before returning sensitive campaign data
- Never expose user lists or member information through typeahead/search endpoints without authorization context
- Implement rate limiting and query validation on autocomplete endpoints to prevent enumeration
- Review all endpoints prefixed with 'admin' to ensure they have appropriate access controls
- Conduct security review of all autocomplete/typeahead endpoints for data exposure risks
- Log and monitor access to sensitive endpoint patterns for anomalous queries

## Variant hunting
Search for similar typeahead endpoints on other advertising platforms (Facebook Ads, Google Ads, LinkedIn)
Test other admin endpoints for similar missing authorization patterns
Look for other autocomplete endpoints that might expose user lists or sensitive enumerations
Test if other query parameters can be used for lateral enumeration
Check if the endpoint supports wildcard queries or partial matching for broader information disclosure
Test for IDOR vulnerabilities in campaign ID or user ID parameters
Examine API endpoints that power the admin UI for similar gaps

## MITRE ATT&CK
- T1190
- T1200
- T1526
- T1589
- T1591

## Notes
This is a straightforward authorization bypass vulnerability. The reporter demonstrates the issue clearly through the PoC. The vulnerability required authentication to Twitter itself but not to the sensitive endpoint, which is still a significant exposure. The endpoint should have verified the requester had authorization for the specific campaign being queried. The JSON response structure (user_name_info element) suggests this was copied from internal admin tools without proper access control implementation.

## Full report
<details><summary>Expand</summary>

Hi Twitter !!

I just wanted to report a major flaw which I found in https://ads.twitter.com , hoping it make twitter more secure and I am glad for being a part of it.

**Vulnerability Name**:  OWASP:A6 Sensitive data Exposure

**Vulnerable URL**: https://ads.twitter.com/admin/accounts_typeahead.json?query=*****

**Vulnerability Overview**: Information Disclosure without any *authentication* .

**Proof of Concept:**
   - Log into twitter account first.
   - Go to this URL https://ads.twitter.com/admin/accounts_typeahead.json?query=avicoder
   - Change the query string to any other account or screen_name ex: *microsoft*
   - You can view all the information about the account associated with the  campaign.
   - Usually this information is only visible to members of campaign.
   - Look at user_name_info element in JSON POC which actually exposing the members associated with campaign. 

**I attached the json file when I query my account in private window..
Its gives me all information about members linked to the campaign without any need of being (admin,manager,analyst)**

I made this report short  unlike my previous reports but it is to the point.
Please revert back if more information is needed. 

*Happy to help*
#:)#
**avicoder**



</details>

---
*Analysed by Claude on 2026-05-24*
