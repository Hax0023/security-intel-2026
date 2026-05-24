# Directory Listing and Information Disclosure via IP Address Bypass on newsletter.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 145603 | https://hackerone.com/reports/145603
- **Submitted:** 2016-06-18
- **Reporter:** mefkan
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Directory Listing, Authentication Bypass, Virtual Host Configuration Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
Authentication controls and directory listing protections on newsletter.nextcloud.com were implemented at the domain level rather than the IP level, allowing attackers to bypass restrictions by accessing the server directly via IP address (88.198.160.137). This exposure reveals sensitive information including phpList version 3.2.5 and access to administrative interfaces and design pages that should require authentication.

## Attack scenario
1. Attacker performs reconnaissance and discovers the IP address 88.198.160.137 hosting newsletter.nextcloud.com through DNS enumeration or WHOIS lookup
2. Attacker bypasses domain-based authentication by making HTTP requests directly to the IP address instead of using the domain name
3. Attacker accesses http://88.198.160.137/admin/ and gains unauthenticated access to the phpList admin interface that requires authentication when accessed via the domain
4. Attacker views page source and identifies phpList version 3.2.5, enabling version-specific vulnerability research
5. Attacker enumerates directories using the IP address (http://88.198.160.137/images/, http://88.198.160.137/admin/ui/) to discover functionality hidden by domain-level restrictions
6. Attacker accesses design pages and administrative UI at http://88.198.160.137/admin/ui/dressprow/pages/design.php to gather intelligence for crafting targeted attacks

## Root cause
Security controls were implemented using virtual host/domain-based routing (HTTP Host header validation) without corresponding IP-level restrictions. The web server was misconfigured to enforce authentication and directory listing protections only for requests matching the domain name, leaving direct IP-based access unprotected. This is a common misconfiguration in systems using virtual hosting where security rules are applied at the application layer rather than the infrastructure layer.

## Attacker mindset
Reconnaissance-focused threat actor identifying infrastructure weaknesses. The attacker demonstrates methodical enumeration of bypass techniques (domain vs IP access) and systematic directory discovery. Their intent appears to be information gathering for follow-on attacks rather than immediate exploitation, as evidenced by the statement that 'an attacker can use this information for future bugs.' This represents the OSINT/reconnaissance phase of an attack chain.

## Defensive takeaways
- Implement security controls at multiple layers (web server, firewall, application) rather than relying solely on domain-based routing
- Configure web server to enforce authentication and access controls based on IP/network level rules, not just HTTP Host headers
- Disable directory listing across all access vectors (domain and IP) using web server configuration (.htaccess, nginx directives)
- Implement network-level protections: use firewall rules to restrict direct IP access, bind services to localhost, or use reverse proxy with strict host validation
- Apply HTTP Strict-Transport-Security (HSTS) and Host validation headers to prevent IP-based bypass attempts
- Regularly audit web server configurations for authentication bypass conditions, particularly in virtual host setups
- Keep application frameworks and plugins (phpList) updated to patch known vulnerabilities disclosed through version enumeration
- Monitor and alert on unusual access patterns (requests to IP addresses that differ from domain-based access patterns)
- Implement rate limiting and WAF rules to detect automated reconnaissance attempts

## Variant hunting
Look for similar virtual host bypass vulnerabilities in: other Nextcloud deployments, phpList instances, and web applications using domain-based authentication without IP-level controls. Search for other services on the same IP range (88.198.160.0/24) that may have similar misconfigurations. Check for directory listing enabled on administrative endpoints across different subdomain configurations. Test for Host header injection and HTTP request smuggling that could bypass virtual host restrictions.

## MITRE ATT&CK
- T1592 - Gather Victim Host Information (version enumeration via page source)
- T1589 - Gather Victim Identity Information (discovery of administrative interfaces)
- T1526 - Passive Scanning (reconnaissance via IP enumeration)
- T1087 - Account Discovery (identification of admin interfaces)
- T1040 - Network Sniffing (implicit: domain to IP mapping discovery)
- T1538 - Reconnaissance via Web (directory enumeration, source code analysis)

## Notes
Report demonstrates a classic virtual hosting misconfiguration where security was implemented in application/domain layer without corresponding infrastructure-level controls. The vulnerability is relatively low-risk from an exploitation standpoint (design pages and version info alone), but valuable for threat actors in reconnaissance phase. The phpList version disclosure is particularly useful as version 3.2.5 may have known CVEs. Nextcloud should have patched by implementing IP-level restrictions, validating Host headers strictly, or using a reverse proxy/WAF. The report format suggests an experienced security researcher, though the writeup could be more detailed regarding proof of actual admin functionality access.

## Full report
<details><summary>Expand</summary>

Hi,

This is the domain that we are going to work about it as you know:

https://newsletter.nextcloud.com/

Firstly I want to tell https://newsletter.nextcloud.com/admin when you are trying to navigate this link it needs authentication.But when you are doing this with via IP http://88.198.160.137/admin/ you can reach the admin page.And with this you are gettin information about phpList.

view-source:http://88.198.160.137/index.php

Go that page you'll see this code in the source       title="powered by phpList version 3.2.5,

Let's talk about directory listening.

Again.when you are trying navigate this https://newsletter.nextcloud.com/images/ it is saying "Not authorized." but you can reach the directories via IP


PoC:

Take a look at links below

http://88.198.160.137/images/

http://88.198.160.137/admin/ui/

I can even access the designing page with this link

http://88.198.160.137/admin/ui/dressprow/pages/design.php

Probably this design page is helping you when you are creating the codes of html pages on the newsletter.Anyway an attacker can use this informations for future bugs,or he can provide useful information

Thanks already,

mefkan


</details>

---
*Analysed by Claude on 2026-05-24*
