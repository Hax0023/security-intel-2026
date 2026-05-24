# Subdomain Takeover on proxies.sifchain.finance pointing to Vercel

## Metadata
- **Source:** HackerOne
- **Report:** 1487793 | https://hackerone.com/reports/1487793
- **Submitted:** 2022-02-21
- **Reporter:** hrdfrdh
- **Program:** Sifchain
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain proxies.sifchain.finance is configured with a CNAME pointing to Vercel (cname.vercel-dns.com) but the corresponding Vercel project no longer exists or is not claimed. An attacker can create a Vercel project and claim this subdomain to host arbitrary content. This enables phishing, malware distribution, and brand impersonation attacks against Sifchain users.

## Attack scenario
1. Attacker identifies that proxies.sifchain.finance resolves to unclaimed Vercel infrastructure via DNS CNAME record
2. Attacker creates a Vercel account and registers a new project
3. Attacker adds proxies.sifchain.finance as a custom domain in Vercel project settings
4. Attacker creates a fake login page or malicious content on the Vercel project mimicking Sifchain's legitimate services
5. Users attempting to access proxies.sifchain.finance are redirected to attacker's malicious site hosted on Vercel
6. Attacker harvests credentials, injects malicious code, or distributes malware while maintaining appearance of legitimacy

## Root cause
DNS CNAME record for proxies.sifchain.finance points to Vercel infrastructure but the corresponding Vercel project has been deleted, removed, or never properly claimed. Dangling DNS records create a window of opportunity for subdomain takeover when the target service allows new users to claim unclaimed domains.

## Attacker mindset
An opportunistic attacker scanning for dangling DNS records targeting popular web hosting platforms. The attacker recognizes this as an easy path to impersonate a legitimate DeFi platform, steal user credentials, or distribute malware with built-in trust from the domain reputation.

## Defensive takeaways
- Regularly audit all DNS records (A, CNAME, MX, NS) for dangling or obsolete entries pointing to third-party services
- Implement a process to claim or delete subdomains on all external hosting platforms (Vercel, GitHub Pages, Heroku, AWS, etc.) when no longer in use
- Maintain an inventory of all subdomains and their corresponding services with ownership assignments
- Use DNS monitoring tools to detect unclaimed or misconfigured DNS records
- Implement CAA records to restrict certificate issuance on company domains
- For critical subdomains, consider using subdomain validation mechanisms or service-specific security configurations
- Establish DNS hygiene as part of infrastructure maintenance and cleanup procedures
- Monitor for DNS changes and alert on modifications to critical subdomain configurations

## Variant hunting
Look for other Sifchain subdomains pointing to third-party platforms (GitHub Pages, Heroku, AWS S3, Azure, Firebase, etc.). Check for similar patterns across other crypto/DeFi projects. Scan for CNAME records pointing to services with unclaimed domain policies. Review git history or wayback machine to identify deprecated services still referenced in DNS.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1589: Gather Victim Identity Information
- T1583: Acquire Infrastructure
- T1598: Phishing for Information
- T1566: Phishing

## Notes
This is a classic subdomain takeover vulnerability with clear exploit path and high business impact. The reporter provided excellent documentation with references to established research. The vulnerability allows complete control of the subdomain including HTTPS via Vercel's certificate handling. Immediate remediation is required as this is actively exploitable. The financial/DeFi context increases severity due to phishing risk and user trust exploitation potential.

## Full report
<details><summary>Expand</summary>

Hello Team,

Subdomain takeover vulnerabilities occur when a subdomain (subdomain.example.com) is pointing to a service (e.g. GitHub pages, Heroku, etc.) that has been removed or deleted. This allows an attacker to set up a page on the service that was being used and point their page to that subdomain. For example, if subdomain.example.com was pointing to a GitHub page and the user decided to delete their GitHub page, an attacker can now create a GitHub page, add a CNAME file containing subdomain.example.com, and claim subdomain.example.com.
Here there is a Sifchain domain  (proxies.sifchain.finance) which is pointing towards vercel pages so  this domain can be taken over can can be used to do any type of attacks mostly i can make a fake login page on your behalf and spoof your users, this is a critical vulnerability and needs to be fixed .

{F1627827}

Vulnerable url : https://proxies.sifchain.finance/

{F1627821}

Cname: cname.vercel-dns.com
Name: proxies.sifchain.finance
Type: CNAME
Class: IN

## Steps To Reproduce/Concept:

1. Visit https://vercel.com/login and login with dev sifchain account

2. Check the availability of the proxies.sifchain.finance sub domain at https://vercel.com/[YourUsername]/sveltekit/settings/domains

3. The proxies.sifchain.finance sub domain does not exist. Potential to be claimed by others

## Remediation:
Remove the cname entry or claim the subdomain proxies.sifchain.finance on vercel.com

## References:
https://github.com/EdOverflow/can-i-take-over-xyz/issues/183

{F1627822}
{F1627826}

https://github.com/EdOverflow/can-i-take-over-xyz
https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/
https://0xpatrik.com/subdomain-takeover/
http://yassineaboukir.com/blog/neglected-dns-records-exploited-to-takeover-subdomains/

Best Regards,
@hrdfrdh

## Impact

Fake website
Malicious code injection
Users tricking
Company impersonation
This issue can have really huge impact on the companies reputation someone could post malicious content on the compromised site and then your users will think it's official but it's not

</details>

---
*Analysed by Claude on 2026-05-24*
