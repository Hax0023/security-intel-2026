# Stored XSS in Direct debit name

## Metadata
- **Source:** HackerOne
- **Report:** 45233 | https://hackerone.com/reports/45233
- **Submitted:** 2015-01-26
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
1. Make new or edit old Direct debit (for example https://mobilevikings.be/en/account/easypay/correct-direct-debit-mandate/111366/)
2. Fill owners name with payload asdf'"><script>alert(document.cookie)</script>
3. Save form. 
We got Stored XSS in pages:
https://mobilevikings.be/en/account/easypay/
https://mobilevikings.be/en/account/easypay/history/111366/
https://mobilevikings.be/en/accoun

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

1. Make new or edit old Direct debit (for example https://mobilevikings.be/en/account/easypay/correct-direct-debit-mandate/111366/)
2. Fill owners name with payload asdf'"><script>alert(document.cookie)</script>
3. Save form. 
We got Stored XSS in pages:
https://mobilevikings.be/en/account/easypay/
https://mobilevikings.be/en/account/easypay/history/111366/
https://mobilevikings.be/en/account/easypay/auto-sms-topup/?req_subscription=1030418
And admin area pages may be affected.

The really interesting thing is if we press https://mobilevikings.be/en/account/easypay/287740/suspend/ link we got this cookie setted:
Set-Cookie	messages="e052df5f3af892c7a61d74d0d9a6ab14c7f1631c$[[\"__json_message\"\0540\05425\054\"Successfully suspended asdf'\\\"><script>alert(document.cookie)</script> <span>BE61310126985517</span>\"]]"; Path=/

So we have a properly signed cookie with XSS payload. And if we found some way to setup it (it may be some xss on mobilevikings.be subdomain or CRLF issue in some data which used in header) we can use this xss vector too.

</details>

---
*Analysed by Claude on 2026-05-24*
