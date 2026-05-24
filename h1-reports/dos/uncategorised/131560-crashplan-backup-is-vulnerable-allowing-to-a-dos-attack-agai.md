# CrashPlan Backup Server DoS via Unrate-Limited Friend Code Brute Force

## Metadata
- **Source:** HackerOne
- **Report:** 131560 | https://hackerone.com/reports/131560
- **Submitted:** 2016-04-17
- **Reporter:** ddworken
- **Program:** Uber
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service, Brute Force Attack, Insufficient Rate Limiting, Insecure Default Configuration
- **CVEs:** None
- **Category:** uncategorised

## Summary
CrashPlan's backup server at backup.uber.com is vulnerable to brute force attacks due to lack of rate limiting on friend code validation endpoints. An attacker can enumerate the 6-digit alphanumeric friend code (2.1B possibilities) and gain unauthorized write access to upload arbitrary data, exhausting storage and preventing legitimate employee backups.

## Attack scenario
1. Attacker identifies CrashPlan backup server running on backup.uber.com:443
2. Attacker discovers the friend code feature allows backup uploads from external computers using 6-digit alphanumeric codes
3. Attacker writes script to brute force the friend code validation endpoint without rate limiting constraints
4. Attacker successfully enumerates the valid friend code for Uber's CrashPlan instance
5. Attacker uploads large volumes of malicious/junk data using the valid friend code
6. Legitimate Uber employee backups fail due to exhausted storage capacity (Denial of Service)

## Root cause
CrashPlan lacks rate limiting on the friend code validation endpoint combined with insecure default configuration allowing inbound backups from untrusted sources. The 6-digit code space is computationally feasible to brute force, and no authentication or authorization validation prevents unauthorized uploads.

## Attacker mindset
External threat actor targeting enterprise backup infrastructure to disrupt business continuity. Attacker recognized that backup systems are critical infrastructure and that filling storage would impact all employees. Attack requires no authentication and exploits product design flaws rather than implementation bugs.

## Defensive takeaways
- Implement aggressive rate limiting on all authentication/validation endpoints, especially those with small keyspace (2.1B iterations)
- Apply secure defaults: disable inbound backup features unless explicitly enabled with strong justification
- Deploy network segmentation and firewall rules restricting backup server access to known internal subnets
- Implement exponential backoff and account lockout mechanisms after repeated failed validation attempts
- Monitor for brute force patterns on validation endpoints (multiple failed attempts from single source)
- Use CAPTCHA or challenge-response after initial failed attempts to defeat automated enumeration
- Implement stronger friend codes (longer, higher entropy) if feature must remain enabled
- Regularly audit backup infrastructure for unnecessary exposed services and features

## Variant hunting
Enumerate other Code42/CrashPlan deployments across enterprise environments for similar misconfiguration
Test other backup solutions (Carbonite, Backblaze, Acronis) for rate limiting on pairing/friend code mechanisms
Investigate other Uber infrastructure services exposed publicly for similar authentication bypass patterns
Search for other instances of CrashPlan with inbound backups enabled on public IPs using port scanning
Test backup restore endpoints for similar rate limiting bypasses that could enable data extraction attacks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force
- T1499 - Endpoint Denial of Service
- T1657 - Man in the Middle

## Notes
Reporter David Dworken responsibly disclosed to both Uber and Code42 (CrashPlan vendor). The vulnerability demonstrates how backup infrastructure exposed to internet requires hardened security posture. The attack is concerning because backup systems are typically deprioritized for hardening despite being critical infrastructure. The 2.1B keyspace is computationally feasible on modern hardware (~days of compute), making this a practical attack vector rather than theoretical.

## Full report
<details><summary>Expand</summary>

```backup.uber.com``` hosts a CrashPlan backup server on port 443. CrashPlan allows users to backup to a friends computer by entering a 6 digit alphanumeric code. This means there are 2,176,782,336 total CrashPlan friend codes. While this is a high number, it is completely possible to brute force this as CrashPlan does not have any rate limiting on their end point to check the validity of a code. 

By iterating through all the friend codes I would be able to find the friend code for the CrashPlan instance running on ```backup.uber.com``` thereby allowing me to upload my data to the server hosting ```backup.uber.com```. 

I wasn't quite sure what to categorize this as so I put it down as a denial of service vulnerability since it would allow me to fill the ```backup.uber.com``` server up with data so that employees would not be able to backup their data. 

In order to patch this you have to go into the settings in CrashPlan and disable "Inbound backup from other computers". If you are using this feature, you should add a firewall between ```backup.uber.com``` to block connections not originating from Uber. 

I am also reporting this to Code42 (creators of CrashPlan) to suggest that they switch to a secure default. 

Thanks,
David Dworken

</details>

---
*Analysed by Claude on 2026-05-24*
