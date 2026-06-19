# Hacking Millions of Modems - Home Network Traffic Interception and Modem Compromise

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Independent Research / Bug Bounty (Multiple ISPs/Vendors)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Unauthenticated Remote Code Execution, Insecure Default Credentials, Man-in-the-Middle Attack, DNS Hijacking, Router/Modem Compromise
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A researcher discovered that their home modem had been compromised and was actively intercepting and replaying HTTP traffic from all devices on the home network to a malicious DigitalOcean IP address. Through traffic analysis and threat intelligence, the attacker was identified as running phishing infrastructure and C&C operations targeting cybersecurity companies and major brands from the same compromised infrastructure for over 3 years.

## Attack scenario (step by step)
1. Attacker gains initial access to ISP modem/CPE hardware through default credentials, unpatched vulnerabilities, or supply chain compromise
2. Attacker configures modem to intercept all outbound HTTP traffic from connected devices using packet inspection/redirection
3. Attacker replays HTTP requests to malicious infrastructure (159.65.76.209) hosted on DigitalOcean for traffic analysis, credential harvesting, or further exploitation
4. Researcher notices anomalous HTTP requests appearing in web server logs from unknown IP after sending requests from home network
5. Investigation via IP ownership, VirusTotal, and URLscan reveals attacker infrastructure hosting phishing campaigns and malware C&C
6. Researcher confirms modem compromise affects all devices on network (multiple devices, multiple cloud providers), indicating network-layer interception

## Root cause
Home network modem compromised with malicious firmware or configuration enabling transparent HTTP traffic interception and forwarding to attacker-controlled infrastructure. Likely vectors: unpatched modem vulnerabilities, default/weak credentials, supply chain compromise, or malicious ISP-level injection.

## Attacker mindset
Opportunistic actor leveraging compromised modem infrastructure for multiple purposes: phishing campaign support against corporate targets (ISG Latam), brand impersonation (Adidas), and mail server hosting. Demonstrates intent to harvest credentials from multiple targets while maintaining low operational security visibility through infrastructure reuse.

## Defensive takeaways
- Monitor DNS resolution and HTTP traffic for anomalous request patterns or duplicate requests from unexpected sources
- Implement certificate pinning and HPKP for critical applications to prevent MITM attacks
- Regularly audit modem logs and access patterns; change default credentials immediately upon provisioning
- Deploy network segmentation to isolate IoT/modem devices from critical systems
- Enable HTTPS/TLS for all traffic; avoid plain HTTP for sensitive operations
- Implement host-based monitoring to detect unauthorized traffic interception or redirection
- Maintain updated firmware on all network edge devices; subscribe to ISP/vendor security advisories
- Use VPN/proxy for all remote work to encrypt traffic end-to-end, bypassing modem-level inspection
- Monitor egress traffic for connections to known malicious infrastructure using threat feeds

## Variant hunting
Search for similar patterns: (1) Modems with open/accessible admin interfaces; (2) Known modem vulnerabilities (D-Link, TP-Link, Arista, etc.) with RCE capabilities; (3) ISP-provided CPE devices with insecure defaults; (4) Traffic interception signatures in IDS rules; (5) Similar DigitalOcean or cloud-hosted phishing/C&C infrastructure; (6) DNS spoofing attacks on home networks; (7) Modem firmware analysis for backdoors or HTTP traffic sniffing modules

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (modem vulnerability)
- T1199 - Trusted Relationship (ISP/modem provider trust)
- T1557 - Adversary-in-the-Middle (HTTP interception/replay)
- T1040 - Traffic Capture (packet inspection)
- T1071 - Application Layer Protocol (HTTP smuggling)
- T1005 - Data from Local System (network traffic collection)
- T1041 - Exfiltration Over C2 Channel (traffic replay to C&C)
- T1566 - Phishing (BeEF phishing sites)
- T1589 - Gather Victim Identity Information (credential harvesting)

## Notes
This is a sophisticated supply chain/ISP-level attack affecting potentially millions of end users. The attacker's ability to maintain infrastructure for 3+ years without ISP suspension suggests either compromised ISP infrastructure, bulletproof hosting, or sophisticated obfuscation. The writeup demonstrates excellent incident response methodology but lacks final remediation details and responsible disclosure timeline. Critical for organizations: this attack bypasses standard endpoint security controls and requires network-layer defenses.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
