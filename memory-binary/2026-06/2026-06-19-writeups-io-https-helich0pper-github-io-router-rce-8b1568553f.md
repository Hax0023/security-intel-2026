# Pivot Into A Network Using A Compromised Router

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** ISP Router (unspecified vendor)
- **Bounty:** Not mentioned
- **Severity:** CRITICAL
- **Vuln types:** Command Injection, Unauthenticated Remote Code Execution, Bind Shell, Lateral Movement, Network Pivoting
- **Category:** memory-binary
- **Writeup:** https://helich0pper.github.io/router_rce/

## Summary
An ISP-provisioned router was found containing an unauthenticated bind shell listening on port 40001 with root privileges, likely deployed for remote maintenance purposes. The researcher discovered 55+ affected routers on a single subnet, enabling attackers to pivot into internal networks and compromise downstream devices without authentication.

## Attack scenario (step by step)
1. Attacker scans external IP address and discovers open port 40001 on router
2. Attacker connects to bind shell on port 40001 using netcat, gaining unauthenticated root shell access
3. Attacker executes 'arp -a' command on compromised router to enumerate internal network IP addresses
4. Attacker uses compromised router to port-scan internal targets (e.g., Metasploitable at 192.168.1.108)
5. Attacker uploads full-featured networking tools (busybox-mips with complete netcat) to router for enhanced reconnaissance
6. Attacker connects through pivoted router to compromised internal hosts and exploits them (e.g., telnet to port 23 with default credentials)

## Root cause
ISP deployed unauthenticated bind shell on router for remote maintenance access without proper security controls (no authentication, no firewall restrictions, exposed to WAN)

## Attacker mindset
Opportunistic network reconnaissance and lateral movement. Attacker views router compromise as entry point for internal network access, leveraging it as a proxy to bypass network segmentation and exploit downstream systems with default credentials.

## Defensive takeaways
- Remove or disable all backdoor maintenance shells before customer deployment
- Implement authentication on all management interfaces, even internal ones
- Restrict bind shell access to specific trusted IP addresses or disable external access entirely
- Change default credentials on all pre-deployed devices
- Segment networks to prevent compromised routers from accessing internal resources
- Implement firewall rules on router to block internal network scanning from WAN-connected services
- Deploy EDR/monitoring on internal network to detect lateral movement attempts
- Audit and monitor router firmware for unauthorized modifications or shells
- Implement rate-limiting on port scanning attempts from router interfaces

## Variant hunting
['Search for other ISP-provided router models with similar maintenance shells on known ports (40001, 5900, 9999, etc.)', 'Scan for bind shells on alternative TCP/UDP ports across ISP network ranges', 'Identify other ISP firmware versions with embedded unauthenticated services', 'Search for other devices (modems, gateways, IoT) with similar maintenance backdoors', 'Check for hardcoded credentials in router firmware strings', 'Analyze firmware for command injection vulnerabilities in web interface input fields']

## MITRE ATT&CK
- T1190
- T1021.004
- T1021.001
- T1046
- T1557.002
- T1040
- T1589.002
- T1592
- T1199
- T1133

## Notes
This is a critical supply-chain security failure where ISP introduced backdoors into customer networks. The researcher responsibly disclosed the vulnerability and demonstrated real-world pivoting attack. The writeup lacks specific router vendor/model details and ISP disclosure status. The bind shell appears intentionally deployed rather than accidental vulnerability, suggesting systemic security negligence or intentional backdooring for ISP support access that was never properly secured or removed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
