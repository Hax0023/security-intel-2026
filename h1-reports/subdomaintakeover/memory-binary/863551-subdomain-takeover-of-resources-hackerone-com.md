# Subdomain Takeover of resources.hackerone.com via Unclaimed Uberflip Domain

## Metadata
- **Source:** HackerOne
- **Report:** 863551 | https://hackerone.com/reports/863551
- **Submitted:** 2020-04-30
- **Reporter:** amans
- **Program:** HackerOne
- **Bounty:** $5,071
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain resources.hackerone.com has a CNAME record pointing to read.uberflip.com but is not registered/claimed in any HackerOne-owned Uberflip account. An attacker could register an Uberflip account and claim this unclaimed subdomain to redirect traffic and serve malicious content. This allows arbitrary control over a subdomain under a trusted HackerOne domain.

## Attack scenario
1. Attacker discovers resources.hackerone.com resolves to CNAME read.uberflip.com
2. Attacker verifies the domain returns 'Non-hub domain' error, indicating it's not claimed in any Uberflip account
3. Attacker creates a new Uberflip account with email and credentials
4. Attacker navigates to Uberflip domain configuration settings and adds resources.hackerone.com as a custom domain
5. Uberflip validates the CNAME record points to their infrastructure (which it does) and grants attacker control
6. Attacker can now host content, redirect users, or perform phishing attacks from the trusted HackerOne subdomain

## Root cause
HackerOne configured DNS CNAME for resources.hackerone.com pointing to Uberflip's infrastructure but failed to complete the integration by claiming/registering the domain in a HackerOne-owned Uberflip account. This created a dangling DNS record that any Uberflip user can claim.

## Attacker mindset
An attacker recognizes that resources.hackerone.com is a subdomain of a high-trust security company domain. By claiming the unclaimed Uberflip resource, they gain instant credibility and can redirect users expecting HackerOne content to attacker-controlled Uberflip pages for phishing, malware distribution, or social engineering attacks.

## Defensive takeaways
- Always complete third-party service integrations: claim/register custom domains in the external service immediately after configuring DNS
- Audit all CNAME records quarterly to identify dangling or unclaimed domains pointing to third-party services
- Implement DNS monitoring to alert on resolution errors or unexpected responses from configured subdomains
- Use subdomain takeover scanning tools in CI/CD pipelines to catch misconfigured delegations
- Document ownership of all DNS records and require sign-off before DNS changes propagate to production
- Consider using DNS CAA or similar mechanisms to restrict who can claim your domains on third-party services

## Variant hunting
Scan all HackerOne subdomains for similar dangling CNAME records pointing to Heroku, GitHub Pages, AWS, Shopify, or other popular services
Check for other Uberflip-related subdomains or API endpoints that may have incomplete integrations
Test other security/tech companies' subdomains for similar unclaimed third-party service delegations
Look for subdomains with A/AAAA records pointing to inactive/unavailable IPs that could be IP reassignment takeovers
Search for MX records pointing to unclaimed email service providers that could enable email hijacking

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (via redirects from trusted domain)
- T1190 - Exploit Public-Facing Application (via compromised subdomain)
- T1598.003 - Phishing for Information: Spearphishing Link (credential harvesting)
- T1584.001 - Compromise Infrastructure: Domains (subdomain takeover)

## Notes
This is a classic subdomain takeover vulnerability resulting from incomplete third-party service integration. The researcher responsibly disclosed without attempting to claim the domain themselves. The fix is straightforward: HackerOne must claim the domain in their Uberflip account or remove the CNAME record entirely. The vulnerability likely went unnoticed because the subdomain wasn't actively monitored and returned a benign error message rather than a server controlled by an attacker.

## Full report
<details><summary>Expand</summary>

Hello,

I just went to https://resources.hackerone.com/ and it shows an error "Non-hub domain, The URL you've accessed does not provide a hub. Please check the URL and try again." also i've checked the CNAME is poiting to read.uberflip.com which means if it is not added it can be added to any account, as [Uberflip documentation](https://help.uberflip.com/hc/en-us/articles/360018786372-Custom-Domain-Set-up-Your-Hub-on-a-Subdomain) suggests that after your subdomain is pointing to their CNAME which is read.uberflip.com, your subdomain should be added to your account so it shows the URL you chose for your hub. As i couldn't signup on their website to test due to signup problems, i just wanted your confirmation whether this subdomain is added in uberflip account or not. If not then claim it otherwise any one can add or claim this to their Uberflip account

## Impact

Subdomain takeover.

</details>

---
*Analysed by Claude on 2026-05-24*
