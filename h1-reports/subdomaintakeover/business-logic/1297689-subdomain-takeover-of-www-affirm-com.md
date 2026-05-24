# Subdomain Takeover of www█████████.affirm.com via Unclaimed AWS S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 1297689 | https://hackerone.com/reports/1297689
- **Submitted:** 2021-08-10
- **Reporter:** ian
- **Program:** Affirm
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** business-logic

## Summary
A subdomain (www█████████.affirm.com) had a DNS record pointing to an AWS S3 bucket (affirm-prod-www-cms█████████) that no longer existed, allowing the researcher to claim and take control of the bucket. The attacker could serve arbitrary content, obtain TLS certificates, and potentially intercept traffic intended for legitimate Affirm resources.

## Attack scenario
1. Researcher discovers that www█████████.affirm.com resolves to an AWS S3 bucket via DNS CNAME records
2. Researcher identifies that the S3 bucket 'affirm-prod-www-cms█████████' no longer exists in Affirm's AWS account
3. Researcher creates a new S3 bucket with the same name in their own AWS account
4. DNS resolution now points to the attacker-controlled S3 bucket instead of a non-existent resource
5. Attacker uploads malicious content (index.html proof-of-concept) to the bucket
6. Attacker can obtain valid TLS certificate for the domain, serve malicious content, or conduct OAuth/cookie-based attacks if domain whitelists exist

## Root cause
Affirm failed to properly decommission DNS records when S3 buckets were deleted. The CNAME record for www█████████.affirm.com was not removed when the underlying S3 bucket was removed, creating a dangling DNS reference that could be claimed by an attacker.

## Attacker mindset
Opportunistic vulnerability discovery through reconnaissance. The attacker scanned Affirm subdomains, identified dead endpoints, and exploited AWS S3's global namespace to claim the bucket. The attacker demonstrated responsible disclosure by creating a proof-of-concept while acknowledging regional constraints that could make the attack more impactful.

## Defensive takeaways
- Implement DNS record lifecycle management - remove CNAME records when external resources are decommissioned
- Establish an inventory of all third-party integrations and cloud resources referenced in DNS
- Implement automated scanning for dangling DNS records and orphaned cloud resources
- Use S3 bucket policies and conditions to prevent unauthorized bucket creation with similar names
- Enable AWS Config rules to detect and alert on unused S3 buckets
- Regularly audit DNS records for references to deleted or non-existent resources
- Consider using private S3 buckets with restricted access patterns rather than public-facing configurations

## Variant hunting
Search for other Affirm subdomains with similar naming patterns that may point to deleted resources. Check for other cloud providers (Azure Blob Storage, Google Cloud Storage, CloudFront distributions) that may have similar dangling resource issues. Examine subdomains across different environments (staging, testing, development) that may have been decommissioned without proper DNS cleanup.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1584.004 - Compromise Infrastructure: Network Infrastructure

## Notes
The researcher noted AWS S3's region-specific behavior where incorrect region endpoints return PermanentRedirect errors. This actually limited the impact of the PoC since the bucket would need to be in the correct region (████-2) to fully function, but the researcher appropriately avoided moving it to prevent the bucket from being claimed by other malicious actors. The vulnerability assumes potential impact through OAuth whitelisting, cookie domain scoping, or other trust relationships tied to the domain.

## Full report
<details><summary>Expand</summary>

## Summary
Hi there, assuming you want this report as your policy mentions Affirm resources with third-parties, but the scope was a little unclear. Regardless, www█████.affirm.com points to an AWS S3 bucket `affirm-prod-www-cms█████████` that no longer exists. I was able to take control of this bucket and put my own content onto it. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

**Note:** S3 has a weird quirk where the bucket's region may cause errors if a request to a bucket is addressed to the wrong region. I assume your CDN points to `████-2`, but my bucket is in `us-east-1`. When you make a request to this domain, S3 shows a redirect error because of this. If I wanted to move the bucket to the correct region (for the PoC to fully work), it would put it at risk of being claimed by attackers/others. Hopefully, this is enough for you.

### PoC
To see that the domain points to the `affirm-prod-www-cms█████` bucket:

```
% curl https://www██████████.affirm.com
[...]
<Code>PermanentRedirect</Code>
<Message>The bucket you are attempting to access must be addressed using the specified endpoint. Please send all future requests to this endpoint.</Message>
<Endpoint>s3.amazonaws.com</Endpoint>
<Bucket>affirm-prod-www-cms████</Bucket>
[...]
```

Following this redirect, to see the PoC:
```
% curl https://s3.amazonaws.com/affirm-prod-www-cms████████/index.html
<!-- taken over by hackerone.com/ian bugcrowd.com/iangcarroll ian@lhost.sh -->
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
