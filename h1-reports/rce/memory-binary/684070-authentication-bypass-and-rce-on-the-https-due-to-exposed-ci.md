# Authentication Bypass and RCE via Exposed Cisco TelePresence SX80 with Default Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 684070 | https://hackerone.com/reports/684070
- **Submitted:** 2019-08-29
- **Reporter:** sp1d3rs
- **Program:** Undisclosed (HackerOne Report #684070)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Default Credentials, Authentication Bypass, Remote Code Execution, Insecure Device Configuration, Exposed Management Interface
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Cisco TelePresence SX80 video conferencing device was exposed on the internet with unchanged default credentials, allowing unauthenticated attackers to gain full administrative access. The attacker could leverage this access to execute arbitrary code, add malicious startup scripts, intercept communications, and establish persistent backdoors on the device.

## Attack scenario
1. Attacker discovers publicly exposed Cisco TelePresence SX80 device via IP scanning or shodan.io-style reconnaissance
2. Attacker identifies the device type and attempts default credentials for Cisco TelePresence systems
3. Attacker successfully authenticates to the web management interface using unchanged default credentials
4. Attacker navigates to the scripts management section at /web/scripts endpoint
5. Attacker uploads malicious startup scripts that execute arbitrary code with device privileges
6. Attacker gains persistent code execution and can intercept video/audio conferencing data, monitor sensitive discussions, or pivot to internal network

## Root cause
Device deployed to production with default credentials never changed from factory settings. No network segmentation or access controls to restrict administrative interface exposure to internet. Lack of mandatory credential change during initial setup process.

## Attacker mindset
Target high-value devices in corporate environments (training rooms, boardrooms, auditoriums) to establish persistent surveillance capability. Default credentials provide easy entry point requiring minimal reconnaissance. Focus on persistent backdoor rather than destructive access to avoid detection while gathering intelligence from sensitive meetings and communications.

## Defensive takeaways
- Enforce mandatory password changes for all networked devices during deployment and initial configuration
- Implement network segmentation to restrict management interfaces to internal-only access via VPN/bastion hosts
- Disable default accounts entirely or enforce complex unique credentials before device activation
- Deploy intrusion detection for failed authentication attempts on management interfaces
- Conduct periodic audits of internet-exposed network devices and management services
- Implement device hardening baselines that disable unnecessary services and restrict script upload capabilities
- Use configuration management tools to enforce security baselines across all video conferencing devices
- Monitor for unauthorized script uploads or modifications to startup configurations

## Variant hunting
Search for other exposed Cisco TelePresence models (SX20, SX40, SX60, MX series) with default credentials. Check for similar patterns on other video conferencing equipment (Polycom, Cisco Webex Room devices, etc.). Look for exposed management interfaces on ports commonly used by conferencing devices (80, 443, 8080). Investigate other ASNs belonging to same organization for similar misconfigurations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (Default Credentials)
- T1199 - Trusted Relationship
- T1059 - Command and Scripting Interpreter
- T1543 - Create or Modify System Process (startup scripts)
- T1021 - Remote Service Session Initiation
- T1021.001 - Remote Service Session Initiation - RDP
- T1110.001 - Brute Force - Credentials

## Notes
Report contains redacted information (IP addresses, credentials, URLs). The vulnerability represents a critical supply chain/trusted device compromise vector since video conferencing systems are present in sensitive meeting spaces. The attacker's observation about 'silent compromise' for data interception is particularly concerning in boardroom/executive contexts. Suggests these devices may not have been asset-tracked or security-scanned properly before deployment. The mention of ASN verification indicates organizational scope determination was part of reporter's reconnaissance.

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
*Analysed by Claude on 2026-05-12*
