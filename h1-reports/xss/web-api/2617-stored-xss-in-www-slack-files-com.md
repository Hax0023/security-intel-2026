# Stored XSS in www.slack-files.com

## Metadata
- **Source:** HackerOne
- **Report:** 2617 | https://hackerone.com/reports/2617
- **Submitted:** 2014-03-01
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

We can create posts under https://subdomain.slack.com/files/create/post

Post will have XSS payload like "><img src=x onerror=alert(10);> in title and body

We save it and hit "Create public link" and once we share the link it will trigger XSS.

Example/POC: https://slack-files.com/T025LLJ2X-F025N8W7W-3a5691

Thanks

Prakhar Prasad

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

Hi,

We can create posts under https://subdomain.slack.com/files/create/post

Post will have XSS payload like "><img src=x onerror=alert(10);> in title and body

We save it and hit "Create public link" and once we share the link it will trigger XSS.

Example/POC: https://slack-files.com/T025LLJ2X-F025N8W7W-3a5691

Thanks

Prakhar Prasad

</details>

---
*Analysed by Claude on 2026-05-24*
