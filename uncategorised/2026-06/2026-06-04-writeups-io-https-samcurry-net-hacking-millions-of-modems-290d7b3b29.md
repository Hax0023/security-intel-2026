# Hacking Millions of Modems - Home Network Traffic Interception and Router Compromise Investigation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Independent Security Research / Responsible Disclosure
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Unauthenticated Remote Code Execution, HTTP Traffic Interception, Router/Modem Compromise, Man-in-the-Middle Attack, Insecure Device Management Interface
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
Security researcher Sam Curry discovered that his home network traffic was being intercepted and replayed by an unknown attacker (IP 159.65.76.209) across multiple devices and networks, indicating a compromised modem or router. Investigation revealed the attacker's IP belonged to malicious infrastructure previously used for phishing campaigns against cybersecurity companies and C&C operations, suggesting widespread modem compromise affecting millions of devices.

## Attack scenario (step by step)
1. Attacker gains unauthorized access to consumer modem/router firmware, likely through unpatched vulnerability or weak credentials
2. Attacker deploys traffic interception capabilities to capture HTTP requests from all devices on the compromised network
3. When victim sends HTTP request to external server, modem intercepts and forwards request to attacker-controlled server (159.65.76.209)
4. Attacker replays the same HTTP request 10-12 seconds later to attacker infrastructure for analysis/exploitation
5. This behavior persists across multiple victim devices (computer, iPhone) and external cloud providers (AWS, GCP), confirming router-level compromise
6. Attacker infrastructure is identified as hosting previous phishing campaigns and C&C operations, indicating persistent threat group

## Root cause
Modems and routers shipped with unpatched vulnerabilities, weak default credentials, or insecure management interfaces that allowed remote attackers to achieve code execution and install traffic monitoring/interception malware. The attacker infrastructure remained operational for 3+ years without suspension, suggesting widespread deployment across ISP networks.

## Attacker mindset
Threat actor operating persistent, multi-purpose malware infrastructure for various cybercriminal activities including phishing, credential harvesting, and C&C operations. The reuse of same infrastructure across different campaigns suggests either same threat group or shared compromised resources. Goal appears to be mass surveillance/data harvesting from home networks rather than targeted attacks.

## Defensive takeaways
- Regularly update modem/router firmware and disable UPnP/port forwarding features unless necessary
- Change default admin credentials on all network devices immediately after installation
- Monitor network traffic patterns for unexpected outbound connections and request replays
- Use HTTPS exclusively to prevent HTTP traffic interception at network layer
- Implement network segmentation to isolate IoT/networking devices from critical systems
- Monitor DNS requests for suspicious domains and implement DNS filtering
- Request automatic security updates from ISP and enable them by default on modems
- Use VPN for all network traffic to encrypt communications end-to-end
- Regularly audit modem logs and access logs for unauthorized access attempts
- Contact ISP if suspicious outbound traffic is detected from home network

## Variant hunting
Hunt for similar patterns: (1) Mass HTTP request interception from residential networks, (2) Traffic replay with 10-15 second delays, (3) DigitalOcean IP space hosting phishing/C&C infrastructure, (4) Modem models with known RCE vulnerabilities being exploited at scale, (5) ISP-level traffic monitoring suggesting modem firmware compromise, (6) Multiple phishing campaigns from same infrastructure, (7) Residential bot networks making requests to external servers automatically

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (modem web interface)
- T1592 - Gather Victim Device Information (traffic analysis)
- T1557 - Adversary-in-the-Middle (HTTP interception)
- T1041 - Exfiltration Over C2 Channel (traffic replay to C&C)
- T1199 - Trusted Relationship (compromised modem)
- T1200 - Hardware Additions (firmware modification)
- T1566 - Phishing (BeEF phishing sites)
- T1071 - Application Layer Protocol (HTTP abuse)
- T1219 - Remote Access Software (C&C infrastructure)

## Notes
Writeup appears incomplete (ends mid-sentence). Researcher successfully identified attack vector as modem compromise rather than personal device compromise through systematic elimination. Investigation linked attacker infrastructure to previous phishing campaigns against Crowdstrike-partnered company (ISG Latam). Suggests large-scale modem botnet operation affecting millions of devices globally. No specific modem models or vulnerabilities identified in provided excerpt. The 3-year operational window without suspension indicates either compromised ISP infrastructure or widespread tolerance from hosting providers for phishing/C&C activities. This represents critical vulnerability in residential network security and ISP accountability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
