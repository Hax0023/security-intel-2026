# Possible Domain Takeover on AWS Instance via Dangling CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 1390782 | https://hackerone.com/reports/1390782
- **Submitted:** 2021-11-03
- **Reporter:** samuelsiv
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Infrastructure Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
A CNAME DNS record for traefik-livedemo.rocket.chat points to a deprovisioned AWS Elastic Load Balancer endpoint that returns NXDOMAIN errors. An attacker can claim the orphaned ELB resource and redirect traffic to a malicious server, enabling phishing attacks against users trusting the legitimate domain.

## Attack scenario
1. Attacker identifies the dangling CNAME record via DNS enumeration pointing to a0e7eaaaa82f611e9b1cc0e9ccd15f3e-557536140.us-west-2.elb.amazonaws.com
2. Attacker confirms the endpoint is unowned by querying the IP address and receiving NXDOMAIN response
3. Attacker creates an AWS account and sets region to us-west-2
4. Attacker creates a new Application Load Balancer with the matching prefix identifier (a0e7eaaaa82f611e9b1cc0e9ccd15f3e) to claim the same endpoint
5. Attacker configures the ALB to serve phishing content mimicking Rocket.Chat login page
6. Users attempting to access traefik-livedemo.rocket.chat are redirected to attacker's phishing server, compromising credentials

## Root cause
The organization failed to clean up DNS records when deprovisioning AWS ELB resources. The CNAME record remained pointing to a non-existent ELB endpoint, creating an orphaned DNS entry. AWS allows re-claiming ELB endpoints using predictable naming schemes, enabling subdomain takeover.

## Attacker mindset
Opportunistic attacker exploiting common cloud infrastructure hygiene failures. The attacker recognizes that dangling DNS records pointing to AWS resources are re-claimable due to predictable naming conventions. The legitimate 'rocket.chat' brand trust provides excellent phishing opportunity with minimal effort required.

## Defensive takeaways
- Implement DNS record cleanup procedures as part of resource deprovisioning workflows
- Regularly audit all DNS records (CNAME, A, MX) against actual deployed infrastructure
- Use monitoring tools to detect and alert on NXDOMAIN responses from owned domains
- Implement certificate transparency monitoring to detect unauthorized certificate issuance
- Require TTL reduction and manual verification before CNAME record deletion
- Segregate production domains from development/demo subdomains using separate infrastructure
- Use automated scanning to identify subdomain takeover vulnerabilities
- Implement cloud resource naming policies resistant to enumeration attacks

## Variant hunting
Search for other rocket.chat subdomains with CNAME records pointing to AWS resources
Enumerate other ELB endpoints in us-west-2 region with similar naming patterns
Check for similar dangling records pointing to CloudFront, S3, or other AWS services
Investigate sister organizations or related projects for similar misconfiguration patterns
Look for orphaned DNS records pointing to other cloud providers (Azure, GCP) with similar claim mechanisms

## MITRE ATT&CK
- T1190
- T1586
- T1598
- T1566
- T1583.1
- T1584.1

## Notes
The report demonstrates a classic subdomain takeover vulnerability with strong phishing impact. The attacker mindset section reveals this is likely low-hanging fruit in bug bounty programs. The report lacks specific impact metrics (number of users affected, data exposed) and no evidence is provided that the takeover was actually successful, only that it appeared possible. The AWS region specification (us-west-2) and ELB naming convention details are crucial for reproducibility. This vulnerability class has been well-documented in security research; organizations should prioritize detection and prevention as part of standard infrastructure lifecycle management.

## Full report
<details><summary>Expand</summary>

The vulnerable domain possibly available for takeover is:` traefik-livedemo.rocket.chat (CNAME: a0e7eaaaa82f611e9b1cc0e9ccd15f3e-557536140.us-west-2.elb.amazonaws.com)`.
This domain, contains a record pointing to these an WS instance. When querying for any IP under the instance, I got returned an NXDomain error.

Steps to claim the instances:
Log-in or register into AWS. (Region has to be set as us-west-2)
Go onto the "Elastic LoadBalancer" section
Click "Create Loadbalancer"
Click "Application Loadbalancer"
Input the name before the final dash and the numbers. (eg: a0e7eaaaa82f611e9b1cc0e9ccd15f3e )
Deploy it, and check if the numbers are the same.

It might take a few to get the right one, but with an automated script I am certainly sure that it is achievable.

## Impact

The attacker might be able to takeover the domain, and gain access to the domain. An user, recognizing the domain recalling "rocket.chat" would let the user trust the page, and then, give the attacker his credentials via a phishing form.

</details>

---
*Analysed by Claude on 2026-05-24*
