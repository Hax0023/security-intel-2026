# Authentication Bypass and RCE on Cisco TelePresence SX80 via Default Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 684758 | https://hackerone.com/reports/684758
- **Submitted:** 2019-08-29
- **Reporter:** sp1d3rs
- **Program:** Undisclosed (Cisco TelePresence environment)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Default Credentials, Authentication Bypass, Remote Code Execution, Insufficient Access Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Cisco TelePresence SX80 device was exposed on the internet with unchanged default credentials (admin:admin), allowing unauthenticated attackers to gain administrative access. Once authenticated, attackers can upload and execute arbitrary startup scripts through the web interface, achieving remote code execution and full device compromise.

## Attack scenario
1. Attacker identifies Cisco TelePresence SX80 device via network scanning or public IP enumeration
2. Attacker attempts default credentials (admin:admin) against the web management interface
3. Authentication succeeds due to unchanged default password
4. Attacker navigates to the scripts management section (/web/scripts) with admin privileges
5. Attacker uploads malicious startup scripts or payload files
6. Scripts execute with device privileges, providing RCE and persistent backdoor access

## Root cause
Device deployed with default credentials never changed during initial setup and provisioning. Lack of enforced credential change policy or pre-deployment hardening checklist. Device remained unused since 2017 without security updates or monitoring.

## Attacker mindset
Opportunistic actor leveraging publicly routable infrastructure and well-known default credentials for videoconferencing equipment. Sequential scanning of IP ranges after initial successful exploitation. Focus on persistence through startup scripts rather than volatile exploitation. Targeting devices in communication/collaboration spaces for data interception.

## Defensive takeaways
- Enforce mandatory credential change on first login before device can be used
- Implement network segmentation for management interfaces - restrict administrative access to specific VLANs
- Deploy continuous credential scanning to detect default credentials on Internet-exposed assets
- Require multi-factor authentication for privileged device management functions
- Disable or restrict script upload/execution capabilities unless explicitly required
- Implement device lifecycle management with regular firmware patching schedules
- Monitor for devices with unchanged default credentials across all asset classes
- Apply principle of least privilege for default admin accounts
- Conduct regular security assessments of remote/unused devices

## Variant hunting
Search for other Cisco TelePresence models (SX20, SX40, SX60) with default credentials; audit related endpoints for script upload functionality; check for other ASN 257 IP ranges with exposed management interfaces; identify similar videoconferencing equipment (Polycom, Avaya) with weak authentication

## MITRE ATT&CK
- T1190
- T1200
- T1078
- T1078.001
- T1547.013
- T1199
- T1566

## Notes
Report demonstrates sequential vulnerability discovery in same network range (ASN 257), suggesting systemic lack of security controls. Previous report #684070 indicates pattern of unpatched/misconfigured devices. Critical concern is silent compromise potential for data interception in meeting rooms rather than obvious RCE. Device inactivity since 2017 indicates insufficient asset inventory and lifecycle management.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I was able to identify another one Cisco TelePresence SX80 device located on the https://████████ right near the previous device `████` (after #684070 report I decided to check ████* range)
According to the IP Info: https://ipinfo.io/AS257/████0/24 it belongs to ASN with ID 
```
AS257 ███
```

The mentioned instance has same credentials `admin:admin`.
This instance is different and less used, the logs reveals that last time device was used in 2017 year.

##POC
https://████████
Login with `admin:admin`
███████
Since we are logged in as admin, we can completely control the device and all connections, and add our startup scripts via https://███████/web/scripts thus achiecing code execution.

##Suggested fix
Change the credentials and likely you will need to reset the device to factory settings

## Impact

Potential device compromise and code execution. This devices are used mainly for trainings, briefings, and demonstration rooms, as well as auditoriums, so attacker with full control of the device potentially can intercept the data (RCE potential is interesting, but ability to silently compromise the device and use it as backdoor can be much more harmful).

</details>

---
*Analysed by Claude on 2026-05-12*
