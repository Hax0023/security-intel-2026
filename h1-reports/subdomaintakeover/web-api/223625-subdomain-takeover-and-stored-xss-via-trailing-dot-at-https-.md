# Subdomain Takeover via Trailing Dot at coding-exercises.udemy.com

## Metadata
- **Source:** HackerOne
- **Report:** 223625 | https://hackerone.com/reports/223625
- **Submitted:** 2017-04-25
- **Reporter:** cha5m
- **Program:** Udemy
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Configuration Error, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A subdomain takeover vulnerability exists at coding-exercises.udemy.com due to a trailing dot (FQDN) in the DNS configuration pointing to GitBook's infrastructure. An attacker can access the trailing dot variant (coding-exercises.udemy.com.) to interact with GitBook's custom domain feature, potentially taking over the subdomain. This issue is compounded by a previously reported stored XSS vulnerability (#222337) on the same subdomain.

## Attack scenario
1. Attacker discovers that coding-exercises.udemy.com is hosted on GitBook infrastructure via CNAME records
2. Attacker identifies that GitBook's custom domain feature accepts domain configurations, including those with trailing dots
3. Attacker accesses the subdomain with a trailing dot (coding-exercises.udemy.com.) which resolves differently due to FQDN interpretation
4. Attacker gains access to the GitBook instance or custom domain configuration interface
5. Attacker modifies the custom domain configuration to point to attacker-controlled infrastructure
6. Attacker serves malicious content at coding-exercises.udemy.com, combining with stored XSS for maximum impact

## Root cause
Udemy delegated coding-exercises.udemy.com to GitBook via CNAME record, but GitBook's custom domain validation did not properly handle or reject FQDN variants with trailing dots. DNS resolvers treat trailing dots as absolute names (FQDN), allowing the attacker to access the domain through an alternative DNS path. Additionally, Udemy did not implement CNAME/subdomain takeover protections or monitoring.

## Attacker mindset
Opportunistic attacker leveraging DNS quirks and third-party hosting misconfigurations. The attacker systematically explored DNS behavior, recognized the trailing dot variance, and connected it to subdomain takeover patterns seen in other services. The combination with existing stored XSS (report #222337) shows intent to maximize impact.

## Defensive takeaways
- Validate and monitor all subdomains and CNAME delegations, including FQDN variants
- Implement DNS security monitoring to detect unauthorized changes to delegated subdomains
- When using third-party services, ensure SLAs include subdomain takeover prevention and rapid incident response
- Conduct security reviews of all third-party hosted content, especially when combined with user-facing features
- Implement DNSSEC and HSTS to mitigate DNS-based attacks
- Test custom domain features in third-party services for trailing dot and FQDN variants
- Establish incident response procedures with third-party hosting providers for subdomain takeover scenarios
- Consider using subdomain takeover monitoring services

## Variant hunting
Test all subdomains with trailing dots to identify CNAME delegation variants
Enumerate other Udemy subdomains delegated to third-party services (GitHub Pages, Heroku, etc.)
Check for dangling DNS records or CNAME records pointing to decommissioned services
Investigate GitBook competitor services (Hugo, Sphinx hosting) for similar custom domain validation flaws
Review other subdomains using similar third-party hosting patterns for trailing dot vulnerabilities
Test internationalized domain names and punycode variants
Check for subdomain wildcards and their interaction with trailing dots

## MITRE ATT&CK
- T1190
- T1199
- T1584.001
- T1583.001
- T1657

## Notes
The reporter demonstrated maturity by: (1) reporting to both Udemy and GitBook, (2) acknowledging third-party scope questions, (3) providing clear DNS evidence, and (4) referencing similar vulnerability patterns. The vulnerability chain of subdomain takeover + stored XSS represents severe impact. The trailing dot variant is a subtle attack vector often overlooked in domain validation. Resolution required coordination between Udemy and GitBook, suggesting organizational complexity in third-party hosting scenarios. Report filed April 2017, reflecting historical significance of this attack class.

## Full report
<details><summary>Expand</summary>

Hello @Udemy!

Summary
=====
I previously reported a cross-site scripting vulnerability ( #222337 ) at coding-exercises.udemy.com. I recently discovered that GitBook-hosted sites are also vulnerable to subdomain takeovers due to a trailing dot vulnerability in the GitBook "Custom Domain" feature (seen below).

{F179119}

Proof of Concept
=====
The taken-over subdomain can be found here: `https://coding-exercises.udemy.com.` (notice the trailing dot).

First, we will look at the ```dig``` results for ```coding-exercises.udemy.com.``` (with the trailing dot)

```
Chases-MacBook-Air:~ chase$ dig coding-exercises.udemy.com.

; <<>> DiG 9.8.3-P1 <<>> coding-exercises.udemy.com.
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 38225
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;coding-exercises.udemy.com.	IN	A

;; ANSWER SECTION:
coding-exercises.udemy.com. 1	IN	CNAME	www.gitbooks.io.
www.gitbooks.io.	3301	IN	CNAME	cdn.gitbook.com.
cdn.gitbook.com.	2494	IN	A	138.197.194.9

;; Query time: 342 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Apr 24 21:24:39 2017
;; MSG SIZE  rcvd: 115
```
And now the ```dig``` results for ```coding-exercises.udemy.com```
```
Chases-MacBook-Air:~ chase$ dig coding-exercises.udemy.com

; <<>> DiG 9.8.3-P1 <<>> coding-exercises.udemy.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1203
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;coding-exercises.udemy.com.	IN	A

;; ANSWER SECTION:
coding-exercises.udemy.com. 267	IN	CNAME	www.gitbooks.io.
www.gitbooks.io.	3268	IN	CNAME	cdn.gitbook.com.
cdn.gitbook.com.	2461	IN	A	138.197.194.9

;; Query time: 785 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Apr 24 21:25:12 2017
;; MSG SIZE  rcvd: 115
```

Mitigation
=====
I noticed that this service is hosted by GitBook, however, your bug bounty brief does not state that third-party hosted services being out of scope. I have also reported these issues directly to GitBook in an attempt to get them resolved ASAP. However, it might be worthwhile for you, an actual GitBook customer, to reach out directly to get them resolved quicker.

Example
=====
Here is an example of another report with a trailing dot causing a subdomain takeover in a service:
* https://hackerone.com/reports/174417

Please let me know if you have any other questions. I would be more than happy to help! :)

Thank you and best regards,
n0rb3r7

</details>

---
*Analysed by Claude on 2026-05-24*
