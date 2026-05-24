# XSS in SHOPIFY: Unsanitized Supplier Name  can lead to XSS in Transfers Timeline

## Metadata
- **Source:** HackerOne
- **Report:** 167075 | https://hackerone.com/reports/167075
- **Submitted:** 2016-09-09
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello

I would like to report an XSS happening in Transfer Timeline because the Supplier Name input is not sanitized as it should!

***POC***
Set Supplier Name to "><img src=x onerror=prompt('XSS')>
Create a Transfer with multiple items and cancel on of the items.
Review the timeline
In the timeline you will see `You canceled items in a shipment from SUPPLIER NAME` which since it is unsanitized it

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

Hello

I would like to report an XSS happening in Transfer Timeline because the Supplier Name input is not sanitized as it should!

***POC***
Set Supplier Name to "><img src=x onerror=prompt('XSS')>
Create a Transfer with multiple items and cancel on of the items.
Review the timeline
In the timeline you will see `You canceled items in a shipment from SUPPLIER NAME` which since it is unsanitized it will trigger XSS

{F118573}
{F118574}

Live XSS is here https://whitehat-3.myshopify.com/admin/transfers/11073

Hope it will be triaged and fixed



</details>

---
*Analysed by Claude on 2026-05-24*
