# Server Side Request Forgery (SSRF) in Jabber Settings Admin Control Panel

## Metadata
- **Source:** HackerOne
- **Report:** 1018568 | https://hackerone.com/reports/1018568
- **Submitted:** 2020-10-26
- **Reporter:** they
- **Program:** phpBB
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Information Disclosure, Port Scanning
- **CVEs:** None
- **Category:** web-api

## Summary
The Jabber settings panel in phpBB's Administrator Control Panel fails to validate the 'jabber server' parameter, allowing attackers to make arbitrary network connections to localhost and internal network resources. This enables port scanning, service enumeration, and potential interaction with internal services that should not be accessible from the web interface.

## Attack scenario
1. Attacker gains access to Administrator Control Panel (via credential compromise, privilege escalation, or admin account compromise)
2. Attacker navigates to Jabber settings configuration page
3. Attacker modifies 'jabber server' parameter to 127.0.0.1 and sets 'Jabber port' to target port (e.g., 3306 for MySQL, 5432 for PostgreSQL)
4. Attacker enables the Jabber service by checking the 'Enabled' radio button and submitting the form
5. Application attempts to connect to the specified internal service and returns connection status/error messages
6. Attacker analyzes error messages and response times to identify running services, enumerate ports, and potentially gather version information

## Root cause
The application does not implement input validation or IP address filtering on the 'jabber server' parameter, allowing specification of arbitrary hostnames and IP addresses including localhost (127.0.0.1) and internal network resources. No firewall rules or network segmentation prevents the application from initiating connections to internal services.

## Attacker mindset
An admin-level attacker seeks to maximize reconnaissance capabilities by leveraging the application's trust relationship with internal infrastructure. By abusing legitimate configuration parameters, the attacker can perform network reconnaissance without triggering external security controls, using error messages and response patterns to map internal services and identify potential targets for further exploitation.

## Defensive takeaways
- Implement strict input validation on all hostname/IP address parameters: whitelist allowed servers, reject localhost (127.0.0.1, ::1) and private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Apply network segmentation: restrict outbound connections from application servers to only necessary internal services via firewall rules and egress filtering
- Implement connection timeouts and rate limiting on external connection attempts to prevent port scanning abuse
- Sanitize error messages: avoid returning detailed socket errors, connection refused messages, or service banners that enable service enumeration
- Add audit logging for all administrative configuration changes involving network parameters, including IP addresses and ports attempted
- Use allowlist approach: if Jabber server is required, pre-configure trusted servers and disallow dynamic configuration
- Implement CSRF protections on sensitive admin configuration changes
- Regular security review of admin-level functionality with focus on SSRF-prone parameters (URLs, hostnames, IP addresses, ports)

## Variant hunting
Check other admin configuration panels for similar hostname/IP parameters (email servers, webhooks, API endpoints, notification services, backup/restore features)
Search for other network-based integrations (LDAP, DNS, SMTP, NTP, SNMP) that may accept arbitrary hostnames
Review any functionality that accepts URLs or remote server configurations without proper validation
Check if SSRF can be chained with local file inclusion (file:// protocol) or DNS rebinding attacks
Test whether connections can be made to non-standard ports on external networks if firewall allows outbound connections
Verify if error messages leak service version information or internal network topology details

## MITRE ATT&CK
- T1190
- T1046
- T1592
- T1087
- T1040

## Notes
This vulnerability requires Administrator Control Panel access, limiting the attack surface to compromised admin accounts or initial access scenarios. However, the ability to port scan and enumerate internal services significantly increases the value of admin-level compromise. phpBB 3.3.1 is affected; version check recommended to determine if this affects current maintained releases. The vulnerability demonstrates how legitimate-appearing configuration parameters can be weaponized for internal reconnaissance.

## Full report
<details><summary>Expand</summary>

## Overview
The 'Jabber settings' panel inside the Administrator Control Panel can be used to access resources that would otherwise only be accessible by the host machine, including resources/services hosted on the `localhost` interface. This can be performed by setting the 'jabber server' parameter to the desired IP address, such as `127.0.0.1` and the port to the desired port. In some cases, service type/version numbers can be gathered as well as this information is printed to screen.

## How to trigger
Set 'jabber server' to 127.0.0.1
Set 'Jabber port' to whatever port you want to check.
Check the 'Enabled' radio button
Click submit

If the port is closed, you will see a socket error message 'Connection refused' error like this:
{F1051582}

Some such as mysqld simply return:
> Could not authorize on Jabber server.

## Example Recording
I have hosted an internal sshd service on `127.0.0.1:2222` to demonstrate that software type and version information is returned to the Administrator Control Panel. I am `ssh`'d into `phpbb-ubuntu`, which is running the aforementioned sshd service in debug mode so you can see the request hit. 
{F1051590}

## Setup info
Base OS: Ubuntu 20.04.1
phpbb Version: 3.3.1
{F1051573}

## Impact

An attacker could use this to interact with and enumerate services and resources on behalf of the host machine (including resources hosted on the `localhost` interface). This can be used to port scan and, in some cases, perform service versioning/enumeration on the `localhost` interface as well as on machines hosted on the same network as the phpbb host machine.

</details>

---
*Analysed by Claude on 2026-05-24*
