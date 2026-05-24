# DNS Misconfiguration Leads to Subdomain Takeover via Dangling CNAME (max1.liveplan.com)

## Metadata
- **Source:** HackerOne
- **Report:** 1294492 | https://hackerone.com/reports/1294492
- **Submitted:** 2021-08-07
- **Reporter:** melbadry9
- **Program:** LivePlan
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, DNS Misconfiguration, Infrastructure Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain max1.liveplan.com is configured with a CNAME pointing to an EC2 instance's public DNS name (ec2-54-68-121-128.us-west-2.compute.amazonaws.com) instead of an Elastic IP. When the EC2 instance was terminated, the public IP was released back to AWS's pool, allowing an attacker to claim the IP by launching a new EC2 instance and effectively taking over the subdomain. The attacker's SSL certificate for *.test.tugo.com domains proved active control over the subdomain.

## Attack scenario
1. Attacker discovers that max1.liveplan.com resolves to EC2 public DNS: ec2-54-68-121-128.us-west-2.compute.amazonaws.com
2. Attacker identifies the IP address 54.68.121.128 and determines it is currently unassigned after the original EC2 instance was terminated
3. Attacker launches their own EC2 instance in the same AWS region (us-west-2) and AWS assigns the previously released IP 54.68.121.128 to their instance
4. The dangling CNAME record still points to the public DNS name, which now resolves to the attacker's controlled EC2 instance
5. Attacker configures their EC2 instance to serve HTTPS traffic and obtains an SSL certificate for the domain
6. Attacker achieves complete subdomain takeover, able to serve malicious content or intercept communications intended for max1.liveplan.com

## Root cause
LivePlan used EC2 instance public DNS names as CNAME targets instead of static Elastic IPs, combined with failure to clean up DNS records when infrastructure is decommissioned. EC2 public IPs are ephemeral and can be reassigned to other instances when released, creating a window for takeover.

## Attacker mindset
An attacker performing reconnaissance would systematically scan for dangling DNS records by identifying CNAME records pointing to cloud provider DNS names. Upon finding max1.liveplan.com pointing to an EC2 DNS, they would check if the IP is available in AWS, lease it, and host malicious content. This is a low-effort, high-impact attack requiring minimal technical skill.

## Defensive takeaways
- Always use static Elastic IPs or load balancer DNS names for CNAME records instead of EC2 instance public DNS names
- Implement DNS record cleanup workflows tied to infrastructure decommissioning processes
- Regularly audit DNS records for dangling entries using tools that check certificate validity and response content
- Use ALIAS records (AWS Route53) pointing directly to ELB/ALB instead of CNAME when possible
- Monitor for new EC2 instances launching with previously-used IP addresses in your monitored ranges
- Implement DNS validation checks in CI/CD pipelines to catch dangling records before they pose risks
- Consider using dedicated DNS monitoring services that alert on certificate changes or subdomain takeover indicators

## Variant hunting
Search for other subdomains using EC2 public DNS CNAME records across the organization's DNS zone files. Cross-reference terminated EC2 instances with their former IP addresses against current AWS IP pool allocations. Check CloudFront, S3, and other AWS services for similar misconfigurations where service endpoints are used as CNAME targets without proper lifecycle management. Review SSL certificates issued for company domains to identify active takeovers on other subdomains.

## MITRE ATT&CK
- T1190
- T1584
- T1583.001
- T1098.003

## Notes
This report references a similar finding (#1069795), suggesting this is a known misconfiguration pattern. The attacker demonstrated proof of takeover by retrieving SSL certificate data showing *.test.tugo.com domains, proving they had control over HTTPS traffic. The vulnerability is particularly dangerous because the dangling DNS record remains valid and pointing to a real IP, but that IP is now under different control. AWS-specific: Elastic IPs should be reserved for persistent infrastructure or properly deallocated when no longer needed.

## Full report
<details><summary>Expand</summary>

## Summary
The issue happens due to using EC2 public DNS instead of using Elastic IPs as `CNAME` record. This report is simliar to report #1069795
 
## Misconfiguration

- DNS Records

```json
{
  "host": "max1.liveplan.com",
  "resolver": [
    "1.0.0.1:53"
  ],
  "a": [
    "54.68.121.128"
  ],
  "cname": [
    "ec2-54-68-121-128.us-west-2.compute.amazonaws.com"
  ],
  "status_code": "NOERROR",
  "timestamp": "2021-08-07T13:41:48.3522806+02:00"     
}
```

- If the EC2 instance is killed or terminated and the DNS was not updated this will lead to creating a dangling DNS record for the subdomain.
- The EC2 IP will be released to AWS IPs pool, This mean it's possible to assign the IP to new EC2 instance.

## PoC

- SSL Certificate Data pulled from `https://max1.liveplan.com` on date `7/8/2021 - 1:40PM`.
- Data was pulled using [SSLEnum](https://github.com/melbadry9/SSLEnum)

```json
{
  "name": "max1.liveplan.com",
  "org": [],
  "cn": [
    "*.test.tugo.com"
  ],
  "alt_doms": [
    "*.test.tugo.com",        
    "*.dev.tugo.com",
    "*.uat.tugo.com"
  ],
  "dangling": true
}
```

- This does prove that `max1.liveplan.com` is currently taken over by  someone.

{F1403387}
 
## Fix
- Use Elastic IPs instead of the public DNS of EC2 instance or clear DNS records for mentioned subdomain

## Supporting Material/References:
- https://blog.melbadry9.xyz/dangling-dns/aws/ddns-ec2-current-state

## Impact

- This could allow the takeover of the EC2 instance IP that will lead to subdomain takeover.

</details>

---
*Analysed by Claude on 2026-05-24*
