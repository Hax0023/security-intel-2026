# Subdomain Takeover on .mil Domain via Dangling CNAME Record

## Metadata
- **Source:** HackerOne
- **Report:** 2499178 | https://hackerone.com/reports/2499178
- **Submitted:** 2024-05-10
- **Reporter:** martinvw
- **Program:** U.S. Department of Defense / .mil domain
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling CNAME, DNS Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain under a .mil domain contains a CNAME record pointing to an unregistered/available domain (peosol-lg.███), allowing an attacker to register that domain and claim the subdomain. This enables hosting malicious content, intercepting emails, and executing XSS attacks under the .mil domain authority.

## Attack scenario
1. Attacker discovers the subdomain ██████.mil resolves via CNAME to peosol-lg.███ which is available for registration
2. Attacker registers the intermediate domain peosol-lg.███ from the domain registrar
3. Attacker configures DNS records for the newly registered domain to point to attacker-controlled infrastructure
4. Traffic intended for ██████.mil now resolves to attacker's server due to the CNAME chain
5. Attacker hosts malicious content (phishing pages, malware) or intercepts email under the .mil subdomain
6. Users trust the .mil domain and fall victim to XSS, credential theft, or social engineering attacks

## Root cause
The DNS administrator created a CNAME record pointing to a non-existent or unregistered intermediate domain without ensuring that domain was registered and maintained under organizational control. The dangling CNAME was never cleaned up when the intermediate domain became unavailable.

## Attacker mindset
An opportunistic attacker recognizes that .mil domains carry high trust and authority. By taking over a subdomain through a dangling CNAME, they can exploit users' trust in government domains to conduct phishing, credential harvesting, or malware distribution campaigns with significantly higher success rates than if using an unrelated domain.

## Defensive takeaways
- Implement DNS auditing to identify and remediate dangling CNAME records pointing to non-existent or unregistered domains
- Establish a policy requiring all intermediate domains referenced in CNAME records to be registered and actively managed
- Use DNS validation/monitoring tools to continuously scan for subdomain takeover vulnerabilities
- Maintain an inventory of all DNS records and conduct periodic reviews for orphaned or stale entries
- Implement DNSSEC to prevent DNS spoofing attacks that could exacerbate subdomain takeover impact
- For high-value domains like .mil, require MFA and additional approval steps before DNS record modifications
- Monitor external threat databases and domain registrations for attempts to register domains referenced in organizational DNS

## Variant hunting
Search for other subdomains under the same .mil domain using DNS enumeration; audit all CNAME records across the organization's DNS infrastructure; check for dangling CNAIFEs pointing to other TLDs (.com, .org, .net); review recently deleted/expired domains that were previously referenced in CNAME records; check for similar patterns across other government (.gov) and military-adjacent domains

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1200

## Notes
The researcher demonstrated responsible disclosure by choosing not to register the available domain despite being able to do so, citing US residency rules for .us TLD. The HackerOne report ID 2499178 suggests this was submitted through an official bug bounty program. The redacted nature of the actual domain names indicates this involves sensitive military infrastructure. The DIG output confirms NXDOMAIN status with a valid CNAME response, definitively proving the dangling CNAME condition. This is a classic and easily exploitable vulnerability in DNS management.

## Full report
<details><summary>Expand</summary>

**Description:**

The subdomain `█████.mil` is pointing to `peosol-lg.███████.`, the domain `██████` is currently available for registration as can be seen at https://www.godaddy.com/nl-nl/domainsearch/find?domainToCheck=█████

Given the rules, residency of the US, of the `us`-tld I decided not to register the domain, also I do believe the output to be enough.

## References

## Impact

Using this vulnerability an attacker can:
- host unwanted/malicious content under your domain
- receive email on subdomains mentioned above
- effectively execute cross-site scripting attacks
- in some cases, steal cookie data
- in some cases, trick password managers into filling passwords

## System Host(s)
██████████.mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
See the DIG output:

```
√ martinvw@denali:~/src > dig █████.mil

; <<>> DiG 9.10.6 <<>> ████.mil
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 44977
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;█████████.mil.			IN	A

;; ANSWER SECTION:
██████████.mil.		3600	IN	CNAME	peosol-lg.███.

;; AUTHORITY SECTION:
us.			900	IN	SOA	a.cctld.us. admin.tldns.godaddy. 1715345748 1800 300 604800 1800

;; Query time: 166 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Fri May 10 15:06:32 CEST 2024
;; MSG SIZE  rcvd: 148
```

And the GoDaddy page: https://www.godaddy.com/nl-nl/domainsearch/find?domainToCheck=███

And whois:

```
√ martinvw@denali:~/src > whois ████████.
% IANA WHOIS server
% for more information on IANA, visit http://www.iana.org
% This query returned 1 object

refer:        whois.nic.us

domain:       US

organisation: Registry Services, LLC
address:      100 S. Mill Ave, Suite 1600
address:      Tempe AZ 85281
address:      United States of America (the)

contact:      administrative
name:         IANA Contact
organisation: Registry Services, LLC
address:      100 S. Mill Ave, Suite 1600
address:      Tempe AZ 85281
address:      United States of America (the)
phone:        +1 480 505 8800
fax-no:       +1 480 393 4275
e-mail:       iana@about.us

contact:      technical
name:         IANA Contact
organisation: Registry Services, LLC
address:      100 S. Mill Ave, Suite 1600
address:      Tempe AZ 85281
address:      United States of America (the)
phone:        +1 480 505 8800
fax-no:       +1 480 393 4275
e-mail:       iana@about.us

nserver:      B.CCTLD.US 156.154.125.70 2001:502:ad09:0:0:0:0:29
nserver:      F.CCTLD.US 2001:500:3682:0:0:0:0:11 209.173.58.70
nserver:      K.CCTLD.US 156.154.128.70 2001:503:e239:0:0:0:3:1
nserver:      W.CCTLD.US 2001:dcd:1:0:0:0:0:15 37.209.192.15
nserver:      X.CCTLD.US 2001:dcd:2:0:0:0:0:15 37.209.194.15
nserver:      Y.CCTLD.US 2001:dcd:3:0:0:0:0:15 37.209.196.15
ds-rdata:     59017 8 2 7daf469d42b5d8e5537fd4dd4b6057710e9a61f72c32eb7fb6526f52277ec2b0

whois:        whois.nic.us

status:       ACTIVE
remarks:      Registration information: http://www.nic.us

created:      1985-02-15
changed:      2024-04-16
source:       IANA

# whois.nic.us

No Data Found
URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/
>>> Last update of WHOIS database: 2024-05-10T13:10:37Z <<<
```

## Suggested Mitigation/Remediation Actions
Remove CNAME record █████████.mil



</details>

---
*Analysed by Claude on 2026-05-24*
