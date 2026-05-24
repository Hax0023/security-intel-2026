# Domain Takeover at 3hopify.media

## Metadata
- **Source:** HackerOne
- **Report:** 1344982 | https://hackerone.com/reports/1344982
- **Submitted:** 2021-09-20
- **Reporter:** m7mdharoun
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Domain Takeover, Subdomain Takeover, DNS Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A researcher discovered that the domain 3hopify.media, believed to be associated with Shopify, was vulnerable to domain takeover through misconfigured DNS or service settings. The attacker was able to take control of the domain, creating potential for phishing, scams, and brand impersonation attacks against Shopify users.

## Attack scenario
1. Attacker identifies 3hopify.media as a Shopify-associated domain through reconnaissance
2. Attacker discovers the domain has dangling DNS records or points to a service with unclaimed namespace
3. Attacker registers or claims the available service namespace that the domain points to
4. Attacker gains full control over domain resolution and content serving
5. Attacker sets up phishing pages or malicious content impersonating Shopify services
6. Users visiting the domain are redirected to attacker-controlled infrastructure for credential harvesting or scams

## Root cause
The domain was likely pointed to a third-party service (possibly a subdomain hosting service, CDN, or application platform) that allowed unclaimed namespace claims. The domain's DNS records were not properly cleaned up or the service endpoint was not claimed by Shopify, leaving it vulnerable to takeover by external actors.

## Attacker mindset
Opportunistic attacker leveraging domain enumeration to find forgotten or improperly managed properties. The attacker seeks to abuse the Shopify brand trust for phishing, fraud, and user scams with minimal effort.

## Defensive takeaways
- Implement DNS audit processes to identify and reclaim all company domains and subdomains
- Monitor for dangling DNS records pointing to unclaimed third-party services
- Establish a domain lifecycle management policy to ensure timely claims on all service platforms
- Use CNAME monitoring and alerting to detect when domains point to unreachable or unowned services
- Maintain an inventory of all domains owned or used by the organization and verify active claims quarterly
- Implement DNSSEC to prevent DNS hijacking attacks
- Use domain takeover detection services that continuously scan for vulnerable configurations

## Variant hunting
Search for other Shopify subdomains with similar naming patterns (hopify, shopify variants)
Check for other .media or alternative TLD registrations of company-related domains
Scan DNS records for CNAME or NS records pointing to orphaned services
Identify other domains pointing to the same unclaimed service namespace
Test for other third-party service integrations that may have similar misconfiguration patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
The report is minimal and lacks technical details about the specific takeover method. The researcher did not provide clear evidence of the takeover mechanism (DNS, service platform, etc.). This report likely received significant bounty due to the critical impact on a major e-commerce platform's reputation and the immediate phishing/fraud risk to customers.

## Full report
<details><summary>Expand</summary>

Hi,
I believe that `3hopify.media` is belong to your company Shopify. 

{F1454834}

I able to takeover this domain by Your Service .



# `Poc :`
Please visit https://3hopify.media or https://www.3hopify.media

## Impact

Scam Users .. etc

</details>

---
*Analysed by Claude on 2026-05-24*
