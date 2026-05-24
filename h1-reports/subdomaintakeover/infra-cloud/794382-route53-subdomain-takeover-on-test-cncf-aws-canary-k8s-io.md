# Route53 Subdomain Takeover via Dangling NS Records on test-cncf-aws.canary.k8s.io

## Metadata
- **Source:** HackerOne
- **Report:** 794382 | https://hackerone.com/reports/794382
- **Submitted:** 2020-02-12
- **Reporter:** rhynorater
- **Program:** Kubernetes
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Improper Resource Cleanup
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain test-cncf-aws.canary.k8s.io was vulnerable to takeover because NS record delegations remained in the parent zone after the child zone was deleted. An attacker could create a new Route53 zone with matching nameservers and claim the subdomain, then create arbitrary DNS records including POC subdomains.

## Attack scenario
1. Attacker identifies dangling NS records pointing to Route53 nameservers for test-cncf-aws.canary.k8s.io
2. Attacker creates a new Route53 zone matching the target subdomain name
3. Attacker associates the zone with the same AWS Route53 nameservers referenced in the dangling NS records
4. Attacker creates arbitrary DNS records under the claimed subdomain (e.g., poc.test-cncf-aws.canary.k8s.io)
5. Attacker can now host malicious content, capture cookies with wildcard scope, or serve phishing pages under the legitimate domain
6. Users trust the subdomain due to parent domain reputation, increasing attack effectiveness

## Root cause
When the original Route53 zone was deleted, the NS record delegation in the parent zone (canary.k8s.io) was not removed. This left the subdomain pointing to specific Route53 nameservers that could be claimed by any AWS account creating a zone with that name.

## Attacker mindset
An attacker monitoring DNS infrastructure for misconfigured delegations can systematically identify zones with orphaned NS records. Route53's predictable nameserver naming scheme makes it trivial to claim a zone once the delegation is identified. The attacker leverages domain reputation to conduct secondary attacks like cookie theft or phishing.

## Defensive takeaways
- Always remove NS record delegations from the parent zone before deleting the child zone
- Implement automated checks to detect orphaned/dangling NS records in DNS zones
- Use DNS CNAME instead of NS delegation where possible to reduce attack surface
- Maintain an inventory of all active DNS delegations and regularly audit for abandoned subdomains
- Monitor Route53 zones for unauthorized zone creation attempts matching organizational domain patterns
- Implement alerting on DNS changes to detect subdomain delegation modifications
- Use DNS CAA records to restrict certificate issuance on delegated subdomains
- Consider locking down Route53 permissions to prevent unauthorized zone creation in production accounts

## Variant hunting
Search for other CNCF or k8s.io subdomains with similar patterns that may have dangling NS records
Check for other canary.k8s.io subdomains pointing to AWS Route53 nameservers
Identify production zones in same AWS account that may share similar cleanup patterns
Scan for other organizations' Route53 accounts with public NS record delegations
Look for subdomains with NS records but no corresponding zone delegation documentation
Hunt for zones deleted in past 6-12 months that may still have NS delegations in parent zones

## MITRE ATT&CK
- T1584.002
- T1583.001
- T1190
- T1199

## Notes
This vulnerability affects a CNCF (Cloud Native Computing Foundation) infrastructure component. The attack requires no authentication and only network access to DNS infrastructure. The impact is amplified because the parent domain (k8s.io) is highly trusted in the Kubernetes community. This is a classic example of improper resource cleanup where infrastructure changes are not fully reverted.

## Full report
<details><summary>Expand</summary>

## Summary:
I discovered that it was possible to takeover ` test-cncf-aws.canary.k8s.io` by assigning a zone to that name with one of the following nameservers in Route53:
```
test-cncf-aws.canary.k8s.io. 3600 IN    NS      ns-265.awsdns-33.com.
test-cncf-aws.canary.k8s.io. 3600 IN    NS      ns-687.awsdns-21.net.
test-cncf-aws.canary.k8s.io. 3600 IN    NS      ns-1458.awsdns-54.org.
test-cncf-aws.canary.k8s.io. 3600 IN    NS      ns-1825.awsdns-36.co.uk.
```
Once the zone was claimed, I was able to create DNS records under this host. Consider the following record:
```
poc.test-cncf-aws.canary.k8s.io
```

##Steps To Reproduce:
1. See above domain

##Remediation Instructions
Remove the NS record delegation NS privs on a subdomain before you delete the zone

## Impact

With this vulnerability, an attacker can host arbitrary content under your domain. This can allow an attacker to host brand-damaging materials, steal sensitive * scoped session cookies, and even escalate other vulnerabilities.

</details>

---
*Analysed by Claude on 2026-05-24*
