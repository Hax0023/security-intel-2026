# Subdomain Takeover at odoo-staging.exness.io

## Metadata
- **Source:** HackerOne
- **Report:** 1540252 | https://hackerone.com/reports/1540252
- **Submitted:** 2022-04-13
- **Reporter:** omer
- **Program:** Exness
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain odoo-staging.exness.io contains a CNAME record pointing to exness-stg.odoo.com, which appears to be unclaimed or no longer actively managed. An attacker could claim the target domain on Odoo's infrastructure and redirect traffic to a malicious server, enabling phishing and scam attacks against users accessing this staging subdomain.

## Attack scenario
1. Attacker identifies that odoo-staging.exness.io resolves via CNAME to exness-stg.odoo.com
2. Attacker verifies that exness-stg.odoo.com is no longer claimed or actively hosted on Odoo infrastructure
3. Attacker registers or claims the exness-stg.odoo.com subdomain on Odoo's platform
4. Attacker configures the claimed subdomain to serve malicious content (phishing pages, malware)
5. Users attempting to access odoo-staging.exness.io are redirected to attacker-controlled content
6. Attacker harvests credentials, spreads malware, or executes social engineering attacks

## Root cause
The organization created a CNAME record for odoo-staging.exness.io pointing to an external domain (exness-stg.odoo.com) without ensuring persistent ownership or active management of the target domain. The staging subdomain was not properly decommissioned or the CNAME target was abandoned.

## Attacker mindset
An attacker recognizes that staging/development subdomains are often less monitored and valuable for establishing trust through legitimate-looking domain names. By exploiting the dangling CNAME, they can impersonate Exness services to conduct sophisticated phishing campaigns or distribute malware to users expecting a legitimate staging environment.

## Defensive takeaways
- Maintain an inventory of all CNAME records and regularly audit their targets to identify dangling or orphaned DNS entries
- Implement DNS monitoring to alert on unclaimed or resolvable subdomain targets
- Use subdomain takeover scanning tools as part of continuous security assessments
- Establish a process to decommission subdomains properly, including cleanup of DNS records and coordination with external domain owners
- Consider implementing CNAME flattening or alternative DNS validation methods to reduce takeover surface
- Apply certificate transparency monitoring to detect unauthorized certificates for corporate subdomains
- Restrict DNS zone editing permissions and require change approvals for CNAME modifications

## Variant hunting
Scan other Exness subdomains for similar dangling CNAME records pointing to external services
Check for CNAME records pointing to abandoned Odoo staging environments or test instances
Identify other third-party service CNAMEs (CDN, email services) that may be unclaimed
Search for historical DNS records of decommissioned services using passive DNS databases
Examine subdomains across different Exness environments (dev, staging, qa) for inconsistent CNAME management

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a classic subdomain takeover vulnerability resulting from inadequate DNS hygiene. The staging designation makes it particularly valuable for attackers as users may have lower security expectations for non-production environments. The attacker did not need to compromise Exness infrastructure directly; instead, they could simply claim an orphaned subdomain on the external provider's platform.

## Full report
<details><summary>Expand</summary>

**Domain:**
>https://odoo-staging.exness.io

**PoC**
>https://odoo-staging.exness.io

**Cname:**
```
$ host odoo-staging.exness.io
odoo-staging.exness.io is an alias for exness-stg.odoo.com.
exness-stg.odoo.com has address 141.95.172.222
exness-stg.odoo.com mail is handled by 10 eu123a.odoo.com.
```

## Impact

Scam, phishing

</details>

---
*Analysed by Claude on 2026-05-24*
