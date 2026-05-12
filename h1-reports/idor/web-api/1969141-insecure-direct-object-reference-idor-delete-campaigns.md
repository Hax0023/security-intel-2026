# Insecure Direct Object Reference (IDOR) - Unauthorized Campaign Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 1969141 | https://hackerone.com/reports/1969141
- **Submitted:** 2023-05-02
- **Reporter:** datph4m
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An authenticated attacker can delete any campaign on HackerOne by manipulating the campaign_id parameter in a GraphQL mutation request. The application fails to verify that the authenticated user owns or has permission to modify the targeted campaign, allowing deletion of campaigns from any program.

## Attack scenario
1. Attacker authenticates to HackerOne and obtains a valid session cookie and CSRF token
2. Attacker intercepts or crafts a POST request to the GraphQL endpoint with an UpdateCampaign mutation
3. Attacker base64-decodes an accessible campaign_id to understand the format (gid://hackerone/Campaign/[ID])
4. Attacker modifies the campaign_id to target a campaign from a different program by changing the numeric ID portion
5. Attacker base64-encodes the modified campaign_id and sends the request with the spoofed campaign_id parameter
6. The server processes the mutation without verifying authorization, resulting in deletion of the targeted campaign

## Root cause
The backend fails to implement proper authorization checks on the UpdateCampaign GraphQL mutation. The application only validates that the user is authenticated but does not verify ownership or team membership before allowing campaign modifications. The campaign_id parameter is treated as a direct object reference without access control validation.

## Attacker mindset
An authenticated attacker with basic HTTP interception skills can systematically enumerate and delete campaigns across all programs. The base64 encoding is trivial to decode/encode, and the sequential numeric IDs suggest campaigns are easily discoverable. This enables griefing, sabotage, or competitive disruption.

## Defensive takeaways
- Implement strict authorization checks on every mutation/query operation - verify user has explicit permission to modify the targeted resource
- Use indirect object references (tokens, UUIDs) instead of sequential IDs when possible, combined with permission validation
- Validate that the authenticated user belongs to the team/organization that owns the campaign before allowing modifications
- Implement rate limiting on mutation operations to detect and block bulk deletion attempts
- Add audit logging for all campaign modifications to detect unauthorized access patterns
- Use the principle of least privilege - ensure GraphQL mutations require explicit ownership verification, not just authentication
- Implement field-level permissions in GraphQL schema to prevent unauthorized mutations at the schema level

## Variant hunting
Search for similar authorization bypass vulnerabilities in other GraphQL mutations: CreateCampaign, DeleteCampaign (if exists separately), UpdateBountyTable, UpdateProgram. Check for IDOR in REST endpoints with sequential IDs. Test other resource types (reports, bounties, targets) for identical authorization flaws. Review all mutations accepting team_id or program_id parameters for cross-tenant access.

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
The writeup uses base64-encoded GraphQL IDs (likely following Relay cursor specification). The vulnerability is straightforward - no complex exploitation required. The bounty amount is redacted in the original submission. This is a critical business impact issue as campaigns drive the core bug bounty program functionality.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi Team, 

I think I can delete any Campaigns based on campaign_id


### Steps To Reproduce

Follow the POST request below

````
POST /graphql HTTP/2
Host: hackerone.com
Cookie: yourcookie
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://hackerone.com/organizations/opensea_demo/campaigns/242/edit
Content-Type: application/json
X-Csrf-Token: ███
X-Product-Area: campaigns
X-Product-Feature: edit
X-Datadog-Origin: rum
X-Datadog-Parent-Id: 9027318766950450042
X-Datadog-Sampling-Priority: 1
X-Datadog-Trace-Id: 87799383677632658
Content-Length: 851
Origin: https://hackerone.com
Dnt: 1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers

{"operationName":"UpdateCampaign","variables":{"product_area":"campaigns","product_feature":"edit","input":{"campaign_id":"Z2lkOi8vaGFja2Vyb25lL0NhbXBhaWduLzI0NA==","team_id":"Z2lkOi8vaGFja2Vyb25lL0VuZ2FnZW1lbnRzOjpCdWdCb3VudHlQcm9ncmFtLzU3MzI4","bounty_table_row_id":"Z2lkOi8vaGFja2Vyb25lL0JvdW50eVRhYmxlUm93LzEwODM2","start_date":"2023-05-05T09:00:00Z","end_date":"2023-05-08T05:00:00Z","critical":3,"high":2,"medium":1.5,"low":1.5,"structured_scope_ids":[],"researchers_information":"ccccccccccccccc"}},"query":"mutation UpdateCampaign($input: UpdateCampaignInput!) {\n  updateCampaign(input: $input) {\n    was_successful\n    errors {\n      edges {\n        node {\n          id\n          type\n          field\n          message\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

````

Decode base64 of campaign_id to get **gid://hackerone/Campaign/244**

Increase or decrease the number after Campaign and re-encode it with base64

At the campaign_id parameter in the request change it to another program's ongoing campaign_id parameter.

Then send Campaign request of any program to be deleted.

## Impact

Can delete all Campaign on hackerone or any program

</details>

---
*Analysed by Claude on 2026-05-11*
