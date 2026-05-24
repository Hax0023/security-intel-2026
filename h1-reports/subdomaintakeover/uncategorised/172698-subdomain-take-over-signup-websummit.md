# Subdomain Takeover: signup.websummit.net pointing to unclaimed Heroku application

## Metadata
- **Source:** HackerOne
- **Report:** 172698 | https://hackerone.com/reports/172698
- **Submitted:** 2016-09-28
- **Reporter:** glc
- **Program:** Web Summit
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain signup.websummit.net contains a CNAME record pointing to wsv1.herokuapp.com, a Heroku application that was never claimed or secured by Web Summit. An attacker could register this Heroku app name and serve malicious content, impersonating the company to steal credentials or distribute malware. The 'signup' subdomain makes this particularly dangerous as it targets user registration flows.

## Attack scenario
1. Attacker discovers signup.websummit.net resolves to unclaimed wsv1.herokuapp.com via DNS enumeration
2. Attacker registers wsv1 application on Heroku platform, gaining control of the DNS resolution
3. Attacker clones the legitimate Web Summit signup page and hosts it on their Heroku instance
4. Attacker distributes phishing links via email or forums pointing to signup.websummit.net
5. Users trust the legitimate domain name and enter credentials on the attacker-controlled fake signup page
6. Attacker harvests credentials and uses them to compromise user accounts or resell the data

## Root cause
Web Summit delegated the signup.websummit.net subdomain to Heroku via CNAME record (wsv1.herokuapp.com) but failed to register or claim ownership of the target application on the Heroku platform. When the Heroku app was decommissioned without being explicitly removed from DNS records, it became available for anyone to claim.

## Attacker mindset
Reconnaissance-focused adversary exploiting common operational oversight. The attacker recognized the high-value nature of 'signup' subdomain and the ease of exploiting unclaimed third-party services. Low effort, high reward attack targeting credential harvesting through impersonation.

## Defensive takeaways
- Maintain an inventory of all DNS records, especially CNAME entries pointing to third-party services
- When decommissioning external services, immediately remove associated DNS records
- Claim and secure all subdomains on third-party platforms (Heroku, GitHub Pages, etc.) even if not currently in use
- Implement regular subdomain enumeration and validation to detect dangling DNS records
- Monitor for unauthorized content hosted on your delegated subdomains
- Use subdomain takeover detection tools and services as part of security monitoring
- Document which third-party services are authorized to serve content under company domains

## Variant hunting
Scan entire domain for other CNAME records pointing to external services (GitHub Pages, AWS S3, Azure, Heroku, etc.)
Check for MX records pointing to unclaimed third-party email services
Look for A/AAAA records pointing to IP addresses no longer in use or belonging to third-party services
Enumerate common subdomains (www, mail, signup, login, api, cdn, etc.) for similar misconfigurations
Review historical DNS records using WHOIS/Shodan to identify previously active services
Test other subdomains for similar takeover vulnerabilities across the organization

## MITRE ATT&CK
- T1583.001
- T1589.001
- T1190
- T1566.002

## Notes
Researcher responsibly claimed the vulnerable subdomain on Heroku to prevent exploitation and offered to return it. This is a textbook subdomain takeover vulnerability with clear credential harvesting intent. Web Summit should audit all external DNS delegations immediately. The vulnerability affects user trust in the signup process and directly enables phishing/credential theft.

## Full report
<details><summary>Expand</summary>

Subdomain take over



Hi,

You have a subdomain aka `signup.websummit.net` that point to a third party service hosted on Heroku: `wsv1.herokuapp.com`. The nslookup command shows the DNS configuration.

```
$ nslookup signup.websummit.net 8.8.8.8
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
signup.websummit.net	canonical name = wsv1.herokuapp.com.
wsv1.herokuapp.com	canonical name = us-east-1-a.route.herokuapp.com.
Name:	us-east-1-a.route.herokuapp.com
Address: 23.23.94.135
```

However it seems that your didn't own/claim the name `wsv1` on Heroku. That means an attacker could take it and trick your users/staff by copying your primary website and design.


**PoC:**

See the attached screenshots.


**Risk:**

- fake website
- malicious code injection
- users tricking
- company impersonation

Since the vulnerable subdomain is called `signup`, it's a perfect place to create a fake login/subscribe page to steal users credentials. An attacker would post links on forums or send emails and then wait for people to signup on the site he owns.


**Remediation:**

Remove the cname entry or claim the subdomain `wsv1` on Heroku.
See also:
https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/
https://medium.com/@atom/subdomain-takeover-through-external-services-f0f7ee2b93bd#.hglqnm2gg
http://yassineaboukir.com/blog/neglected-dns-records-exploited-to-takeover-subdomains/


Note that I claimed the domain on Heroku, let me know if you want to get it back, I'll delete it soon.

</details>

---
*Analysed by Claude on 2026-05-24*
