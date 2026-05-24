# IDOR in backup recovery functionality

## Metadata
- **Source:** HackerOne
- **Report:** 1901713 | https://hackerone.com/reports/1901713
- **Submitted:** 2023-03-12
- **Reporter:** theelgo64
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** businesslogic
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
Hi team I hope you are well, there is an issue let me to takeover any backup via recover it to my machine.

## Steps To Reproduce
1. Login https://mc-beta-cloud.acronis.com
2. Visit the DEVICES section [you must have 2 devices]
3. Click on any device has a backup [device_1]
4. Click on recovery > select machine > select the second machine [device_2]
5. follow the steps to recover the ba

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

## Summary
Hi team I hope you are well, there is an issue let me to takeover any backup via recover it to my machine.

## Steps To Reproduce
1. Login https://mc-beta-cloud.acronis.com
2. Visit the DEVICES section [you must have 2 devices]
3. Click on any device has a backup [device_1]
4. Click on recovery > select machine > select the second machine [device_2]
5. follow the steps to recover the backup to [device_2]
6. In the burp search for this endpoint ```/bc/api/ams/recovery/plan_operations/run```
7. Send the request again via ==X-Apigw-Session== session from another organization.


## POC

{F2222128}

## Impact

- Backup Takeover via recovery function.

</details>

---
*Analysed by Claude on 2026-05-24*
