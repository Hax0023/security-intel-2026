# Enabled xmlrpc.php File Allowing XSPA, Brute-force, and DoS Attacks

## Metadata
- **Source:** HackerOne
- **Report:** 884756 | https://hackerone.com/reports/884756
- **Submitted:** 2020-05-28
- **Reporter:** dhakal_bibek
- **Program:** HackerOne (Undisclosed Target)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Port Attack (XSPA), Brute Force Attack, Denial of Service (DoS), Port Scanning, Credential Enumeration, Insecure Direct Object References
- **CVEs:** None
- **Category:** memory-binary

## Summary
The xmlrpc.php file was found to be publicly accessible and enabled on the target WordPress installation, allowing attackers to perform Server-Side Port Scanning (XSPA), brute-force authentication attacks against admin credentials, and launch distributed denial-of-service attacks. The vulnerability stems from the XML-RPC API not being properly restricted or disabled, exposing multiple dangerous RPC methods like wp.getUsersBlogs to unauthenticated attackers.

## Attack scenario
1. Attacker discovers xmlrpc.php is publicly accessible by visiting https://target/xmlrpc.php
2. Attacker uses xml-rpc system.listMethods() to enumerate available RPC procedures exposed by the WordPress installation
3. Attacker exploits wp.getUsersBlogs() or similar methods combined with pingback functionality to perform XSPA attacks and internal port scanning
4. Attacker leverages the exposed RPC interface to conduct brute-force attacks against wp.getUser() or authentication methods to steal admin credentials
5. Attacker automates requests from multiple sources/botnet to cause DoS by overwhelming the server with resource-intensive RPC calls (e.g., wp.getPostList with large iterations)
6. Attacker gains unauthorized access to WordPress admin panel or causes service disruption depending on attack objective

## Root cause
WordPress xmlrpc.php file was not disabled or restricted from external access despite being unused. Default WordPress installation leaves XML-RPC enabled, exposing multiple RPC methods that lack proper authentication, rate limiting, and access controls. No firewall rules or .htaccess restrictions were implemented to limit access to the endpoint.

## Attacker mindset
Opportunistic reconnaissance attacker scanning for low-hanging fruit. XML-RPC is a well-known, documented attack vector on WordPress installations. Attacker likely used automated WordPress vulnerability scanners to discover the enabled endpoint, then leveraged publicly available exploitation techniques. Motivation is credential theft, network reconnaissance, or launching coordinated DoS campaigns from compromised infrastructure.

## Defensive takeaways
- Disable xmlrpc.php if not required by adding 'disable_xmlrpc' => true to wp-config.php or via plugin
- Implement Web Application Firewall (WAF) rules to block access to xmlrpc.php endpoints entirely
- Use .htaccess or server-level rules to restrict access to xmlrpc.php by IP whitelist only
- Implement rate limiting and CAPTCHA on XML-RPC login attempts if xmlrpc.php must remain enabled
- Disable dangerous XML-RPC methods via plugin if full disabling is not possible
- Monitor server logs for suspicious xmlrpc.php requests and brute-force patterns
- Enforce strong, unique admin passwords and implement account lockout after failed attempts
- Conduct regular security audits of WordPress installations to identify enabled but unused features
- Deploy intrusion detection to flag multiple failed XML-RPC authentication attempts from single or multiple sources

## Variant hunting
Check for other exposed WordPress API endpoints: /wp-json/wp/v2/users, /wp-admin/user-new.php
Search for publicly accessible wp-config.php, wp-settings.php backups
Enumerate other WordPress admin endpoints without proper authentication (/wp-admin/, /wp-admin/users.php)
Test for pingback XSPA vulnerabilities using trackback functionality
Identify WordPress installations with debug mode enabled (wp-config.php with WP_DEBUG = true)
Look for outdated plugins that expose XML-RPC methods without authentication
Test for XML-RPC authentication bypass via WordPress user enumeration endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (xmlrpc.php endpoint exploitation)
- T1046 - Network Service Discovery (port scanning via XSPA/pingback)
- T1110 - Brute Force (credential brute-force attacks via wp.getUsersBlogs)
- T1498 - Network Denial of Service (DoS via resource-intensive XML-RPC calls)
- T1592 - Gather Victim Identity Information (user enumeration via XML-RPC methods)
- T1526 - Network Service Scanning (internal reconnaissance via XSPA attacks)

## Notes
Report lacks specific technical details on exploitation steps and impact quantification. References provided are educational but generic. The vulnerability is not a zero-day; it's a configuration/hardening issue documented since WordPress 3.5+. Severity is context-dependent: high for targets with weak credentials, critical if combined with other vulnerabilities. Report quality could be improved with: actual proof-of-concept code, timing/response analysis, affected user count, and business impact assessment.

## Full report
<details><summary>Expand</summary>

##Summary:

Hello team,

I have found a security vulnerability inhttps://███████/xmlrpc.php which lets attacker to:

1: XSPA or PortScan

2: Bruteforce

3:DOS and much more

##Description:

##Impact
Step-by-step Reproduction Instructions
█████████
1: Go to https://██████/xmlrpc.php to check if it is enabled or not.

Remediation:
If the xmlrpc.php file is not being used, it should be disabled and removed completely to avoid any potential risks. Otherwise, it should at the very least be blocked from external access.

Reference:
https://medium.com/@the.bilal.rizwan/wordpress-xmlrpc-php-common-vulnerabilites-how-to-exploit-them-d8d3c8600b32

https://medium.com/@protector47/how-to-hack-wordpress-website-via-xmlrpc-php-61c813fa3740

https://hackerone.com/reports/325040?fbclid=IwAR0qgG-Xfzfi8epruslb_aB91f-Nj8DitF0su8O9ibFKSFdvefJ8h_qWNyc

https://hackerone.com/reports/752073?fbclid=IwAR2i3AM4woHlr01MvyJR-Vu485XQg_gxb1doWmAhSBTfxPK9cUSRFxO2iFo

## Impact

This method is also used for brute force attacks to stealing the admin credentials and other important credentials

This can be automated from multiple hosts and be used to cause a mass DDOS attack on the victim.

</details>

---
*Analysed by Claude on 2026-05-24*
