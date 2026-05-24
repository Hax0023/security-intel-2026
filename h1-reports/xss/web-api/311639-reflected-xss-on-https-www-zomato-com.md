# Reflected XSS on https://www.zomato.com

## Metadata
- **Source:** HackerOne
- **Report:** 311639 | https://hackerone.com/reports/311639
- **Submitted:** 2018-02-02
- **Reporter:** strukt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

I found an XSS issue due to the incorrect handling of the \ character in a <script> context, the following link works as a PoC that alerts the location of the document:

https://www.zomato.com/googleOAuth2Callback?)}(alert)(location);{%3C!--&state=\

The issue exists because, given that the \ character supplied as the `state` parameter value is not well escaped and reflected into the page,

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

Hello,

I found an XSS issue due to the incorrect handling of the \ character in a <script> context, the following link works as a PoC that alerts the location of the document:

https://www.zomato.com/googleOAuth2Callback?)}(alert)(location);{%3C!--&state=\

The issue exists because, given that the \ character supplied as the `state` parameter value is not well escaped and reflected into the page, we are able to use it to escape the " and then inject our own JS code to execute it on the page.

Note: This only works when the page is opened by an authenticated user

## Impact

This allows an attacker to inject custom Javascript codes that can be used to steal information from Zomato's user base and lure them to malicious websites on the internet on behalf of Zomato's website.

</details>

---
*Analysed by Claude on 2026-05-24*
