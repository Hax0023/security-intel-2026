# Reflective XSS on wholesale.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 106293 | https://hackerone.com/reports/106293
- **Submitted:** 2015-12-21
- **Reporter:** krankopwnz
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
There is a reflected XSS issue on wholesale.shopify.com

Steps to reproduce:
Call the following URL in Mozilla Firefox:
https://wholesale.shopify.com/asd%27%3Balert%28%27XSS%27%29%3B%27

An alert box with "XSS" appears. This means that an attacker has full control of the scripts, that are executed in the victims browser.

An attack vector would be sending an evil link via e-mail, messenger, etc. A

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

There is a reflected XSS issue on wholesale.shopify.com

Steps to reproduce:
Call the following URL in Mozilla Firefox:
https://wholesale.shopify.com/asd%27%3Balert%28%27XSS%27%29%3B%27

An alert box with "XSS" appears. This means that an attacker has full control of the scripts, that are executed in the victims browser.

An attack vector would be sending an evil link via e-mail, messenger, etc. As the victim trusts the domain wholesale.shopify.com, it will click the link and could be redirected to a site hosting a browser exploit kit.
This abuses the trust of shopify.com

The main problem with that XSS is, that in script context the quotes, double quotes and ">" + "<" are not encoded at all.

I suggest to convert them either to hex values or escape them.


</details>

---
*Analysed by Claude on 2026-05-24*
