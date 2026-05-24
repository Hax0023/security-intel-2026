# Subdomain Takeover at status0.stripo.email via Dangling CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 737695 | https://hackerone.com/reports/737695
- **Submitted:** 2019-11-14
- **Reporter:** haxorpunk
- **Program:** Stripo
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling CNAME, DNS Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain status0.stripo.email contained a CNAME record pointing to stats.uptimerobot.com without an active account, allowing attackers to claim ownership via UptimeRobot and impersonate the service. This enabled arbitrary content hosting and potential phishing attacks under Stripo's domain.

## Attack scenario
1. Attacker discovers status0.stripo.email resolves to uptimerobot.com via DNS enumeration
2. Attacker verifies the CNAME record (stats.uptimerobot.com) is unclaimed in UptimeRobot
3. Attacker creates a free UptimeRobot account and claims the subdomain
4. Attacker configures a malicious status page or phishing content
5. Attacker sends phishing emails appearing to come from Stripo's status domain
6. Victims trust the message due to legitimate domain authority and interact with malicious content

## Root cause
Stripo failed to clean up or reclaim DNS CNAME records for deprecated subdomains after discontinuing the associated UptimeRobot service. The subdomain remained in DNS pointing to an unclaimed third-party service, creating a dangling reference exploitable by any actor.

## Attacker mindset
Low-effort attack requiring only DNS reconnaissance and creating a free third-party account. Appealing for domain reputation abuse, phishing campaigns, and impersonation without technical sophistication.

## Defensive takeaways
- Implement DNS audit procedures to identify and remove dangling CNAME, A, and MX records
- Maintain inventory of all subdomains and their purposes with regular reconciliation
- Establish decommissioning checklist requiring DNS cleanup when retiring services
- Monitor DNS changes through DNSSEC or external DNS monitoring tools
- Periodically scan for unclaimed third-party service integrations
- Use DNS CAA records to restrict certificate issuance on unused subdomains
- Implement automated alerts for unused subdomain claims on common platforms

## Variant hunting
Check other Stripo subdomains for similar dangling CNAME patterns
Search for other services pointing to abandoned third-party platforms (Heroku, Shopify, GitHub Pages, AWS)
Review organizational DNS for MX records pointing to discontinued mail providers
Scan for CNAME records with typos or deprecated service endpoints
Test takeoverability of subdomains across known vulnerable platforms

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link

## Notes
Straightforward subdomain takeover requiring minimal technical skill. Researcher demonstrated responsible disclosure by parking the domain rather than weaponizing it. Impact limited by lack of SSL/TLS certificate capability but still enables phishing and status page impersonation. Similar to HackerOne disclosed takeovers on platforms with user-claimed subdomains.

## Full report
<details><summary>Expand</summary>

Hi ,

The subdomain status0.stripo.email was pointed at uptimerobot.com
whereas it was not being used , but having Cname record as stats.uptimerobot.com .
Hence anyone can takeover it.

I have parked it with atest account on uptimerobot.com

{F634639}

{F634636}

thanks

## Impact

Anyone can use this subdomain on uptimerobot.com with a false message.

</details>

---
*Analysed by Claude on 2026-05-24*
