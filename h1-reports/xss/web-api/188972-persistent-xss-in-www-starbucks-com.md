# Persistent XSS via Unregistered Elastic Beanstalk Subdomain

## Metadata
- **Source:** HackerOne
- **Report:** 188972 | https://hackerone.com/reports/188972
- **Submitted:** 2016-12-06
- **Reporter:** ddworken
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS) - Persistent, Subdomain Takeover, Improper Resource Loading
- **CVEs:** None
- **Category:** web-api

## Summary
Starbucks loads JavaScript from an unregistered Elastic Beanstalk subdomain (starbucksmacchiato-prod.elasticbeanstalk.com) on product pages. An attacker could register this domain on AWS Elastic Beanstalk and serve malicious JavaScript, resulting in persistent XSS affecting all users who visit the affected pages. The vulnerability exists because Starbucks references an external dependency that was never properly provisioned or has been deprovisioned.

## Attack scenario
1. Attacker identifies that starbucksmacchiato-prod.elasticbeanstalk.com domain is unregistered by performing DNS lookups
2. Attacker registers the subdomain as an Elastic Beanstalk application with AWS
3. Attacker deploys malicious JavaScript payload to the Elastic Beanstalk environment
4. When users visit https://www.starbucks.com/coffee/espresso/latte-macchiato, the page loads the attacker-controlled script
5. Attacker's JavaScript executes in users' browsers with full context of starbucks.com origin
6. Attacker steals session cookies, payment information, user credentials, or performs actions on behalf of users

## Root cause
Starbucks hardcoded an external Elastic Beanstalk subdomain reference in production code without ensuring domain registration and ownership was secured. The domain appears to have never been registered or was deprovisioned without updating the references. No Content Security Policy or integrity checks (SRI - Subresource Integrity) were implemented to prevent unauthorized script execution.

## Attacker mindset
An opportunistic attacker would perform reconnaissance across target websites for broken or unregistered external dependencies. The low barrier to entry (registering a domain on AWS) combined with high impact (persistent XSS affecting all users) makes this an attractive target. The attacker would monitor for payment data, session tokens, or user PII that could be monetized.

## Defensive takeaways
- Implement Content Security Policy (CSP) with strict script-src directives to whitelist only trusted sources
- Use Subresource Integrity (SRI) hashes for all external JavaScript dependencies to detect tampering
- Audit all hardcoded external domain references and ensure they are properly registered and monitored
- Implement a process to regularly verify that all external dependencies are still under your control
- Use internal CDNs or self-host critical JavaScript dependencies rather than relying on external third-party domains
- Monitor DNS records and implement DNS security (DNSSEC) to prevent subdomain takeovers
- Establish a code review process that flags external domain references for security validation
- Use automated dependency scanning tools to identify broken or dangling external resources

## Variant hunting
Search for other unregistered or abandoned Elastic Beanstalk subdomains across Starbucks properties (mobile apps, payment systems, loyalty programs). Check for similar patterns on competitor websites (coffee chains, QSR brands) that load scripts from unregistered third-party infrastructure. Look for other abandoned AWS resources (S3 buckets, CloudFront distributions) that could be claimed. Scan for hardcoded domain references in JavaScript files that lack CSP/SRI protections.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1583.001 - Acquire Infrastructure - Domains
- T1583.006 - Acquire Infrastructure - Web Services
- T1657 - Financial Theft

## Notes
The researcher demonstrated excellent responsible disclosure practices by identifying the vulnerability without actually exploiting it, explaining the security and ethical concerns (data collection, AWS costs). The vulnerability represents a critical gap in dependency management and highlights the risks of referencing external resources without proper ownership verification. This is a textbook example of subdomain takeover combined with persistent XSS for maximum impact on a high-traffic e-commerce platform.

## Full report
<details><summary>Expand</summary>

There is a persistent XSS in 

```
https://www.starbucks.com/coffee/espresso/latte-macchiato
```

It is caused by loading scripts from: 

```
//starbucksmacchiato-prod.elasticbeanstalk.com/scripts/bn-v1.0.0-Release-min.js
```

Note that ```starbucksmacchiato-prod.elasticbeanstalk.com``` is not registered on elastic beanstalk. You can verify this by looking up the IP address for this subdomain and noting that it does not resolve. Through registering that domain on elastic beanstalk and deploying a webserver that responds to that request with javascript, an attacker could get a persistent XSS on Starbuck's website. 

I have not registered that domain with Elastic Beanstalk since it would give me a large amount of information about the user's of Starbuck's website (and it would incur a large amount of traffic-more than I'd like to pay for on AWS!). If you would like me to do so, let me know but I do not want to go past the bounds of acceptable testing. 

Thanks,
David Dworken

</details>

---
*Analysed by Claude on 2026-05-12*
