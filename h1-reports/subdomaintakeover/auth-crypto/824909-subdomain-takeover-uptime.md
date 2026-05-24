# Subdomain Takeover - uptime.btfs.io

## Metadata
- **Source:** HackerOne
- **Report:** 824909 | https://hackerone.com/reports/824909
- **Submitted:** 2020-03-19
- **Reporter:** ahmed_alwardani
- **Program:** BTFS (BitTorrent File System)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Domain/Subdomain Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A subdomain (uptime.btfs.io) was found pointing to UptimeRobot service but was not claimed by the organization, allowing an attacker to register and claim ownership of the subdomain. This enables potential malware distribution, phishing campaigns, XSS attacks, and credential harvesting under a legitimate organization domain.

## Attack scenario
1. Attacker discovers through DNS enumeration or passive scanning that uptime.btfs.io resolves to UptimeRobot CNAME records
2. Attacker verifies the UptimeRobot account associated with the subdomain is unclaimed or abandoned
3. Attacker registers a new UptimeRobot account and claims ownership of the uptime.btfs.io subdomain
4. Attacker gains full control of the subdomain content and can serve arbitrary pages under the legitimate btfs.io domain
5. Attacker uses the compromised subdomain for phishing, malware distribution, or XSS attacks against users trusting the btfs.io domain
6. Victims interact with the attacker-controlled content believing it originates from the legitimate organization

## Root cause
The organization created a DNS record pointing to UptimeRobot service but failed to claim or properly configure the corresponding account, leaving the subdomain in an unclaimed state. Additionally, lack of regular subdomain inventory auditing and monitoring allowed the dangling DNS record to persist.

## Attacker mindset
Opportunistic reconnaissance attacker who systematically enumerates subdomains, identifies unclaimed third-party service integrations, and exploits weak claim/verification mechanisms to gain control of trusted organizational infrastructure for malicious purposes.

## Defensive takeaways
- Maintain comprehensive inventory of all organizational subdomains and third-party service integrations
- Implement automated monitoring to detect and alert on dangling DNS records pointing to unclaimed services
- Establish process to claim and fully configure all third-party service accounts before creating associated DNS records
- Regularly audit DNS records and remove or properly secure any subdomains no longer in active use
- Implement CNAME validation and verification requirements before DNS resolution
- Use subdomain takeover scanning tools as part of security testing pipeline
- Monitor for newly registered accounts on third-party services using organizational domain names

## Variant hunting
Search for other unclaimed subdomains pointing to common SaaS platforms (Heroku, Zendesk, Shopify, etc.)
Check for dangling CNAME records across all organizational subdomains
Identify subdomains pointing to deprecated or decommissioned services
Look for MX records pointing to unclaimed email service providers
Enumerate subdomains used for monitoring, status pages, or internal tools
Test third-party services for account registration using organizational domain names

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1583.001 - Acquire Infrastructure: Domains
- T1036.005 - Masquerading: Match Legitimate Name or Location
- T1608.004 - Stage Capabilities: Drive-by Target

## Notes
This is a classic subdomain takeover via dangling DNS record. The reporter demonstrated clear impact by actually claiming the subdomain. The presence of a password-protected login page (A123456789) suggests this was a legitimate but abandoned UptimeRobot integration. The vulnerability allows complete account takeover and content control under a trusted domain, making it particularly dangerous for phishing and malware campaigns.

## Full report
<details><summary>Expand</summary>

Hello Team:

i can't report it to the company so i hope to accept it as a valid bug , i found subdomain takeover in your subdomain ```uptime.btfs.io``` , i found this subdomain pointed to uptimerobot and not claimed so i signedup in uptimerobot and claimed it.

POC:
------

1 - open https://uptime.btfs.io/
2 - you need a password to login ```A123456789```
3 - {F753695}

## Impact

- Subdomain takeover can be abused to do several things like :
Malware distribution
Phishing / Spear phishing
XSS
Authentication bypass
Legitimate mail sending and receiving on behalf of ford subdomain

</details>

---
*Analysed by Claude on 2026-05-24*
