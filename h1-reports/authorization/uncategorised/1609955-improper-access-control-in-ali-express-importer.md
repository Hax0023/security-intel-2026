# Improper Access Control in Ali Express Review Importer - Unauthorized Judge.me Review Access

## Metadata
- **Source:** HackerOne
- **Report:** 1609955 | https://hackerone.com/reports/1609955
- **Submitted:** 2022-06-23
- **Reporter:** penguinshelp
- **Program:** Judge.me / HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authentication, Cross-App Session Exploitation, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with access only to the Ali Express Review Importer app can view all Judge.me reviews (including hidden/archived ones) by reusing authentication cookies from the Ali Express app to make requests to the Judge.me endpoint. The vulnerability exists because the Ali Express Review Importer establishes a valid Judge.me session that can be hijacked to bypass app-level access controls.

## Attack scenario
1. Attacker gains staff account with limited permissions restricted to only Ali Express Review Importer app
2. Attacker opens Ali Express Review Importer app to establish a valid Judge.me authentication session
3. Attacker intercepts the refresh request in Ali Express app and extracts the authentication cookie
4. Attacker crafts a request to the Judge.me API endpoint (judge.me/index.json) with the intercepted cookie
5. Attacker bypasses app-level access controls and gains unauthorized access to all Judge.me reviews
6. Attacker can view sensitive data including hidden, archived, and restricted reviews without proper authorization

## Root cause
The Ali Express Review Importer app authenticates to Judge.me on behalf of the user, creating a session that grants full access to Judge.me endpoints regardless of the staff member's actual app permissions. The Judge.me API does not validate that the requestor has explicit access to the Judge.me app itself, instead relying solely on cookie-based authentication without proper scope validation.

## Attacker mindset
A disgruntled or curious staff member with limited intentional permissions seeks to view sensitive customer reviews they shouldn't have access to. They recognize that the Ali Express app's backend communication with Judge.me can be leveraged to bypass frontend access restrictions by reusing authenticated sessions across app boundaries.

## Defensive takeaways
- Implement proper authorization checks at the API endpoint level to verify user has explicit access to the resource/app, not just valid authentication
- Use scoped tokens or session tokens that limit access based on the originating app and user's actual permissions
- Do not allow inter-app session reuse without explicit authorization checks
- Validate that API requests originate from authorized sources and that users have permission to the specific endpoint being accessed
- Implement audit logging for cross-app API access attempts
- Use separate authentication contexts for different apps rather than sharing global sessions
- Implement rate limiting and anomaly detection on API endpoints that serve sensitive data

## Variant hunting
Check other Judge.me integrations for similar cross-app authentication reuse patterns
Test whether other Shopify apps owned by Judge.me have similar improper access control issues
Examine if other endpoints in Judge.me API have insufficient authorization checks
Review all staff app permission boundaries to identify other potential scope bypass scenarios
Investigate whether admin endpoints are accessible through limited-permission app sessions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1110 - Brute Force (session reuse)
- T1078 - Valid Accounts (token hijacking)
- T1537 - Transfer Data to Cloud Account

## Notes
This is the third similar report from the same researcher (references #1450807 and #1382652), indicating a pattern of improper access control across Judge.me apps. The vulnerability requires the attacker to be a legitimate staff member with at least one app installed, making this a medium-complexity privilege escalation. The researcher provided detailed step-by-step reproduction steps with supporting materials, demonstrating the severity and ease of exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
Good day team,

I found another improper access control flaw in Ali Express Review Importer that can be used to view all and any existing reviews in Judge.Me app. This is similar to my other reports  #1450807 and #1382652. Basically the same bug with #1450807 just on a different app and endpoint :)

## Steps To Reproduce:

1. Login as an admin to your test Shopify instance

2. Install the apps 'Judge.me Product Reviews' and 'Ali Express Review Importer' (both owned by Judge.me)

2. Add a new review to your Judge.Me app. 'Reviews' ->  'Write a Review'

2. Add/Edit a Shopify staff member and give access only to 'Ali Express Review Importer' app 

2. Login to the staff account with only 'Ali Express Review Importer'

2. Go to apps and open the 'Ali Express Review Importer' to establish/start Judge.me session

2. Visit this url to attempt to view reviews from Judge.Me App: `https://judge.me/index.json?shopdomain={yourshop}.myshopify.com&page=1&2. 
per_page=25&offset=0` . Capture the request for this using any proxy intercepting tool like Burp Suite 

2. Since you don't have a valid session for the Judge.Me app you will be prompted to login as a shop owner

2. Now in the 'Ali Express Review Importer app, click 'Reviews' -> and then click the refresh icon on the left side of the search bar. Capture the request for this one too since we'd need the cookie in the request.
{F1785201}

2. Replace the cookie in the request from step 7 to the recently acquired cookie in step 9

2. Send the edited request, the request from step 6 with the new cookie, and you should now be able to view any reviews including hidden/archived ones from Judge.Me App without having access to the Judge.Me app itself

Note: 
Steps 1-4 are done by Admin
Steps 5-11 are done by user with only Ali Express Importer access

## Supporting Material/References:
{F1785202}

If you have any questions on this or if there's anything I can help with please let me know.

Have a nice day!

-PenguinsHelp

## Impact

Staff with no access to 'Judge.me App' can view reviews which they supposedly doesn't have access to

</details>

---
*Analysed by Claude on 2026-05-24*
