# Subdomain Takeover of datacafe-cert.starbucks.com via Dangling CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 665398 | https://hackerone.com/reports/665398
- **Submitted:** 2019-08-01
- **Reporter:** parzel
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain datacafe-cert.starbucks.com contained a CNAME record pointing to an unclaimed Azure Web App (s00397nasv101-datacafe-cert.azurewebsites.net). An attacker registered the Azure service and gained full control over the subdomain, enabling arbitrary content delivery including XSS, phishing, and session hijacking attacks. The researcher responsibly released the Azure resource after demonstrating the vulnerability.

## Attack scenario
1. Attacker discovers dangling CNAME record for datacafe-cert.starbucks.com pointing to s00397nasv101-datacafe-cert.azurewebsites.net
2. Attacker verifies the Azure Web App is unclaimed and available for registration
3. Attacker registers/claims the Azure Web App with the matching subdomain name
4. Attacker deploys malicious content (XSS payload, phishing page, credential stealer) to the Azure service
5. Legitimate users accessing datacafe-cert.starbucks.com are served attacker-controlled content
6. Attacker performs session hijacking, credential theft, or malware distribution through the compromised subdomain

## Root cause
DNS CNAME record was not cleaned up after deprovisioning the associated Azure Web App, creating a dangling pointer that any user could claim. Lack of DNS hygiene and monitoring for orphaned cloud resources.

## Attacker mindset
An opportunistic attacker scanning for dangling DNS records in high-value domains. The low effort required (simple DNS lookup, Azure registration) combined with high reward (full subdomain control of major brand) makes this an attractive target. The attacker could leverage the subdomain for phishing (especially given the 'cert' naming suggests certificate/authentication context), stealing Starbucks user credentials, or distributing malware.

## Defensive takeaways
- Implement DNS monitoring and alerting for dangling CNAME/NS records pointing to cloud providers
- Establish DNS cleanup procedures when deprovisioning cloud resources, including verification of record removal
- Maintain comprehensive inventory of all DNS records and their corresponding cloud resources
- Regularly audit DNS configurations for orphaned or unclaimed cloud service pointers
- Consider implementing CNAME constraints or CNAME cloaking to reduce takeover surface
- Reserve/claim unclaimed subdomains on cloud platforms when identifying them during security reviews
- Use domain lock/protection mechanisms on cloud provider accounts to prevent unauthorized resource registration

## Variant hunting
Scan other Starbucks subdomains for dangling CNAME records pointing to Azure, AWS S3, GitHub Pages, Heroku, etc.
Look for NXDOMAIN responses followed by successful registration on cloud platforms
Check for similar patterns across retail/hospitality industry domains
Search for unclaimed cloud resources with company-specific naming patterns in DNS
Investigate subdomains with 'cert', 'internal', 'dev', 'staging' prefixes that may be forgotten

## MITRE ATT&CK
- T1190
- T1566.002
- T1589
- T1598

## Notes
This is a classic subdomain takeover via dangling DNS pointer. The researcher demonstrated responsible disclosure by registering the resource, proving impact, and then releasing it. The 'cert' in the subdomain name suggests it may have handled certificate-related operations, potentially increasing impact for phishing or man-in-the-middle attacks. Azure Web Apps are common targets for this vulnerability due to the predictable naming format (*.azurewebsites.net). Report ID 665398 indicates this was a known issue class at the time of reporting.

## Full report
<details><summary>Expand</summary>

**Summary:**
The subdomain datacafe-cert.starbucks.com had an CNAME record pointing to an unclaimed Azure webservice. This is a high severity security issue because an attacker can register the subdomain on Azure and therefore can own the subdomain datacafe-cert.starbucks.com.

**Description:**
The dangling CNAME record of datacafe-cert.starbucks.com is pointing to s00397nasv101-datacafe-cert.azurewebsites.net which was not claimed by you. I registered a service with this name and therefore was able to takeover the subdomain. Every attacker doing this has afterwords full control over the contents served on this subdomain.

**Platform(s) Affected:** 
http://datacafe-cert.starbucks.com/
https://datacafe-cert.starbucks.com/

## Supporting Material/References:
view-source:http://datacafe-cert.starbucks.com/

## How can the system be exploited with this bug?
The full domain can be taken over. Arbitrary content can be served under it.

## How did you come across this bug ?
I noticed the dangling CNAME record of datacafe-cert.starbucks.com.

## Recommendations for fix
1) Remove the dangling CNAME record from datacafe-cert.starbucks.com
2) I release s00397nasv101-datacafe-cert.azurewebsites.net
3) You can reclaim it if you want

## Impact

This issue can be exploited in several ways, for example but not limited to: XSS, Phishing, Session Hijacking due to bypassing of SOP

</details>

---
*Analysed by Claude on 2026-05-24*
