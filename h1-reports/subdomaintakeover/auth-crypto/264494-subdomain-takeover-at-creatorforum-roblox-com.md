# Subdomain Takeover at creatorforum.roblox.com via Dangling CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 264494 | https://hackerone.com/reports/264494
- **Submitted:** 2017-08-30
- **Reporter:** jackb898
- **Program:** Roblox
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, CNAME Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain creatorforum.roblox.com pointed to a non-existent Discourse instance via CNAME record, creating a subdomain takeover vulnerability. An attacker with a Discourse account could register the orphaned domain and assume control of the Roblox subdomain. The vulnerability was remediated by Roblox after responsible disclosure.

## Attack scenario
1. Attacker enumerates Roblox subdomains and identifies creatorforum.roblox.com
2. Attacker performs DNS lookups and discovers a CNAME record pointing to a non-existent Discourse domain
3. Attacker creates a Discourse account and registers the orphaned domain that the CNAME references
4. The DNS CNAME resolution now points to the attacker-controlled Discourse instance
5. Attacker gains full control over the subdomain content and can serve malicious content under Roblox's domain
6. Attacker can perform phishing, malware distribution, or session hijacking attacks targeting Roblox users

## Root cause
Infrastructure drift and inadequate DNS hygiene. The CNAME record for creatorforum.roblox.com was not removed or updated after the underlying Discourse service was decommissioned, leaving a dangling DNS reference vulnerable to takeover.

## Attacker mindset
Passive reconnaissance and opportunistic exploitation. The attacker demonstrated responsible behavior by immediately reporting rather than exploiting, but a malicious actor would have recognized this as a straightforward path to subdomain control requiring minimal effort and technical skill.

## Defensive takeaways
- Implement regular DNS audits to identify and remove dangling or orphaned records
- Establish automated monitoring for CNAME records that resolve to non-existent domains
- Document all subdomains and their associated services with an inventory management system
- Implement a decommissioning checklist that includes DNS record removal/validation
- Use subdomain takeover detection tools in continuous monitoring pipelines
- Consider CNAME flattening or alternative DNS strategies to reduce takeover surface
- Monitor third-party service registrations to prevent registration of domains matching dangling CNAMEs

## Variant hunting
Look for other Roblox subdomains pointing to Heroku, GitHub Pages, Firebase, AWS S3, or other commonly abandoned services. Check for CNAME records pointing to deprecated platforms or services no longer in use. Investigate subdomains with similar naming patterns (e.g., forum, community, discuss) that may share the same infrastructure drift issue.

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a textbook subdomain takeover case demonstrating the importance of DNS hygiene. The vulnerability required no authentication bypass or exploitation complexity—simply registering an orphaned service would grant full control. The reporter's responsible disclosure process and Roblox's swift remediation prevented potential damage. Subdomain takeovers remain prevalent in large organizations due to infrastructure sprawl and inadequate decommissioning procedures.

## Full report
<details><summary>Expand</summary>

Hello.

A few days ago, I was looking at Roblox subdomains, and I noticed an unusual one called creatorforum.roblox.com. Upon further investigation, I visited it and saw that creatorforum.roblox.com's CNAME was a nonexistant Discourse website.
 I immediately reported to info@roblox.com, and eventually talked to Antek Baranski on the bugbounty@roblox.com email address. The issue has been fixed since reporting, but I was told to send a report here.

If I had a Discourse account, I could've taken over the CNAME for creatorforum.roblox.com and then it would've been a full subdomain takeover on that subdomain.

As mentioned earlier in the report, the issue has been resolved and as you can see the subdomain creatorforum.roblox.com no longer exists.


Thanks,
Jack

</details>

---
*Analysed by Claude on 2026-05-24*
