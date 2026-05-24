# Clickjacking on Important Functions of Yelp

## Metadata
- **Source:** HackerOne
- **Report:** 305128 | https://hackerone.com/reports/305128
- **Submitted:** 2018-01-16
- **Reporter:** hk755a
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple critical user interaction functions on Yelp.com lack clickjacking protection, allowing attackers to trick users into performing unintended actions such as reporting profiles, following users, or sending compliments through hidden iframes. The vulnerability bypasses CSRF protections by requiring minimal user interaction (a single click) and affects user trust and platform reputation.

## Attack scenario
1. Attacker crafts a malicious webpage containing hidden iframes that load Yelp functionality URLs (report profile, follow user, send compliment)
2. Attacker embeds these iframes with transparent overlays or disguises them as legitimate clickable content on the attacker's website
3. Victim visits the malicious webpage while logged into Yelp
4. Victim unknowingly clicks on what appears to be legitimate content, but actually clicks the transparent iframe triggering the Yelp action
5. The victim's authenticated session executes unintended actions (reporting innocent profiles, sending offensive messages, or following unwanted users)
6. Victim realizes the harm caused to other users or discovers their account was misused, damaging trust in Yelp platform

## Root cause
Yelp fails to implement the X-Frame-Options HTTP response header on sensitive user interaction endpoints, allowing these pages to be embedded in iframes on third-party websites. Without frame-busting mechanisms, the application cannot prevent unauthorized framing.

## Attacker mindset
An attacker would exploit this to conduct large-scale harassment campaigns, create fake user interactions to manipulate review systems, damage user reputation through false reports, or send offensive messages impersonating legitimate users. The attack requires no technical sophistication and provides plausible deniability.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all sensitive user interaction endpoints
- Add Content-Security-Policy header with frame-ancestors directive to prevent framing from external origins
- Implement frame-busting JavaScript code as defense-in-depth (though header-based protection is primary)
- Add CSRF tokens to state-changing operations (though this alone does not prevent clickjacking)
- Require explicit user confirmation dialogs for sensitive actions (follow, report, message) before executing
- Implement SameSite cookie attributes to limit cross-site request execution
- Conduct security review of all endpoints that modify user state or send user-generated content

## Variant hunting
Search for other state-changing endpoints on Yelp: account preference modifications, payment method updates, review deletions, privacy settings changes, notification preferences, business claim actions, and any endpoints accepting user-controlled messages or content.

## MITRE ATT&CK
- T1189 Service Exploitation (clickjacking as service exploitation)
- T1566 Phishing (social engineering via clickjacking)
- T1539 Steal Web Session Cookie (if combined with session hijacking)
- T1583 Acquire Infrastructure (malicious website hosting)

## Notes
Report demonstrates lack of basic HTTP security headers. The vulnerability affects user trust and platform integrity. Proof-of-concept video provided but not reviewed in this analysis. Multiple endpoints affected suggests systemic lack of clickjacking protection across Yelp application. This is a common finding on large platforms and relatively straightforward to fix with proper header implementation.

## Full report
<details><summary>Expand</summary>

##SUMMARY:
Few Important function of yelp.com are vulnerable to ClickJacking Attack.

##DESCRIPTION:
Please have an Introduction about the vulnerability Type: https://en.wikipedia.org/wiki/Clickjacking
ClikcJacking is similar to CSRF with just an extra involvement of the victim to click somewhere on the ClickJacked page (which is usually done very easily). 
It bypasses CSRF token protection & Its impact could be critical depending on the component/function it can affect. At yelp.com I have found the following functions to be vulnerable:

##1.) Report A profile  (With custom Message in it)
**Using URL:**
https://www.yelp.com/flag_content?message=This%20person%20is%20abusive&flag_id=aV0sVlYtxt7_2SJ7X_b-3A&flag_type=user_profile&previous_url=%2Fuser_details%3Fuserid%3DaV0sVlYtxt7_2SJ7X_b-3A

##2.) Follow a user
**Using URL:** 
https://www.yelp.com/following_user/add?dst_user_id=aV0sVlYtxt7_2SJ7X_b-3A&previous_url=/user_details?userid=aV0sVlYtxt7_2SJ7X_b-3A

##3.) Send A Compliment (With Custom message in it)**
**Using URL:**
https://www.yelp.com/thanx?message=go%20to%20hell&previous_url=/user_details?userid=aV0sVlYtxt7_2SJ7X_b-3A&user_id=aV0sVlYtxt7_2SJ7X_b-3A

##POC:
*PLEASE WATCH THE 1 minute POC VIDEO TO SEE HOW THESE URL ARE EMBEDDED INTO HIDDEN IFRAMES AND HOW THE VICTIM IS EXPLOITED. THE HTML FILES USED IN THE VIDEO ARE ATTACHED IN THIS REPORT*
*THE POC ALSO SHOWS THE IMPACT OF THE VULNERABILITY*

##MITIGATION
These attacks could be circumvented by using "X-Frame-Options" Header.

## Impact

Such vulnerability when exploited in the wild by the attackers would :
1.) Affect the users interaction on your platform. Such unintended behavior is definitely not wanted by any user.
2.) Such effect upon your users could significantly harm your overall reputation and customer loss.

</details>

---
*Analysed by Claude on 2026-05-24*
