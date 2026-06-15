# Hacking Millions of Modems - HTTP Traffic Interception and Replay Attack

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Independent Research / Bug Bounty (No specific program mentioned)
- **Bounty:** Not Specified
- **Severity:** Critical
- **Vuln types:** Man-in-the-Middle (MITM) Attack, HTTP Traffic Interception, Router/Modem Compromise, DNS Hijacking, Firmware Vulnerability, Insufficient Access Controls
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A security researcher discovered that HTTP traffic from their home network was being intercepted and replayed by an unknown attacker using a compromised modem or router. The attacker's infrastructure (159.65.76.209 on DigitalOcean) was previously used for phishing campaigns targeting cybersecurity companies, suggesting organized cybercriminal activity targeting millions of connected modems.

## Attack scenario (step by step)
1. Attacker gains control of ISP-provided modem/router through firmware vulnerability or weak credentials
2. Attacker configures router to intercept all outgoing HTTP traffic from connected devices
3. When researcher sends HTTP request from home network, modem captures the request
4. Attacker's infrastructure replays the captured HTTP request from external IP (159.65.76.209) to exfiltrate data
5. Attacker repeats process across millions of customer modems nationwide, creating botnet for traffic interception
6. Attacker leverages same infrastructure for secondary malicious activities (phishing, C&C operations)

## Root cause
Modems shipped with default/hardcoded credentials, unpatched firmware vulnerabilities, or insecure management interfaces allowing remote compromise. Modem firmware likely lacked proper HTTPS enforcement and had built-in HTTP interception capabilities for ISP monitoring that were exploited.

## Attacker mindset
Sophisticated cybercriminal group operating infrastructure for 3+ years without disruption. Demonstrates capability to compromise consumer hardware at scale and monetize through multiple attack vectors (phishing, malware C&C, data exfiltration). Reuses infrastructure across different campaigns, suggesting operational efficiency over operational security.

## Defensive takeaways
- Implement mandatory HTTPS for all traffic; HTTP should never be trusted on consumer networks
- ISPs must secure modem firmware with regular patches and disable default credentials immediately upon deployment
- Implement certificate pinning in applications to prevent MITM attacks even with compromised network hardware
- Monitor for unexpected outbound traffic patterns from home network devices
- Segment IoT/modem devices on separate network from sensitive systems
- Enable automatic firmware updates on all consumer networking equipment
- ISPs should implement modem anomaly detection systems to identify compromise signatures
- Disable HTTP and telnet management interfaces on modems; enforce strong, unique credentials
- Implement threat intelligence sharing between ISPs to identify compromised modem botnet activity

## Variant hunting
Search for similar MITM attacks on consumer routers (TP-Link, Netgear, Linksys, etc.); investigate other DigitalOcean IPs associated with phishing domains; analyze traffic patterns for unexplained HTTP request replays; monitor ISP forums for reports of traffic interception; correlate modem compromise with downstream phishing/malware campaigns.

## MITRE ATT&CK
- T1557 - Adversary-in-the-Middle
- T1557.002 - MITM: ARP Cache Poisoning
- T1557.003 - MITM: DHCP Spoofing
- T1190 - Exploit Public-Facing Application
- T1586 - Compromise Accounts
- T1199 - Trusted Relationship
- T1566.002 - Phishing: Spearphishing Link
- T1571 - Non-Standard Port
- T1041 - Exfiltration Over C2 Channel

## Notes
The writeup demonstrates exceptional investigative methodology using IP reputation analysis, domain history tracking, and controlled testing. The researcher's finding suggests a supply-chain attack vector affecting millions of modems. The attacker's infrastructure overlap between phishing (ISG Latam), malware C&C, and traffic interception indicates a coordinated criminal operation. The 3+ year operational period without ISP suspension suggests either weak ISP security monitoring or potential ISP complicity. This represents a critical vulnerability in consumer broadband infrastructure with massive scope.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
