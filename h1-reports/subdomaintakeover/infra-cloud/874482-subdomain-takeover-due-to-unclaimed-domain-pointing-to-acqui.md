# Subdomain Takeover due to Unclaimed Domain Pointing to Acquia Cloud

## Metadata
- **Source:** HackerOne
- **Report:** 874482 | https://hackerone.com/reports/874482
- **Submitted:** 2020-05-14
- **Reporter:** kumarp16
- **Program:** MyOmnipod
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A DNS record for qa.myomnipod.com points to Acquia Cloud infrastructure but the domain was never claimed or configured within the Acquia management console. An attacker could claim this unclaimed domain through Acquia and serve arbitrary content, impersonating the organization.

## Attack scenario
1. Attacker enumerates subdomains and discovers qa.myomnipod.com
2. Attacker visits the subdomain and observes Acquia Cloud 'Web Site Not Found' error indicating the domain is unclaimed
3. Attacker creates an Acquia Cloud account and registers the unclaimed qa.myomnipod.com domain through Acquia's management console
4. Attacker gains ability to host arbitrary content at qa.myomnipod.com, potentially serving malware, phishing pages, or stealing credentials
5. Users and systems trusting the myomnipod.com domain may interact with attacker-controlled content on the subdomain
6. Attack remains difficult to trace as the attacker operates through a legitimate third-party service

## Root cause
Organization created DNS CNAME/A record pointing to Acquia Cloud infrastructure for qa.myomnipod.com but failed to claim and configure the domain within Acquia's management console. The subdomain was abandoned without proper cleanup or ownership verification.

## Attacker mindset
Reconnaissance and enumeration to identify forgotten infrastructure; opportunistic takeover of misconfigured third-party service pointers; leveraging legitimate SaaS platforms to bypass domain verification and establish credibility for phishing/malware campaigns.

## Defensive takeaways
- Maintain inventory of all DNS records and their corresponding third-party services
- Implement regular DNS hygiene audits to identify and remove dangling records
- Claim and configure all subdomains in third-party services immediately after DNS creation
- Monitor for unclaimed subdomains through continuous security scanning
- Implement CNAME validation and enforcement policies before allowing DNS changes
- Set up alerts for subdomain enumeration results showing third-party service errors
- Document all third-party service integrations and establish ownership verification processes
- Periodically verify that all configured third-party domains remain active and claimed

## Variant hunting
Search for other subdomains (staging, dev, test, api, mail) pointing to Acquia or other SaaS platforms
Check for similar patterns with Heroku, GitHub Pages, Shopify, Azure, AWS CloudFront, and other common hosting platforms
Identify subdomains with generic Acquia error messages across the organization's domain namespace
Use certificate transparency logs to find all subdomains and cross-reference with DNS records
Scan for CNAME records pointing to Acquia infrastructure that lack corresponding subdomain claims

## MITRE ATT&CK
- T1583.001
- T1566.002
- T1589.001

## Notes
This is a classic subdomain takeover vulnerability (CWE-404: Improper Resource Validation). The researcher responsibly disclosed without claiming the domain due to resource constraints. Acquia's error message explicitly states the requirement to claim domains through their console, making detection straightforward for attackers. Organizations should treat all DNS CNAME/A records as security-critical assets requiring lifecycle management.

## Full report
<details><summary>Expand</summary>

ssue Details

The consultant identified that subdomain http:// or https://qa.myomnipod.com 

Web Site Not Found

Sorry, we could not find any content for this web address. Please check the URL.

If you are an Acquia Cloud customer and expect to see your site at this address, you'll need to add this domain name to your site via the Acquia Network management console.

Error Is displayed.

How did you come across this bug ?

Using enumeration, I was able to discover this domain and determined it

NOTE: The hostname was not claimed by me also because i need to pay certain amount to host a website.

## Impact

Sub-domain take over attacks can happen when a company creates a dns entry that points to a third party service, however forgets about the third party application leaving it vulnerable to be hijacked by another party. Hackers can claim subdomains with the help of external services. This attack is practically non-traceable.

</details>

---
*Analysed by Claude on 2026-05-24*
