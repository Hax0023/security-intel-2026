# Cisco IOS XE Authentication Bypass and Remote Code Execution via Path Validation Flaw

## Metadata
- **Source:** HackerOne
- **Report:** 2778350 | https://hackerone.com/reports/2778350
- **Submitted:** 2024-10-12
- **Reporter:** odaysec
- **Program:** Cisco
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln:** Authentication Bypass, Path Traversal, Improper Input Validation, Remote Code Execution, Privilege Escalation
- **CVEs:** CVE-2023-20198, CVE-2023-20273
- **Category:** memory-binary

## Summary
A critical authentication bypass vulnerability in Cisco IOS XE allows unauthenticated attackers to reach the webui_wsma_http endpoint by exploiting improper path validation in Nginx filtering. By bypassing authentication, attackers can execute arbitrary Cisco IOS commands with Privilege 15 privileges and make unauthorized configuration changes. When chained with CVE-2023-20273, this enables escalation to root-level Linux OS access for malware implantation.

## Attack scenario
1. Attacker identifies exposed Cisco IOS XE instance with vulnerable web UI component
2. Attacker crafts HTTP request bypassing Nginx path filtering to reach unauthenticated webui_wsma_http endpoint
3. Attacker sends SOAP XML request to cisco:wsma-exec endpoint with malicious commands in execCLI element
4. System executes arbitrary commands with Privilege 15 context without authentication validation
5. Attacker creates local user account with Privilege 15 via cisco:wsma-config SOAP endpoint
6. Attacker leverages CVE-2023-20273 with newly created credentials to escalate to Linux root and deploy persistent implant

## Root cause
Improper path validation in Nginx reverse proxy fails to adequately filter requests before they reach the webui_wsma_http backend. The WSMA (Web Services Management Agent) endpoints lack sufficient authentication verification on incoming SOAP requests, allowing unauthenticated access to command execution interfaces designed for privileged operations.

## Attacker mindset
Opportunistic actor seeking high-impact initial access to critical network infrastructure. The exploitation chain suggests sophisticated understanding of Cisco architecture, chaining multiple vulnerabilities for escalation. The targeting of MTN Cameroon indicates possible nation-state or advanced persistent threat activity leveraging public-facing Cisco devices as beachheads for enterprise compromise.

## Defensive takeaways
- Immediately patch Cisco IOS XE to versions containing fixes for path validation and WSMA authentication
- Implement network segmentation to restrict access to web UI components to trusted administrative networks only
- Deploy Web Application Firewall (WAF) rules to detect and block SOAP requests with suspicious execCLI payloads
- Monitor for unusual WSMA endpoint access patterns and XML SOAP requests from unauthenticated sources
- Implement robust authentication and authorization checks at all SOAP endpoint handlers, not relying on upstream filters
- Regular vulnerability scanning of internet-facing Cisco devices to identify and remediate exposure
- Enforce strict change management requiring multi-factor authentication for configuration modifications
- Monitor syslog and system logs for unexpected user creation or privilege escalation events

## Variant hunting
Search for similar authentication bypass patterns in other Cisco web UI components and SOAP/XML-RPC endpoints. Examine path traversal techniques that bypass reverse proxy filters in other network device manufacturers (Juniper, Arista, F5). Investigate whether similar improper input validation exists in other WSMA-related services or backup/recovery interfaces that may have relaxed authentication.

## MITRE ATT&CK
- T1190
- T1036
- T1548
- T1133
- T1021
- T1059
- T1098

## Notes
Report contains significant redactions of IP addresses, CVE numbers, and hostnames. The PoC demonstrates practical end-to-end exploitation including discovery methodology via Shodan-like searches. Attribution to MTN Cameroon suggests active wild exploitation. CVE-2023-20273 escalation path indicates this was likely part of coordinated campaign affecting multiple Cisco customers. The chaining of two vulnerabilities for complete system compromise demonstrates need for defense-in-depth strategies beyond single vulnerability patches.

## Full report
<details><summary>Expand</summary>

## Summary:
CVE-███████ is characterized by improper path validation to bypass Nginx filtering to reach the webui_wsma_http web endpoint without requiring authentication. By bypassing authentication to the endpoint, an attacker can execute arbitrary Cisco IOS commands or issue configuration changes with Privilege 15 privileges. Further attacks involved exploitation of CVE-2023-20273 to escalate to the underlying Linux OS root user to facilitate implantation.

This PoC exploits CVE-█████████ to leverage two different XML SOAP endpoints:
The vulnerability check, config, and command execution options all target the `cisco:wsma-exec` SOAP endpoint to insert commands into the `execCLI` element tag.
The add user option targets the `cisco:wsma-config` SOAP endpoint to issue a configuration change and add the Privilege 15 account. This endpoint could be [ab]used to make other configuration changes, but thats outside the scope of this PoC.

## Proof On Concepts :
See below for an example request that bypasses authentication on vulnerable instances of IOS-XE. This POC creates a user named baduser with privilege level 15. Let’s dig into the details.
{F3672631}

  1. Sign in as any user ███ query
  1. Visit Searchbar and Search Query ██████████: "MTN Innovation Centre"`
  1. Found domain owned by MTN Cameroon as `███`
  1. Intercept url to burp-suite and sent to repeater
  1. Sent to intruder and Set up the [exploits here](█████████)
  1. Run exploits bellow command 

```bash
exploit.py -t ████ -c

Testing for vulnerability
Target IP:      █████
Target URL:     █████████
Vulnerable:     True
IOS Ver:        ISR4331/K9 europ-constantia-2 IOS 16.6 Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.4, RELEASE SOFTWARE (fc3)

Done.
```
```bash
exploit.py -t █████ -g

Selected Target:        ██████
Running in Exec Mode
Executing Command:      sh run

Sending exploit to target URL:  █████

Building configuration...
Current configuration : 17326 bytes
```
```bash
enable secret 5 $1$vF3Q$wplcifyib3DUyzbgcUGe/1
enable password 7 1214041E1E
snmp-server trap-source GigabitEthernet0/0/0.3029
snmp-server source-interface informs GigabitEthernet0/0/0.3029
snmp-server contact ████ ██████
```
and you can see all the sensitive for configuration was exposed

{F3672637}

{F3672640}

{F3672642}


## Supporting Material/References:
  * [Cisco Advisory](███████)
  * [horizon3ai CVE-██████ research](██████████)
  * [horizon3ai CVE-██████ PoC](██████)
  * [LeakIX CVE-2023-20273 PoC](██████████)

## Impact

Cisco is providing an update for the ongoing investigation into observed exploitation of the web UI feature in Cisco IOS XE Software. We are updating the list of fixed releases and adding the Software Checker. Our investigation has determined that the actors exploited two previously unknown issues. The attacker first exploited CVE-█████ to gain initial access and issued a privilege 15 command to create a local user and password combination. This allowed the user to log in with normal user access. The attacker then exploited another component of the web UI feature, leveraging the new local user to elevate privilege to root and write the implant to the file system.

</details>

---
*Analysed by Claude on 2026-05-24*
