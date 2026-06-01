# Hacking Millions of Modems - HTTP Traffic Interception via Compromised ISP Infrastructure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** ISP/Modem Manufacturers (Comcast, Cox, Charter, etc.)
- **Bounty:** Unknown/Self-Reported
- **Severity:** critical
- **Vuln types:** Man-in-the-Middle (MITM) Attack, HTTP Traffic Interception, Router/Modem Compromise, ISP Infrastructure Compromise, Malware Distribution via ISP, DNS Hijacking
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
Researcher discovered that HTTP traffic from his home network was being intercepted and replayed by an attacker-controlled DigitalOcean IP address (159.65.76.209), indicating modem compromise. Investigation revealed the IP had previously hosted phishing infrastructure targeting ISG Latam (South American cybersecurity firm) and other malicious activities, suggesting sophisticated attacker infrastructure repurposing.

## Attack scenario (step by step)
1. Attacker compromises ISP modem/router firmware or exploits default credentials to gain remote access
2. Attacker installs HTTP proxy/MITM capability on modem to intercept and log all outbound HTTP traffic
3. Victim sends HTTP request from home network devices (computer, iPhone, etc.)
4. Modem firmware forwards copy of HTTP request to attacker's command-and-control server (159.65.76.209)
5. Attacker replays HTTP request 10-12 seconds later from external infrastructure to fingerprint destination services
6. Attack scales to millions of modems potentially compromised with same malware/firmware modification

## Root cause
Compromised modem firmware or exploitable services (TR-069, UPnP, default credentials) allowing remote code execution and MITM proxy installation. Lack of firmware signature verification and secure boot mechanisms in consumer ISP-provided modems.

## Attacker mindset
Opportunistic cybercriminal operating infrastructure-as-a-service for multiple purposes: phishing campaigns, botnet C&C, HTTP MITM proxy for credential harvesting, data exfiltration, and traffic analysis. Reuses infrastructure across campaigns while avoiding ISP/provider detection for 3+ years.

## Defensive takeaways
- Implement mandatory HTTPS/TLS for all HTTP traffic to prevent MITM interception of sensitive data
- Deploy certificate pinning in applications to detect unauthorized proxies
- Enable modem firmware signature verification and secure boot in consumer devices
- Monitor outbound HTTP requests for unexpected replays or time-delayed forwarding patterns
- Require strong authentication on modem management interfaces; disable TR-069/UPnP by default
- Implement DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) to prevent DNS hijacking
- Use VPN for all traffic on untrusted networks including home ISP networks
- Monitor for IOCs from known malicious DigitalOcean IPs; coordinate with providers on abuse suspension
- Regular firmware audits and signed updates for all modem/router devices
- Deploy network segmentation to isolate IoT/modem traffic from critical devices

## Variant hunting
['Search VirusTotal/URLhaus for other domains hosted on DigitalOcean IP ranges known for phishing/malware', 'Hunt for HTTP 10-12 second replay patterns in ISP traffic logs indicating MITM proxy behavior', 'Analyze modem firmware across major ISPs (Comcast, Cox, Charter, AT&T) for hidden HTTP proxy services or backdoor listening ports', 'Correlate ISP router model compromises with known vulnerabilities (CVE-2022-27255 for Netgear, CVE-2020-28394 for various models)', 'Investigate other known malicious DigitalOcean IPs for similar phishing/BeEF hosting patterns', 'Search for BeEF exploitation kits hosted on compromised ISP infrastructure globally', 'Check SHODAN/Censys for exposed modem management interfaces with default credentials across ISP ranges', 'Hunt for TR-069 RCE exploitation attempts in ISP network logs']

## MITRE ATT&CK
- T1557.002 - Adversary-in-the-Middle: HTTPS Interception
- T1557.001 - Adversary-in-the-Middle: ARP Spoofing
- T1040 - Traffic Sniffing
- T1071.001 - Application Layer Protocol: Web Protocols
- T1190 - Exploit Public-Facing Application (modem firmware RCE)
- T1133 - External Remote Services (modem management interfaces)
- T1200 - Hardware Additions (modem/router compromise)
- T1570 - Lateral Tool Transfer (MITM proxy distribution)
- T1027 - Obfuscated Files or Information (firmware rootkit)
- T1105 - Ingress Tool Transfer (malware distribution via MITM)

## Notes
This represents a supply-chain attack on consumer ISP infrastructure affecting potentially millions of end-users. The attacker's ability to maintain control for 3+ years without detection suggests systemic vulnerabilities in modem security and ISP monitoring. The reuse of infrastructure across multiple campaigns (phishing, C&C, traffic interception) indicates centralized criminal operation. Critical finding that HTTP traffic could be intercepted and replayed at scale, highlighting massive security implications for unencrypted communications. Investigation incomplete in original writeup regarding full scope of compromise and number of affected modems. Recommendations should include mandatory HTTPS enforcement and firmware hardening across entire ISP industry.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
