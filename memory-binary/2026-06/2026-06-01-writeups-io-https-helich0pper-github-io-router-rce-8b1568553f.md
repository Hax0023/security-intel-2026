# Pivot Into A Network Using A Compromised Router

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** ISP Router (unspecified vendor/model)
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln types:** Command Injection, Unauthenticated Bind Shell, Lack of Access Controls, Network Pivoting/Lateral Movement
- **Category:** memory-binary
- **Writeup:** https://helich0pper.github.io/router_rce/

## Summary
An ISP-provisioned router contained an unauthenticated bind shell listening on port 40001 that granted root-level access without requiring credentials. This vulnerability allowed an attacker to pivot into the internal network, enumerate connected devices via ARP, and launch attacks against internal systems from an external position.

## Attack scenario (step by step)
1. Attacker discovers ISP router with open port 40001 through network reconnaissance (nmap scanning)
2. Attacker connects to bind shell via netcat without authentication and gains root shell access
3. Attacker enumerates internal network devices using ARP cache (arp -a) to identify targets like 192.168.1.108
4. Attacker performs port scanning of identified internal targets using netcat or uploaded busybox binary
5. Attacker selects target with open services (SSH, FTP, Telnet) and exploits vulnerabilities or weak credentials
6. Attacker gains code execution on internal network device, establishing persistent presence

## Root cause
Router shipped with or was provisioned with an unauthenticated root bind shell for ISP maintenance purposes, exposing critical network access without authentication, authorization, or encryption mechanisms

## Attacker mindset
Opportunistic exploitation of ISP maintenance infrastructure; recognizing that default credentials and administrative backdoors provide rapid network pivoting capability; leveraging router as trusted internal device to bypass perimeter security

## Defensive takeaways
- Disable or require authentication for all administrative access channels including maintenance shells
- Implement firewall rules to restrict bind shell ports from external access
- Change default credentials immediately upon router provisioning
- Conduct security audit of ISP-provided equipment before deploying on networks
- Implement network segmentation to limit impact of router compromise
- Deploy intrusion detection on perimeter to identify suspicious outbound connections from router
- Monitor ARP traffic and unexpected internal network reconnaissance from router
- Require VPN or certificate-based authentication for remote maintenance access

## Variant hunting
Search for other ISP-provisioned router models with maintenance backdoors; identify other common maintenance ports (4000, 4001, 5000, 8888); check for hardcoded credentials in router firmware; look for unauthenticated Telnet/SSH services on ISP equipment; examine router syslog for maintenance access patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021.001 - Remote Services: SSH
- T1021.023 - Remote Services: Telnet
- T1087.001 - Account Discovery: Local Account
- T1580 - Cloud Infrastructure Discovery
- T1046 - Network Service Discovery
- T1018 - Remote System Discovery
- T1557.002 - Man-in-the-Middle: ARP Cache Poisoning
- T1570 - Lateral Tool Transfer
- T1021 - Remote Services

## Notes
The researcher responsibly disclosed findings through a blog post rather than public exploit. The vulnerability appears systemic across 55+ routers on the same ISP subnet, suggesting either mass provisioning with maintenance backdoors or post-deployment compromise by automated botnets. The bind shell lacked any authentication, making it trivially exploitable. The router's trusted position on internal network made it ideal for lateral movement. Busybox binary limitations required creative exploitation (dev/null redirection) demonstrating resourcefulness. The ISP's maintenance infrastructure became an attacker's entry point, highlighting how operational convenience can create critical security flaws.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
