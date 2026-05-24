# Subdomain Takeover via Dangling Heroku DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 221133 | https://hackerone.com/reports/221133
- **Submitted:** 2017-04-15
- **Reporter:** b3nac
- **Program:** Gratipay
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Improper Resource Deallocation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Gratipay's subdomain www.gratipay.com.herokudns.com pointed to Heroku infrastructure but had no corresponding application deployed, allowing an attacker to claim the domain and host arbitrary content. The dangling DNS CNAME record created a classic subdomain takeover vulnerability where an unclaimed third-party service could be registered by an attacker.

## Attack scenario
1. Attacker discovers that www.gratipay.com.herokudns.com resolves to Heroku infrastructure
2. Attacker verifies no active Heroku application is associated with this domain
3. Attacker creates a Heroku account and registers the vulnerable subdomain via 'heroku domains:add' command
4. Attacker deploys malicious application to their Heroku account
5. Attacker refreshes the subdomain and confirms their malicious content is now served
6. Attacker can perform phishing, malware distribution, or other attacks using the legitimate Gratipay domain

## Root cause
Organization failed to clean up or remove DNS records pointing to third-party services (Heroku) after decommissioning the associated application, leaving a dangling CNAME record that could be claimed by an attacker with a legitimate account on that service.

## Attacker mindset
Opportunistic reconnaissance - attacker systematically scanned organization's DNS records, identified unused third-party service pointers, and exploited the low barrier to claim unregistered domains on public cloud platforms. Low effort, high impact attack requiring only a valid account on the target service.

## Defensive takeaways
- Maintain inventory of all DNS records and regularly audit for dangling or unused entries
- Implement automated monitoring to detect DNS CNAME records pointing to unclaimed services
- Establish decommissioning procedures that explicitly remove DNS records when retiring third-party service integrations
- Use DNS validation and verification to ensure domains are actively in use before pointing to external services
- Monitor third-party service provider announcements for subdomain takeover vulnerabilities in their services
- Implement CAA (Certification Authority Authorization) records to restrict certificate issuance for critical domains

## Variant hunting
Scan organization's DNS records for CNAME entries to other hosting providers (AWS, Azure, GitHub Pages, etc.)
Test GitHub Pages takeover by checking if org.github.io resolves but has no repository
Identify subdomains with S3 bucket CNAME records (*.s3.amazonaws.com) that may point to deleted buckets
Look for CNAME records pointing to CDN services (Cloudflare, Akamai) without active configurations
Search for dangling DNS records pointing to Firebase, Vercel, Netlify, or other popular deployment platforms
Check for subdomain CNAME records to abandoned Zendesk, Auth0, or other service provider instances

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1583.008 - Acquire Infrastructure: Malware
- T1589.001 - Gather Victim Org Info: Credentials
- T1598 - Phishing: Spearphishing Link
- T1608.004 - Stage Capabilities: Drive-by Target

## Notes
This is a classic and straightforward subdomain takeover vulnerability. The attack required no exploitation of Heroku itself - only that Heroku allows users to add domains to their accounts. The vulnerability existed purely due to organizational hygiene failure in DNS management. Similar to the well-documented cases of GitHub Pages and Heroku subdomain takeovers. The proof-of-concept was simple and effective, demonstrating the risk clearly.

## Full report
<details><summary>Expand</summary>

# One of Gratipay's sub domains points to Heroku with no app created.

## Description

Gratipay's sub domain http://www.gratipay.com.herokudns.com/ points to Heroku but is not in use. 

## Steps To Reproduce

###Details

 - Upon realization of vulnerability, installed and created a Heroku dependencies and application.

 - Added http://www.gratipay.com.herokudns.com/ to my list of domains through Heroku CLI. 

heroku domains:add www.gratipay.com.herokudns.com

After verifying my Heroku account this was easy to point the sub domain to my application. 

- Uploaded my application with text "B3nac sub domain takeover POC." and refreshed the domain to find it pointed to my application successfully.  
  
## Fix

If the domain is not in use, then it is recommended to point the dns entry away from the third party program.

## Supporting Material/References:

  * I've attached the uploaded takeover python application/website screenshot.

</details>

---
*Analysed by Claude on 2026-05-24*
