# Coinbase Android Application - Bitcoin Wallet Leaks OAuth Response Code

## Metadata
- **Source:** HackerOne
- **Report:** 5314 | https://hackerone.com/reports/5314
- **Submitted:** 2014-03-31
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

There's a simple bug here, the Coinbase Android App. "BitCoin Wallet" leaks the **OAuth** Response Code which can be obtained using `adb logcat -s Coinbase` command line for testing, and any Android application on the same phone can read the response code for the user by reading the logs. As of now nothing can be harmed with OAuth Response code, but along with the hardcoded `client secret` 

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

There's a simple bug here, the Coinbase Android App. "BitCoin Wallet" leaks the **OAuth** Response Code which can be obtained using `adb logcat -s Coinbase` command line for testing, and any Android application on the same phone can read the response code for the user by reading the logs. As of now nothing can be harmed with OAuth Response code, but along with the hardcoded `client secret` we can obtain the `access_token`.

This bug is similar to this - http://attack-secure.com/all-your-facebook-access-tokens-are-belong-to-us/

So using the stolen response code and `client secret` we can derive the `access_token`

POC: https://www.dropbox.com/s/zionksi1pt7lot5/Coinbase-Android.mov

</details>

---
*Analysed by Claude on 2026-05-24*
