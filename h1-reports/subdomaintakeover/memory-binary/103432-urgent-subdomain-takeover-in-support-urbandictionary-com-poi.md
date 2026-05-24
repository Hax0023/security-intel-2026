# Subdomain Takeover in support.urbandictionary.com pointing to Zendesk

## Metadata
- **Source:** HackerOne
- **Report:** 103432 | https://hackerone.com/reports/103432
- **Submitted:** 2015-12-04
- **Reporter:** harrymg
- **Program:** Urban Dictionary
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain support.urbandictionary.com pointed to an unclaimed Zendesk instance, allowing any attacker to register a Zendesk account and claim the subdomain. This enabled attackers to serve arbitrary content to users trusting the Urban Dictionary domain, potentially facilitating phishing, malware distribution, or credential theft.

## Attack scenario
1. Attacker discovers support.urbandictionary.com displays 'No help desk configured' Zendesk error page
2. Attacker creates a Zendesk account and registers the exact subdomain through Zendesk signup process
3. Attacker configures malicious content on the claimed Zendesk instance (phishing forms, malware links, etc.)
4. Urban Dictionary users visit support.urbandictionary.com, trusting the legitimate domain
5. Users interact with attacker-controlled content, potentially compromising credentials or installing malware
6. Attacker harvests sensitive data or leverages the trusted domain for further attacks

## Root cause
Urban Dictionary created a DNS CNAME or similar record pointing support.urbandictionary.com to Zendesk but failed to claim/configure the Zendesk account, leaving it in an unclaimed state where any third party could register it.

## Attacker mindset
Low-effort, high-impact attack requiring only basic signup capability. Attacker recognizes subdomain trust inheritance—users assume any subdomain belongs to the parent organization. This is opportunistic abuse of poor DNS hygiene and service integration management.

## Defensive takeaways
- Audit all DNS records and ensure every external service reference (CNAME, A records) points to claimed/configured accounts
- Implement a process to verify ownership of all third-party services before creating DNS records
- Regularly scan for dangling DNS records pointing to unclaimed service instances
- Monitor for subdomain takeover indicators (error pages, unclaimed account messages)
- Use DNSSEC and DNS monitoring tools to detect unauthorized changes
- Maintain an inventory of all subdomains and their associated services/owners
- Implement strict access controls on DNS management to prevent orphaned records
- Consider using service providers that offer subdomain verification/claiming mechanisms

## Variant hunting
Search for other Urban Dictionary subdomains pointing to unclaimed external services (AWS S3, GitHub Pages, Heroku, Firebase, etc.). Check sibling organizations or related properties for similar Zendesk misconfigurations. Look for patterns where companies use subdomain services without proper lifecycle management.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a classic subdomain takeover case where the vulnerability exists purely due to operational/configuration failures rather than code flaws. The Zendesk error message itself acts as a helpful guide for attackers, indicating the service is unclaimed and providing signup instructions. This report predates widespread subdomain takeover awareness; such vulns are now commonly automated in security scanning tools.

## Full report
<details><summary>Expand</summary>

Hi. I found out that one of your subdomain which is http://support.urbandictionary.com/ can be taken over or is vulnerable to subdomain takeover. If youre gonna visit the site... you will see saying:

No help desk at support.urbandictionary.com

There is no help desk configured at this address. This means that the address is available and that you can claim it at http://www.zendesk.com/signup/

Which means that the subdomain can be claimed by anyone. Just easy, register and then set it up. Claimed. If claimed, hackers can do something bad about it especially to urbandictionary users.. Please fix Asap.. Thanks

For more info please read this:
http://labs.detectify.com/post/109964122636/hostile-subdomain-takeover-using

</details>

---
*Analysed by Claude on 2026-05-24*
