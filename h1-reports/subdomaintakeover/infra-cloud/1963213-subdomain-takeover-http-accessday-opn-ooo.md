# Subdomain Takeover via Unclaimed Wix Delegation - accessday.opn.ooo

## Metadata
- **Source:** HackerOne
- **Report:** 1963213 | https://hackerone.com/reports/1963213
- **Submitted:** 2023-04-27
- **Reporter:** secsoya
- **Program:** OPN (Organization not explicitly named in report)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
An unclaimed subdomain (accessday.opn.ooo) was found to be delegated to Wix CDN without being properly registered or claimed, leaving it vulnerable to takeover. An attacker could register this subdomain on Wix and serve arbitrary content from the organization's namespace, potentially leading to credential theft, malware distribution, or reputational damage.

## Attack scenario
1. Attacker discovers the subdomain accessday.opn.ooo resolves to Wix CDN infrastructure
2. Attacker identifies that no legitimate Wix site claims this subdomain (unclaimed state)
3. Attacker creates a Wix account and claims the subdomain through Wix's domain registration process
4. Attacker hosts malicious content (phishing page, malware, etc.) on the claimed subdomain
5. Users and security systems trust the domain due to parent domain reputation
6. Attacker exfiltrates credentials, distributes malware, or damages organization reputation

## Root cause
DNS misconfiguration resulting in dangling CNAME/NS records pointing to Wix CDN for a subdomain that was never claimed or registered. Lack of ongoing DNS hygiene and subdomain enumeration practices allowed orphaned DNS entries to persist.

## Attacker mindset
Opportunistic reconnaissance during domain enumeration. Attacker leverages common hosting platform delegations to identify low-hanging fruit. Minimal effort required to claim unclaimed subdomains on popular platforms like Wix, making this an attractive target for initial access or malicious hosting.

## Defensive takeaways
- Implement regular subdomain enumeration and DNS audits to identify dangling records
- Maintain inventory of all subdomains and their current purpose/owner
- Implement CNAME validation to prevent pointing to unclaimed third-party services
- Use CAA records to restrict certificate issuance for subdomains
- Monitor DNS changes and implement alerting for new subdomain registrations
- Decommission unused subdomains or park them with content indicating non-use
- Implement subdomain takeover detection tools in CI/CD pipeline
- Establish process to claim or secure all subdomains on hosted platforms if delegated

## Variant hunting
Search for other *.opn.ooo subdomains pointing to Wix or other SaaS platforms
Check for subdomains delegated to: GitHub Pages, Heroku, Firebase, Azure, AWS, Vercel, Netlify
Look for CNAME records pointing to unclaimed third-party services
Scan for SSL certificates issued for opn.ooo subdomains to identify scope
Check DNS history (SecurityTrails, Censys) for delegation changes indicating abandonment

## MITRE ATT&CK
- T1587.001 - Acquire Infrastructure: Domains
- T1583.001 - Acquire Infrastructure: Domains
- T1556 - Modify Authentication Process
- T1598.003 - Phishing: Spearphishing Link
- T1189 - Drive-by Compromise

## Notes
Report references similar vulnerabilities (reports #1256389, #996956, #1183296) indicating this is a recurring issue. Subdomain takeover severity depends on usage context - could facilitate phishing, malware distribution, or credential harvesting. No bounty amount provided in report, suggesting possible duplicate or low-priority classification by program.

## Full report
<details><summary>Expand</summary>

I found unused accessday.opn.ooo subdomain was delegated to wix.com and not claimed.

##Steps To Reproduce:
- Visit http://accessday.opn.ooo/
- This domain pointing towards to WIX cdn, anyone can claim this subdomain

##Similar report:
https://hackerone.com/reports/1256389
https://hackerone.com/reports/996956
https://hackerone.com/reports/1183296

## Impact

An attacker can claim this subdomain and abused for specific purposes

</details>

---
*Analysed by Claude on 2026-05-24*
