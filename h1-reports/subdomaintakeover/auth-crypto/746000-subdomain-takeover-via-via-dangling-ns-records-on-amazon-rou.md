# Subdomain Takeover Via Dangling NS Records on Amazon Route 53

## Metadata
- **Source:** HackerOne
- **Report:** 746000 | https://hackerone.com/reports/746000
- **Submitted:** 2019-11-25
- **Reporter:** todayisnew
- **Program:** CNCF (Cloud Native Computing Foundation)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Records, Namespace Hijacking
- **CVEs:** CVE-2017-14389
- **Category:** auth-crypto

## Summary
A subdomain (api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io) was pointed to AWS Route 53 nameservers that were subsequently deleted, leaving dangling NS records. An attacker successfully created a matching Route 53 zone and achieved complete DNS control over the subdomain, enabling arbitrary DNS record creation and domain takeover.

## Attack scenario
1. Attacker identifies that target subdomain has NS records pointing to AWS Route 53
2. Attacker discovers that the Route 53 zone has been deleted by the domain owner
3. Attacker creates a new Route 53 zone with the same subdomain name
4. Attacker creates arbitrary DNS records (A, AAAA, MX, TXT) in the hijacked zone
5. Attacker uses DNS control to create email addresses at the domain for authentication bypass
6. Attacker leverages domain control to request SSL certificates via email validation or access admin panels

## Root cause
The organization deleted NS records and Route 53 zone without ensuring no dangling references remained. The NS records continued to point to deleted AWS Route 53 nameservers, allowing any attacker to register a matching zone and claim authority over the domain.

## Attacker mindset
Opportunistic reconnaissance-driven approach. Attacker systematically checked DNS configurations, identified orphaned nameserver records, and exploited the registration window to claim the abandoned zone before the organization could reclaim it. The attacker demonstrated responsible disclosure by providing proof-of-concept and remediation guidance.

## Defensive takeaways
- Audit all DNS records and remove dangling NS records before deleting Route 53 zones
- Implement DNS takeover monitoring and alerting for critical domains
- Use subdomain enumeration and validation in CI/CD pipelines to detect orphaned subdomains
- Establish domain lifecycle management procedures with formal decommissioning checklists
- Consider using domain monitoring services to detect unauthorized NS record changes
- Implement CAA records to restrict SSL certificate issuance
- Regularly validate that all NS records point to active nameservers you control
- Use private DNS zones in Route 53 for internal subdomains where possible

## Variant hunting
Search for other subdomains in target organization using certificate transparency logs, DNS historical records, and subdomain enumeration tools. Check for other potential dangling NS records pointing to orphaned AWS Route 53, GCP Cloud DNS, Azure DNS, or other cloud nameserver infrastructure. Investigate subdomains with CNAME records pointing to deleted S3 buckets, CloudFront distributions, or other cloud resources.

## MITRE ATT&CK
- T1190
- T1584.001
- T1583.001
- T1589.001
- T1598.003
- T1566.002

## Notes
CVE-2017-14389 referenced for similar DNS takeover vulnerability class. Reporter provided detailed impact analysis including email impersonation, admin panel access via email verification, and SSL certificate issuance via DCV validation. The attack is low complexity requiring only network access and no privileges. Dangling DNS records represent a common infrastructure debt issue in organizations with frequent resource provisioning/deprovisioning.

## Full report
<details><summary>Expand</summary>

Good day, I truly hope it treats you great on your side of the screen :)




I have found that your website http://api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io is pointed via Name Server records to AWS route 53.

These name server records have been deleted, I was able to create a matching zone file, and takeover full control of the domain, and all DNS records.

It is possible to create any subdomain, MX records, A, AAAA, txt, PTR any records to control the domain.

Please let me know any subdomain I can create if needed to show impact, I have used test.yourdomain to show the risk here.

I am able to make an email address at your domain and send and receive responses. This allows access to admin panels that are secured by needing an email address at your domain.takeover.
Google Docs, Slack Chats, anywhere the authentication needed is an email address at your domain is now accessible with this risk.

This also allows access to the postmaster account for the subdomain, which will allow me to whitelist SSL issuing aliases via email validation:

https://support.dnsimple.com/articles/ssl-certificates-email-validation/#requirements
https://www.digicert.com/ssl-support/validation/not-receiving-dcv-emails.htm


Please see my POC (Pug of Concept)
http://api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io

POC Video:
https://web.archive.org/web/20191125154616/http://api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io/

Support for High Impact Rating: (7.5)

https://nvd.nist.gov/vuln/detail/CVE-2017-14389

Attack Vector (AV): Network
Attack Complexity (AC): Low
Privileges Required (PR): None
User Interaction (UI): None
Scope (S): Unchanged
Confidentiality (C): None
Integrity (I): High
Availability (A): None



Please verify your dns settings have been updated lag for domain propagation can take place.
https://dnschecker.org/#A/api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io

Options How to fix:

1) Remove the Name Server records that point to Name Servers you do not control.

2) Ask me to remove my registered Name Servers on AWS Route 53 and you can re register yours :)

May you be well on your side of the screen :)

-Eric

## Impact

Impact:

Cyber attackers can launch a phishing campaign leveraging your established (soon to be impacted) brand reputation.

The victim has no way of telling, whether the content is served by the domain owner or the cyber attacker.

Attackers can also chain higher severity attacks to this. Many applications expose session cookies to a wildcard domain (*.example.com),
so any subdomain can access them. An attacker can take a forgotten subdomain, trick the user to visit it, and extract cookies 
(even those with secure flag). This can be seen as an advanced version of XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
