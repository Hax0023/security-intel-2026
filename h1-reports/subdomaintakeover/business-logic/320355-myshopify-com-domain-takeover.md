# myshopify.com Domain Takeover Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 320355 | https://hackerone.com/reports/320355
- **Submitted:** 2018-02-27
- **Reporter:** 0xacb
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Domain Takeover, Subdomain Hijacking, Insufficient Domain Verification
- **CVEs:** None
- **Category:** business-logic

## Summary
A security researcher discovered a domain takeover vulnerability in Shopify's myshopify.com domain management system during black box testing of their website. The vulnerability allowed adding unverified domains to a Shopify store, potentially enabling subdomain hijacking attacks. The exact exploitation method was not fully documented by the researcher, but involved bypassing the DNS verification checks.

## Attack scenario
1. Attacker creates a trial Shopify account without proper authorization through the partners program
2. Attacker explores the domain management endpoints and DNS verification tool
3. Attacker discovers insufficient validation in one of the domain submission endpoints
4. Attacker successfully adds unverified domains to their store by circumventing DNS checks
5. Added domains remain in 'Not connected' state but are registered to the attacker's store
6. Attacker could potentially claim or redirect traffic to myshopify.com subdomains owned by other users

## Root cause
The domain verification mechanism in Shopify's domain management system had insufficient validation. The system allowed domain submission through certain endpoints without properly enforcing DNS verification checks, enabling attackers to register domains they did not own or verify.

## Attacker mindset
The researcher demonstrated a methodical black box testing approach, attempting multiple attack vectors (open redirect bypass, RCE via DNS tool, command injection) while probing the domain management endpoints. The researcher was transparent about their testing methodology and willingness to cooperate with the security team.

## Defensive takeaways
- Implement strict domain ownership verification for all domain management endpoints
- Enforce consistent validation logic across all domain submission pathways
- Verify DNS records from authoritative nameservers before allowing domain registration
- Implement rate limiting and monitoring on domain management operations
- Maintain clear security testing guidelines and encourage authorized penetration testing through proper channels
- Log and alert on suspicious domain registration activities
- Implement CSRF tokens and additional authentication checks for sensitive domain operations

## Variant hunting
Check for similar domain verification bypass in other Shopify services (shopify.com stores, apps)
Test alternate endpoints that might accept domain submissions with different validation logic
Attempt to register domains belonging to other users or known brand names
Test wildcard domain registration attempts
Probe for race conditions in domain verification timing windows
Examine API endpoints for domain management that might bypass web UI protections
Test subdomain takeover on other Shopify-owned domains and services

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains

## Notes
The researcher did not provide detailed exploitation steps or proof of concept, stating they did not save their Burp session. The vulnerability was discovered by Shopify's security team through activity log inspection rather than being fully documented by the researcher. The report demonstrates responsible disclosure despite the researcher initially testing without proper authorization. The exact bypass mechanism remains unclear from this writeup alone.

## Full report
<details><summary>Expand</summary>

Hello Shopify Security Team,

I just received your email and I'm sorry for any inconvenience. Yes, it was me.
Basically, I just tried to audit your website using some black box testing. Unfortunately, I didn't read about those guidelines, such as creating a store on https://partners.shopify.com/ and I created a normal trial account.

I'm glad you found a bug as a result of inspecting my activity logs. And you're right, I didn't notice the bug.

I tried many different things, such as:

- I tried to bypass the open redirect filter, without success: https://www.shopify.com/login?redirect=//acme
- I explored the domain DNS check tool to get RCE without success. I tried to use some command injection techniques, but I didn't receive any requests on my server (█████). I tried to use curl and netcat to perform external requests.
- I think I managed to add domains that were not verified by the DNS tool by submitting them using the last endpoint, but those domains remain "Not connected".

I have all my requests on Burp, but I didn't save the session. As far as I can remember, this was what I tested. I would like to know what was the bug. If possible, I would like to test it further.

Thank you,
André

## Impact

None

</details>

---
*Analysed by Claude on 2026-05-24*
