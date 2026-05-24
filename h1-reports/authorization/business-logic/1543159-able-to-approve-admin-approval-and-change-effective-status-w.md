# Bypass Ad Review Process by Directly Modifying Admin Approval and Effective Status via API

## Metadata
- **Source:** HackerOne
- **Report:** 1543159 | https://hackerone.com/reports/1543159
- **Submitted:** 2022-04-17
- **Reporter:** bisesh
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Insufficient Input Validation, Business Logic Bypass, Missing Authorization Checks
- **CVEs:** None
- **Category:** business-logic

## Summary
Reddit's ad platform allows authenticated users to bypass the mandatory admin review process by directly modifying API parameters (admin_approval and effective_status) via PATCH requests to the ads API endpoint. This enables attackers to activate unapproved advertisements and circumvent payment verification requirements, allowing malicious ads to be delivered without review.

## Attack scenario
1. Attacker creates a campaign on ads.reddit.com which enters PENDING status
2. Campaign requires admin approval and payment details before ads can be delivered
3. Attacker intercepts or crafts a PATCH request to /api/v2.0/accounts/{account_id}/ads/{ad_id}
4. Attacker modifies JSON payload to set admin_approval=APPROVED, effective_status=ACTIVE, configured_status=ACTIVE
5. Reddit API accepts the unauthorized state change without validation
6. Ad is activated and delivered to users; attacker receives approval confirmation email despite bypassing review

## Root cause
The API endpoint lacks server-side authorization and validation checks to ensure that only Reddit admins can modify admin_approval status, and that state transitions follow the required business logic (review → payment → approval → activation). Client-side state is trusted without backend enforcement.

## Attacker mindset
Opportunistic attacker discovering that sensitive status fields can be modified directly through API calls without proper authorization. Motivation is to deliver unapproved content (potentially malicious, fraudulent, or policy-violating ads) while bypassing safety controls and payment requirements.

## Defensive takeaways
- Implement strict server-side authorization checks - admin_approval field should only be modifiable by Reddit backend admins, never by campaign owners
- Enforce state machine validation - enforce mandatory workflow (PENDING → UNDER_REVIEW → APPROVED/REJECTED, separate from payment verification)
- Separate concerns - use read-only fields for admin-controlled states; prevent users from directly setting admin_approval or effective_status
- Require payment verification before any status activation - validate payment details exist before allowing ACTIVE status
- Add audit logging for all status changes with admin-only modification flags
- Implement API input validation - reject payloads containing admin-controlled fields from non-admin users
- Use enum/whitelist validation - restrict status values to legitimate state transitions only

## Variant hunting
Test other admin-controlled fields for similar direct modification (budget approval, payment status, content moderation flags)
Check if other PATCH endpoints on ads-api.reddit.com have similar authorization bypass (campaigns, billing, account settings)
Attempt to modify other users' ad accounts by changing account_id in URL path
Test if DELETE operations on ads require proper authorization or can be abused
Check if PUT requests to ads endpoint have same vulnerability
Investigate if ad delivery can be queried/modified through other API versions (v1, v3)
Test if configured_status can be set to malicious values beyond ACTIVE

## MITRE ATT&CK
- T1190
- T1199
- T1592
- T1566

## Notes
This is a critical business logic bypass affecting platform integrity and advertiser trust. The vulnerability allows complete circumvention of fraud prevention, content review, and payment collection systems. The fix requires architectural changes to enforce proper authorization boundaries rather than client-side validation. Reddit appears to have trusted client-submitted state values without backend verification of user authority to modify those fields.

## Full report
<details><summary>Expand</summary>

## Summary:

In https://ads.reddit.com/ you can create campaign under which you can create ads , once you create new campaign , it is on pending stage and will not be delivered unless you add payment details and is reviewed by admin and approved according to what it says here https://advertising.reddithelp.com/en/categories/ad-review/about-reddits-ad-review-process . But changing the value of admin_approval to APPROVED and effective_status to ACTIVE , the ads is approved and thus we receive the confirmation email from reddit ads that our ads is approved .

## Impact:
Can bypass the review process and change the ads status to approve and active without payment process .

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Create a campaign from https://ads.reddit.com 
  1. Go to https://ads.reddit.com/dashboard, you will see a table list that shows your ads and campaign , there the status is stated as PENDING . And we know according to what reddit says , our ads needs to get reviewed by reddit members , but updating the value from api changes our status to ACTIVE . Hence ad is successfully delivered . 
POC video is attached . 

███████

```
PATCH /api/v2.0/accounts/█████/ads/██████████ HTTP/2
Host: ads-api.reddit.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://ads.reddit.com/
Authorization: bearer token
Content-Type: application/json
Origin: https://ads.reddit.com
Content-Length: 101
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
X-Pwnfox-Color: magenta
Te: trailers

{"data":
{"configured_status":"ACTIVE",
"effective_status":"ACTIVE",
"admin_approval":"APPROVED"
}}

```

## Supporting Material/References:


  * [attachment / reference]

## Impact

Can bypass the review process and change the ads status to approve and active without payment process .

</details>

---
*Analysed by Claude on 2026-05-24*
