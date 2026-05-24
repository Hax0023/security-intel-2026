# Authentication bypass and RCE on the https://████ due to exposed Cisco TelePresence SX80 with default credentials

## Metadata
- **Source:** HackerOne
- **Report:** 684070 | https://hackerone.com/reports/684070
- **Submitted:** 2019-08-29
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** memory-binary

## Summary
##Description
Hello. I was able to identify Cisco TelePresence SX80 device located on the https://█████
According to the IP Info: https://ipinfo.io/████████it belongs to ASN with ID 
```
███████
```
so it's likely in scope of the program.
The mentioned instance has default credentials `████`

##POC
https://███████
Login with `█████████`
████
Since we are logged in as ███, we can completely control

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

##Description
Hello. I was able to identify Cisco TelePresence SX80 device located on the https://█████
According to the IP Info: https://ipinfo.io/████████it belongs to ASN with ID 
```
███████
```
so it's likely in scope of the program.
The mentioned instance has default credentials `████`

##POC
https://███████
Login with `█████████`
████
Since we are logged in as ███, we can completely control the device and all connections, and add our startup scripts via https://██████████/web/scripts

##Suggested fix
Change the credentials and likely you will need to reset the device

## Impact

Potential device compromise and code execution. This devices are used mainly for trainings, briefings, and demonstration rooms, as well as auditoriums, so attacker with full control of the device potentially can intercept the data (RCE potential is interesting, but ability to silently compromise the device and use it as backdoor can be much more harmful).

</details>

---
*Analysed by Claude on 2026-05-24*
