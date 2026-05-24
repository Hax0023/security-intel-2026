# Subdomain Takeover via Unclaimed CNAME to Azure Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1457928 | https://hackerone.com/reports/1457928
- **Submitted:** 2022-01-22
- **Reporter:** martinvw
- **Program:** Undisclosed (H1 Report #1457928)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain pointing to an outdated, unclaimed Azure endpoint via CNAME record was vulnerable to takeover. The researcher claimed the domain and redirected it to a blank page as a mitigation measure pending vendor remediation. This vulnerability could allow attackers to serve arbitrary content, perform phishing attacks, or steal user data through the compromised subdomain.

## Attack scenario
1. Attacker discovers subdomain CNAME pointing to an unclaimed/expired Azure endpoint
2. Attacker claims the Azure domain and gains control over the endpoint
3. Attacker hosts malicious content (phishing page, XSS payload, credential harvester) on the compromised domain
4. Users visit the subdomain and are served attacker-controlled content with trust derived from the parent domain
5. Attacker steals session cookies, performs credential harvesting, or exploits XSS to access user accounts
6. Attacker exfiltrates sensitive data or performs account takeovers

## Root cause
DNS CNAME record left pointing to an outdated/unclaimed third-party resource (Azure endpoint) after the original service was decommissioned or migrated. The organization failed to clean up dangling DNS records during infrastructure changes.

## Attacker mindset
Opportunistic reconnaissance targeting common cloud providers' unused endpoints. Attackers actively scan for dangling CNAME records pointing to Azure, AWS, GitHub Pages, and other services where domains can be claimed. This is a low-effort, high-reward attack requiring only domain enumeration and claiming available cloud resources.

## Defensive takeaways
- Implement DNS auditing to identify and remove dangling CNAME records before decommissioning services
- Maintain an inventory of all DNS records and their purposes with regular reviews
- Use monitoring/alerting for DNS changes and orphaned records
- Implement CNAME validation in application code to verify expected endpoints
- Consider using DNS CAA records to restrict SSL/TLS certificate issuance for critical domains
- Include subdomain takeover checks in security testing and bug bounty programs
- Use automated tools (e.g., SubdomainTakeover, can-i-take-over-xyz) in CI/CD pipelines

## Variant hunting
Scan all subdomains for CNAME records pointing to AWS (s3, cloudfront, elastic beanstalk), GitHub Pages, Azure, Heroku, and other popular platforms
Identify subdomains with no A/AAAA records but valid CNAME records pointing to non-existent targets
Check for CNAMEs pointing to decommissioned services or expired service endpoints
Look for dangling CNAME chains (CNAME pointing to another CNAME that points nowhere)
Test for NS record changes that leave subdomains pointing to uncontrolled nameservers
Identify subdomains returning 404s, connection timeouts, or default provider pages

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1566 Phishing
- T1598 Phishing for Information
- T1187 Forced Authentication
- T1040 Network Sniffing
- T1056 Input Capture

## Notes
The researcher demonstrated responsible disclosure by claiming the domain themselves and redirecting to a safe page rather than exploiting it or allowing a malicious actor to do so. The POC was hosted at an obscure URL preventing accidental exploitation. This is a textbook subdomain takeover case where DNS infrastructure was not properly maintained during service lifecycle changes. The vulnerability is critical because the parent domain's trust extends to all subdomains by default in same-site cookie policies and CORS configurations.

## Full report
<details><summary>Expand</summary>

I have found a subdomain of `███████` to be vulnerable to takeovers via a CNAME to unclaimed domain. I have claimed this domain and redirected them to a blank page to prevent a bad actor from doing so in the meantime, and hosted a POC file at obscure URLs. These are the following domains I discovered and the outdated endpoints on Azure to which they point:

█████ --> ████

...and the proof-of-concept file is at the following location:

https://████████/proof.e7437329-ab61-4f22-a049-df5b3685313a.txt

I have not hosted any other file nor attempted any other vector of attack.

## Impact

You're probably familiar with takeovers like this by now, but through this vulnerability, it would be possible for an attacker to obtain cookies and other sensitive information from your users via phishing, cookie hijacking, or XSS.

More info on possible attack vectors can be found at MDN: https://developer.mozilla.org/en-US/docs/Web/Security/Subdomain_takeovers

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
To confirm the issue visit:

https://████████/proof.e7437329-ab61-4f22-a049-df5b3685313a.txt

## Suggested Mitigation/Remediation Actions
Remove CNAME of █████



</details>

---
*Analysed by Claude on 2026-05-24*
