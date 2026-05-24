# Subdomain Takeover via Unclaimed Google Sites (moderator.ubnt.com)

## Metadata
- **Source:** HackerOne
- **Report:** 181665 | https://hackerone.com/reports/181665
- **Submitted:** 2016-11-11
- **Reporter:** madrobot
- **Program:** Ubiquiti Networks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Unclaimed Third-Party Service
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain moderator.ubnt.com contains a CNAME record pointing to abandoned Google Sites infrastructure (ghs.google.com), allowing an attacker to claim the unclaimed Google Site and take over the subdomain. This enables attackers to serve arbitrary content, conduct phishing attacks, or damage the company's reputation through the trusted ubnt.com domain.

## Attack scenario
1. Attacker discovers moderator.ubnt.com resolves to 216.58.203.243 (Google's infrastructure)
2. Attacker identifies the subdomain points to an unclaimed Google Sites project
3. Attacker navigates to Google Sites and claims the abandoned project using standard Google account registration
4. Upon successful claim, attacker gains full control of the subdomain's DNS resolution to their attacker-controlled Google Site
5. Attacker hosts malicious content (phishing forms, malware, credential harvesting) on the now-controlled subdomain
6. Users trust the ubnt.com domain and interact with attacker content, resulting in credential theft or malware distribution

## Root cause
Ubiquiti created a CNAME record pointing to Google Sites infrastructure but failed to properly claim and maintain the corresponding Google Site project. The abandoned resource remained unclaimed, allowing any attacker to register it and gain control over the subdomain.

## Attacker mindset
Opportunistic attacker performing reconnaissance of target domains, identifying dangling DNS records pointing to third-party services, and exploiting weak governance of abandoned properties to hijack subdomains for phishing, malware distribution, or brand damage.

## Defensive takeaways
- Maintain comprehensive inventory of all subdomains and their DNS records
- Regularly audit DNS CNAME records and verify corresponding third-party service ownership
- Implement automated monitoring to detect unclaimed or abandoned third-party resources
- Establish ownership and access controls for all third-party services (Google Sites, AWS, Azure, etc.)
- Implement DNS monitoring tools to alert on dangling DNS records
- Use subdomain takeover detection services during security assessments
- Document lifecycle management for subdomains including decommissioning procedures
- Consider using CAA records and other DNS security controls

## Variant hunting
Search for other Ubiquiti subdomains pointing to Google infrastructure (ghs.google.com, appspot.com, herokuapp.com, GitHub Pages, etc.). Check for subdomains pointing to abandoned AWS S3 buckets, Azure blob storage, Firebase projects, or other third-party services with user-claimable namespaces.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1566.002 - Phishing: Spearphishing Link
- T1589.001 - Gather Victim Identity Information: Credentials

## Notes
This is a duplicate of report #179110. The reporter provided video proof-of-concept demonstrating successful claim of the subdomain. The vulnerability is particularly high-impact given the trust users place in the ubnt.com domain and Ubiquiti's position as a network equipment manufacturer. Subdomain takeover via dangling DNS is a well-known attack class (documented in bug bounty reports since 2014+) that should be detected through standard reconnaissance scans.

## Full report
<details><summary>Expand</summary>

Hello __Team__

This report is same as #179110

One of your subdomain http://moderator.ubnt.com is pointing towards
```
216.58.203.243    moderator.ubnt.com
216.58.203.243    ghs.google.com
216.58.203.243    ghs.l.google.com
```
{F134183}
And it is unclaimed

When I open it 
it is showing 

{F134184}

__Impact__ :-
An attacker can claim this subdomain by requesting a process of registering this abandoned subdomain to his name.

And attacker can fully take over this subdomain and do whatever he wants. this can cause huge damage to the website's main domain as well as to the company.

I Recommend removing  the Cname and DNS connecting to it.

You can read about this sort of attacks here : https://www.siteground.com/tutorials/googleapps/google_calendar.htm

To clarify your doughs I just added video POC

>1ST Video Is about how I am able to claim it https://youtu.be/51Ku4cGbijE
>2ND Video is proof when trying to claim it for the second time https://youtu.be/GJcWsHJj8aE

</details>

---
*Analysed by Claude on 2026-05-24*
