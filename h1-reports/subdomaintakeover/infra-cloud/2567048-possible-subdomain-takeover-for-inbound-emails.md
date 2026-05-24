# Subdomain Takeover via Unclaimed SendGrid CNAME Record

## Metadata
- **Source:** HackerOne
- **Report:** 2567048 | https://hackerone.com/reports/2567048
- **Submitted:** 2024-06-20
- **Reporter:** cryptic_
- **Program:** Smule
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain email.smule.com contains a CNAME record pointing to SendGrid's infrastructure but the subdomain is not properly claimed or configured on SendGrid, leaving it available for takeover. An attacker could register this subdomain on SendGrid and potentially intercept inbound emails or conduct further attacks against Smule users.

## Attack scenario
1. Attacker discovers email.smule.com resolves to SendGrid via CNAME record using DNS enumeration (dig/nslookup)
2. Attacker confirms SendGrid subdomain is unclaimed by visiting email.smule.com and receiving 404 response
3. Attacker creates a SendGrid account and registers the email.smule.com subdomain within SendGrid's management panel
4. Attacker gains control of inbound email routing for the email.smule.com domain
5. Attacker intercepts emails, performs phishing attacks using legitimate domain, or accesses sensitive communications
6. Attacker leverages email access for account takeover or social engineering against Smule employees/users

## Root cause
DNS CNAME record points to SendGrid infrastructure for a subdomain that was either abandoned, migrated, or never properly configured/claimed on the third-party service. No monitoring or regular audit of DNS records for claimed vs unclaimed external service references.

## Attacker mindset
Opportunistic reconnaissance: scan for dangling DNS records pointing to popular services, identify unclaimed subdomains, register them on the target service, and leverage email access for credential harvesting, impersonation, or further lateral movement.

## Defensive takeaways
- Maintain an inventory of all DNS records and map them to active services
- Regularly audit DNS configuration to identify and remove dangling CNAME records
- For each external service integration, verify the subdomain is properly claimed and configured
- Implement DNS monitoring to alert on unclaimed subdomains pointing to known services
- Use CAA records to restrict certificate issuance for corporate domains
- Establish process for decommissioning services that includes DNS cleanup
- Monitor for domain registration attempts using your subdomains across major service providers

## Variant hunting
Check for other *.smule.com subdomains pointing to GitHub Pages, Heroku, AWS CloudFront, Azure, or Fastly
Search for subdomains pointing to discontinued hosting providers or outdated services
Identify subdomains with CNAME records that resolve to 404 pages across the organization
Use DNS datasets to find patterns of abandoned CNAME records in similar companies
Check for NS record delegations to services no longer in use

## MITRE ATT&CK
- T1584.001
- T1098
- T1190
- T1566.002

## Notes
Low-hanging fruit vulnerability commonly found during reconnaissance. SendGrid context is particularly sensitive due to email handling. The fix is straightforward: either claim the subdomain on SendGrid or remove the CNAME record entirely. Reporter provided clear reproduction steps and relevant references to similar vulnerabilities.

## Full report
<details><summary>Expand</summary>

Hello Smule Security Team,
I'm cryptic_, I have identified that the affected url points to sendgrid.net, via a DNS CNAME record. As a result of this an attacker could potentially initate a subdomain take over by registering the subdomain email.smule.com on sendgrid and consiquently leverage this for further attacks. Additionally it has been noted that sendgrid is a service for email marketing so theoretically should an attacker be able to gain access to the subdomain they could potentially gain access to emails too.

## Affected URL
email.smule.com


## Steps To Reproduce:

  1. Go to email.smule.com
  2. You will see 404 Not Found 
  1. Use this command to see the CNAME Record - dig 

## Risk Breakdown
Risk: Medium
Difficulty to Exploit: Medium
Authentication: None

## Recommended Fix
Check your DNS-configuration for subdomains pointing to services not in use.
Set up your external service so it fully listens to your wildcard DNS.


## Reference
https://www.hackerone.com/blog/Guide-Subdomain-Takeovers
http://blog.pentestnepal.tech/post/149985438982/reading-ubers-internal-emails-uber-bug-bounty
https://hackerone.com/reports/166826
https://hackerone.com/reports/403822

## Impact

A way to take over subdomain for inbound emails. An attacker can simply register to sendgrid and takeover this subdomain.

</details>

---
*Analysed by Claude on 2026-05-24*
