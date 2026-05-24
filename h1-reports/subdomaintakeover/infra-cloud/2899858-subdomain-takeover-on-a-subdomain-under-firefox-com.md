# Subdomain Takeover on Firefox.com via Unclaimed CNAME Target

## Metadata
- **Source:** HackerOne
- **Report:** 2899858 | https://hackerone.com/reports/2899858
- **Submitted:** 2024-12-14
- **Reporter:** martinvw
- **Program:** Mozilla - HackerOne
- **Bounty:** Not specified in excerpt
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS CNAME Misconfiguration, Certificate Authority Account Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain under firefox.com was configured as a CNAME pointing to www.mozilla.org but the target was not claimed/registered at the hosting provider, allowing an attacker to register it and take control. The attacker could serve malicious content, set large cookies to perform DoS attacks, or launch phishing/malware campaigns leveraging the trusted Firefox/Mozilla domain.

## Attack scenario
1. Attacker identifies a CNAME record under firefox.com pointing to an unclaimed hosting provider account (e.g., www.mozilla.org)
2. Attacker registers/claims the target domain at the hosting provider before Mozilla does
3. Attacker gains control of the subdomain and can serve arbitrary content over HTTP
4. Attacker leverages the trusted firefox.com domain for phishing, malware distribution, or tracking campaigns
5. Attacker exploits shared cookie domain to set large cookies (100KB+) causing DoS to legitimate firefox.com users
6. CAA records prevent HTTPS certificate issuance but HTTP attacks remain viable

## Root cause
DNS misconfiguration where a CNAME record points to a hosting provider account that was never claimed or registered by Mozilla, combined with insufficient validation that all CNAME targets are properly controlled before DNS delegation.

## Attacker mindset
Opportunistic reconnaissance of DNS infrastructure; identifying dangling CNAME records that point to unclaimed third-party resources; exploiting trust in legitimate domains for malware/phishing distribution; abusing cookie mechanisms for user disruption.

## Defensive takeaways
- Implement continuous monitoring and auditing of all DNS records (A, AAAA, CNAME, MX, etc.) to identify dangling or unclaimed targets
- Maintain an inventory of all third-party hosting providers and hosting accounts; verify they are claimed and controlled
- Establish automated checks to ensure CNAME targets are registered and actively managed before DNS delegation
- Implement CAA records (as Mozilla does) but also validate HTTPS certificate generation attempts as an early warning system
- Use subdomain takeover detection tools to identify vulnerable DNS configurations
- Implement SameSite cookie attributes to prevent cross-subdomain cookie abuse
- Implement Content Security Policy (CSP) headers to limit attack surface even on vulnerable subdomains
- Regular security review of DNS infrastructure as part of attack surface management

## Variant hunting
Search for other subdomains under mozilla.com, mozilla.net, mozgcp.net, mozaws.net with CNAME records; check for dangling A/AAAA records pointing to discontinued hosting; review old DNS records in DNS history archives (e.g., SecurityTrails, DNSDumpster); identify other organizations with similar multi-TLD presence that may have unclaimed CNAME targets.

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (using trusted domain)
- T1583.001 - Acquire Infrastructure: Domains (subdomain takeover)
- T1195.3 - Supply Chain Compromise: Compromise Hardware Supply Chain (infrastructure compromise)
- T1189 - Drive-by Compromise (malware distribution via trusted domain)
- T1499.4 - Denial of Service: Application Layer (cookie-based DoS)

## Notes
Report contains redacted information (██) indicating sensitive details about the specific subdomain and hosting provider. CAA records provided partial mitigation by preventing HTTPS certificate issuance but did not prevent HTTP attacks. The reporter demonstrated understanding of both direct impacts (malware, phishing) and indirect impacts (cookie-based DoS). This is a classic example of subdomain takeover via unclaimed CNAME targets, a known vulnerability class documented in HackerOne and OWASP. Mozilla's scope explicitly includes subdomain takeover PoCs for their owned domains, indicating this vulnerability class is actively targeted and valued by the program.

## Full report
<details><summary>Expand</summary>

## Summary:
Subdomain takeover via ██████████ of █████

## Steps To Reproduce:

The subdomain ████ is a CNAME to www.mozilla.org (which is hosted at ███████), however it was not currently registered at ███████. By claiming it I was able to take it over.

As PoC please visit: ██████

It seems that the CAA records does not allow ████████ to generate an SSL certificate for me.

## Supporting Material/References:
Following the documentation of this program I decided to report it:

> Domain takeovers supported by a proof of concept for *.mozilla.org, *.mozilla.com, *.mozilla.net, *.firefox.com, *.mozgcp.net and *.mozaws.net in addition to the list of sites in scope. If the domain is pointing to a claimed instance by another company, then the report will not be eligible for bounty.

## Impact

## Summary:

Given this is a very generic and thrust worthy domain name it is suitable for a malware campaign. Besides that it could maybe read some non-secure cookie but that is not that likely.

We could however, use the domain to block access of individual user by setting some large cookies, see for example www.firefox.com after setting 100kb of cookies via http://████/large-cookies.html

{F3852214}

This action can also be performed via eg a tracking pixel.

</details>

---
*Analysed by Claude on 2026-05-24*
