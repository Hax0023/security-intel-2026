# Subdomain Takeover via Unclaimed Piwik Cloud Subdomain

## Metadata
- **Source:** HackerOne
- **Report:** 111078 | https://hackerone.com/reports/111078
- **Submitted:** 2016-01-16
- **Reporter:** ketan_patil
- **Program:** Piwik
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Insufficient Access Control, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An unclaimed subdomain (gratipay.piwik.pro) was available for registration and takeover through Piwik Cloud's signup process without proper ownership verification. An attacker could register this subdomain and associate it with their account, potentially gaining access to services or data intended for the legitimate gratipay.com organization.

## Attack scenario
1. Attacker identifies unclaimed subdomain gratipay.piwik.pro hosted on Piwik Cloud infrastructure
2. Attacker visits the subdomain and observes message indicating it is available for registration
3. Attacker navigates to piwik.pro/cloud and completes signup process with arbitrary credentials
4. Attacker enters 'gratipay.com' as the subdomain during account setup without verification
5. Piwik Cloud provisions the subdomain to attacker's account without validating ownership of gratipay.com
6. Attacker gains control of gratipay.piwik.pro and can host content, intercept traffic, or perform phishing attacks

## Root cause
Piwik Cloud failed to implement proper domain ownership verification before allowing users to claim subdomains during signup. The system did not validate that the user requesting a subdomain has legitimate ownership rights to the associated base domain (gratipay.com).

## Attacker mindset
Opportunistic attacker scanning for available subdomains on cloud platforms, recognizing that unclaimed subdomains often represent security gaps where takeover is possible. The attacker systematically tests whether registration controls exist by attempting to claim the subdomain through normal signup flow.

## Defensive takeaways
- Implement mandatory domain ownership verification before subdomain allocation (DNS TXT record, CNAME, or email validation)
- Maintain accurate DNS records and monitor for dangling DNS pointers that reference unowned resources
- Require proof of ownership (e.g., DNS record creation, email verification from domain contact) before provisioning customer subdomains
- Implement rate limiting and automated monitoring to detect bulk subdomain registration attempts
- Conduct regular audits of all allocated subdomains to identify orphaned or unclaimed entries
- Use CNAME flattening or ALIAS records carefully to prevent intermediate subdomain exposure
- Implement Content Security Policy (CSP) and other headers to mitigate impact if subdomain is compromised

## Variant hunting
Search for similar cloud service platforms (AWS, Azure, Heroku, etc.) that allocate customer subdomains without verification. Look for other Piwik Cloud subdomains that may be unregistered. Check for DNS records pointing to Piwik infrastructure that lack corresponding active accounts. Investigate other SaaS platforms offering branded subdomains to identify similar control gaps.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1584 - Compromise Infrastructure
- T1583 - Acquire Infrastructure

## Notes
This is a classic subdomain takeover vulnerability affecting multi-tenant cloud platforms. The reporter provided clear reproduction steps but minimal technical detail. The vulnerability allows account takeover of the Piwik Cloud service associated with gratipay, not necessarily takeover of gratipay.com itself, though the subdomain could be abused for credential harvesting or phishing against gratipay users. The report demonstrates the importance of verification controls in multi-tenant SaaS environments where customers claim branded subdomains.

## Full report
<details><summary>Expand</summary>

Dear Team,

I find bug in https://gratipay.piwik.pro/ i can take over account https://gratipay.piwik.pro/
I share with you  setup 

1) https://gratipay.piwik.pro/
2) Then i see msg like this  ( "THIS SUBDOMAIN IS AVAILABLE!
gratipay.piwik.pro is available! Use this subdomain for your Piwik Cloud service. To activate this subdomain, simply sign up to Piwik Cloud. ") 
3)Then i open  http://piwik.pro/cloud
4)  Put user name ans password 
5) gratipay.com add  in my account 

I share with you POC for your more information 

Thank you 

</details>

---
*Analysed by Claude on 2026-05-24*
