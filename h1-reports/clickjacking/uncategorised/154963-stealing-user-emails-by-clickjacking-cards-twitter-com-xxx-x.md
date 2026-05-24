# Email and Username Theft via Clickjacking on Twitter Cards

## Metadata
- **Source:** HackerOne
- **Report:** 154963 | https://hackerone.com/reports/154963
- **Submitted:** 2016-07-29
- **Reporter:** akhil-reni
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, Missing X-Frame-Options Header, UI Redressing, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twitter's card generation endpoint (cards.twitter.com) lacked X-Frame-Options headers, allowing attackers to iframe the page and conduct clickjacking attacks to steal user emails and usernames. When victims interacted with the hidden iframe, their sensitive information was exfiltrated to attacker-controlled domains.

## Attack scenario
1. Attacker creates a malicious webpage containing an invisible iframe pointing to a Twitter card URL
2. Attacker overlays visual elements on the page to trick users into clicking where the hidden iframe's button is located
3. Victim visits the attacker's webpage unaware of the hidden iframe
4. When victim clicks on what appears to be a legitimate element, they actually click the Twitter card's button within the hidden iframe
5. Twitter card processes the interaction and sends victim's email and username to attacker's domain
6. Attacker harvests the stolen credentials for further malicious purposes

## Root cause
The Twitter cards endpoint failed to implement the X-Frame-Options HTTP header (or Content-Security-Policy frame-ancestors directive) to prevent the page from being embedded in iframes on untrusted domains. This allowed any website to iframe the card content and manipulate user interaction through clickjacking.

## Attacker mindset
An attacker recognizing that Twitter cards collect user email data and lack proper framing protection saw an opportunity for large-scale credential harvesting with minimal technical complexity. The attack requires only basic HTML knowledge and can be deployed across multiple malicious sites to maximize victim reach.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN header on all user-interactive endpoints to prevent framing attacks
- Use Content-Security-Policy with frame-ancestors directive as defense-in-depth against clickjacking
- Implement frame-busting JavaScript as an additional layer: if (self !== top) { top.location = self.location; }
- Add visual indicators or warnings when pages are being accessed within frames from different origins
- Conduct security audits specifically for clickjacking vulnerabilities on all endpoints handling sensitive user data
- Consider requiring explicit user confirmation or CSRF tokens for sensitive operations like email submission
- Regular penetration testing focused on framing and UI redressing attacks

## Variant hunting
Check other Twitter endpoints (tweet composer, DM interface, settings pages) for missing framing headers
Test third-party card providers and embedded content platforms for similar clickjacking vulnerabilities
Investigate whether other social media platforms (Facebook, LinkedIn, TikTok) have similar card endpoints susceptible to framing
Look for endpoints that combine form submission with user authentication to identify high-value clickjacking targets
Test for double-framing attacks where nested iframes might bypass certain protections
Check for bypasses using sandbox attribute or other iframe restrictions that might have false security posture

## MITRE ATT&CK
- T1189 - Drive-by Compromise (malicious webpage delivery)
- T1598 - Phishing (credential harvesting)
- T1566 - Phishing (getting victims to visit malicious site)
- T1539 - Steal Web Session Cookie (potential for authenticated session hijacking)
- T1040 - Network Sniffing (observing exfiltrated emails)

## Notes
This is a classic clickjacking vulnerability with significant real-world impact due to Twitter's large user base. The attack is trivial to execute and requires no special permissions or user-agent spoofing. The report demonstrates good security research practices by providing clear proof-of-concept code. This vulnerability class remains prevalent because many developers overlook the importance of framing headers despite being a OWASP Top 10 issue. The report date (2016) predates widespread browser adoption of SameSite cookies but framing headers were already well-established security practice.

## Full report
<details><summary>Expand</summary>

**Hello**

In twitter you can create cards to generate leads.
For example:
https://twitter.com/i/cards/tfw/v1/759046372544741376?cardname=promotion&autoplay_disabled=true&earned=true&lang=en&card_height=357

If you visit the above URL and click the button your email and username is sent to my domain.

Since this page is missing X-FRAME-HEADERS,
a user could simply iframe the URL and could steal victim's emails.

**Proof of concept code**
```
<html>
<iframe src=https://twitter.com/i/cards/tfw/v1/759046372544741376?cardname=promotion&autoplay_disabled=true&earned=true&lang=en&card_height=357>
</html>
```

**Regards,
Akhil**

</details>

---
*Analysed by Claude on 2026-05-24*
