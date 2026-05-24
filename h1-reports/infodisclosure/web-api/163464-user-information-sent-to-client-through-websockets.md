# User Information sent to client through websockets

## Metadata
- **Source:** HackerOne
- **Report:** 163464 | https://hackerone.com/reports/163464
- **Submitted:** 2016-08-26
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hey,

I noticed when monitoring the websocket requests that the account information of many users, including email address, is sent to the client. For example:

```
██████

██████████

█████████

████████

███████

```

There's hundreds of these requests, each containing user information. Please let me know if this is meant to be happening, but I didn't see a list of users on the site.

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

Hey,

I noticed when monitoring the websocket requests that the account information of many users, including email address, is sent to the client. For example:

```
██████

██████████

█████████

████████

███████

```

There's hundreds of these requests, each containing user information. Please let me know if this is meant to be happening, but I didn't see a list of users on the site.

</details>

---
*Analysed by Claude on 2026-05-24*
