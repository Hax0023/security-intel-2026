# Unauthorized access of Monero wallet by unprivileged process via port hijacking

## Metadata
- **Source:** HackerOne
- **Report:** 462442 | https://hackerone.com/reports/462442
- **Submitted:** 2018-12-14
- **Reporter:** thanhb
- **Program:** Monero
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Privilege escalation, Server impersonation, Man-in-the-middle attack, Insecure authentication (client-only), Local attack vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unprivileged local user can hijack the Monero wallet RPC server by pre-occupying its listening port before the legitimate server starts. The HTTP digest authentication only validates clients, not servers, allowing an attacker to impersonate the RPC server and intercept wallet commands like account creation. This is particularly dangerous when the RPC service is configured to auto-start without GUI feedback.

## Attack scenario
1. Attacker gains local access to victim's computer as unprivileged user (guest account, shared enterprise machine, or fast user switching on Windows)
2. Attacker runs malicious background process that binds to the same port number the victim's Monero RPC server will use
3. Victim attempts to start the legitimate Monero wallet RPC server, which fails silently if auto-started without GUI notification
4. Victim believes RPC server is running normally and connects wallet client, unaware it's communicating with attacker's server
5. Attacker intercepts RPC commands including wallet creation, transaction signing, or credential handling
6. Attacker gains full control over wallet accounts and cryptocurrency assets

## Root cause
The vulnerability stems from three design flaws: (1) HTTP digest authentication only authenticates clients, not servers, providing no server identity verification; (2) RPC server binding to localhost:port is vulnerable to local port hijacking with no exclusive binding mechanism; (3) No visual/audible feedback when RPC service fails to start, allowing silent operation of attacker's impersonation server

## Attacker mindset
Low-skilled attacker with local system access can execute a sophisticated impersonation attack requiring no privilege escalation. The attacker exploits the common user practice of auto-starting services and the asymmetric authentication scheme. The attack is attractive because it requires minimal effort, no vulnerability exploitation, and provides complete access to cryptocurrency assets.

## Defensive takeaways
- Implement mutual TLS authentication requiring server certificate verification, not just client authentication
- Use OS-level exclusive port binding mechanisms or file locking to prevent port hijacking by unprivileged users
- Restrict RPC server binding to localhost with explicit ACL checks against calling process ownership/group membership
- Provide explicit user notification (GUI popup, tray alert) when RPC service fails to start or cannot bind to port
- On multi-user systems, implement per-user isolation of RPC services or require admin privileges for RPC binding
- Consider moving RPC interface to a privileged service (systemd socket activation) to prevent unprivileged hijacking
- Log all RPC server startup/failure events and wallet account creation events for detection

## Variant hunting
Search for similar authentication-bypass vulnerabilities in other cryptocurrency wallets, password managers, and security-critical applications that: (1) implement client-only authentication schemes, (2) bind to localhost without exclusive locking, (3) have auto-start functionality without user feedback, (4) run on shared/multi-user systems. Check hardware token applications, VPN clients, and enterprise security software for identical port hijacking patterns.

## MITRE ATT&CK
- T1548.004 - Abuse Elevation Control Mechanism (Bypass User Account Control)
- T1021.004 - Remote Services (SSH)
- T1021.001 - Remote Desktop Protocol
- T1021.006 - Windows Remote Management
- T1056.004 - Input Capture (Network Device)
- T1040 - Network Sniffing
- T1187 - Forced Authentication
- T1557.002 - Man-in-the-Middle: ARP Cache Poisoning (local variant)

## Notes
This vulnerability was presented at USENIX Security 2018 and DefCon, indicating a systemic issue across multiple security-critical applications. The attack is particularly concerning for cryptocurrency because: (1) no transaction confirmation or user interaction required, (2) attacker gains persistent wallet access, (3) irreversible financial loss possible. The 'silent failure' aspect (RPC binding fails but service appears running to user) is a critical design flaw that amplifies risk. Enterprise environments with centralized access control are especially vulnerable as any domain user becomes a potential attacker on shared machines.

## Full report
<details><summary>Expand</summary>

## Description:
As per our understanding, Monero wallet app provides a separate executable for the user to enable the RPC interface (monero-wallet-rpc). When the user runs the executable, the RPC server will start on a port number that is specified by the user. The RPC server authenticates the client with the HTTP digest access authentication scheme, which is based on a simple challenge-response paradigm. Basically, the client receives a nonce from the server and then replies with a MD5 hash value of the username, the password, the nonce, the HTTP method, and the URI. 

An attacker is a non-privileged user, who can sign in to the victim’s computer with his own credentials or guest account. The attacker first needs to run a process in the background when the victim is using the computer. On Linux and macOS, the attacker only needs to log in, run the process, and leave it running when he logs out. On Windows, user processes are killed at the end of the login session, and thus the attacker needs to do fast user switching to leave his session in the background. The attacker can also remotely run his malicious process if SSH or remote desktop is enabled on the target computer.

With the malicious process running in the background, it is possible to perform server impersonation on the Monero wallet by hijacking the port number before the victim starts the RPC server. The digest access authentication mechanism does not help here because it only authenticates the client. However, the RPC executable will fail to start if the port that it uses has already been taken. While this allows the victim to detect the attack, it does not free him from risks. For example, an aggressively-caching user may attach the RPC executable to the operating system's startup to launch it automatically after login for convenience. In that case, since the RPC server process does not have a GUI to notify the victim that it has failed, the victim will not notice the failure and thus assume that the RPC server is running. Hence, the attacker's malicious server captures commands from the benign client. An example of such commands is “create_wallet”, which tells the server to create a new wallet account. This allows the attacker to have access to the new account because it is created by the attacker instead of the real wallet application.

The attack is straightforward, and no privilege escalation is needed. Also, there are many potential attackers who can perform the attack. For example, in enterprise environments that employ centralized access control mechanisms and allow login by multiple users to the same computer, anyone is a potential attacker. Any computer with guest account enabled is similarly vulnerable.

## Releases Affected:
Tested on Monero wallet 0.12.3

## How to fix:
We found similar issues on other cryptocurrencies’ wallet applications and are working with them to address the issues. There are various ways to prevent the attack, some of which are as follows:
- Mandate the use of TLS on the RPC interface.
- The RPC server accepts only RPC clients that are owned by users belonging to Administrators or a special group.

## Supporting Material/References:
Recently, we have shown similar critical vulnerabilities in many well-known password managers, hardware tokens, and other security-critical applications at Usenix Security and DefCon: 
https://www.usenix.org/conference/usenixsecurity18/presentation/bui

## Impact

Access to the victim's wallet without knowing authentication credentials.

</details>

---
*Analysed by Claude on 2026-05-24*
