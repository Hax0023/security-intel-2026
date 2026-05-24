# Possible XSS

## Metadata
- **Source:** HackerOne
- **Report:** 123278 | https://hackerone.com/reports/123278
- **Submitted:** 2016-03-15
- **Reporter:** paulos__
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I opened this report as soon as I have read https://mathiasbynens.github.io/rel-noopener/

It doesn't necessarly affect HackerOne, nor have i given it enough time to get a working dom manipulation.
But since Markdown allows creating **target** attributes to anchor tags, it may be possible to get this executed. even if it doesn't, I think you shouldn't let users set the target=_blank attribute

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

I opened this report as soon as I have read https://mathiasbynens.github.io/rel-noopener/

It doesn't necessarly affect HackerOne, nor have i given it enough time to get a working dom manipulation.
But since Markdown allows creating **target** attributes to anchor tags, it may be possible to get this executed. even if it doesn't, I think you shouldn't let users set the target=_blank attribute to their links. I reported this because I know (and have read similar reportes where) hackerone cares about even the slightest possiblites of this kinds of bugs existing

Markdown can create them using:
```
[link](url){:target="_blank"}
```

Thanks,
Paulos

</details>

---
*Analysed by Claude on 2026-05-24*
