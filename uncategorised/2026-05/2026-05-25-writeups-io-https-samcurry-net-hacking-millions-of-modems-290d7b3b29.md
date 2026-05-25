# Hacking Millions of Modems - Home Network Traffic Interception and Modem Compromise Investigation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Independent security research / self-discovery
- **Bounty:** None disclosed
- **Severity:** critical
- **Vuln types:** Modem compromise/malware, Man-in-the-Middle (MITM), HTTP traffic interception, DNS hijacking, Lack of modem authentication/authorization, Insecure default credentials on modem
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
Security researcher Sam Curry discovered that his home modem had been compromised and was intercepting and replaying HTTP traffic from all devices on his network to an attacker-controlled IP address (159.65.76.209 on DigitalOcean). Through investigation, he determined the IP belonged to infrastructure previously used for phishing campaigns targeting South American cybersecurity companies and BeEF exploitation frameworks, suggesting widespread modem malware affecting millions of consumer devices.

## Attack scenario (step by step)
1. Attacker gains initial access to modem through weak default credentials, unpatched firmware vulnerability, or supply chain compromise
2. Malware installed on modem intercepts all HTTP traffic traversing the device from all connected clients
3. When victim sends HTTP request from home network, modem forwards legitimate traffic but also exfiltrates/replays request to attacker infrastructure
4. Attacker's server at 159.65.76.209 receives replayed requests from victim's modem within seconds of original request
5. Attacker can monitor victim's web activities, perform session hijacking, credential theft, or inject malicious content into responses
6. Attack persists transparently across all devices on network (computers, phones, IoT) as modem-level MITM

## Root cause
Modems shipped with exploitable vulnerabilities (likely unpatched firmware) or weak default credentials that allowed unauthorized administrative access. Lack of integrity verification and encryption of modem management interfaces enabled persistent malware installation.

## Attacker mindset
Opportunistic cybercriminals operating from bulletproof hosting with low operational security awareness, maintaining long-term persistence (3+ years) by blending activities (phishing infrastructure, C&C servers, router malware distribution). Low concern for detection or ISP/hosting provider enforcement.

## Defensive takeaways
- Implement mandatory modem firmware updates with integrity checking and secure boot mechanisms
- Enforce strong default credentials and require password changes on first login
- Deploy ISP-level traffic inspection to detect unusual outbound modem communications
- Monitor modem access logs and anomalous DNS/HTTP patterns indicating compromise
- Use HTTPS/DNS-over-HTTPS for all traffic to prevent plaintext interception at network edge
- Implement certificate pinning for critical applications to detect MITM attempts
- Regular security audits of home network devices and firmware inventory
- Consumer awareness campaigns about modem security and rebooting devices regularly

## Variant hunting
['Search VirusTotal, URLhaus, and abuse.ch for other domains/IPs historically associated with same infrastructure or campaigns', 'Hunt for BeEF console fingerprints and characteristic HTTP request patterns across ISP netblocks', 'Correlate DHCP logs and ISP traffic data for similar modem-level traffic replay signatures', 'Investigate other DigitalOcean IPs historically hosting phishing/BeEF infrastructure', 'Search Shodan/Censys for exposed modem management interfaces with default credentials', 'Monitor for DNS sinkhole data indicating mass modem DNS hijacking campaigns', 'Analyze firmware samples from affected modem models for backdoors and malware signatures']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (modem firmware vulnerabilities)
- T1078 - Valid Accounts (default modem credentials)
- T1557 - Man-in-the-Middle (HTTP traffic interception)
- T1557.002 - ARP Spoofing/DHCP Spoofing (network-level MITM)
- T1071.001 - Application Layer Protocol (HTTP exfiltration)
- T1041 - Exfiltration Over C2 Channel
- T1566.002 - Phishing (Adidas/ISG Latam phishing campaigns)
- T1005 - Data from Local System (intercepting all network traffic)
- T1040 - Traffic Sniffing (passive HTTP interception)

## Notes
This writeup documents a real-world large-scale modem compromise affecting potentially millions of devices. The investigation methodology demonstrates excellent forensic thinking (testing multiple AWS instances, then GCP to isolate attack origin). The attacker's use of the same infrastructure for years across multiple malicious purposes (phishing, C&C, malware distribution) while hosted on major provider suggests significant operational gaps in abuse monitoring. The exact modem model/ISP affected is not explicitly stated but context clues suggest a major consumer ISP. This incident likely represents the tip of a much larger modem botnet. Published vulnerability details would likely appear in subsequent security research or disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
