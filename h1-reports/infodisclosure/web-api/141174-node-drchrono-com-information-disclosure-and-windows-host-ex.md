# node.drchrono.com - Information Disclosure and Windows Host Exposed

## Metadata
- **Source:** HackerOne
- **Report:** 141174 | https://hackerone.com/reports/141174
- **Submitted:** 2016-05-26
- **Reporter:** bashlogic
- **Program:** drchrono
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Information Disclosure, Banner Grabbing, Insecure Service Configuration, Unnecessary Service Exposure, Missing Authentication Controls, Weak Access Controls
- **CVEs:** None
- **Category:** web-api

## Summary
A Windows server (node.drchrono.com) exposed multiple administrative services to the internet including FTP, SSH, RDP, and SMB with numerous security misconfigurations. The server leaked sensitive version information through service banners and lacked proper authentication controls, enabling reconnaissance and brute-force attacks. The combination of exposed RDP without NLA, open SMB with default accounts, and information disclosure created a critical attack surface.

## Attack scenario
1. Attacker discovers node.drchrono.com and performs port scanning to identify open TCP ports (21, 22, 135, 445, 3389, 5986, 47001)
2. Attacker connects to FTP and SSH services to extract version information via banner grabbing, identifying specific software versions vulnerable to known exploits
3. Attacker notes RDP is exposed without Network Level Authentication (NLA) and connects to gather OS version details
4. Attacker enumerates SMB (445) and identifies default/weak local administrator account through enumeration tools
5. Attacker launches brute-force attack against SMB using harvested version information and known vulnerabilities specific to the identified OS/service versions
6. Upon successful credential compromise, attacker gains full administrative access via RDP or SMB to the exposed Windows host

## Root cause
Administrative services were exposed to the internet without implementing security best practices including: failure to disable or customize service banners, lack of network access controls, absence of authentication pre-requisites (NLA) on RDP, and non-hardened default configurations on SMB and account management.

## Attacker mindset
An attacker would recognize this as a low-hanging fruit scenario where reconnaissance is trivial due to overly verbose service banners. The lack of authentication controls on remote access services (RDP without NLA) combined with weak account management (default local administrator) creates an easy path from external reconnaissance to full system compromise with minimal effort required.

## Defensive takeaways
- Remove version information from all service banners (FTP welcome messages, SSH banners) to hinder reconnaissance
- Implement Network Level Authentication (NLA) for RDP to require authentication before establishing connection
- Disable or rename default local administrator accounts and implement account lockout policies where possible
- Restrict administrative service access to trusted internal subnets/IPs using firewall rules (Windows Firewall or hardware firewalls)
- Close or bind administrative services (RDP, SSH, FTP, WinRM) only to internal interfaces, not listening on all interfaces
- Enable strong encryption for all remote access services and disable insecure protocols
- Conduct regular security configuration reviews against CIS benchmarks and hardening guides
- Implement robust logging and monitoring on all administrative service access attempts
- Maintain current patching across all services, particularly FTP and SSH implementations
- Use firewall rules and VPN requirements for accessing administrative services rather than direct internet exposure

## Variant hunting
Search for other drchrono infrastructure exposing similar service combinations; look for other organizations with identical port profiles (21, 22, 135, 445, 3389, 5986, 47001) which suggest standardized but insecure Windows deployments; hunt for FileZilla FTP servers with version disclosure enabled; identify SSH services with banner configuration issues; audit other companies' RDP deployments lacking NLA

## MITRE ATT&CK
- T1040 - Network Sniffing
- T1592 - Gather Victim Host Information
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1046 - Network Service Discovery
- T1598 - Phishing for Information
- T1110 - Brute Force
- T1110.001 - Password Guessing
- T1021.001 - Remote Services: Remote Desktop Protocol
- T1021.002 - Remote Services: SSH
- T1078 - Valid Accounts
- T1078.001 - Valid Accounts: Default Accounts

## Notes
This report exemplifies a critical infrastructure security failure where administrative services were deployed with default/unsafe configurations directly exposed to the internet. The vulnerability chain is straightforward: information disclosure → reconnaissance → weak authentication → compromise. The reporter appropriately provided remediation guidance for each identified issue. No actual exploitation occurred - the researcher responsibly reported configuration weaknesses before attempting access. The lack of specified bounty amount suggests this may have been a lower-tier report or the bounty details were redacted. This incident highlights the importance of following security hardening baselines (CIS Benchmarks) and applying principle of least privilege to network access.

## Full report
<details><summary>Expand</summary>

This host has the following TCP ports open;
* 21 - FTP
* 22 - SSH
* 135 - Windows RPC Dynamic
* 445 - Microsoft DS
* 3389 - Remote Desktop
* 5986 - PowerShell Remoting
* 47001 - WinRM

The server appears to be secured well on the whole.
However the services SSH and FTP do all give out some information.
Please see attached images for the versions given out.
This information could be used by a malicious attacker, to create a targeted attack vector, on the underlying server.

To remove the FileZilla ftp server version go to the options and ensure the **%v** is removed from the welcome message. See the screenshot named **Remove FileZilla version.PNG**.

To remove the banner version from the SSH service locate the SSH configuration file and open it up in notepad, find the line with the option named **banner** and set it to **none**. The default location for Windows is **C:\Program Files\OpenSSH\etc\ssh_config**.

The remote desktop is widely open and does not require any form of authentication to connect. As you will see in the screenshot named **Remote Desktop.png** it clearly states the OS version running, which again all helps a malicious attacker. You can not remove this information however you can protect against it. It is highly recommended that you enable network level authentication (NLA), this means that you are not able to connect to remote desktop unless you are authenticated first. Also ensure that you have set the remote desktop to use high encryption. More information about this can be found here https://technet.microsoft.com/en-us/library/cc770833(v=ws.11).aspx.

With Microsoft DS (445 SMB) open, ensure you have disabled the local administrator account or at least renamed it from default. This account can not be locked out, allowing for unlimited password guesses against it. This would facilitate an attacker, as they could use this service to brute force the password until obtained. As remote desktop is open they could simply login to the server with full administrative privileges once the password has been revealed.

I would highly recommend ensuring that you have had a build review completed on the server by an experienced security professional as the server is very open to the internet. If money is an issue then ask your administration team to follow the guidance from the CIS benchmarks, available at https://benchmarks.cisecurity.org/downloads/benchmarks/.

Final general advice is to not open the ports to the world when there is no need and to ensure that the FTP/SSH service installed is always fully patched.
The ports identified are useful for internal administration only, I would recommend limiting their availability to your trusted subnets or IP addresses. This can be done using the windows firewall or a hardware firewall such as checkpoint.



</details>

---
*Analysed by Claude on 2026-05-24*
