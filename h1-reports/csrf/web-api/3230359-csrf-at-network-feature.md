# CSRF at Network feature

## Metadata
- **Source:** HackerOne
- **Report:** 3230359 | https://hackerone.com/reports/3230359
- **Submitted:** 2025-06-30
- **Reporter:** psfauzi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
A csrf vulnerability was found in the network feature, where an attacker can change Network Routing settings by sending a csrf script to the victim.

## Steps To Reproduce:
1. Prepare the csrf script as below.

```
<html><body><a href="https://lichess.org/account/network?usingAltSocket=false">click</a></script></body></html>
```

2. save the script above to your server. for example csr

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

## Summary:
A csrf vulnerability was found in the network feature, where an attacker can change Network Routing settings by sending a csrf script to the victim.

## Steps To Reproduce:
1. Prepare the csrf script as below.

```
<html><body><a href="https://lichess.org/account/network?usingAltSocket=false">click</a></script></body></html>
```

2. save the script above to your server. for example csrf.html

3. send to the victim registered in the Lichess application

Proof :
Victim set Network Routing feature to ==Use CDN Routing==:
{F4509912}

Attacker sent csrf to victim:
{F4509921}

Victim visit the csrf link then pressing the click button from the csrf that the attacker sent
{F4509929}

  * [attachment / reference]

{F4509951}

## Impact

An irresponsible malicious user can change network routing settings by sending a csrf script to the victim.

</details>

---
*Analysed by Claude on 2026-05-24*
