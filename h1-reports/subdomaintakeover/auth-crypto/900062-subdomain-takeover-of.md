# Subdomain Takeover via Unclaimed Azure CDN Profile

## Metadata
- **Source:** HackerOne
- **Report:** 900062 | https://hackerone.com/reports/900062
- **Submitted:** 2020-06-16
- **Reporter:** flavsec_
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A dangling DNS CNAME record pointing to an unclaimed Azure CDN profile allowed an attacker to register a matching CDN profile and claim the subdomain. By creating an Azure Web App and configuring the CDN to use it as an origin, the attacker was able to serve arbitrary content from the target subdomain.

## Attack scenario
1. Attacker performs reconnaissance using DNS enumeration (dig) to identify subdomains and find NXDOMAIN status with dangling CNAME records
2. Attacker identifies that the CNAME record points to an unclaimed Azure CDN endpoint
3. Attacker creates a new Azure CDN Profile with a name matching the dangling CNAME record
4. Attacker provisions an Azure Web App and uploads malicious content (HTML/JavaScript)
5. Attacker configures the CDN profile to use the Web App as its origin and sets the custom domain to the target subdomain
6. Attacker enables SSL/TLS, and the subdomain now resolves to attacker-controlled content, enabling phishing, data theft, or malware distribution

## Root cause
Orphaned DNS CNAME record pointing to a decommissioned or never-claimed Azure CDN profile. The organization failed to either remove the DNS record or permanently claim the corresponding cloud resource, leaving it available for registration by attackers.

## Attacker mindset
Opportunistic reconnaissance-driven attacker leveraging common misconfiguration patterns. The attacker methodically enumerated subdomains, identified the weakness, and leveraged accessible cloud infrastructure to claim the domain without requiring credentials or exploiting complex vulnerabilities.

## Defensive takeaways
- Implement DNS hygiene practices: remove unused DNS records and audit CNAME records for dangling pointers
- Use DNS-level protections: claim or reserve subdomain names in DNS even if not actively used
- Establish cloud resource lifecycle management: track all CDN profiles, Web Apps, and other cloud services with documented ownership
- Monitor for unclaimed subdomains: regularly scan DNS records for NXDOMAIN status or outdated CNAME targets
- Implement certificate pinning or DNSSEC to prevent DNS hijacking attacks
- Use subdomain takeover detection tools and services to proactively identify vulnerable subdomains
- Enforce principle of least privilege: restrict who can create Azure CDN profiles and Web Apps

## Variant hunting
Check for other cloud providers with similar subdomain registration weaknesses (AWS CloudFront, Cloudflare, Akamai)
Scan for GitHub Pages, Heroku, or other PaaS subdomain takeovers via dangling CNAME records
Identify bucket-based takeovers (S3, Azure Blob Storage) where bucket names match subdomain patterns
Look for forgotten or abandoned Azure App Service custom domains that can be reclaimed
Enumerate other Azure resources (Function Apps, Logic Apps) that may have custom domain bindings
Test for mail server takeovers via dangling MX records on similar subdomains

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1598
- T1091

## Notes
This is a classic example of subdomain takeover via dangling DNS records. The vulnerability is prevalent across organizations due to poor DNS management during service decommissioning. Azure CDN profiles specifically are attractive targets because they can be quickly configured to serve attacker content. The report demonstrates that even without any authentication bypass or technical exploit, simple misconfigurations can lead to complete subdomain compromise. The redacted nature of the report suggests the vulnerability was in a significant organization. Similar patterns have been documented in bug bounty databases and should trigger company-wide DNS audits.

## Full report
<details><summary>Expand</summary>

**Summary:**
I was able to claim the subdomain: ████ using Microsoft Azure ( CDN profiles)

**Description:**

## Impact
Platform(s) Affected:
Subdomain
Azure CDN

## Step-by-step Reproduction Instructions

1. Using dig, I was able to determine that the subdomain '███████' was vulnerable to takeover. The record showed status: NXDOMAIN and was pointing to the CNAME: █████.
2. Using this information, I was able to create a new Azure CDN Profile with the name '██████████'. This would resolve to the CNAME record mentioned above.
3. I then created a Web App domain through Azure  where I uploaded a small proof html file through FTP, I then set the CDN's origin type to WebApp and selected the url that I created earlier, this would serve the proof file (█████/proof.html) , Last and final step I set the custom domain to ███████ and enabled ssl.
4. I was then able to view the uploaded site at https://████████/proof.html

## Suggested Mitigation/Remediation Actions
To mitigate this issue you can:

Remove the DNS record from the DNS zone if it is no longer needed.
Claim the domain name in a permanent DNS record so it cannot be used elsewhere.

## Impact

This is extremely vulnerable to attacks as a malicious user could create any web page with any content and host it on the ████ domain. This would allow them to post malicious content which would be mistaken for a valid site. They could steal cookies, bypass domain security, steal sensitive user data, malware distribution, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
