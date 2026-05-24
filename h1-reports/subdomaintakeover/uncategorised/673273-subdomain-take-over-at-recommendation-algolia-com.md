# Subdomain Takeover at recommendation.algolia.com via Dangling CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 673273 | https://hackerone.com/reports/673273
- **Submitted:** 2019-08-14
- **Reporter:** badcracker
- **Program:** Algolia
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling CNAME, DNS Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain recommendation.algolia.com contains a CNAME record pointing to recommendation.us, which is an unregistered/available domain for purchase. An attacker could purchase recommendation.us and claim ownership of the subdomain, potentially hosting malicious content under the Algolia domain.

## Attack scenario
1. Attacker identifies that recommendation.algolia.com resolves via CNAME to recommendation.us
2. Attacker verifies that recommendation.us domain is available for registration
3. Attacker purchases the recommendation.us domain
4. DNS propagation occurs, pointing recommendation.algolia.com traffic to attacker-controlled infrastructure
5. Attacker hosts malicious content (phishing, malware, adult content) accessible via recommendation.algolia.com
6. Victims trust the Algolia domain and interact with attacker's malicious content

## Root cause
Dangling CNAME configuration: DNS record points to an external domain (recommendation.us) that is not registered or is no longer under the organization's control, creating an unclaimed namespace that can be registered by attackers.

## Attacker mindset
Opportunistic threat actor scanning for misconfigured DNS records and dangling external domain references. Low effort, high impact attack requiring only domain registration to compromise a trusted subdomain.

## Defensive takeaways
- Audit all CNAME records pointing to external domains and verify continued ownership/control
- Remove or update dangling CNAME records that point to unregistered/abandoned domains
- Implement DNS monitoring to detect changes or takeover attempts on critical subdomains
- Use DNS security services that detect and alert on subdomain takeover vulnerabilities
- Establish process to retire subdomains and clean up associated DNS records when services are decommissioned
- Consider using CNAME validation mechanisms or certificate pinning for critical services

## Variant hunting
Scan all Algolia subdomains for CNAME records pointing to external domains
Check for CNAME records pointing to cloud services (AWS, Azure, GitHub Pages) without proper ownership verification
Identify expired or unregistered domains referenced in MX, NS, or other DNS records
Search for similar patterns across related domains (.com, .io, .net variants)
Review DNS history using tools like SecurityTrails to find previously registered dangling references

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1584.001 - Compromise Infrastructure: Domains
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link

## Notes
This is a classic subdomain takeover vulnerability with clear exploitation path. The report lacks detail on impact confirmation and proof of concept attachment reference (F555251) is not accessible. The vulnerability would allow complete impersonation of Algolia's recommendation service, potentially affecting reputation and user trust.

## Full report
<details><summary>Expand</summary>

##Description
hello sir,
your subdomain recommendation.algolia.com cname is recommendation.us and recommendation.us is for sell which can lead to subdomain take over
##steps to reproduce
1. check the cname of recommendation.algolia.com
2. see that the cname "recommendation.us" is for sell using lookup tool

##poc:
{F555251}

## Impact

Attackers are able to purchase recommendation.us then they will be able to takeover recommendation.algolia.com and post porn pictures or phishing forums

</details>

---
*Analysed by Claude on 2026-05-24*
