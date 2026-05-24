# Domain Takeover Risk on doesfranshaveashell.com Due to Expiration

## Metadata
- **Source:** HackerOne
- **Report:** 692068 | https://hackerone.com/reports/692068
- **Submitted:** 2019-09-10
- **Reporter:** magic_spell
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Domain Expiration/Takeover, Typosquatting Vulnerability, Subdomain Hijacking Risk
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The researcher reported that the domain doesfranshaveashell.com expired on 2019-09-02 and was serving advertisements instead of legitimate content. If the domain owner fails to renew before the grace period expires, an attacker could register the expired domain or a similar typosquatted variant to perform phishing, credential theft, or other malicious activities.

## Attack scenario
1. Attacker monitors the expired domain and discovers it has entered the redemption/grace period with no renewal activity
2. Attacker registers a typosquatted variant (e.g., doesfranhaveashell.com) or waits for the grace period to end to claim the original domain
3. Attacker clones the legitimate website content using cached versions from search engines
4. Attacker hosts phishing pages, credential harvesting forms, or distributes malware through the newly controlled domain
5. Users visiting the expired domain or typosquatted variant are redirected to attacker's malicious site
6. Attacker steals user sessions, credentials, or performs UI redress attacks to compromise user accounts and data

## Root cause
Domain expiration without timely renewal. The registrar may have failed to send adequate renewal reminders, or the domain owner neglected to enable auto-renewal. The grace period and redemption period create a window of opportunity for domain hijacking.

## Attacker mindset
Opportunistic cybercriminal seeking to abuse an abandoned asset. The attacker views the expiration as a low-cost entry point ($9.88/year) to launch phishing campaigns, steal credentials, distribute malware, or perform typosquatting attacks against users with muscle memory or bookmarks to the original domain.

## Defensive takeaways
- Enable automatic domain renewal at the registrar to prevent expiration lapses
- Set up proactive renewal reminders 60-90 days before expiration
- Register common typosquatted variants of your domain to prevent attacker registration
- Monitor WHOIS records and domain status changes regularly
- Implement DNSSEC to prevent DNS hijacking
- Establish a domain renewal process with multiple stakeholders to ensure continuity
- Consider registering your domain for multi-year periods to reduce renewal overhead
- Use domain monitoring tools to alert on status changes and expiration dates

## Variant hunting
Search for other expired or expiring domains belonging to the same organization
Monitor registrar new domain registrations similar to the organization's domain portfolio
Check for newly registered typosquatted domains that target the organization's primary domains
Investigate subdomain hijacking on expired subdomains with dangling DNS records
Review DNS history and WHOIS history to identify patterns of domain management neglect

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing for Information: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1187 - Forced Authentication

## Notes
This report demonstrates a common but often overlooked vulnerability in organizational infrastructure management. The researcher provided detailed threat modeling including typosquatting, phishing, and credential theft scenarios. The domain status was 'clientTransferProhibited' at report time, which offered some protection, but the grace period represented a critical window. This type of vulnerability requires organizational discipline rather than technical patching. The researcher demonstrated good security hygiene by responsibly disclosing the risk rather than exploiting it.

## Full report
<details><summary>Expand</summary>

###Summary

Hi Ed,

I'm not so sure if registrar inform your domain had expired or it will auto renew upon reaching. To be safe, I decide to manual inform you.

###Step to Reproduce

So lately I notice that http://doesfranshaveashell.com/ is no longer operate. It will show some advertisements there.

{F579676}



 It was expired on 2019-09-02. Latest status is `clientTransferProhibited`, which is currently locked for being transferable to another host party. Which I believe is a good news.

{F579687}
https://www.whois.com/whois/doesfranshaveashell.com

So PoC is that I'll get 404 page return by current time as I going http://doesfranshaveashell.com/keybase.txt.
{F579688}


Here is the PoC cache page I able to pull out, 28 August 2019 from Google storage. Not sure how long cache page serving soon.
{F579691}

###Scenario of exploit
As latest status is `clientTransferProhibited`, which  limit the security risk. Exploit person usually perform another typosquatting attack.

As quoted phrases from https://www.namecheap.com/security/domain-phishing-security-attacks-guide/

1. Typosquatting

```
Singular and Plural Versions - Buy both versions of your domain name to be on the safe side, portland-car-repair.com and portland-car-repairers.com for example.
```

Exploit person will buy doesfranhaveashell.com at $9.88/year to trick user. They can craft same page just like the previous cache page, add extra new features & declare that real doesfranshaveashell.com no longer in operating since expired reach out, by making official statement. It fact it just missing a letter 's' from initial domain.

Here is the order summary & cost;
{F579708}

Exploit person could perform variant of attack, example stealing cookies from victim session, or perform UI redress attack. They can frame out target page they like to trick user redirected links from doesfranhaveashell.com . 
Or create imitation login forms to steal victim real username account & password, by claiming will send 
monthly newsletters to subscriber. Or registered account could benefit some gift.

When doesfranshaveashell.com change status to release, they will purchase immediately to takeover this domain from owner, which is you.

___
As I am not sure how long is the grace period available by registrar. Some registrar offer days, one week, or up to months. While some offer extra redemption period as well to customer.




Nevertheless, hope this could help as a small reminder that your domain recently expired.

Best regards,

## Impact

- Not timely renewed or restored after expiration, domain might be made purchase available for others registration on a first-come-first-served basis.
- Pass out grace period might release status to be ready purchase by exploit person to takeover domain

</details>

---
*Analysed by Claude on 2026-05-24*
