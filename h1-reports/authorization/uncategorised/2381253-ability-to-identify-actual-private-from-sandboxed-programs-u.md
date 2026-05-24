# Information Disclosure: Private Program Detection via CSV Export Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 2381253 | https://hackerone.com/reports/2381253
- **Submitted:** 2024-02-20
- **Reporter:** ketr0it
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Improper Access Control, Program Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The terms_acceptance_data.csv endpoint lacks proper authorization checks, allowing any unauthenticated user to determine whether a program is private, sandboxed, or public based on HTTP response behavior. By probing the endpoint with different program handles, attackers can enumerate and identify private programs that should remain confidential.

## Attack scenario
1. Attacker discovers the /terms_acceptance_data.csv endpoint exists on HackerOne programs
2. Attacker compiles list of potential target companies that might have private programs
3. Attacker iterates through company names/handles probing the CSV endpoint
4. Attacker observes differential responses: successful download for sandboxed programs, access denied/404 for private programs, and 404 for non-existent programs
5. Attacker uses response patterns to reliably identify which companies have private bug bounty programs on HackerOne
6. Attacker gains reconnaissance of target programs before attempting other attacks or social engineering

## Root cause
The CSV export endpoint performs insufficient authorization validation, failing to enforce consistent access controls across program types (public, sandboxed, and private). The endpoint was likely protected at the GraphQL layer but not the direct file serving layer, creating an authorization bypass.

## Attacker mindset
Reconnaissance and intelligence gathering. Attacker seeks to identify high-value targets (companies with private programs) without authorization. The differential response behavior allows fingerprinting program status as a side-channel leak.

## Defensive takeaways
- Implement consistent authorization checks at all endpoint layers, not just GraphQL APIs
- Avoid creating observable behavioral differences in responses that leak information (timing, content, status codes)
- Apply identical access control logic to file exports and dynamic endpoints
- Return consistent 404 responses for both non-existent and unauthorized resources to prevent enumeration
- Audit all program-related endpoints for similar authorization bypasses
- Consider rate limiting and monitoring for bulk endpoint probing attempts

## Variant hunting
Search for other program-related export endpoints (reports CSV, submissions data, user lists). Check whether similar authorization bypasses exist in: /advanced_vetting endpoint, other program settings pages, historical data exports, program analytics endpoints, or related file download functionality. Test with different program types (public, private, sandboxed, invite-only).

## MITRE ATT&CK
- T1526 - Reconnaissance: External Enumeration
- T1087 - Account Discovery: Internet-based enumeration
- T1592 - Gather Victim Identity Information
- T1538 - SaaS Infrastructure Abuse

## Notes
The report demonstrates clear differential behavior between sandboxed (accessible), private (denied), and non-existent (404) programs, creating a reliable enumeration vector. HackerOne's own security-test-invite-only program appears misconfigured as it allows CSV access. The impact directly violates HackerOne's confidentiality policy for private programs. This is a relatively low-effort, high-confidence reconnaissance attack with minimal technical barriers.

## Full report
<details><summary>Expand</summary>

I was looking through the settings of one of my sandboxed programs I use for testing and I noticed some weird behavior, when we go to any program's advanced vetting page hackerone.com/$handle/advanced_vetting, it loads up regardless of permission, granted no other confidential info is displayed since the GraphQL request appropriately restricts unauthorized users so this is what is shown:
{F3061767}
although this shouldn't happen, so far there wouldn't a significant risk from this behavior alone, but one thing I noticed from the Advanced vetting page (when it loads properly, of course) is that it has a link to download a .csv file:
{F3061769}
that leads to https://hackerone.com/$handle/terms_acceptance_data.csv
I decided to experiment with this link and sure enough, I found some risky behavior, when any HackerOne user goes to https://hackerone.com/$SANDBOXED_PROGRAM/terms_acceptance_data.csv the request goes through and we download the csv file, although it doesn't have any relevant information, just default text, take for example my own sandboxed program https://hackerone.com/test_pie77/terms_acceptance_data.csv if you or any user in Hackerone go to that link the request will go through and download the csv file, now let's take for example, ██████, they have a totally private program although you can access the embedded report submission form from their own security page, so if we go to █████ we can see that the request doesn't go through, confirming that the program is, in fact, private and we know that it is private and exists because when we try with a handle that doesn't exist it shows the Hackerone default 404 page like this:
{F3061796}
but when we go to ███ program:
█████████
it shows a different response
I tried this with other actual private programs and the behavior was the same, the request didn't go through, I tried with other sandboxed programs of mine using a second account and the behavior was the same, the request did go through, the only private program it did work was in HackerOne's own dummy invite-only program at https://hackerone.com/security-test-invite-only/terms_acceptance_data.csv this could be due to some misconfiguration on HackerOne's side as the request does goes through and we can see the csv file has been modified.
{F3061793}

### Steps To Reproduce

1. Use my sandboxed program as an example: https://hackerone.com/test_pie77/terms_acceptance_data.csv or replace my program's handle with a sandboxed program of yours and use a second account and go to that link
2. Check how you can download the Csv file confirming the program is sandboxed
3. Now replace the sandboxed program's handle with a private program's handle and see how it doesn't work, confirming the program is private

## Impact

Here we can clearly identify which programs are private, we can build a script or just try manually using company names that we might believe have a private program in Hackerone and check if they actually have one, leading to some loss of the confidentiality of all private programs in HackerOne. This is confirmed to be a valid vulnerability going by this text on HackerOne's policy page:
{F3061814}

</details>

---
*Analysed by Claude on 2026-05-24*
