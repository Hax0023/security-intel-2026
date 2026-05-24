# Race Condition in Definition Votes

## Metadata
- **Source:** HackerOne
- **Report:** 152717 | https://hackerone.com/reports/152717
- **Submitted:** 2016-07-21
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** racecondition
- **CVEs:** None
- **Category:** business-logic

## Summary
There exists a race condition vulnerability in definition votes, allowing any user to artificially manipulate the number of up/down votes for a definition by making asynchronous requests to vote. A malicious user can use this method to reach any number of up or down votes for a definition.

See the attached screenshot for an example.

POC:

1. Visit any definition.
2. Intercept a vote of the defin

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

There exists a race condition vulnerability in definition votes, allowing any user to artificially manipulate the number of up/down votes for a definition by making asynchronous requests to vote. A malicious user can use this method to reach any number of up or down votes for a definition.

See the attached screenshot for an example.

POC:

1. Visit any definition.
2. Intercept a vote of the definition, such as with Chrome Developer tools or BurpSuite.
3. Make the opposite vote, so you are able to vote again.
4. Copy the vote request as a curl command, and in the command line execute the command in the format (command) & (command).
4. Revisit the vote. There will now be 2 votes cast, and a negative number of the opposite votes. This can be repeated by removing your vote and executing the request again.

Please let me know if you have any questions,

Jack

</details>

---
*Analysed by Claude on 2026-05-24*
