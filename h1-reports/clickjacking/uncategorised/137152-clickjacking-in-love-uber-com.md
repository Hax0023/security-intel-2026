# Clickjacking in love.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 137152 | https://hackerone.com/reports/137152
- **Submitted:** 2016-05-08
- **Reporter:** mkap
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, Missing X-Frame-Options Header, UI Redressing
- **CVEs:** None
- **Category:** uncategorised

## Summary
The love.uber.com domain lacks X-Frame-Options HTTP header protection, allowing the site to be embedded in iframes controlled by attackers. This enables clickjacking attacks where malicious content can be overlaid on legitimate UI elements to deceive users into unintended actions.

## Attack scenario
1. Attacker creates a malicious webpage and embeds love.uber.com in an invisible or semi-transparent iframe
2. Attacker overlays fake login forms or action buttons on top of the framed content
3. Attacker uses CSS positioning and opacity manipulation to make the overlay appear legitimate while concealing the actual Uber site
4. User visits attacker's page and attempts to interact with what appears to be legitimate Uber controls
5. User's clicks are redirected to attacker's fake forms, stealing credentials or triggering unintended actions
6. Attacker harvests sensitive data or performs unauthorized actions on behalf of the victim

## Root cause
The application fails to implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) to restrict iframe embedding. This allows any external website to load the vulnerable domain in an iframe without restriction.

## Attacker mindset
Opportunistic attacker leveraging a common web vulnerability to create convincing phishing or credential harvesting attacks. The attacker recognizes that trusted brand pages are high-value targets when combined with UI redressing techniques, as users are more likely to trust the visual appearance.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN HTTP header on all responses to prevent iframe embedding
- Add Content-Security-Policy header with frame-ancestors directive as defense-in-depth measure
- Conduct regular security reviews of all subdomains including marketing/specialized sites like love.uber.com
- Implement frame-busting JavaScript as an additional layer (though header-based solutions are preferred)
- Monitor for unauthorized framing attempts and alert on suspicious iframe embedding patterns

## Variant hunting
Search for other Uber subdomains lacking frame protection (*.uber.com). Verify if staging, development, or less-monitored properties share the same vulnerability. Check for subdomain takeover scenarios combined with clickjacking on legitimate-looking domains.

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1566.004

## Notes
This is a straightforward clickjacking vulnerability report. While the POC appears credible based on the description, the actual impact depends on the sensitive actions available on love.uber.com. The report lacks technical depth regarding CSRF token handling and whether the vulnerability could be chained with other attacks. The bounty amount is not disclosed in the provided content.

## Full report
<details><summary>Expand</summary>

Hi , 


Your domain love.uber.com is vulnerable to Clickjacking.

I'm able to load the domain love.uber.com in an iframe , 
so an attacker can certainly take advantage of this clickjacking bug in love.uber.com

Click-jacking is a process of “stealing” clicks on your site, redirecting them to other places,  by putting your page in an iframe and placing the attacker’s content over yours. The idea is to make this look as seamless as possible, so the user can’t tell right away that something is wrong.

if someone frames your site and puts login controls directly over yours, then even tools like SiteKey , won’t prevent them from collecting username and password data.

POC Screenshot Attached !

</details>

---
*Analysed by Claude on 2026-05-24*
