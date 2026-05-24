# Subdomain Takeover at status-stage0.stripo.email

## Metadata
- **Source:** HackerOne
- **Report:** 781614 | https://hackerone.com/reports/781614
- **Submitted:** 2020-01-23
- **Reporter:** laz0rde
- **Program:** Stripo (via HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain status-stage0.stripo.email contained a dangling CNAME record pointing to stats.uptimerobot.com without an active uptimerobot account, allowing takeover via UptimeRobot account creation. The researcher successfully registered the subdomain through UptimeRobot's service, demonstrating the vulnerability.

## Attack scenario
1. Attacker discovers status-stage0.stripo.email resolves to uptimerobot.com via CNAME record
2. Attacker verifies the UptimeRobot account/subdomain is unclaimed and available for registration
3. Attacker creates a new UptimeRobot account and claims the stats.uptimerobot.com subdomain
4. Attacker gains control over content served at status-stage0.stripo.email
5. Attacker hosts malicious content, phishing pages, or XSS payloads on the takeover subdomain
6. Victims visiting status-stage0.stripo.email or receiving emails appear to come from trusted Stripo domain

## Root cause
DNS CNAME record pointing to third-party service (UptimeRobot) without maintaining an active account or service claim, leaving the subdomain orphaned and available for hostile registration.

## Attacker mindset
Opportunistic attacker performing subdomain enumeration and CNAME analysis to identify dangling DNS records associated with trusted domains, seeking to exploit brand reputation for phishing, malware distribution, or credential harvesting.

## Defensive takeaways
- Regularly audit all DNS records (A, CNAME, MX) and identify dangling/unused entries
- Implement DNS monitoring and alerting for changes to DNS configurations
- Maintain inventory of third-party services and their associated subdomains
- Decommission CNAME records when services are no longer in use rather than leaving them orphaned
- Consider using CNAME flattening or subdomain takeover protection services
- Implement CAA records to restrict certificate issuance on company domains
- Use security scanning tools to detect dangling DNS records automatically
- Enforce subdomain naming conventions to identify staging/deprecated infrastructure

## Variant hunting
Search for other dangling CNAME records pointing to common third-party services (Heroku, GitHub Pages, AWS CloudFront, Shopify, Zendesk, etc.). Check staging/development subdomains (stage, staging, test, dev, qa, stg) which are more likely to be abandoned.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1187

## Notes
Reporter referenced similar vulnerability (HackerOne #737695) on different subdomain of same organization, suggesting potential pattern of DNS management issues. Subdomain takeover severity elevated when targeting stage/production infrastructure that maintains user trust and potentially handles sensitive operations.

## Full report
<details><summary>Expand</summary>

The subdomain status-stage0.stripo.email was pointed at uptimerobot.com
whereas it was not being used , but having Cname record as stats.uptimerobot.com .
Hence anyone can takeover it.

I have parked it with an account on uptimerobot.com
note : 
this issue is similar to [report](https://hackerone.com/reports/737695)
but with another subdomain

## Impact

Subdomain takeover can be abused to do several things like :

Malware distribution
Phishing / Spear phishing
XSS
Authentication bypass
Legitimate mail sending and receiving on behalf of ford subdomain
...
List goes on and on

</details>

---
*Analysed by Claude on 2026-05-24*
