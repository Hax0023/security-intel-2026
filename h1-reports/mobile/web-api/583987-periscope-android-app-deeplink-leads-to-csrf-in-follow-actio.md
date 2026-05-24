# Periscope Android App Deeplink CSRF in Follow Action

## Metadata
- **Source:** HackerOne
- **Report:** 583987 | https://hackerone.com/reports/583987
- **Submitted:** 2019-05-18
- **Reporter:** kunal94
- **Program:** Twitter/Periscope
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Cross-Site Request Forgery (CSRF), Unsafe Deeplink Handling, Missing Intent Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The Periscope Android app implements deeplink handlers for user profiles that directly execute follow actions without CSRF protection or user confirmation. Unlike the web version which prompts users before following, the app deeplink pscp://user/<user-id>/follow automatically follows users when clicked from external sources. This allows attackers to perform unauthorized follow actions via malicious links embedded in webpages or messages.

## Attack scenario
1. Attacker creates an HTML page containing a link to pscp://user/<attacker-target>/follow
2. Attacker distributes the link via social engineering, ads, or compromised websites to Periscope Android app users
3. Victim with Periscope app installed clicks the link while browsing in Chrome or other browser on Android
4. Browser detects the pscp:// deeplink scheme and launches Periscope app with the follow intent
5. Periscope app processes the deeplink without confirmation and directly follows the attacker's target user
6. Victim unknowingly follows the attacker's chosen user without explicit consent

## Root cause
The Periscope Android app registers deeplink handlers for user profiles (pscp://user and pscpd://user schemes) that directly execute follow actions based on intent parameters without: (1) CSRF token validation, (2) user confirmation dialogs, or (3) intent origin validation. The app mirrors web URL patterns but removes the web version's protective confirmation flow.

## Attacker mindset
An attacker seeks to manipulate user follower counts, boost visibility of target accounts, or perform coordinated follow campaigns. By exploiting the lack of confirmation dialogs, they can silently execute actions across multiple victims without their awareness. The deeplink mechanism provides a low-friction attack vector requiring minimal technical sophistication.

## Defensive takeaways
- Implement CSRF token validation for all state-changing operations triggered via deeplinks, even for authenticated users
- Add explicit user confirmation dialogs for sensitive actions (follow, unfollow, subscribe) initiated via deeplinks
- Validate deeplink origin and only allow follow actions from trusted sources or through direct user interaction
- Ensure feature parity between web and mobile security controls - if web requires confirmation, mobile should too
- Implement intent origin verification to detect and block deeplinks from untrusted apps or browsers
- Consider rate-limiting follow actions from deeplink sources to detect automated abuse campaigns
- Log all deeplink-triggered actions for security monitoring and user audit trails

## Variant hunting
Check if unfollow action (pscp://user/<user-id>/unfollow) has same vulnerability
Test broadcast channel subscription deeplinks (pscp://channel/<id>/subscribe) for CSRF
Examine if other state-changing actions (block, mute, favorite) via deeplinks lack CSRF protection
Verify if pscpd:// scheme (debug variant) has additional bypass opportunities
Test discovery/recommendation deeplinks for injected actions
Check if the vulnerability exists in other Twitter properties (Twitter app deeplinks, TweetDeck)
Examine if app-to-app deeplinks have different CSRF protections than browser-triggered ones

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1021.007 - Remote Services: Shared Webroot Directory

## Notes
Report demonstrates clear understanding of CSRF mechanics and deeplink architecture. The comparison between web (protected) and mobile (unprotected) implementations is insightful. Video PoC provided but not accessible in text. App version 1.25.5.93 affected. Report lacks evidence of actual bounty resolution or patching status. Issue affects any authenticated Periscope user with the vulnerable app version installed, making scope potentially significant for large user bases.

## Full report
<details><summary>Expand</summary>

Hello Twitter Team

#Summary
This issue is mainly in the Periscope Android app against CSRF follow action using deeplink.

#Description
In normal Periscope Website, when we share a follow link like `www.pscp.tv/<user-id>/follow`, we get a response whether to follow a person or not, giving us an option, means CSRF protection is there in Periscope web application.
However, in the Periscope Android App, there are some internal deep links by which we can perform Direct CSRF in terms of the following user using internal deeplinks.

#POC

In Android Manifest XML file, internal deeplinks are described as

```html
<data android:host="user" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="user" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="broadcast" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="broadcast" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="channel" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="channel" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="discover" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="discover" android:pathPrefix="/" android:scheme="pscpd"/>
```
+ It means we can use ` pscp://user/<user-id> or pscpd://user/<user-id>`
+ Now,normally if we share follow link from website, it'll be like this, `www.pscp.tv/<user-id>/follow`, further give us option to follow them or not.

+ In deeplink, we can use the same follow-link in this way - `pscp://user/user-id/follow`, Once you visit this link from the browser, you'll directly follow any person in periscope android app.

+ Here is the Final POC
```html
<!DOCTYPE html>
<html>
<a href="pscp://user/<any user-id>/follow">CSRF DEMO</a>
</html>
```
+ Visit the above POC html page from android chrome browser, click on link and you'll follow anyone directly inside Periscope android app.

#Attachment (Video)
{F492266}

+ App Info - Periscope V 1.25.5.93

Thanks
Kunal

## Impact

+ Using Periscope deeplink like pscp://user/user-id/follow, it's possible to perform Direct CSRF Follow against any user in periscope android app.

</details>

---
*Analysed by Claude on 2026-05-24*
