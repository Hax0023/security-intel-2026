# Balance Manipulation - BUG

## Metadata
- **Source:** HackerOne
- **Report:** 94925 | https://hackerone.com/reports/94925
- **Submitted:** 2015-10-20
- **Reporter:** datokaa
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** businesslogic
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hello once again,

I have discovered another balance manipulation bug. This time it is much more simpler, but basically has the same outcome. 

EXPLANATION: When you create basic standard Vault and transfer money from your Main Wallet to the vault the balance doesn't "lock up", which means that even when the transfer is pending to the vault you are still freely able to transfer the balance to othe

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

Hello once again,

I have discovered another balance manipulation bug. This time it is much more simpler, but basically has the same outcome. 

EXPLANATION: When you create basic standard Vault and transfer money from your Main Wallet to the vault the balance doesn't "lock up", which means that even when the transfer is pending to the vault you are still freely able to transfer the balance to other btc wallets from your main wallet. Once you approve the transfer to Vault your balance would go into Negative resulting in balance manipulation.

If you have any more questions/concerns feel free to ask.


Thanks,

David.

</details>

---
*Analysed by Claude on 2026-05-24*
