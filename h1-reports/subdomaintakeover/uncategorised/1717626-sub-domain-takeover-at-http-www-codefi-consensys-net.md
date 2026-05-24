# Subdomain Takeover at www.codefi.consensys.net via Unclaimed Squarespace Domain

## Metadata
- **Source:** HackerOne
- **Report:** 1717626 | https://hackerone.com/reports/1717626
- **Submitted:** 2022-09-30
- **Reporter:** krrish_hackk
- **Program:** ConsenSys (HackerOne)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain www.codefi.consensys.net had a CNAME record pointing to Squarespace but was never claimed by ConsenSys, allowing an attacker to register a Squarespace account and claim the domain. This enabled complete takeover of the subdomain, allowing the attacker to host malicious content under ConsenSys's domain.

## Attack scenario
1. Enumerate subdomains of consensys.net using reconnaissance tools like Subfinder
2. Identify subdomains returning 404 status codes with Squarespace's 'Domain Not Claimed' message
3. Locate www.codefi.consensys.net pointing to unclaimed Squarespace hosting infrastructure
4. Create a new account on Squarespace and access domain management features
5. Add the target subdomain (www.codefi.consensys.net) to the attacker's Squarespace account
6. Host phishing content, malware, or perform XSS/CSRF attacks leveraging the trusted ConsenSys domain

## Root cause
DNS CNAME record for www.codefi.consensys.net pointed to Squarespace infrastructure without the corresponding virtual host being claimed or provisioned. The subdomain was left in a dangling state during deprovisioning or initial misconfiguration, allowing third-party claim.

## Attacker mindset
Systematic reconnaissance of large organizations' subdomains to identify low-hanging fruit. Attacker recognized that unclaimed hosting providers (Squarespace) allow domain claims without ownership verification, enabling rapid takeover with minimal effort and cost.

## Defensive takeaways
- Maintain comprehensive inventory of all subdomains and their hosting providers
- Implement deprovisioning process: remove DNS records BEFORE terminating virtual hosts
- Implement provisioning process: claim virtual hosts BEFORE creating DNS records
- Monitor for dangling DNS records through regular scanning and alerting
- Coordinate between infrastructure, DNS administration, and hosting teams to prevent gaps
- Periodically audit all subdomains for unclaimed or unresponsive hosting endpoints
- Configure DNS with explicit monitoring to catch orphaned records
- Use DNS CAA records to restrict certificate issuance on subdomains

## Variant hunting
Search for other ConsenSys subdomains with Squarespace/Heroku/GitHub Pages/Azure/AWS S3 CNAME records returning 404 or 'Domain Not Claimed' messages. Check for similar patterns across other cryptocurrency/blockchain organizations with extensive subdomain infrastructure.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1185

## Notes
Classic subdomain takeover vulnerability often overlooked due to organizational sprawl. The vulnerability is easily exploitable once discovered but requires proper lifecycle management processes to prevent. The impact extends beyond simple content hosting to token theft, phishing, and CSP bypass scenarios. This demonstrates importance of infrastructure governance in large organizations.

## Full report
<details><summary>Expand</summary>

Summary:
 
Subdomain takeovers:

A subdomain takeover occurs when an attacker gains control over a subdomain of a target domain. Typically, this happens when the subdomain has a canonical name (CNAME) in the Domain Name System (DNS), but no host is providing content for it. This can happen because either a virtual host hasn't been published yet or a virtual host has been removed. An attacker can take over that subdomain by providing their own virtual host and then hosting their own content for it.

If an attacker can do this, they can potentially read cookies set from the main domain, perform cross-site scripting, or circumvent content security policies, thereby enabling them to capture protected information (including logins) or send malicious content to unsuspecting users.

 Steps To Reproduce:

  1. GO to http://consensys.net and find its sub-domains using Subfinder.
  1. now find sub-domains status code.
  1. Search for 404 code.
 4.  its showing :- 
Domain Not Claimed
This domain has been mapped to Squarespace, but it has not yet been claimed by a website. If this is your domain, claim it in the Domains tab of your Website Manager.
5. now create a account at Squarespace, create a website template and then go to use a domain i own.
 6. then copy and paste http://www.codefi.consensys.net/  and  boom sub-domain takeover completed.

Supporting Material/References:

POC is attached below.


 How to prevent it ?

Preventing subdomain takeovers is a matter of order of operations in lifecycle management for virtual hosts and DNS. Depending on the size of the organization, this may require communication and coordination across multiple departments, which can only increase the likelihood for a vulnerable misconfiguration.

Define standard processes for provisioning and deprovisioning hosts. Do all steps as closely together as possible.
Start provisioning by claiming the virtual host; create DNS records last.
Start deprovisioning by removing DNS records first.
Create an inventory of all of your organization's domains and their hosting providers, and update it as things change, to ensure that nothing is left dangling.

## Impact

Risks of a Subdomain Takeover:-

Various risks could be the result of a subdomain takeover.

1. Bypassing CSRF protection
2. Phishing
3. Leak of OAuth 2.0 Tokens
4. The redirect is only performed if the target URL is trusted. If all subdomains are trusted as target URL, an attacker might be able to get OAuth 2.0 tokens via a target URL which points to a compromised subdomain.
5. Bypass Content Security Policy
6. A, AAAA and CNAME Records

</details>

---
*Analysed by Claude on 2026-05-24*
