# Hacking Millions of Modems - ISP/Modem Traffic Interception and Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Self-discovered vulnerability affecting millions of modem users
- **Bounty:** No bounty mentioned - self-researched investigation
- **Severity:** critical
- **Vuln types:** Man-in-the-Middle (MITM) Attack, HTTP Traffic Interception, Modem Compromise, ISP-level Traffic Manipulation, DNS Hijacking, Request Replay Attack
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A researcher discovered that their HTTP traffic was being intercepted and replayed by an unknown IP address (159.65.76.209 on DigitalOcean) across all devices on their home network. Investigation revealed the IP was previously used for phishing campaigns against cybersecurity firms and BeEF-based malicious infrastructure, suggesting widespread modem compromise affecting millions of users.

## Attack scenario (step by step)
1. Attacker compromises ISP modem firmware or gains ISP-level access to traffic routing
2. When victim sends HTTP request from any device on home network, traffic is intercepted at modem/ISP level
3. Request is replayed to attacker-controlled DigitalOcean IP (159.65.76.209) within 10 seconds
4. Attacker captures request data, potentially exfiltrating credentials, tokens, or sensitive information from HTTP requests
5. Same behavior confirmed across multiple devices (computer, iPhone) and multiple cloud providers (AWS, GCP)
6. Attacker maintains persistence through compromised modem firmware while hosting phishing and C&C infrastructure

## Root cause
Modem firmware compromise allowing transparent HTTP traffic interception and relay to attacker-controlled infrastructure. Traffic bypasses encryption by targeting Layer 2/3 network level before HTTPS encryption is applied, or intercepting unencrypted HTTP requests.

## Attacker mindset
Opportunistic threat actor operating low-visibility, long-persistence infrastructure for multiple purposes: credential harvesting via phishing, malware C&C, and transparent traffic interception for data theft. Reuses IP addresses across campaigns to reduce infrastructure costs while maintaining operational security against detection.

## Defensive takeaways
- Deploy HTTPS/TLS everywhere - unencrypted HTTP traffic is vulnerable to ISP/network-level interception
- Monitor modem firmware for unauthorized modifications and enable secure boot if available
- Implement certificate pinning in applications to prevent MITM attacks even with compromised CA
- Use VPN/encrypted tunnels for all traffic, especially from home networks
- Monitor for unexpected traffic patterns and replay attacks in access logs
- Regularly audit modem settings and default credentials - change all default passwords
- Enable DNS-over-HTTPS (DoH) and DNSSEC to prevent DNS hijacking
- Use network-level monitoring to detect suspicious outbound traffic from local devices
- Segment home network to isolate IoT and smart home devices from critical systems
- Contact ISP if modem appears compromised; request firmware audit and replacement

## Variant hunting
Search for similar long-lived compromised infrastructure across ISPs; investigate other DigitalOcean IPs hosting phishing/BeEF sites; track domains isglatam.online, isglatam.tk, regional.adidas.com.py and associated infrastructure; analyze modem firmware for backdoors targeting common models (TP-Link, Netgear, Motorola, Arris); hunt for other requests replayed to 159.65.76.209 or similar patterns in ISP/network logs; investigate mx12.* domains for active C&C infrastructure.

## MITRE ATT&CK
- T1557.002 - Man-in-the-Middle: ARP Cache Poisoning (network-level interception)
- T1557.001 - Man-in-the-Middle: LLMNR/NBT-NS Spoofing (DNS hijacking variant)
- T1040 - Traffic Sniffing
- T1041 - Exfiltration Over C2 Channel
- T1071.001 - Application Layer Protocol: Web Protocols
- T1190 - Exploit Public-Facing Application (modem firmware exploitation)
- T1200 - Hardware Additions (modem firmware implant)
- T1566.002 - Phishing: Spearphishing Link (BeEF infrastructure)
- T1598 - Phishing for Information
- T1651 - Domain Trust Discovery (intercepting network traffic to map infrastructure)

## Notes
Writeup appears incomplete (cuts off mid-sentence). Critical infrastructure vulnerability affecting millions. Attacker IP (159.65.76.209) shows long operational tenure (3+ years) with multiple concurrent campaigns (phishing, C&C, MITM). Suggests well-resourced threat group or compromised upstream provider. ISG Latam connection indicates potential targeting of security professionals and companies. Request replay attack strategy suggests sophisticated understanding of network architecture. Severity amplified by affects on unencrypted HTTP - modern internet should enforce HTTPS but legacy systems remain vulnerable.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
