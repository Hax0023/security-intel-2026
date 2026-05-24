# Open SSH Port 10022 Exposes Version Information Leading to Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 223421 | https://hackerone.com/reports/223421
- **Submitted:** 2017-04-24
- **Reporter:** str33
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Banner Grabbing, Unnecessary Open Port
- **CVEs:** None
- **Category:** web-api

## Summary
An open SSH port (10022) on weblate.org exposes OpenSSH version and Debian OS version information through banner grabbing, allowing attackers to enumerate system details. While not directly exploitable without valid credentials, this information disclosure enables threat actors to identify potential vulnerabilities matching specific software versions.

## Attack scenario
1. Attacker performs network reconnaissance using nmap against weblate.org to identify open ports
2. Attacker discovers port 10022 is open and accessible from the internet
3. Attacker connects via telnet to port 10022 and receives SSH banner with version details (OpenSSH version, Debian version)
4. Attacker captures this information and cross-references it against known CVE databases for matching versions
5. Attacker uses version information to prioritize exploitation attempts or social engineering tactics
6. If vulnerable versions exist, attacker crafts targeted exploits knowing exact software versions in use

## Root cause
SSH service listening on non-standard port 10022 with default banner disclosure enabled; insufficient network segmentation allowing public access to administrative services; banner grabbing not disabled in SSH configuration

## Attacker mindset
Information gatherer performing passive reconnaissance; attempting to reduce attack surface by identifying technology stack and versions; building target profile for vulnerability mapping and exploitation prioritization

## Defensive takeaways
- Disable SSH banner or customize it to avoid revealing version information (SSH config: Banner /etc/ssh/banner.txt with generic message)
- Restrict SSH access to specific IP ranges or VPN only using firewall rules
- Use non-standard ports for administrative services but do not rely on obscurity as primary defense
- Implement network segmentation to prevent direct internet access to SSH ports
- Maintain regular patching schedule for OpenSSH and OS components regardless of version visibility
- Monitor for unauthorized access attempts to non-standard SSH ports
- Consider using security tools like fail2ban to rate-limit connection attempts

## Variant hunting
Similar information disclosure vulnerabilities may exist on other non-standard ports; banner grabbing on MySQL (3306), PostgreSQL (5432), Redis (6379), or other database services; HTTP headers leaking server version information; SMTP banner disclosure; FTP banner grabbing

## MITRE ATT&CK
- T1590.003 - Gather Victim Network Information: IP Addresses
- T1046 - Network Service Discovery
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1592.002 - Gather Victim Host Information: Software, Patches, and Version Details

## Notes
Reporter correctly notes this is low-risk if patching is current; however, version disclosure still violates defense-in-depth principles. Port 10022 suggests intentional SSH exposure, possibly for administrative access, making network-level controls critical. The 'protocol mismatch' error when typing suggests proper SSH key-based authentication enforcement, which is a positive security control.

## Full report
<details><summary>Expand</summary>

Open port 10022 leads to disclosure of open-ssh version and current Debian version being used.

POC- 
1. I performed an nmap scan ( nmap -A -T4 -p- weblate.org)
2. I saw the port 10022 was open and I did a telnet connect to the port.
3. As soon as I did the telnet connect it returned me the openssh version and the debian version (check the .png file)
4.I wasn't able to run any sort of commands as whatever I typed returned a protocol mismatch error.


This doesn't necessarily mean a security issue as long as everything is being patched regularly. 


</details>

---
*Analysed by Claude on 2026-05-24*
