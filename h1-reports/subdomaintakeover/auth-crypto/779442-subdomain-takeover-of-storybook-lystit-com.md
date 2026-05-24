# Subdomain Takeover of storybook.lystit.com via Dangling CNAME to Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 779442 | https://hackerone.com/reports/779442
- **Submitted:** 2020-01-21
- **Reporter:** parzel
- **Program:** Lyst (assumed from domain lystit.com)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Unrestricted S3 Bucket Registration, Cross-Site Scripting (XSS), Same-Origin Policy Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain storybook.lystit.com contained a dangling CNAME record pointing to an unclaimed AWS S3 bucket. An attacker could register the S3 bucket with the same name and enable static website hosting to fully takeover the subdomain, enabling arbitrary content injection including XSS payloads.

## Attack scenario
1. Researcher discovers storybook.lystit.com CNAME record points to a non-existent S3 bucket endpoint
2. Attacker enumerates DNS records and identifies the target S3 bucket name from the dangling CNAME
3. Attacker creates AWS S3 bucket with identical name (storybook.lystit.com)
4. Attacker enables static website hosting on the S3 bucket
5. Attacker uploads malicious HTML/JavaScript files to serve XSS payloads through the legitimate subdomain
6. Victims visiting storybook.lystit.com execute attacker-controlled scripts, potentially bypassing SOP protections for sibling domains

## Root cause
Organization failed to clean up dangling DNS CNAME records after decommissioning or migrating the S3 bucket infrastructure, leaving the subdomain vulnerable to registration by third parties

## Attacker mindset
Systematic reconnaissance of DNS infrastructure to identify takeover opportunities; recognition that unclaimed cloud resources create high-impact attack surface; understanding that subdomain control enables attacks on parent domain trust boundaries

## Defensive takeaways
- Implement DNS hygiene practices: regularly audit and remove dangling CNAME records during service decommissioning
- Maintain inventory of all DNS records and cloud resources with cross-reference validation
- Implement preventive controls on cloud provider side (e.g., S3 bucket ownership verification, DNS CNAME validation)
- Monitor for suspicious DNS resolution patterns or unclaimed resource registrations
- Use certificate-based subdomain validation to prevent unauthorized HTTPS hosting
- Implement Content Security Policy (CSP) headers on parent domain to limit impact of subdomain compromise
- Regular security scanning for dangling DNS records using automated tools

## Variant hunting
Search for other dangling CNAME records across the organization's DNS infrastructure pointing to: unclaimed CloudFront distributions, unused Heroku apps, abandoned GitHub Pages deployments, deregistered Firebase projects, unused Azure App Service endpoints, and expired third-party service integrations

## MITRE ATT&CK
- T1190
- T1584.001
- T1583.001
- T1598.002

## Notes
This is a classic subdomain takeover vulnerability with clear business impact. The researcher provided working POC including XSS demonstration. The fix is straightforward (remove CNAME record) but the discovery highlights the importance of DNS cleanup during infrastructure changes. S3 bucket naming conflicts are particularly dangerous because S3 bucket namespaces are global across all AWS accounts.

## Full report
<details><summary>Expand</summary>

# Summary:
The subdomain storybook.lystit.com had an CNAME record pointing to an unclaimed S3 bucket. This is a high severity security issue because an attacker can register the bucket on AWS and therefore can serve her own content on the subdomain. This allows for various attacks.

# Description:
The dangling CNAME record of storybook.lystit.com is pointing to ███████ and the bucket which could not be found was: "storybook.lystit.com". I was able to register a S3 bucket with this name in AWS. After enabling static website hosting I was able to takeover the subdomain and serve arbitrary content. I am serving a POC to proof I am controlling the subdomain as well as a simple XSS POC.

# POC
POC: view-source:http://storybook.lystit.com/
Stored XSS: http://storybook.lystit.com/asdjklkas1312das879123.html
{F691531}
{F691530}

# Supporting Material/References:
https://www.hackerone.com/blog/Guide-Subdomain-Takeovers

# Recommendations for fix
Remove the dangling CNAME record from storybook.lystit.com

## Impact

The domain takeover allows various attacks. As the full domain is attacker controlled it can be used to serve XSS attacks, phishing campaigns and might be used to bypass the Same Origin Policy on other lystit.com domains and services.

</details>

---
*Analysed by Claude on 2026-05-24*
