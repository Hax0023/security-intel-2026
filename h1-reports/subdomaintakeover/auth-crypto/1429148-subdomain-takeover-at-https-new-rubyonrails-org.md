# Subdomain Takeover at https://new.rubyonrails.org/

## Metadata
- **Source:** HackerOne
- **Report:** 1429148 | https://hackerone.com/reports/1429148
- **Submitted:** 2021-12-16
- **Reporter:** nagli
- **Program:** Ruby on Rails
- **Bounty:** Not specified (reported as OOS)
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain new.rubyonrails.org was pointing to an unclaimed GitHub Pages repository, allowing an attacker to claim it and host arbitrary content. This DNS misconfiguration created a subdomain takeover vulnerability on a high-profile domain that could be exploited for phishing, malware distribution, or stealing cookies.

## Attack scenario
1. Attacker discovers that new.rubyonrails.org resolves to an unclaimed GitHub Pages domain
2. Attacker creates a GitHub account and registers a repository matching the expected GitHub Pages naming convention
3. GitHub allows the attacker to claim the subdomain through their repository
4. Attacker deploys malicious HTML/JavaScript content to the claimed subdomain
5. Legitimate users visiting new.rubyonrails.org are served attacker-controlled content
6. Attacker exploits shared root domain cookies or launches phishing/malware campaigns leveraging trusted domain reputation

## Root cause
DNS CNAME record pointing to a GitHub Pages domain that was never claimed or was abandoned without proper cleanup. The organization failed to either maintain active ownership of the GitHub repository or remove the DNS record when the repository was no longer in use.

## Attacker mindset
Opportunistic reconnaissance of subdomain infrastructure; easy wins via abandoned/misconfigured DNS records pointing to third-party hosting services. High-value target due to domain reputation and potential for cookie theft or phishing campaigns.

## Defensive takeaways
- Regularly audit all DNS records and remove or update dangling CNAME records pointing to third-party services
- Implement monitoring to detect unclaimed subdomains resolving to hosting providers (GitHub Pages, Heroku, AWS, etc.)
- Use subdomain takeover detection tools as part of security scanning pipeline
- Establish DNS hygiene practices: document all DNS records and their purpose; set expiration policies for unused records
- For GitHub Pages: either maintain active repository ownership or explicitly remove DNS records
- Implement DNSSEC and CAA records to prevent unauthorized service binding
- Use automated tooling (e.g., SubDomainizer, Nuclei templates) to scan for common takeover vectors

## Variant hunting
Scan all subdomains of ruby-related domains for similar dangling DNS records
Check other Rails-related properties (rubyonrails.com, railsguidelines.org, etc.) for abandoned subdomains
Search for CNAME records pointing to Heroku, Vercel, Netlify, AWS CloudFront, Azure, or other hosting services
Test other common subdomain patterns (staging., dev., api., blog., etc.) for takeover vulnerabilities
Monitor Certificate Transparency logs for issuance to rubyonrails.org subdomains that may indicate attacker activity

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1584.001 - Compromise Infrastructure: Domains
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
Reporter explicitly noted the issue is out-of-scope (OOS) but emphasized severity due to domain reputation. The finding demonstrates that even high-profile organizations can have DNS misconfigurations. The simple proof-of-concept (serving HTML file) was sufficient to demonstrate the vulnerability. Subdomain takeovers on primary domains are particularly dangerous as they can inherit trust and cookie permissions from parent domain.

## Full report
<details><summary>Expand</summary>

## Disclaimer

I know it's OOS but the issue is pretty serious because of the attractive domain name "new.rubyonrails.org" basically anyone could have put malware there.

## Summary
Hi!

I discovered that new.rubyonrails.org was pointing to an unclaimed Github Page, making it vulnerable to subdomain takeover.
I've managed to claim it in my Github-account and added a simple html file as POC:

{F1548667}

`https://new.rubyonrails.org`

## Mitigation
- Remove the DNS record

Best regards,
nagli

## Impact

Subdomain takeovers can be used for
- Cookies set to the root domain will be shared with this subdomain and can be obtained
- Stored XSS (arbitrary javascript code can be executed in a users browser)
- Phishing
- Hosting malicious content

</details>

---
*Analysed by Claude on 2026-05-24*
