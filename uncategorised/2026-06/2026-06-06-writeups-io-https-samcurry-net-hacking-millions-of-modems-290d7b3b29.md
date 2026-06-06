# Hacking Millions of Modems - HTTP Traffic Interception via Compromised ISP/Modem Infrastructure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Self-discovered / Bug Bounty Independent Research
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Man-in-the-Middle (MITM) Attack, Network Traffic Interception, Modem Compromise, ISP-level Traffic Hijacking, HTTP Traffic Replay, DNS Manipulation
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A security researcher discovered their home network traffic was being intercepted and replayed by an attacker operating a malicious IP address (159.65.76.209 hosted on DigitalOcean). The attacker had compromised either the researcher's modem or ISP infrastructure, allowing them to capture and replay HTTP requests from all devices on the home network. Threat intelligence analysis revealed the IP address had previously hosted phishing infrastructure targeting South American cybersecurity firms and BeEF-based attack frameworks.

## Attack scenario (step by step)
1. Attacker compromises modem firmware or gains access to ISP-level routing infrastructure, positioning themselves as MITM for home network traffic
2. Researcher sends HTTP request from home network to external AWS server (54.156.88.125:8000)
3. Attacker intercepts the HTTP request before it leaves the home network/ISP gateway
4. Attacker replays the identical HTTP request from their own DigitalOcean IP address (159.65.76.209) within 10 seconds
5. Researcher observes duplicate requests in server logs from unknown IP, indicating traffic interception
6. Attacker maintains persistent access to harvest credentials, exfiltrate data, or conduct further reconnaissance on all devices sharing the compromised network

## Root cause
Compromised modem firmware or ISP-level routing infrastructure allowing packet capture and replay. The attacker maintained persistent network access at the ISP/gateway level rather than individual device compromise, enabling systematic interception of all outbound HTTP traffic from the home network.

## Attacker mindset
Sophisticated threat actor operating multi-purpose malicious infrastructure. Evidence suggests they are conducting targeted phishing campaigns against enterprise security companies (ISG Latam, Crowdstrike partners) while simultaneously operating router/modem malware C&C infrastructure. The reuse of infrastructure across multiple campaign types suggests either an organized crime operation or APT group utilizing shared infrastructure.

## Defensive takeaways
- Enforce HTTPS/TLS for all network communications to prevent plaintext HTTP traffic interception and replay
- Implement certificate pinning in applications to detect MITM attacks using forged certificates
- Regularly update and audit modem firmware; consider replacing ISP-provided modems with security-hardened alternatives
- Monitor outbound DNS queries and HTTP traffic patterns for anomalous replay behavior
- Implement network intrusion detection systems (IDS) to identify duplicate request patterns from unexpected sources
- Use VPN on all home network devices to encrypt traffic at application level before ISP-level interception
- Enable UPnP/DHCP filtering and disable unnecessary services on network gateways
- Conduct forensic analysis on all network devices when traffic interception is suspected
- Report ISP-level compromises to upstream providers and coordinate with law enforcement

## Variant hunting
['Search VirusTotal for other domains/IPs associated with 159.65.76.209 for related malicious infrastructure', 'Query passive DNS records for domains historically resolving to phishing/C&C IPs hosted on DigitalOcean', 'Analyze BeEF deployment signatures across phishing sites to identify attacker toolkit and variations', 'Hunt for modem firmware samples matching the suspected router malware C&C beaconing pattern', 'Cross-reference whois data for DigitalOcean abuse history related to ISP-targeting phishing campaigns', 'Search for similar HTTP request replay patterns in ISP network traffic logs across multiple ASNs', 'Investigate mx12.* subdomains pattern for additional command-and-control infrastructure']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (modem web interface exploitation)
- T1557 - Adversary-in-the-Middle (network traffic interception at ISP level)
- T1040 - Traffic Capture (HTTP request capture and replay)
- T1041 - Exfiltration Over C2 Channel (data exfiltration via compromised ISP)
- T1566 - Phishing (BeEF phishing framework deployment)
- T1583 - Acquire Infrastructure (DigitalOcean IP for C&C operations)
- T1584 - Compromise Infrastructure (ISP/modem compromise for persistence)
- T1200 - Hardware Additions (potential modem firmware manipulation)
- T1071 - Application Layer Protocol (HTTP for C&C communication)

## Notes
This investigation demonstrates a sophisticated supply-chain attack targeting home network infrastructure. The attacker's ability to maintain operational security while using the same IP for multiple distinct malicious purposes (phishing, C&C, traffic interception) over 3+ years without suspension indicates either compromised abuse reporting at DigitalOcean or deliberate overlooking by the provider. The researcher's methodical elimination process (testing multiple AWS instances, GCP alternative) effectively ruled out cloud provider compromise. The connection to ISG Latam phishing suggests the attacker may be conducting reconnaissance on security professionals working from home during the COVID era. The incomplete blog post suggests further analysis was ongoing regarding attacker motivation and infrastructure scope.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
