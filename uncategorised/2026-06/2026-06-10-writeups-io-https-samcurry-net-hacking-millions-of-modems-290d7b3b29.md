# Hacking Millions of Modems: HTTP Traffic Interception via Compromised ISP Infrastructure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Multiple ISPs / Modem Manufacturers
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Man-in-the-Middle (MITM) Attack, HTTP Traffic Interception, Router/Modem Compromise, ISP Infrastructure Exploitation, DNS Hijacking, Credential Harvesting
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
The researcher discovered that their HTTP traffic was being intercepted and replayed by an unknown IP address (159.65.76.209 on DigitalOcean) after sending requests from multiple home devices. Investigation revealed the IP was previously used for phishing campaigns targeting ISG Latam cybersecurity company, suggesting widespread modem compromise affecting millions of users for malicious purposes including credential harvesting and command-and-control operations.

## Attack scenario (step by step)
1. Attacker compromises ISP DNS servers or home router/modem firmware to redirect or intercept HTTP traffic
2. User sends HTTP request from home network to external server (AWS, GCP, etc.)
3. Modem/ISP intercepts the HTTP request in transit and forwards it to attacker-controlled infrastructure
4. Attacker captures request, extracts sensitive data, cookies, credentials, or other information from the HTTP traffic
5. Attacker replays the request to their own malicious server to harvest additional data or perform phishing attacks
6. Multiple devices on victim's network are simultaneously compromised, allowing attacker to profile all user activity

## Root cause
Compromised modem firmware or ISP-level DNS/traffic manipulation allowing network-wide HTTP interception. Likely vector is weak modem default credentials, unpatched vulnerabilities in modem software, or ISP-level infrastructure compromise. The attacker maintained control of infrastructure across multiple years without detection.

## Attacker mindset
Opportunistic cybercriminal operating infrastructure for multiple purposes: credential harvesting through phishing (BeEF), targeted attacks on security companies (ISG Latam), financial fraud (Adidas phishing), and broad surveillance of home internet users. Long-term, low-profile operation suggests sophistication and willingness to hide activities across years while monetizing access.

## Defensive takeaways
- Always use HTTPS/TLS for all traffic; HTTP remains fundamentally insecure in untrusted networks
- Regularly update and patch modem firmware; use strong, unique admin credentials
- Monitor modem logs and settings for unexpected changes; change default admin passwords immediately
- Use VPN or other encrypted tunnels for sensitive work; isolate critical systems from general home network
- Implement DNS security (DNSSEC) and monitor for unexpected DNS redirects
- ISPs should implement stronger authentication, encryption, and monitoring for residential devices
- Consider replacing ISP-provided modems with trusted third-party devices with active security updates
- Use network monitoring tools to detect unusual outbound connections from home devices
- ISP and modem manufacturer accountability for security - regular penetration testing and firmware audits required

## Variant hunting
Search for similar patterns: residential IP ranges making requests to public cloud services followed by requests from suspicious IPs within 10-30 seconds; BeEF infrastructure deployments on DigitalOcean/similar providers; modem default credentials exploitation tools; ISP DNS poisoning campaigns; phishing domains targeting security companies using same infrastructure; Brazil/Paraguay-based cybercriminal groups with long-lived infrastructure; mass HTTP interception in residential networks.

## MITRE ATT&CK
- T1557.001 - Adversary-in-the-Middle: HTTPS Interception
- T1557.002 - Adversary-in-the-Middle: ARP Cache Poisoning
- T1040 - Traffic Capture
- T1071.001 - Application Layer Protocol: HTTP/HTTPS
- T1041 - Exfiltration Over C2 Channel
- T1566.002 - Phishing: Spearphishing Link
- T1583.006 - Acquire Infrastructure: Web Services
- T1087 - Account Discovery
- T1589.001 - Gather Victim Identity Information: Credentials
- T1590.004 - Gather Victim Network Information: Network Topology
- T1569.002 - Service Execution
- T1059 - Command and Scripting Interpreter

## Notes
This writeup documents a real, critical vulnerability affecting consumer-grade modems and ISP infrastructure. The scale ('millions of modems') suggests either widespread firmware vulnerability or ISP-level compromise. The attacker's long operational history (3+ years) without suspension indicates lack of effective ISP/DigitalOcean monitoring. The connection to ISG Latam phishing suggests possible APT involvement or organized cybercrime. Original researcher demonstrated excellent investigative methodology using threat intelligence, VirusTotal, URLscan, and network analysis. Key insight: HTTP traffic at ISP/modem level is fundamentally untrustworthy; the researcher's concern about AWS compromise and methodical elimination of possibilities was sound security thinking. This incident highlights the critical importance of HTTPS adoption and the vulnerability of home network infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
