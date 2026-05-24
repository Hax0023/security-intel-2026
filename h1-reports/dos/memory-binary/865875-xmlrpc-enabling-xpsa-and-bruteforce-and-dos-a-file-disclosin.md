# XMLRPC Exploitation, Credential Disclosure via Installer Logs, and Pingback DoS

## Metadata
- **Source:** HackerOne
- **Report:** 865875 | https://hackerone.com/reports/865875
- **Submitted:** 2020-05-04
- **Reporter:** tandav
- **Program:** HackerOne (specific program not named)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** XML-RPC Brute Force, Information Disclosure, Denial of Service, Path Traversal / File Disclosure, Weak Access Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
The target exposed XML-RPC functionality at /xmlrpc.php without authentication restrictions, enabling credential brute-force attacks. Administrator credentials were further compromised through publicly accessible installer-log.txt file containing sensitive usernames. XML-RPC pingback functionality could be abused for distributed DoS attacks when mishandled.

## Attack scenario
1. Attacker discovers /xmlrpc.php endpoint is accessible without authentication
2. Attacker accesses installer-log.txt publicly and extracts valid admin username
3. Attacker performs brute-force attack against wp.getUserBlogs or wp.getPost XML-RPC methods using discovered username
4. Upon successful authentication, attacker gains admin access to WordPress installation
5. Attacker leverages XML-RPC pingback functionality (pingback.ping method) from multiple compromised hosts
6. Pingback requests sent to victim server cause resource exhaustion, resulting in distributed denial of service

## Root cause
Multiple security misconfigurations: (1) XML-RPC interface enabled without authentication or rate-limiting, (2) Installer logs and backup files left in web-accessible directory, (3) No restrictions on XML-RPC method execution, (4) Pingback functionality not rate-limited or validated for abuse

## Attacker mindset
Opportunistic reconnaissance and exploitation - attacker systematically identified low-hanging fruit (publicly exposed XML-RPC, installer artifacts), combined multiple weaknesses into a complete attack chain for credential theft and infrastructure disruption. The multi-vector approach demonstrates understanding of WordPress attack surface and ability to chain vulnerabilities for maximum impact.

## Defensive takeaways
- Disable XML-RPC entirely via wp-config.php (define('XMLRPC_REQUEST', false)) if not required
- If XML-RPC is necessary, implement IP whitelisting and strong authentication
- Remove or restrict access to installer logs, backup files, and configuration files from web root
- Implement rate-limiting on XML-RPC authentication attempts and pingback requests
- Monitor for XML-RPC brute-force patterns (multiple failed authentication attempts)
- Use Web Application Firewall rules to block suspicious XML-RPC requests
- Regularly audit file permissions and ensure sensitive files are not world-readable
- Implement CAPTCHA or IP-based restrictions for administrative interfaces
- Use security headers and robots.txt to prevent discovery of sensitive paths

## Variant hunting
Hunt for: (1) Other XML-RPC enabled WordPress instances via port scans + /xmlrpc.php fingerprinting, (2) Exposed installation/setup files (.setup.php, wp-admin/install.php, setup-config.php), (3) Backup files with predictable names (.bak, .backup, .old extensions), (4) Log files in web-accessible directories, (5) XML-RPC pingback abuse in CloudFlare/WAF logs, (6) Similar patterns in other CMS platforms (Movable Type, Drupal XML-RPC), (7) Information disclosure through wp-json endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (if credentials used for social engineering)
- T1583 - Acquire Infrastructure (setting up bot nodes for distributed DoS)
- T1592 - Gather Victim Identity Information
- T1110 - Brute Force (credential stuffing via XML-RPC)
- T1020 - Automated Exfiltration (via compromised admin account)
- T1499 - Service Exhaustion Flood (pingback DoS)
- T1526 - Enumerate External Targets
- T1538 - Cloud Service Discovery

## Notes
The report demonstrates a complete attack chain combining reconnaissance (installer log discovery), credential compromise (XML-RPC brute force), and impact (DoS via pingback). The vulnerability severity is amplified by chaining multiple weaknesses. The attacker referenced publicly available research (Netsparker blog post), indicating this is a known, reproducible attack pattern. Installer logs are a common information disclosure vector in CMS installations and should be treated as critical assets requiring protection.

## Full report
<details><summary>Expand</summary>

## Summary:
[XMLRPC+Installer_logs+Backup_Filename+Admin_username+disclosure]

## Steps To Reproduce:

  1. I was able to successfully exploit XMLRPC with the traditional method, the brute-force was done the username was there in the Installer Logs
  2. path to XMLRPC is http://13.92.255.102/xmlrpc.php + the username is in https://lonestarcell.com/installer-log.txt 
  3. Pingback ping can be used to dos the target server when mishandled
## Supporting Material/References:
I was able to reproduce this whole https://www.netsparker.com/blog/web-security/xml-rpc-protocol-ip-disclosure-attacks/

## Impact

1)Automated once from multiple hosts and be used to cause a mass DDOS attack on the victim.
2) This method is also used for brute force attacks to stealing the admin credentials and other important credentials
3) File disclosure is causing most harm as internal criticals are popping out

</details>

---
*Analysed by Claude on 2026-05-24*
