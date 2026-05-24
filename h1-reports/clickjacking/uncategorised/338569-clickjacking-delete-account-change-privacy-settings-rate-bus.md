# Clickjacking: Delete Account, Change Privacy Settings, Rate Business, Follow/Unfollow (IE)

## Metadata
- **Source:** HackerOne
- **Report:** 338569 | https://hackerone.com/reports/338569
- **Submitted:** 2018-04-15
- **Reporter:** foobar7
- **Program:** Zomato
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header, Insufficient CSP frame-ancestors Directive
- **CVEs:** None
- **Category:** uncategorised

## Summary
Zomato's application lacks X-Frame-Options header protection, allowing pages to be embedded in iframes and subjected to clickjacking attacks in Internet Explorer. Attackers can trick users into performing sensitive actions including account deletion, privacy setting changes, and business ratings through overlaid invisible or semi-transparent frames.

## Attack scenario
1. Attacker creates a malicious webpage hosted on a real domain (not local file) to ensure cookie transmission in IE
2. Attacker embeds a semi-transparent Zomato page within an iframe on their webpage, reducing opacity to 0.2 for visibility
3. Attacker positions invisible divs or uses JavaScript to track the victim's mouse movements and overlay clickable elements on sensitive buttons
4. Victim visits the attacker's webpage and clicks on what appears to be legitimate content on the attacker's page
5. The victim's clicks are actually directed to hidden Zomato buttons (e.g., delete account, change privacy settings, rate business) within the iframe
6. Sensitive actions are executed on the victim's Zomato account without their knowledge or consent

## Root cause
The application fails to implement the X-Frame-Options HTTP response header and relies solely on CSP frame-ancestors directive, which is not enforced in Internet Explorer. This allows the page to be embedded in iframes from any origin, enabling clickjacking attacks.

## Attacker mindset
An attacker could exploit this to manipulate business ratings, delete competitor or victim accounts, expose private profiles by changing privacy settings, or engage in reputation damage by modifying account settings. Business competitors could artificially inflate their own ratings or sabotage rivals.

## Defensive takeaways
- Implement X-Frame-Options header (set to DENY or SAMEORIGIN) as a primary defense mechanism
- Ensure CSP frame-ancestors directive is properly configured and tested across all browsers, especially legacy ones
- Implement token-based CSRF protection for sensitive state-changing operations
- Add user interaction verification for critical actions (e.g., account deletion requires additional confirmation)
- Disable pointer-events on sensitive UI elements or use alternate interaction methods that cannot be clickjacked
- Implement SameSite cookie attribute to limit cookie transmission in cross-origin iframe contexts
- Test security headers across all supported browsers including Internet Explorer
- Consider deprecating IE support or implementing additional protective measures for legacy browser users

## Variant hunting
Check for similar missing X-Frame-Options headers on other critical pages (settings, payment, API endpoints)
Test other state-changing operations (password changes, email modifications, payment method updates) for clickjacking vulnerability
Investigate if the CSP frame-ancestors directive is present but bypassable through other means
Look for other legacy browser-specific security header bypasses (Edge, older Chrome versions)
Test if JavaScript-based origin validation can be bypassed through document.domain manipulation
Search for other sensitive endpoints that accept iframe embedding (admin panels, user profiles, business management)

## MITRE ATT&CK
- T1189 - Drive-by Compromise
- T1566 - Phishing
- T1204 - User Execution
- T1539 - Steal Web Session Cookie

## Notes
The vulnerability is limited to Internet Explorer because Firefox and Chrome enforce the CSP frame-ancestors directive. The attacker requires a real domain for the malicious page to ensure IE sends authentication cookies. A more sophisticated attack could use JavaScript to dynamically follow the victim's mouse pointer, reducing the precision required for clickjacking. The report references a related vulnerability #337219, suggesting a pattern of inadequate framing protections.

## Full report
<details><summary>Expand</summary>

Inspired by report #337219. Please note that this report includes a clear security impact as well as a proof of concept. 

CVSS
----

medium 5.0 [CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L)

Description
-----------

The application does not send a X-Frame-Options header, thus allowing pages to be included in iFrames.

There are some specific actions which can be performed with clicks:

- DOS: Deleting an account (requires 3 clicks)
- Confidentiality/Integrity: Change privacy & notification settings (disabling of "Hide my profile from search engines" / "Prevent my profile from showing up in search results" as well as enabling/disabling of newsletters)
- Integrity: Following/Unfollowing users (requires 1 click), Rating a business (requires 2 clicks), Changing the language of the site, etc. Among other, a business could use this to influence its own rating.

Note that attacks will only work in Internet Explorer.  The CSP directive `frame-ancestors` will prevent inclusion of the page in frames in Firefox and Chrome.

Proof of Concept
----------------

Rate a business:

    <div style="position: absolute; left: 430px; top: 490px; pointer-events: none;">Click 1</div>
    <div style="position: absolute; left: 650px; top: 535px; pointer-events: none;">Click 2</div>
    <iframe style="opacity: 0.2;" height="1000" width="1000" scrolling="no" src="https://www.zomato.com/szczecin/bajgle-kr%C3%B3la-jana-%C5%9Br%C3%B3dmie%C5%9Bcie"></iframe>

The following proof of concepts are specific to one user (in this example with the ID 53373042). A general POC which can be reused across users would require two more clicks (opening the menu drop-down + click on settings).

Delete an Account:

    <div style="position: absolute; left: 70px; top: 860px; pointer-events: none;">Click 1</div>
    <div style="position: absolute; left: 330px; top: 600px; pointer-events: none;">Click 2 & 3</div>
    <iframe style="opacity: 0.2;" height="1000" width="1000" scrolling="no" src="https://www.zomato.com/users/simone-eisenberg-53373042/edit"></iframe>

Change privacy settings: 

	<div style="position: absolute; left: 70px; top: 825px; pointer-events: none;">Click 1</div>
	<div style="position: absolute; left: 295px; top: 900px; pointer-events: none;">Click 2</div>
	<iframe style="opacity: 0.2;" height="1000" width="1000" scrolling="no" src="https://www.zomato.com/users/simone-eisenberg-53453315/edit"></iframe>

Tested with IE11. Note that the script needs to be called on a real domain - not from a local file - as IE will otherwise not send the required cookies.

In a real attack, the zomato page would not be displayed. Javascript could also be used to automatically follow the users mouse pointer, so that a user would only need to click x times anywhere on a page instead of needing to click the specific labels.

## Impact

Delete Account, change privacy settings, rate a business, follow/unfollow, etc.

The hacker selected the **UI Redressing (Clickjacking)** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://www.zomato.com/

**Can a victim be tricked into unknowingly initiating a specific action?**
Yes

**What specific action can the user be tricked into?**
Delete Account, change privacy settings, rate a business, follow/unfollow, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
