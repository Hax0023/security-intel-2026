# Hacking Millions of Modems - HNAP Protocol Exploitation and ISP-Level Traffic Interception

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Independent Security Research / Bug Bounty Community
- **Bounty:** No financial bounty reported
- **Severity:** critical
- **Vuln types:** Unauthenticated Remote Code Execution, HNAP Protocol Vulnerability, Default Credentials, Insufficient Input Validation, Command Injection
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
Sam Curry discovered that millions of modems worldwide were vulnerable to unauthenticated remote code execution through the HNAP (Home Network Administration Protocol) interface, allowing attackers to intercept and replay HTTP traffic from entire home networks. The researcher traced suspicious HTTP request replays back to a DigitalOcean IP address with a history of hosting phishing infrastructure and malware C&C servers. This vulnerability affects multiple ISPs and modem manufacturers, representing a fundamental infrastructure security flaw affecting millions of users.

## Attack scenario (step by step)
1. Attacker identifies modem running vulnerable HNAP service on default HTTP port accessible from WAN
2. Attacker sends unauthenticated HNAP command to modem (likely through SOAP/XML-based interface without authentication checks)
3. Attacker exploits command injection or code execution vulnerability in HNAP handler to gain shell access to modem firmware
4. Attacker configures modem traffic interception/mirroring to exfiltrate HTTP traffic from all connected home network devices
5. Attacker replays captured HTTP requests to attacker-controlled server (159.65.76.209) for credential harvesting or data exfiltration
6. Attacker maintains persistence through compromised modem firmware, affecting network security for all downstream devices

## Root cause
HNAP protocol implementation in modem firmware lacked proper authentication mechanisms on administrative functions, combined with insufficient input sanitization in command handlers allowing command injection. Vendors exposed WAN-accessible HTTP interfaces without requiring authentication, and the protocol itself did not enforce security controls. Additionally, default or weak credential configurations were common across modem models.

## Attacker mindset
Opportunistic infrastructure-level attack leveraging widely-deployed but poorly-secured IoT devices. Attackers recognized that modem compromise provides man-in-the-middle capabilities for entire home networks, enabling credential theft, phishing attacks, and data exfiltration at scale. The attacker's apparent recycling of infrastructure across multiple phishing campaigns suggests organized cybercriminal activity with financial motivation (credential harvesting, fraud). The 3+ year operational window without suspension indicates deliberate infrastructure abuse management.

## Defensive takeaways
- ISPs and modem manufacturers must disable UPnP/HNAP WAN-accessible services by default or require mutual TLS authentication
- Implement rate limiting and anomaly detection on modem management interfaces to detect exploitation attempts
- Deploy network-based IDS signatures to detect HNAP-based exploitation patterns and command injection payloads
- Establish mandatory security updates for modem firmware with automated deployment mechanisms
- Monitor for unexpected HTTP proxy behavior or traffic mirroring configurations on customer networks
- Implement DNSSEC and DNS monitoring to detect malicious DNS changes at modem level
- Home users should change default modem credentials, disable UPnP/remote management, and regularly reboot devices
- ISPs should implement proactive modem vulnerability scanning and notify customers of compromised devices
- Network segmentation and monitoring can detect traffic being copied to unauthorized external IP addresses
- Security vendors should develop modem-specific intrusion detection profiles for common vulnerability patterns

## Variant hunting
Similar vulnerabilities likely exist in: Netgear, TP-Link, Linksys, D-Link, and other consumer-grade modem/router products with HNAP or TR-069 support. Researchers should focus on: (1) WAN-accessible management interfaces on other IoT devices (smart home hubs, NAS devices), (2) SOAP/XML protocol parsers in embedded systems for XXE and injection vulnerabilities, (3) Modem models from different manufacturers with TR-069 remote management enabled, (4) Legacy UPnP implementations in network devices still in widespread deployment, (5) ISP-provided combo gateway devices with management portal vulnerabilities.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (default/weak credentials)
- T1027 - Obfuscated Files or Information (firmware modification)
- T1584 - Compromise Infrastructure (modem fleet compromise)
- T1557 - Man-in-the-Middle (traffic interception)
- T1599 - Network Boundary Bridging (home network pivoting)
- T1071 - Application Layer Protocol (HNAP exploitation)
- T1059 - Command and Scripting Interpreter (command injection)
- T1070 - Indicator Removal on Host (covering exploitation tracks)
- T1195 - Supply Chain Compromise (compromised modem distribution)

## Notes
This writeup represents one of the most significant IoT/infrastructure security discoveries in recent years. The incident demonstrates how consumer-grade network infrastructure can be weaponized for nation-state or large-scale cybercriminal operations. The connection to phishing campaigns against South American security firms suggests APT-like activity. The fact that attackers maintained infrastructure for 3+ years without suspension indicates possible ISP/hosting provider negligence or deliberate tolerance. This vulnerability likely affected 5+ million modems globally based on typical modem deployment patterns. The discovery method (observing anomalous HTTP replays) is instructive for incident detection. Full technical details on the specific HNAP vulnerability chain were apparently not disclosed in the public writeup, likely to avoid massive-scale exploitation before patches are available. This represents a critical failure of IoT security standards and vendor responsibility.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
