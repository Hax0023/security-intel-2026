# Pivot Into A Network Using A Compromised Router

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** ISP Router (unnamed)
- **Bounty:** Not mentioned - appears to be personal research/disclosure
- **Severity:** Critical
- **Vuln types:** Unauthenticated Bind Shell, Command Injection, Lack of Network Segmentation, Default Credentials, Information Disclosure
- **Category:** memory-binary
- **Writeup:** https://helich0pper.github.io/router_rce/

## Summary
A router provisioned by an ISP contained an unauthenticated bind shell listening on port 40001 with root privileges, accessible without authentication. This allowed an attacker to pivot into the internal network, enumerate hosts via ARP, perform port scanning, and compromise internal machines like Metasploitable. The vulnerability affected at least 55 routers on the subnet and likely represents either intentional ISP maintenance backdoors or widespread bot compromise.

## Attack scenario (step by step)
1. Attacker discovers router with exposed bind shell on port 40001 via network scanning or default ISP configurations
2. Attacker connects to port 40001 using netcat and gains unauthenticated root shell access to the router
3. Attacker uses ARP commands on compromised router to enumerate internal network hosts and identify targets (e.g., 192.168.1.108)
4. Attacker transfers busybox-mips binary to router via netcat to enable port scanning capabilities
5. Attacker performs TCP port scans of internal targets from router to identify vulnerable services
6. Attacker exploits identified services (e.g., telnet with default credentials) on internal machines to establish footholds

## Root cause
ISP deployed routers with permanently listening bind shells for remote maintenance purposes without proper authentication, access controls, or network segmentation. The shell runs with root privileges and was either left exposed intentionally or compromised by botnets exploiting default credentials (admin::admin).

## Attacker mindset
Network pivoting and lateral movement opportunist. The attacker recognized that compromising a single router device grants access to an entire internal network previously isolated from external attack. This represents a force multiplier attack where one entry point becomes a beachhead for attacking multiple internal targets. The attacker methodically enumerated the network topology, identified targets, adapted tools to resource-constrained environments, and systematically moved laterally.

## Defensive takeaways
- Never expose management interfaces or maintenance shells to the network without strong authentication and encryption
- Implement network segmentation to isolate router management from guest/user networks
- Change default credentials on all network devices immediately upon deployment
- Regularly audit open ports and listening services on network devices
- Use VPN or out-of-band management channels for remote device administration
- Monitor ARP traffic and implement dynamic ARP inspection (DAI) to detect reconnaissance
- Deploy intrusion detection on internal networks to identify lateral movement attempts
- Conduct security assessments of ISP-provided equipment before deployment
- Implement rate limiting and connection tracking on internal network services
- Use endpoint detection and response (EDR) tools to detect suspicious process execution on internal hosts

## Variant hunting
['Search for other ISP-provided routers with similar maintenance shells or backdoors', 'Test for other listening ports that may contain unauthenticated services', 'Examine router firmware for embedded credentials or hardcoded authentication bypasses', 'Check for other common maintenance tools (SSH, SNMP) running without proper access controls', 'Look for vulnerable versions of busybox or other embedded tools that can be exploited directly', 'Test for command injection vulnerabilities in router web interface input fields', 'Scan for routers with default credentials that may have been compromised by botnets', 'Identify other ISPs or router manufacturers with similar security postures']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (exposed bind shell)
- T1200 - Hardware Additions (ISP router compromise)
- T1557 - Man-in-the-Middle (network positioning)
- T1040 - Traffic Capture/Inspection (ARP enumeration)
- T1046 - Network Service Scanning (port enumeration via netcat)
- T1021 - Remote Services (bind shell access)
- T1078 - Valid Accounts (default credentials msfadmin::msfadmin)
- T1570 - Lateral Tool Transfer (busybox-mips upload)
- T1057 - Process Discovery (enumeration via router tools)
- T1580 - Cloud Infrastructure Discovery (internal network reconnaissance)

## Notes
This writeup documents a serious supply chain security issue where ISP-provided equipment was deployed with maintenance backdoors accessible to anyone on the network. The finding suggests either negligent security practices or intentional backdoors by the ISP. The presence of bind shells on 55+ routers in the subnet indicates this was not a one-off misconfiguration but likely a standard deployment practice. The attacker's methodical approach demonstrates how router compromise enables sophisticated internal network attacks despite perimeter security. The lack of exploitation details and the framing as educational research suggests the author responsibly disclosed findings rather than launching active attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
