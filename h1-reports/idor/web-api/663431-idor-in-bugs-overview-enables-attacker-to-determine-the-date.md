# IDOR in Bugs overview enables attacker to determine the date range a hackathon was active

## Metadata
- **Source:** HackerOne
- **Report:** 663431 | https://hackerone.com/reports/663431
- **Submitted:** 2019-07-29
- **Reporter:** jobert
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
A minor Insecure Direct Object Reference (IDOR) vulnerability is present in the `/bugs` endpoint. One of the Bugs overview filters enables a program member to filter by Hackathon that their program was a part of. This filter is applied when hackathon IDs are provided in the `hackathons` parameter, like https://hackerone.com/bugs?subject=security&hackathons[]=28.

The parameter takes an array of ID

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

A minor Insecure Direct Object Reference (IDOR) vulnerability is present in the `/bugs` endpoint. One of the Bugs overview filters enables a program member to filter by Hackathon that their program was a part of. This filter is applied when hackathon IDs are provided in the `hackathons` parameter, like https://hackerone.com/bugs?subject=security&hackathons[]=28.

The parameter takes an array of IDs and is vulnerable to an IDOR. When a hackathon ID is given that belongs to a private hackathon, a date range will be applied. Based on the extremes of the returned reports submission date, a user could determine the date range of the hackathon.

This vulnerability is easier to exploit for a program that has a lot of reports submitted on different days.

## Impact

The date range of a private hackathon could be determined. At the moment, there aren't any real hackathon objects that are marked as private, so no sensitive information is disclosed.

</details>

---
*Analysed by Claude on 2026-05-24*
