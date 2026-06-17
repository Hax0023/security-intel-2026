# Hacking Millions of Modems: ISP/Modem Compromise and HTTP Traffic Interception

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Not specified - Personal research/investigation
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln types:** Modem/Router Compromise, Man-in-the-Middle (MITM), HTTP Traffic Interception, Malware (Router/Modem), ISP-level Compromise
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/hacking-millions-of-modems

## Summary
A security researcher discovered that their home network traffic was being intercepted and replayed by an unknown IP address (159.65.76.209) hosted on DigitalOcean, suggesting their modem or ISP infrastructure had been compromised with malware. Investigation revealed the IP address had previously hosted phishing infrastructure targeting cybersecurity companies and appeared to be part of a larger criminal operation using router malware for C&C communications and traffic hijacking.

## Attack scenario (step by step)
1. Attacker compromises ISP infrastructure or deploys modem malware across customer networks
2. Victim sends HTTP request from home device to external AWS server
3. Modem/ISP intercepts the HTTP request in transit
4. Attacker's C&C server (159.65.76.209) receives and logs the intercepted traffic
5. Attacker replays the same HTTP request 10 seconds later from their infrastructure
6. Attacker maintains persistent access to victim's network traffic for espionage, credential theft, or further exploitation

## Root cause
Compromise of modem/router firmware or ISP-level infrastructure allowing threat actors to perform MITM attacks on customer traffic. The attacker likely deployed malware across millions of modems to create a botnet for traffic interception and C&C communications.

## Attacker mindset
Sophisticated threat actor operating a multi-purpose criminal infrastructure: leveraging compromised modems for traffic interception, hosting phishing campaigns targeting cybersecurity companies, and maintaining persistent C&C communication channels. The operator demonstrates operational security failures by reusing infrastructure across multiple campaigns over 3+ years without detection.

## Defensive takeaways
- Enable HTTPS/TLS for all communications to prevent HTTP interception at ISP/network layer
- Monitor outbound traffic patterns and identify unexpected requests replayed from unfamiliar IP addresses
- Regularly update modem/router firmware and change default credentials
- Use VPN for all network traffic to obscure communications from ISP-level monitoring
- Implement certificate pinning in security tools and applications
- Monitor DNS queries for anomalies indicating modem DNS hijacking
- Segment critical systems from general home network traffic
- Consider modem firmware integrity verification and signed boot mechanisms
- Request ISP provide modem security updates and implement network-level threat detection

## Variant hunting
Search for similar patterns: (1) MITM attacks at ISP/modem layer intercepting and replaying HTTP traffic; (2) Botnets combining phishing infrastructure with router malware for traffic harvesting; (3) Threat actor infrastructure reusing IP addresses across phishing and C&C campaigns; (4) DigitalOcean IPs hosting BeEF phishing kits combined with ISP compromises; (5) Mass modem exploitation campaigns targeting home networks for traffic interception

## MITRE ATT&CK
- T1557.002 - Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay (MITM)
- T1040 - Traffic Sniffing
- T1041 - Exfiltration Over C2 Channel
- T1071.001 - Application Layer Protocol (HTTP)
- T1583.006 - Acquire Infrastructure: Web Services (DigitalOcean)
- T1566.002 - Phishing: Spearphishing Link
- T1190 - Exploit Public-Facing Application (modem firmware)
- T1547.014 - Boot or Logon Autostart Execution: RC Scripts (router malware persistence)
- T1219 - Remote Access Software (C&C communication)

## Notes
This investigation reveals a sophisticated threat actor operating for at least 3 years without major disruption, suggesting possible complicity or negligence by hosting providers. The writeup does not specify the final resolution or which ISP was compromised. The modem compromise appears to be distribution-wide affecting millions of devices, making this a critical infrastructure vulnerability. The attacker's signature across multiple campaigns (phishing, C&C, traffic interception) indicates a specialized criminal organization rather than opportunistic threat actor. Critical missing information: specific modem manufacturer/model, ISP identification, whether the threat was disclosed to authorities/ISPs, and final remediation steps.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
