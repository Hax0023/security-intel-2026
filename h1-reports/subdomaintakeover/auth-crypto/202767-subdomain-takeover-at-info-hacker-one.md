# Subdomain Takeover at info.hacker.one via Unbounce API Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 202767 | https://hackerone.com/reports/202767
- **Submitted:** 2017-02-02
- **Reporter:** ak1t4
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Third-party Service Vulnerability, Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A subdomain takeover vulnerability was discovered at info.hacker.one due to a CNAME record pointing to Unbounce's service (app.unbounce.com). An authorization bypass in Unbounce's API allowed the researcher to claim the domain without proper ownership verification, enabling arbitrary content hosting on the HackerOne subdomain.

## Attack scenario
1. Attacker identifies that info.hacker.one has a CNAME entry pointing to unbouncepages.com
2. Attacker discovers a zero-day authorization bypass in Unbounce's API that allows claiming domains with existing CNAME records
3. Attacker exploits the API vulnerability to claim the info.hacker.one domain within Unbounce's platform
4. Attacker uploads malicious content (e.g., fake login pages, phishing forms) to the claimed domain
5. Users visiting info.hacker.one are served attacker-controlled content, enabling credential theft or social engineering
6. Attacker can leverage HackerOne's trusted brand to increase attack effectiveness against the organization or its users

## Root cause
Multiple failures: (1) DNS CNAME pointing to external service without active claim, (2) Unbounce API lacking proper domain ownership verification before allowing domain claims, (3) No monitoring or validation of subdomain changes by HackerOne

## Attacker mindset
Opportunistic vulnerability hunter demonstrating that abandoned subdomain configurations combined with vendor API flaws create takeover opportunities. Attacker methodically tested service restrictions, discovered the bypass, and documented proof-of-concept to show real-world impact.

## Defensive takeaways
- Audit all DNS records (CNAME, A, MX) for inactive or orphaned entries pointing to third-party services
- Implement subdomain monitoring and alerting for unexpected CNAME changes
- Maintain an inventory of all subdomains and their operational status
- Coordinate with third-party service vendors to ensure mutual domain verification/deprovisioning
- Regularly test subdomain takeover risks, especially after service migrations or decommissioning
- Contact vendors about discovered authorization bypasses in their domain claiming mechanisms
- Use DNS CAA records and DNSSEC to add additional validation layers

## Variant hunting
Scan other HackerOne subdomains for similar CNAME misconfigurations pointing to managed services
Test other Unbounce competitors (Leadpages, Instapage, etc.) for similar API authorization bypasses
Identify organizations using Unbounce and check for similar subdomain takeover patterns
Review abandoned S3 buckets, GitHub Pages, Heroku apps, and other common CNAME targets in wild subdomains
Test Unbounce API with different domain claiming scenarios to expand exploit scope

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1589 - Gather Victim Identity Information
- T1566 - Phishing

## Notes
This report demonstrates a critical chaining of vulnerabilities: misconfigured DNS + third-party service authorization bypass = domain takeover. The researcher's discovery of a zero-day in Unbounce's API significantly amplifies the impact beyond a simple dangling DNS record. The proof-of-concept clearly shows arbitrary content execution capability. The fix involves both immediate DNS remediation and vendor coordination for the underlying API flaw.

## Full report
<details><summary>Expand</summary>

**Summary:**

Hi team,i've been able to takeover subdomain at __info.hacker.one__,
the CNAME entry in the subdomain is pointing to an external page service (app.unbounce.com). 

#### Actual Dns Entry:

{F156764}


#### Steps To Reproduce

1) I have claimed the domain and placed a page for PoC validation located under: 
Go to -> http://info.hacker.one/blank-page-123133617adasdasdsa/
2) You see the alert box and the subdomain takeover

{F156765}

Private & hide Video PoC at -> https://youtu.be/IcoGM65YyU4


#### How was this possible?

While testing UnbouncePage services i saw that they block any domain that was already claimed, but i decided go  deeper and I found an 0day in their API which allows any user to claim any domain with a DNS entry pointing to -> __unbouncepages.com__, i think this bug compromises All Customers Domains at UnbouncePage Services

#### Security Impact

An attacker can utilize this domain _info.hacker.one_ for targeting the organization by fake login hackerOne forms, or steal sensitive information of teams  (credentials, credit card information, etc)

#### FIX & MITIGATION

*You should immediately remove the DNS-entry for this domain or point it elsewhere if you don't use that service
*Contact vendor asap for patch or launch a Fix


Please let me know if more info needed or any help,

Best Regards,
@ak1t4


</details>

---
*Analysed by Claude on 2026-05-24*
