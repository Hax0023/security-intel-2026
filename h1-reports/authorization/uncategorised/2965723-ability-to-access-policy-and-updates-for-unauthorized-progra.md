# Unauthorized Access to Program Policy and Updates via API Key

## Metadata
- **Source:** HackerOne
- **Report:** 2965723 | https://hackerone.com/reports/2965723
- **Submitted:** 2025-01-30
- **Reporter:** light3r
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, API Authorization Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A user with restricted access to only one program in a multi-program organization could bypass authorization controls via the HackerOne API to access policy and updates from an unauthorized program. The API endpoint failed to properly validate program membership permissions, allowing low-privilege users to retrieve sensitive program data they should not have access to.

## Attack scenario
1. Attacker creates or compromises a low-privilege account with access limited to one program (askcmsakmdfksqa_h1r)
2. Attacker generates an API key using the restricted account credentials
3. Attacker constructs API requests targeting an unauthorized program (askcmsakmdfksqa_h1b) they have no explicit access to
4. The API endpoint /v1/hackers/programs/{program_id}/ processes the request without proper authorization validation
5. Attacker retrieves sensitive program policy, updates, and other restricted data from the unauthorized program
6. Attacker monitors the unauthorized program for ongoing updates and changes, maintaining persistent unauthorized access

## Root cause
The API authorization layer failed to enforce program membership restrictions. The endpoint validated that the user had valid API credentials but did not verify that the user had explicit access permissions to the specific program resource being requested. Authorization checks present in the web UI were not replicated in the API layer.

## Attacker mindset
An insider threat or competitor seeking to gain intelligence on rival bug bounty programs. The attacker methodically tested authorization boundaries, discovering that API access circumvented UI-enforced restrictions. This represents a logical progression from web UI reconnaissance to API exploitation, exploiting the common pattern of inconsistent authorization implementation across interfaces.

## Defensive takeaways
- Implement consistent authorization checks across all API endpoints, mirroring UI-enforced permissions
- Validate program membership for every API request before returning resource data
- Use a centralized authorization service or middleware to enforce access control policies uniformly
- Implement comprehensive API logging and monitoring to detect unusual access patterns across program boundaries
- Apply principle of least privilege to API token scope - consider restricting API tokens to specific programs
- Conduct security testing of APIs separately from UI testing, as authorization logic may diverge
- Add automated tests validating that users cannot access unauthorized resources via API
- Implement rate limiting and anomaly detection for API access across program boundaries

## Variant hunting
Test other API endpoints (/v1/programs, /v1/hackers, /v1/report) for similar authorization bypass patterns
Check if webhooks or webhook management endpoints have the same authorization vulnerability
Test whether the vulnerability extends to creating/modifying resources in unauthorized programs (POST/PATCH/DELETE)
Verify if organization-level API tokens bypass program-level restrictions
Check if invitation/collaboration endpoints allow unauthorized program access
Test GraphQL API if available for similar authorization bypass opportunities
Examine whether the vulnerability applies to other nested resources within programs (reports, comments, attachments)

## MITRE ATT&CK
- T1190
- T1199
- T1087
- T1526
- T1552

## Notes
The report demonstrates a classic inconsistency between UI and API authorization enforcement. The organization's security model attempted to compartmentalize access at the UI level but failed to replicate these controls in the API, creating a privileged bypass vector. The vulnerability particularly impacts organizations using API keys for programmatic access to HackerOne resources. The sensitivity lies in potential exposure of program vulnerability disclosure policies, which could contain exploit details or defensive information.

## Full report
<details><summary>Expand</summary>

#Description:
In an organization with two programs, a user who is only part of one program can still access the policy and updates of the unauthorized program using an API key.  

## **Steps to Reproduce**  

1. In an organization with two programs, navigate to:  
   **[HackerOne Organization Settings](https://hackerone.com/organizations/askcmsakmdfksqa_demo/settings/users)**  
2. Add a new user.  

█████████  

3. Create a low-permission group for one of the two programs, as shown below:  

   ![Low Permissions Group](F4003557)  

4. As shown above, the user should only have access to **askcmsakmdfksqa_h1r**.  
5. Verify the low-permission account access:  

{F4003563}  
{F4003565}

6. Using the low-permission account, navigate to:  
 [HackerOne API Token Settings](https://hackerone.com/settings/api_token/edit)
7. Generate a **HackerOne API key**, then make the following request:  

   ```bash
   curl "https://api.hackerone.com/v1/hackers/programs/askcmsakmdfksqa_h1b/" \
     -X GET \
     -u "██████=" \
     -H 'Accept: application/json'
   ```  

8. The unauthorized user is able to retrieve the policy and updates of the restricted program:  

{F4003567} 

9. If changes or updates occur, they are also accessible:  

   {F4003570}

10. The user can retrieve these updates as well:  

{F4003571}

## Impact

The unauthorized user or have a low permissions can get access to restricted program policy and updates which is contains a sensitive data also the user is unauthorized

</details>

---
*Analysed by Claude on 2026-05-24*
