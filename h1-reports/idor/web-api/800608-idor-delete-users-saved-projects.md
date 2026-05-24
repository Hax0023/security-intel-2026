# IDOR - Delete Users Saved Projects

## Metadata
- **Source:** HackerOne
- **Report:** 800608 | https://hackerone.com/reports/800608
- **Submitted:** 2020-02-20
- **Reporter:** ahmd_halabi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
**Target Url**
https://█████/██████████/█████████={Target_id}

**Summary:**
Hello, I found an IDOR bug in deleting users saved projects. Through changing the search id in the above url in a GET request, you can delete saved projects for any users.

## Step-by-step Reproduction Instructions

1. Navigate to your account -> Saved Searches.
2. Copy the url of the delete request `https://████/█████/███

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

**Target Url**
https://█████/██████████/█████████={Target_id}

**Summary:**
Hello, I found an IDOR bug in deleting users saved projects. Through changing the search id in the above url in a GET request, you can delete saved projects for any users.

## Step-by-step Reproduction Instructions

1. Navigate to your account -> Saved Searches.
2. Copy the url of the delete request `https://████/█████/████████={search_id}`
3. Replace your search id with the target victim search id and send the request. The target saved search will be deleted from the victim
To be more clear I uploaded this video, please watch it.
{}

## Suggested Mitigation/Remediation Actions
Check the user that is deleting the saved searches if he is legitimate and the real owner of that search or not.

## Impact

This would lead the attacker to delete all users saved searches through bruteforcing their ids. And since the id are incremented in an easy sequence, attacker can do this attack very fast.

</details>

---
*Analysed by Claude on 2026-05-24*
