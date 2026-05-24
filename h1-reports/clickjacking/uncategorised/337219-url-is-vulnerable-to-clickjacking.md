# Clickjacking Vulnerability - Missing X-Frame-Options Header on Zomato

## Metadata
- **Source:** HackerOne
- **Report:** 337219 | https://hackerone.com/reports/337219
- **Submitted:** 2018-04-13
- **Reporter:** hacker_one_one
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple Zomato URLs lack X-Frame-Options header protection, allowing attackers to embed pages in iframes and perform clickjacking attacks. An attacker can trick users into unknowingly initiating actions such as modifying account settings, deleting accounts, or changing sensitive user data through UI redressing techniques.

## Attack scenario
1. Attacker creates a malicious webpage containing an invisible iframe pointing to a Zomato user settings page (e.g., /users/[id]/edit)
2. Attacker overlays transparent UI elements on top of the iframe with enticing clickable content (e.g., 'Click here to win a prize')
3. Victim visits the attacker's webpage and clicks on the visible overlay, which unknowingly clicks on hidden Zomato UI elements
4. Victim's authenticated session with Zomato processes the unintended action (e.g., changing email, deleting account, modifying profile)
5. Changes are persisted without victim's knowledge due to existing authentication session
6. Attacker achieves account compromise or data manipulation goals

## Root cause
Zomato failed to implement the X-Frame-Options HTTP response header set to 'DENY' or 'SAMEORIGIN' on sensitive URLs, allowing pages to be embedded in frames from external origins. This is particularly critical for pages handling user actions and sensitive operations.

## Attacker mindset
Attacker recognized that many web applications fail to implement basic clickjacking protections and systematically tested multiple Zomato URLs to identify vulnerable endpoints. The attacker specifically targeted user management and account modification pages where unauthorized actions would have maximum impact.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all pages, especially those with sensitive operations
- Deploy Content-Security-Policy (CSP) frame-ancestors directive as modern replacement for X-Frame-Options
- Apply frame-busting JavaScript code as additional layer of protection for sensitive pages
- Conduct security headers audit across entire application to ensure consistent protection
- Implement SameSite cookie attributes to limit CSRF/clickjacking effectiveness
- Require additional confirmation for sensitive operations (e.g., account deletion, email changes)
- Test security header implementation across different browser versions and configurations

## Variant hunting
Check for missing X-Frame-Options on API endpoints and administrative pages
Test whether CSP frame-ancestors is properly implemented if X-Frame-Options is present
Identify other sensitive operations (payment processing, credential changes) vulnerable to clickjacking
Check if different subdomains have inconsistent security header configurations
Test whether frame-busting code can be bypassed through sandbox attributes or other techniques
Verify protection across mobile app webviews and different user agent scenarios
Test POST-based sensitive operations for CSRF + clickjacking combination attacks

## MITRE ATT&CK
- T1185
- T1566.002

## Notes
Report demonstrates successful exploitation in IE browser specifically, suggesting potential browser-specific bypass or configuration issues. The vulnerability affects multiple URL categories (user profiles, location pages, marketplace pages), indicating systematic missing of security headers across the application rather than isolated instances. The provided proof-of-concept uses frameset which is outdated but effectively demonstrates the vulnerability. Modern exploitation would use iframe-based approaches for better user experience during attack.

## Full report
<details><summary>Expand</summary>

##The browser has verified the identity:
Successfully implemented in IE browser

##Reproduce steps:
URLs do not have X-FRAME-OPTIONS set to DENY or SAMEORIGIN, and they are vulnerable to clickjacking.
Run under the browser's code and you will see that the listed links are vulnerable to clickjacking attacks
```
<html>
	<frameset cols="25%,25%,25%">
		<frame src="https://www.zomato.com/robots.txt" />
		<frame src="https://www.zomato.com/users/fan-feng-52680914" />
		<frame src="https://www.zomato.com/cairns-qld" />
	</frameset>
</html>
```
{F285366}

## Impact

Most of the zomato.com urls were tested and found that most basic urls support iframe display in IE.

E.g:
* https://www.zomato.com/users/fan-feng-52680914/edit
* https://www.zomato.com/invite
* https://www.zomato.com/cairns-qld
* https://www.zomato.com/cairns-qld/caffiend-cairns?zrp_bid=0&zrp_pid=14
* https://www.zomato.com/users/fan-feng-52680914/bookmarks
* https://www.zomato.com/users/fan-feng-52680914/managewallets

The hacker selected the **UI Redressing (Clickjacking)** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
*.zomato.com

**Can a victim be tricked into unknowingly initiating a specific action?**
Yes

**What specific action can the user be tricked into?**
E.g: Hackers can lure users into the personal settings page, change data that is useful to hackers, delete accounts...

</details>

---
*Analysed by Claude on 2026-05-24*
