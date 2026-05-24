# stored xss in transaction

## Metadata
- **Source:** HackerOne
- **Report:** 42161 | https://hackerone.com/reports/42161
- **Submitted:** 2014-12-30
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
1. Open wallet settings and remove maxlength="30" from wallet name input
2. Change name to something like this  asdf'"><script>alert(1)</script>
3. Go to "Send bitcoin" and make inbound transfer from one wallet to another with description: desc<script>alert('xss in description')</script>
4. Submit form
5. After submit we got xss both in "from account" name and "to account" name
6. Go to trans

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

1. Open wallet settings and remove maxlength="30" from wallet name input
2. Change name to something like this  asdf'"><script>alert(1)</script>
3. Go to "Send bitcoin" and make inbound transfer from one wallet to another with description: desc<script>alert('xss in description')</script>
4. Submit form
5. After submit we got xss both in "from account" name and "to account" name
6. Go to transaction history https://wallet.robocoin.com/account/6428d1d8-c499-46ab-8587-74260d898f34
7. Open single transaction details and we got xss in  "from account" name, "to account" name and description.
"To Robocoin wallet" feature has the same fields "from account" and description and may be also affected. If you approve my second account white.hat.audit@gmail.com i will test it. And i think that this issue may affect admin panel.

</details>

---
*Analysed by Claude on 2026-05-24*
