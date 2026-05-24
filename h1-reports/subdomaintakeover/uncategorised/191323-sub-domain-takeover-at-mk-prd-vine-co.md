# Subdomain Takeover at mk.prd.vine.co via Stopped EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 191323 | https://hackerone.com/reports/191323
- **Submitted:** 2016-12-15
- **Reporter:** punkrock
- **Program:** Vine
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Cloud Infrastructure Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The EC2 instance previously hosted at mk.prd.vine.co was stopped and subsequently reassigned to another AWS account or entity, allowing an attacker to potentially serve malicious content via the subdomain. The DNS record pointed to the EC2 instance but lacked proper ownership verification, enabling takeover once the underlying infrastructure changed hands.

## Attack scenario
1. Attacker discovers that mk.prd.vine.co subdomain exists and is pointed to an EC2 instance via DNS
2. Attacker monitors the subdomain and detects that the original EC2 instance has been stopped (port 443 previously closed, now open)
3. Attacker determines the instance has been reassigned to a different AWS account by observing AWS ELB (awselb/2.0) responses
4. Attacker gains control of the reassigned EC2 instance or associated load balancer infrastructure
5. Attacker hosts malicious content, performs phishing attacks, or redirects users to compromise Vine users and damage company reputation
6. Legitimate Vine users trusting the mk.prd.vine.co subdomain are compromised without realizing they're interacting with attacker-controlled infrastructure

## Root cause
Vine failed to implement proper subdomain management practices including: (1) no DNS CNAME/A record verification on subdomain ownership, (2) lack of monitoring for stopped/decommissioned cloud resources, (3) no process to clean up DNS records when underlying infrastructure is deprovisioned, (4) insufficient tracking of legacy subdomains pointing to cloud instances

## Attacker mindset
An attacker systematically enumerates subdomains of Vine and monitors them for signs of infrastructure changes. Upon detecting that mk.prd.vine.co's backing EC2 instance was stopped and reassigned, the attacker recognizes an opportunity to perform domain takeover. The attacker tests the subdomain behavior (port changes, error responses) to confirm the infrastructure has changed hands, indicating they could potentially control it.

## Defensive takeaways
- Implement subdomain enumeration and monitoring for all production domains to detect dangling DNS records
- Establish automated processes to remove DNS records when cloud resources (EC2, S3, ALB) are decommissioned
- Use CNAME validation or DNS TXT record challenges to verify ownership before allowing subdomain delegation
- Implement cloud infrastructure tagging and lifecycle policies to track and manage resource dependencies
- Monitor DNS changes and cloud resource state changes through centralized logging and alerting
- Conduct regular subdomain audits and validate that DNS targets are still active and controlled by the organization
- Implement DNSSEC or other DNS hardening measures to prevent unauthorized DNS modifications

## Variant hunting
Search for other Vine subdomains (*.vine.co, *.prd.vine.co, *.mk.vine.co) that may point to EC2 instances, S3 buckets, CloudFront distributions, or other cloud resources that could be in a stopped/orphaned state. Check for subdomains with similar naming patterns (e.g., other service prefixes like 'api.prd.vine.co', 'cdn.prd.vine.co') that may have been abandoned.

## MITRE ATT&CK
- T1584.001 - Compromise Infrastructure: Domains
- T1583.001 - Acquire Infrastructure: Domains
- T1190 - Exploit Public-Facing Application

## Notes
This report demonstrates a critical oversight in cloud infrastructure lifecycle management. The progression from 'no port 443' to 'port 443 open' with AWS ELB headers indicates infrastructure reassignment rather than modification. The awselb/2.0 response suggests an AWS Application Load Balancer is now fronting the subdomain, pointing to a different backend. This is a classic subdomain takeover scenario exacerbated by AWS's instance recycling and lack of automatic DNS cleanup.

## Full report
<details><summary>Expand</summary>

Hey

It looks like the EC2 Instance at `mk.prd.vine.co` has been stopped and now it has been assigned to someone else

#### Proof of Concept

1. `http://mk.prd.vine.co/` few days back didn't have port 443 open but now it does have an open port 443

Response 
```
< HTTP/1.1 426 Upgrade Required
< Date: Thu, 15 Dec 2016 07:06:34 GMT
< Content-Type: text/plain
< Content-Length: 16
< Connection: keep-alive
```

Also `http://mk.prd.vine.co/%00` pops an error

```
< HTTP/1.1 400 Bad Request
* Server awselb/2.0 is not blacklisted
< Server: awselb/2.0
< Date: Thu, 15 Dec 2016 07:06:58 GMT
< Content-Type: text/html
< Content-Length: 171
< Connection: close

<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<hr><center>awselb/2.0</center>
</body>
</html>
```

So it looks like now someone's load balancer is pointing to `mk.prd.vine.co`

</details>

---
*Analysed by Claude on 2026-05-24*
