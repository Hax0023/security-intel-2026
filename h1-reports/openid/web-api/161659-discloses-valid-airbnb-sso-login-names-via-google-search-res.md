# Airbnb SSO Gateway Discloses Valid Employee Login Names via Google Search Indexing

## Metadata
- **Source:** HackerOne
- **Report:** 161659 | https://hackerone.com/reports/161659
- **Submitted:** 2016-08-20
- **Reporter:** aesteral
- **Program:** Airbnb
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, Missing Security Controls
- **CVEs:** None
- **Category:** web-api

## Summary
An Airbnb SSO gateway domain lacked a robots.txt file, allowing Google crawlers (via Chrome and Google Toolbar) to index URLs containing valid employee login names. This exposed internal directory structure with usernames like /people/alice_brown, making valid @airbnb.com account names searchable via Google.

## Attack scenario
1. Attacker discovers the internal SSO domain is indexed by Google
2. Attacker performs Google dorking query (site:xxxxx) to enumerate valid login names
3. Attacker harvests a list of confirmed valid Airbnb employee usernames from search results
4. Attacker uses usernames for credential stuffing, password spraying, or weak password testing
5. Attacker performs social engineering attacks using confirmed employee names and email patterns
6. Attacker potentially gains unauthorized access to Airbnb corporate systems or services

## Root cause
Missing robots.txt file on the SSO gateway domain combined with the domain being accessible to Google's crawlers via browser telemetry (Chrome, Google Toolbar), despite corporate network segmentation. The application exposed user profile URLs with valid usernames in a predictable URL pattern without search engine exclusion directives.

## Attacker mindset
Reconnaissance-focused attacker leveraging publicly available information (Google search) to build intelligence on Airbnb's internal structure. Threat actor seeks valid usernames as stepping stones for targeted attacks against corporate infrastructure, credential compromise, or social engineering campaigns.

## Defensive takeaways
- Implement robots.txt with 'Disallow: /' to prevent search engine indexing of internal/corporate domains
- Use X-Robots-Tag HTTP header as defense-in-depth to signal no-index to crawlers
- Restrict access to corporate-only domains via network segmentation or VPN requirements
- Disable Chrome telemetry and Google Toolbar data reporting for corporate domains
- Implement authentication and authorization controls to block public URL enumeration
- Regularly audit Google Search Console and perform dorking queries for unintended indexing
- Use noindex meta tags on sensitive pages as additional layering
- Implement rate limiting and access controls on profile/user enumeration endpoints

## Variant hunting
Search for other Airbnb internal domains indexed by Google using site: operators
Check for similar URL patterns revealing employee directories on other SSO gateways
Enumerate subdomains for corporate infrastructure with missing robots.txt
Look for cached versions in Google Cache, Wayback Machine, or archive.org
Test for username enumeration via error messages on login pages
Check for exposed directory listings or auto-indexing of /people/ or similar directories
Search for data breaches or pastes containing Airbnb employee account lists

## MITRE ATT&CK
- T1598.003
- T1589.001
- T1589.002
- T1592.004
- T1591.004
- T1657

## Notes
Report highlights the intersection of security misconfigurations and modern browser/service telemetry. Despite the domain being corporate-network-restricted, Google's products inadvertently crawled and indexed it. This is a low-cost/high-impact reconnaissance vulnerability enabling downstream attacks. The severity is amplified in security-conscious organizations where employee names and email patterns are sensitive. Remediation is straightforward but requires understanding of SEO controls and search engine directives.

## Full report
<details><summary>Expand</summary>

Hello,

There is an Information leakage type weakness present on ███████ which supposedly works as a Single Sign On (SSO) gateway for Airbnb's corporate services. The weakness is present due to lack of robots exclusions policy file (robots.txt) present on this domain which allows web crawlers such as Google add URLs within this domain into their search indexes.

While ██████ is situated behind the coprorate network boundary and is not accessible from the Internet URLs which would generally make it unindexable by Google or other search engines various Google-made products like Chrome browser or Google Toolbar report URLs users open to Google which then adds those into the index making them searchable.

██████████ employs the following URL structure: https://████/people/alice_brown where alice_brown is a valid login name in Airbnb SSO an usually a valid address in @airbnb.com domain. You can see a certain amount of such valid login names at the following Google SERP URL: https://www.google.com/#q=site:██████████&filter=0

This information should obviously be kept private since it gives a malicious party additional knowledge about Airbnb's SSO system, valid account names to test for weak passwords and information for social engineering attacks against Airbnb's empolyees.

It is advised to make these URLs not indexable by supplying Google with a restrictions policy (robots.txt) for this domain.

</details>

---
*Analysed by Claude on 2026-05-24*
