# Domain Takeover via Fastly Subdomain - CSP Bypass at gl-canary.freetls.fastly.net

## Metadata
- **Source:** HackerOne
- **Report:** 716677 | https://hackerone.com/reports/716677
- **Submitted:** 2019-10-17
- **Reporter:** mike12
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Content Security Policy Bypass, Insecure Third-Party Dependency
- **CVEs:** None
- **Category:** auth-crypto

## Summary
GitLab whitelisted the Fastly subdomain gl-canary.freetls.fastly.net in its Content Security Policy for script, style, connect, and worker sources. Any attacker can register a Fastly account, create a service, and claim this subdomain to bypass CSP restrictions and inject malicious scripts into gitlab.com. This allows XSS attacks against GitLab users despite CSP protections.

## Attack scenario
1. Attacker registers a free Fastly account at fastly.com/signup
2. Attacker navigates to Fastly's service management console and creates a new service
3. Attacker specifies gl-canary.global.ssl.fastly.net as the domain, which automatically maps to gl-canary.freetls.fastly.net
4. Attacker configures the Fastly service to serve malicious JavaScript content
5. When a GitLab user visits gitlab.com, the CSP policy allows loading scripts from gl-canary.freetls.fastly.net without restriction
6. If GitLab has an XSS vulnerability, attacker's malicious script executes with full context of gitlab.com, stealing session tokens or performing unauthorized actions

## Root cause
GitLab whitelisted a shared Fastly subdomain in CSP without ensuring exclusive control or DNS ownership verification. Fastly's free TLS service allows any account holder to claim subdomains matching the pattern *.freetls.fastly.net, creating a shared namespace vulnerability. CSP whitelisting assumes domain ownership cannot be disputed.

## Attacker mindset
An opportunistic attacker discovers that a high-value target (GitLab) trusts a shared infrastructure domain. By exploiting Fastly's permissive service creation process, they can claim the whitelisted subdomain with minimal effort and inject malicious content at scale, affecting all GitLab users simultaneously.

## Defensive takeaways
- Never whitelist shared infrastructure domains (CDN, hosting provider generics) in CSP; instead use company-owned domains
- When using third-party infrastructure, ensure exclusive subdomain ownership through DNS CNAME verification or dedicated subdomains
- Regularly audit CSP policies for potential subdomain takeover risks, particularly connect-src, script-src, and style-src directives
- Use nonce-based or hash-based CSP instead of domain whitelisting where possible to reduce surface area
- Implement monitoring to detect unexpected content served from whitelisted domains
- Establish relationship agreements with CDN providers to prevent subdomain reuse or require reservation mechanisms

## Variant hunting
Scan other high-value domains' CSP policies for whitelisted Fastly subdomains (*.freetls.fastly.net, *.fastly.net)
Check for CloudFront, Akamai, or other CDN default subdomains in CSP policies across different organizations
Search for GitHub Pages (*.github.io) whitelisting in CSP, which has similar takeover potential
Look for Heroku, Vercel, or other Platform-as-a-Service default domains in CSP directives
Test if other Fastly subdomains (not just freetls) are claimable by examining Fastly's service creation workflow
Investigate whether whitelisted domains appear in other security headers (CORS, etc.)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (CSP bypass via subdomain takeover)
- T1589 - Gather Victim Identity Information (domain enumeration)
- T1598 - Phishing - Spearphishing Link (delivery mechanism for malicious CSP-bypassed content)
- T1657 - Financial Theft (session hijacking via CSP bypass)

## Notes
This is a critical supply-chain/third-party risk vulnerability. The attack requires no authentication and affects all users simultaneously. The vulnerability persists because CSP policy changes lag behind infrastructure risks. Similar issues have affected AWS S3, GitHub Pages, and Heroku subdomains. Report appears to lack explicit bounty confirmation, suggesting either policy or triage delays.

## Full report
<details><summary>Expand</summary>

Hello Gitlab!

The domain `gl-canary.freetls.fastly.net` is whitelisted in gitlab.com Content Security Policy. See `Content-Security-Policy` HTTP header from gitlab.com:

```
Content-Security-Policy: connect-src 'self' https://assets.gitlab-static.net https://gl-canary.freetls.fastly.net wss://gitlab.com https://sentry.gitlab.net https://customers.gitlab.com https://snowplow.trx.gitlab.net; frame-ancestors 'self'; frame-src 'self' https://www.google.com/recaptcha/ https://www.recaptcha.net/ https://content.googleapis.com https://content-compute.googleapis.com https://content-cloudbilling.googleapis.com https://content-cloudresourcemanager.googleapis.com https://*.codesandbox.io; img-src * data: blob:; object-src 'none'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://assets.gitlab-static.net https://gl-canary.freetls.fastly.net https://www.google.com/recaptcha/ https://www.recaptcha.net/ https://www.gstatic.com/recaptcha/ https://apis.google.com 'nonce-bjSllX/7AnVrXL1QQxsb+w=='; style-src 'self' 'unsafe-inline' https://assets.gitlab-static.net https://gl-canary.freetls.fastly.net; worker-src https://assets.gitlab-static.net https://gl-canary.freetls.fastly.net https://gitlab.com blob:
```

This domain can be controlled from any fastly.com account:
1. Register at https://www.fastly.com/signup
2. Go to https://manage.fastly.com/services/all
3. Create a new service 
4. Use `gl-canary.global.ssl.fastly.net` as domain. (Fastly automatically creates <name>.freetls.fastly.net. See https://docs.fastly.com/en/guides/setting-up-free-tls#support-for-http2-ipv6-and-tls-12)
5. Configure hosts

## Impact

An attacker can use the domain to bypass the CSP and execute malicious client-side code (for example, the client application may have an XSS vulnerability).
The domain could potentially be used elsewhere in Gitlab application (CDN, for example).

</details>

---
*Analysed by Claude on 2026-05-24*
