# XSS in experts.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 57459 | https://hackerone.com/reports/57459
- **Submitted:** 2015-04-20
- **Reporter:** haxs101
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
XSS vulnerability in experts.shopify.com,

Steps to verify:
1. Go  to https://experts.shopify.com
2. Sign up for an `expert`. (Please do note that you must create a new account if you already have, do not use existing account or an account that did not yet apply for an expert) then you will ask to login.
3. Fill up the necessary fields and upload photos.
4. Under `Portfolio Images` put 

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
XSS vulnerability in experts.shopify.com,

Steps to verify:
1. Go  to https://experts.shopify.com
2. Sign up for an `expert`. (Please do note that you must create a new account if you already have, do not use existing account or an account that did not yet apply for an expert) then you will ask to login.
3. Fill up the necessary fields and upload photos.
4. Under `Portfolio Images` put `"><img src=x onerror=alert(document.domain)>` in the `caption` field.
5. Now hit `Save`, you will be redirected to page like this ( http://postimg.org/image/glodr1wj3/ )
6. Click one of the photos where the caption is `"><img src=x onerror=alert(document.domain)>`. XSS now executes.

Proof of concept: http://postimg.org/image/7jrwwaywn/

Please let me know if you need more information about this.

Regards,
Mr. Poo Gay

</details>

---
*Analysed by Claude on 2026-05-24*
