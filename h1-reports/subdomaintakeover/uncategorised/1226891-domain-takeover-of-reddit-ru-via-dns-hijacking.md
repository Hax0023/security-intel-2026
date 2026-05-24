# Domain Takeover of Reddit.ru via DNS Hijacking

## Metadata
- **Source:** HackerOne
- **Report:** 1226891 | https://hackerone.com/reports/1226891
- **Submitted:** 2021-06-15
- **Reporter:** indianajson
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** DNS Hijacking, Improper Access Control, Domain Takeover, Dangling DNS Records
- **CVEs:** None
- **Category:** uncategorised

## Summary
Reddit.ru was vulnerable to DNS hijacking because its hosted zone was deleted from the Reg.ru DNS provider while nameserver records still pointed to Reg.ru at the registrar level. This allowed an attacker to create a new hosted zone and assume complete control of the domain, enabling phishing attacks, malware distribution, and credential harvesting.

## Attack scenario
1. Attacker reviews WHOIS records and identifies Reg.ru as authoritative nameserver for Reddit.ru
2. Attacker runs DIG query and discovers SERVFAIL error indicating missing hosted zone
3. Attacker creates new hosted zone within Reg.ru account with the same domain name
4. Attacker adds malicious DNS records (A, MX, TXT) pointing to attacker-controlled infrastructure
5. Attacker deploys phishing site or proxy using tools like Modlishka to harvest credentials
6. Attacker leverages trusted reddit.ru domain reputation to bypass email spam filters for mass phishing campaigns

## Root cause
Mismatch between registrar-level nameserver configuration (pointing to Reg.ru) and actual DNS zone management state (zone deleted from Reg.ru), creating an orphaned domain vulnerable to zone takeover by any party with access to the DNS provider.

## Attacker mindset
Opportunistic reconnaissance discovering that a major company's primary domain has misconfigured DNS infrastructure with dangling nameservers. Attacker recognizes high-value target due to brand reputation, Russian market presence, and potential for sophisticated phishing campaigns against users.

## Defensive takeaways
- Regularly audit all owned domains to verify both registrar nameserver settings AND actual hosted zones exist at authoritative DNS providers
- Implement monitoring and alerting for DNS resolution failures on critical domains
- Use DNS validation/DNSSEC to prevent unauthorized zone creation
- Maintain domain inventory and perform periodic DNS health checks across all domains
- Implement role-based access controls at DNS providers with approval workflows for zone modifications
- Ensure DNS provider access is restricted and monitored for suspicious zone creation attempts
- Document and automate DNS infrastructure provisioning to prevent manual configuration drift

## Variant hunting
Search for similar patterns in competitor domains: check if other major tech companies have dangling nameserver configurations. Look for domains where WHOIS shows different nameservers than actual DNS resolution. Scan registrar databases for domains with SERVFAIL errors or NS record mismatches. Check for other Reddit-owned domains with similar misconfiguration.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1566.002 - Phishing: Spearphishing Link
- T1598 - Phishing for Information
- T1040 - Network Sniffing
- T1557 - Man-in-the-Middle

## Notes
Reporter demonstrated responsible disclosure by creating the zone themselves to prevent malicious takeover and added identifying TXT record as proof. This is a classic DNS infrastructure management failure combining both technical misconfiguration and process failure. The vulnerability required no authentication bypass or exploitation—only DNS provider access which became available due to zone deletion.

## Full report
<details><summary>Expand</summary>

## Summary

I discovered that Reddit.ru  was vulnerable to DNS hijacking via DNS provider, Reg.ru. This would allow a malicious attacker to control the content on this domain, as well as, create email addresses associated with it... I'm going to be totally honest and say that any of us ethical hackers would have nerded out giving ourselves `@reddit.ru` emails. 

## Explanation

Reviewing the WHOIS records for [Reddit.ru](https://www.whois.com/whois/Reddit.ru) you will see that this is a Reddit-owned domain and that Reg.ru nameservers are listed as the authority for the domain. However, if you had run a DIG request on Reddit.ru you would have gotten a [SERVFAIL error](https://toolbox.googleapps.com/apps/dig/#A/Reddit.ru). This is because, despite having Reg.ru set as the authoritative nameserver with the domain's registrar, the hosted zone in Reg.ru had been deleted, allowing anyone to create the missing hosted zone and take control of the domain's content, including creating email accounts.

## Proof of Concept / Verified Takeover

I created the missing Hosted Zone within Reg.ru as a proof of concept and to keep any malicious actors from hijacking the domain before Reddit could take corrective action. For a visible proof of concept, please check the [TXT records](https://toolbox.googleapps.com/apps/dig/#TXT/Reddit.ru) for Reddit.ru, which will display:

```javascript
reddit.ru.		86400	IN	TXT	"faberge@wearehackerone"
```

## Mitigation

Removing the Reg.ru nameservers for Reddit.ru from your registrar will remove the ability for someone to take control of the domain and will remove my control of the domain. No `@reddit.ru` email for me... how sad.

## Impact

First, DNS hijacking of domains has a higher severity because this vulnerability allows a malicious attacker to completely control all aspects of a domain opening the door to a variety of sophisticated attacks including phishing attacks, and malware distribution. Worse yet, domains owned by reputable companies typically receive greater leniency for spam emails from email providers, thus allowing a malicious attacker to more widely distribute spam than would otherwise be possible.

Second, similar to subdomain takeovers, DNS hijacking has become a more severe issue with the advent of open source tools such as [Modlishka](https://github.com/drk1wi/Modlishka), which would allow a malicious actor to invisibly operate a high fidelity spoof of Reddit. Simply put, nothing would indicate to a user that the site was being controlled by someone else, however, a malicious attacker would be able to invisibly siphon sensitive information without any way to identify the domain as compromised. This would be a highly effective way to siphon Russian user's Reddit credentials.  An ideal option would be to run advertisements on Google Ads targeting  Russian searches for `reddit`. 

Third, since this is a primary domain of Reddit (reddit.ru) the value of this takeover is substantially higher for its ability to negatively impact the brand and would have proven more useful had any of the attack vectors listed above to be executed against it compared to any of the other ~1,000 domains owned by Reddit. 

Overall, this takeover presents a real and present danger to Reddit, Inc.

</details>

---
*Analysed by Claude on 2026-05-24*
