# Subdomain Takeover at api.legalrobot.com via Unclaimed Modulus.io Application

## Metadata
- **Source:** HackerOne
- **Report:** 148770 | https://hackerone.com/reports/148770
- **Submitted:** 2016-07-01
- **Reporter:** fransrosen
- **Program:** Legal Robot
- **Bounty:** Not accepted/No reward requested
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Third-party Service Hijacking
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain api.legalrobot.com was pointed to Modulus.io hosting platform but no application was deployed there, allowing an attacker to claim the domain by registering a new Modulus account and deploying an arbitrary application. The attacker successfully registered a wildcard domain *.legalrobot.com on Modulus.io, redirecting all unclaimed subdomains to their controlled application while leveraging the legitimate SSL certificate.

## Attack scenario
1. Attacker discovers api.legalrobot.com returns 'NO APPLICATION WAS FOUND' error from Modulus.io, indicating a dangling DNS record
2. Attacker creates a new account on Modulus.io hosting platform
3. Attacker attempts to add api.legalrobot.com but discovers it's already reserved; instead registers wildcard domain *.legalrobot.com
4. Modulus.io accepts the wildcard domain registration and provisions it with attacker's application
5. Attacker's application now receives all traffic intended for legalrobot.com subdomains, served over valid SSL
6. Attacker can now phish users, steal credentials, distribute malware, or intercept sensitive communications intended for legalrobot.com services

## Root cause
Legal Robot pointed DNS records to Modulus.io for subdomains without maintaining an active application deployment. The subdomain remained in DNS but no application was running, creating a dangling DNS record. Modulus.io's platform allowed registration of wildcard domains without verification of domain ownership by the registrant.

## Attacker mindset
Opportunistic reconnaissance revealing infrastructure misconfigurations. Attacker identified an unclaimed third-party hosting service integration and exploited the gap between DNS configuration and active deployment to claim the wildcard. The approach was methodical: identify the service provider, create an account, bypass specific domain reservation by using wildcard, and demonstrate control with visible proof-of-concept.

## Defensive takeaways
- Audit all DNS records pointing to third-party services (CDNs, hosting platforms, email providers) to ensure active applications exist
- Implement automated monitoring for dangling DNS records and unclaimed third-party service integrations
- Remove or decommission DNS records immediately when discontinuing use of third-party services
- Claim all wildcard domains defensively if planning to use subdomains with external services
- Use CNAME records instead of A records where possible to reduce takeover surface area
- Establish DNS record inventory and lifecycle management process
- Monitor Modulus.io (and similar platforms) for unauthorized domain registrations matching your domains
- Implement content security policies and subresource integrity checks to mitigate impact of compromised subdomains

## Variant hunting
Search for all subdomains in DNS records (cert transparency, Zone file data, passive reconnaissance) and verify each resolves to active services
Identify patterns of dangling DNS records across target: check for multiple unclaimed subdomains on various platforms
Investigate other Modulus.io integrations and third-party services (Heroku, AWS, Azure, Netlify, Firebase) with similar claim-by-registration models
Review CNAME records pointing to service providers with weak domain ownership validation
Check for expired SSL certificates on unclaimed subdomains that might indicate abandoned integrations
Hunt for similar misconfigurations across organization's subsidiaries and acquired companies

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.1 - Acquire Infrastructure: Domains
- T1589.1 - Gather Victim Identity Information: Credentials
- T1598.3 - Phishing: Spearphishing Link
- T1566.2 - Phishing: Phishing - Spearphishing Attachment

## Notes
Researcher demonstrated responsible disclosure by creating proof-of-concept with identifying comment in HTML and offering to remove the wildcard registration. This is a classic subdomain takeover vulnerability exploiting the gap between DNS delegation and active service deployment. The use of wildcard domain was critical to bypass single-domain reservation. Modulus.io's lack of domain ownership verification enabled the attack. Similar vulnerabilities are likely widespread, prompting researcher to implement automated detection in their scanner.

## Full report
<details><summary>Expand</summary>

Hi,

I noticed that the following domain: api.legalrobot.com was returning the following information:

```
NO APPLICATION WAS FOUND FOR
api.legalrobot.com
```
{F102881}

from Modulus.io. The problem with this is that this tends to be pretty bad depending on the service you use.

In this case, what I did was to create a new account on Modulus, and saw the following setup when I created my own application:
{F102879}

I tried adding the specific domain, but it said it was already added somewhere. The problem was that I then tried with the wildcard: `*.legalrobot.com`, and that actually worked:
{F102878}

Which also made the page resolve my app:
{F102877}

You should not point subdomains to services you do not use (yet). Since I have claimed the wildcard `*.legalrobot.com` now (just for PoC of course), let me know if I should remove this, so you could claim the wildcard yourself, which would probably prevent you completely from risking that subdomains will be taken over.

PoC-link:
https://api.legalrobot.com/
I've just made a simple `Hello World!` but look in the HTML-source for a reference to me:
```
$ curl https://api.legalrobot.com
Hello World!<!--FRANS ROSEN-->
```

Also, please note that Modulus will actually resolve the domain serving SSL, which is a really bad thing.
 
You should remove the DNS post, or let me know if I should remove the wildcard-domain so you could claim it in this service. Let me know if you need additional information.

Also, we'll add this into the scanner during next week since we've seen a couple of clients being affected by this. You do not need to reward me anything as you could see this as a form of premium service or whatnot.. :)

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-24*
