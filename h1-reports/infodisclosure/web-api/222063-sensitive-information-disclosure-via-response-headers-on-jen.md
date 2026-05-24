# Sensitive Information Disclosure via Response Headers on jenkins.brew.sh

## Metadata
- **Source:** HackerOne
- **Report:** 222063 | https://hackerone.com/reports/222063
- **Submitted:** 2017-04-19
- **Reporter:** mrnull1337
- **Program:** Homebrew
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Banner Disclosure, Server Header Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The jenkins.brew.sh server discloses sensitive nginx version information through HTTP response headers, which could aid attackers in identifying known vulnerabilities. This banner disclosure increases attack surface by providing version-specific exploit targeting information.

## Attack scenario
1. Attacker sends HTTP request to jenkins.brew.sh login page
2. Attacker examines response headers and identifies nginx version
3. Attacker cross-references the disclosed version against public vulnerability databases
4. Attacker identifies known CVEs affecting that specific nginx version
5. Attacker crafts targeted exploits based on version-specific vulnerabilities
6. Attacker gains unauthorized access or causes denial of service

## Root cause
Nginx server configured with 'server_tokens on' (default setting), which causes the web server to emit version information in the Server response header and error pages

## Attacker mindset
Reconnaissance-focused: Information disclosure provides free intelligence for targeted exploitation. Attackers routinely scan for version information to identify low-hanging fruit with known public exploits, especially on critical infrastructure like CI/CD systems.

## Defensive takeaways
- Disable server token disclosure by setting 'server_tokens off' in nginx configuration
- Remove or obfuscate all version information from HTTP headers (Server, X-Powered-By, etc.)
- Implement security headers to prevent information leakage (X-Content-Type-Options, X-Frame-Options)
- Keep all software (nginx, Jenkins, etc.) patched to latest versions regardless of version disclosure
- Audit all public-facing services for banner disclosure and version information leakage
- Use Web Application Firewalls (WAF) to strip sensitive headers before reaching clients

## Variant hunting
Check other Homebrew infrastructure servers for similar header disclosures
Examine error pages for version information leakage (common in 404/500 errors)
Look for X-Powered-By, X-AspNet-Version, and other technology-identifying headers
Test for information disclosure in Jenkins instance (version visible in UI)
Scan for git information (.git/config, .git/HEAD) that might disclose system details
Check for directory listing, README files, or other files revealing infrastructure details

## MITRE ATT&CK
- T1590.004 - Gather Victim Identity Information: Identify Cloud Infrastructure
- T1592 - Gather Victim Host Information
- T1590.006 - Gather Victim Network Information: IP Ranges
- T1046 - Network Service Discovery
- T1598 - Phishing for Information

## Notes
This is a classic OSINT/reconnaissance vulnerability. While low severity on its own, banner disclosure is often the first step in a multi-stage attack chain. Jenkins CI/CD systems are high-value targets. The fix is trivial (one configuration line) but frequently overlooked. This report demonstrates good security hygiene from the researcher - identifying low-risk issues that cumulatively improve security posture.

## Full report
<details><summary>Expand</summary>

While logging into jenkins.brew.sh site, the vulnerable nginx version is disclosed via response headers.
There is a chance with known vulnerabilities this could be compromised. so better to avoid banner disclosure with "Server Tokens Prod off" modification in conf file.

Please let me know if any further information is required.

Regards,
Mr_R3boot.

</details>

---
*Analysed by Claude on 2026-05-24*
