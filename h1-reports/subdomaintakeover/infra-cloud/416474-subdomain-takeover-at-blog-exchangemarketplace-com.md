# Subdomain Takeover at blog.exchangemarketplace.com

## Metadata
- **Source:** HackerOne
- **Report:** 416474 | https://hackerone.com/reports/416474
- **Submitted:** 2018-09-30
- **Reporter:** m7mdharoun
- **Program:** exchangemarketplace.com
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain blog.exchangemarketplace.com was vulnerable to subdomain takeover due to a dangling CNAME DNS record pointing to a Shopify instance that was no longer claimed or properly configured. An attacker was able to claim the associated Shopify store and take control of the subdomain, potentially redirecting traffic and impersonating the organization.

## Attack scenario
1. Attacker identifies that blog.exchangemarketplace.com resolves via CNAME to a Shopify domain
2. Attacker discovers the Shopify store associated with that CNAME is unclaimed or abandoned
3. Attacker creates or claims a Shopify store matching the expected hostname
4. Attacker's Shopify store becomes accessible via the blog.exchangemarketplace.com subdomain
5. Attacker can serve malicious content, phishing pages, or perform credential harvesting through the legitimate subdomain
6. Victims trust the subdomain due to legitimate domain ownership, increasing attack success rate

## Root cause
The organization failed to properly manage DNS records when deprovisioning or migrating away from Shopify. The CNAME record pointing to Shopify remained in DNS configuration even after the associated Shopify store was no longer maintained, creating a dangling DNS record that could be claimed by an attacker.

## Attacker mindset
The attacker systematically enumerated subdomains, identified external service dependencies, and discovered the organization no longer actively maintained the Shopify resource. Recognizing the opportunity to claim an unowned Shopify store, the attacker exploited the misconfiguration to achieve subdomain control with minimal effort.

## Defensive takeaways
- Audit all DNS records regularly to identify dangling CNAME/A records pointing to external services
- Implement a DNS hygiene process: remove DNS records when deprovisioning external services
- For Shopify and similar hosted platforms, verify ownership and maintain active claims on all branded subdomains
- Use DNSSEC and monitoring tools to detect unauthorized changes to DNS records
- Maintain an inventory of all external services and their corresponding DNS entries
- Implement certificate monitoring to detect when subdomains are claimed by unauthorized parties
- Consider using subdomain takeover prevention services that monitor for common vulnerable configurations

## Variant hunting
Scan all subdomains of the organization for CNAME records pointing to Heroku, GitHub Pages, Azure, AWS, or other PaaS providers
Check for A records pointing to IP addresses of deprecated services that may be reassigned
Look for MX records pointing to abandoned mail providers or services
Identify subdomains with CNAME records that resolve but the target service shows default/unclaimed pages
Search for historical DNS records using DNS databases to find removed services that may have left dangling records
Test other subdomains of exchangemarketplace.com for similar Shopify takeover opportunities

## MITRE ATT&CK
- T1583.001
- T1584.001
- T1589.001
- T1190

## Notes
This is a classic dangling DNS record vulnerability. The PoC is minimal, but the impact is significant—subdomain takeover can lead to credential theft, malware distribution, and brand reputation damage. The suggested fix is correct but lacks detail on the implementation process. This vulnerability highlights the importance of DNS record lifecycle management during service migrations and deprovisioning.

## Full report
<details><summary>Expand</summary>

Hi ,
 I believe that `exchangemarketplace.com` is belong to shopify it was vulnerable to Subdomain Takeover 
so I takeover it to my shopify store 


>`Poc :` goto
blog.exchangemarketplace.com 


#`Suggested fix :` 
clear your subdomain dns

## Impact

Subdomain Takeover

</details>

---
*Analysed by Claude on 2026-05-24*
