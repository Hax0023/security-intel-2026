# Hacking Millions of Modems - HTTP Traffic Interception via Compromised ISP Infrastructure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Independent Security Research (Self-Reported)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Modem Compromise, Man-in-the-Middle (MITM) Attack, HTTP Traffic Interception and Replay, ISP Infrastructure Abuse, Lack of HTTPS Enforcement, Router/Gateway Malware
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A security researcher discovered their home network traffic was being intercepted and replayed by an unknown attacker operating from DigitalOcean infrastructure. The attacker's IP address (159.65.76.209) was previously used to host phishing sites targeting South American cybersecurity companies, suggesting an organized threat actor with sustained access to ISP/modem infrastructure for multiple campaigns over 3+ years.

## Attack scenario (step by step)
1. Attacker gains initial access to millions of home modems through firmware vulnerabilities, default credentials, or supply chain compromise
2. Compromised modems are configured to intercept HTTP traffic from all connected devices on the network
3. When users send HTTP requests, the modem clones/replays these requests to attacker-controlled infrastructure on DigitalOcean
4. Attacker harvests sensitive data from intercepted requests (authentication tokens, form data, URLs, headers)
5. Same infrastructure is repurposed for secondary malicious activities including phishing campaigns and C&C communications
6. Attacker maintains persistent access across multiple victim networks while conducting concurrent criminal operations

## Root cause
Vulnerabilities in consumer modem firmware allowing remote compromise, combined with inadequate vendor patching cycles and lack of encryption enforcement (HTTPS) for user traffic. Upstream ISP negligence in detecting and preventing malicious traffic patterns from compromised home equipment.

## Attacker mindset
Opportunistic threat actor operating as either a criminal-for-hire or APT group with infrastructure reuse mentality. Demonstrates low operational security (reusing infrastructure for multiple unrelated campaigns), suggesting either low-skill operators or deliberate obfuscation strategy. Willingness to target security professionals indicates confidence in evasion or assumption of low detection probability.

## Defensive takeaways
- Enforce HTTPS/TLS encryption for all HTTP traffic to prevent plaintext interception at ISP/network level
- Implement certificate pinning in critical applications to prevent MITM with fraudulent certificates
- Consumer modem firmware must have secure boot, regular OTA updates, and vulnerability disclosure programs
- Monitor for unexpected outbound traffic from home network gateways, especially replayed or modified HTTP requests
- ISPs should implement anomaly detection for compromised home networks exhibiting traffic mirroring behavior
- Default credentials and known CVEs on modems must be eliminated through vendor recalls and forced updates
- DNS-level security monitoring can detect connections to known malicious infrastructure before HTTP layer
- VPN usage on home networks adds encryption layer independent of modem security posture
- Regular modem firmware audits and penetration testing by vendors and telecom regulators

## Variant hunting
Search for similar modem compromise techniques targeting DOCSIS, NETGEAR, TP-Link, and Linksys devices. Investigate other DigitalOcean ASNs and IP ranges for hosting phishing infrastructure or C&C servers. Cross-reference passive DNS records for domains resolving to compromised ISP address space. Look for BeEF phishing kit deployments with South American geographic targeting. Hunt for firmware signatures in ISP-supplied modems with hardcoded C&C callbacks.

## MITRE ATT&CK
- T1557.002 (Adversary-in-the-Middle: HTTPS Interception)
- T1040 (Traffic Redirection)
- T1041 (Exfiltration Over C2 Channel)
- T1071.001 (Application Layer Protocol: Web Protocols)
- T1583.006 (Acquire Infrastructure: Web Services)
- T1566.002 (Phishing: Spearphishing Link)
- T1199 (Trusted Relationship)
- T1190 (Exploit Public-Facing Application)
- T1547.012 (Boot or Logon Autostart Execution: Print Processors)
- T1105 (Ingress Tool Transfer)

## Notes
This writeup is particularly significant as it documents a consumer-scale supply chain attack affecting potentially millions of modem users. The attacker's infrastructure reuse (phishing, C&C, traffic interception from same IP) suggests either compartmentalization failure or deliberate mixing to confuse attribution. The fact that the researcher could track the threat actor through VirusTotal passive DNS demonstrates the value of infrastructure-centric threat hunting. The 3+ year persistence without suspension suggests either DigitalOcean abuse reporting failures or deliberate tolerance. This represents a critical gap in the consumer IoT/ISP ecosystem where fundamental network security is delegated to vendors with poor security practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
