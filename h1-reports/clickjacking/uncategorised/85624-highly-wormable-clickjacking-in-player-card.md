# Highly wormable clickjacking in Twitter player card via X-Frame-Options bypass

## Metadata
- **Source:** HackerOne
- **Report:** 85624 | https://hackerone.com/reports/85624
- **Submitted:** 2015-08-30
- **Reporter:** filedescriptor
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** clickjacking, iframe embedding, security header bypass, cross-site request forgery
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twitter's Player Card is vulnerable to clickjacking attacks in browsers that don't support CSP2 (Safari, IE) due to insufficient X-Frame-Options validation and lack of frame-busting protection. Attackers can embed Twitter pages within attacker-controlled iframes and overlay fake content to trick users into performing arbitrary actions like tweeting, retweeting, or following accounts, creating a wormable attack vector distributed via tweets.

## Attack scenario
1. Attacker creates a malicious Player Card HTML file that embeds an iframe pointing to twitter.com
2. Attacker hosts this card on a whitelisted domain and tweets it
3. When victims open the tweet in Safari or IE (browsers without CSP2 support), the embedded Twitter page loads inside the attacker's card
4. Attacker overlays fake clickable content (e.g., 'play video' button) on top of the embedded Twitter interface
5. Victim clicks the fake overlay, which actually triggers a click on the hidden Twitter element beneath (e.g., tweet button)
6. Victim unknowingly performs the attacker's desired action, and if it's a retweet of the malicious content, the attack spreads virally

## Root cause
Multiple security mechanisms failed in combination: (1) X-Frame-Options SAMEORIGIN is bypassable via same-origin redirect chains (attacker.com -> twitter.com nesting), (2) CSP2's frame-ancestors directive is unsupported in Safari and IE, leaving no effective clickjacking protection, and (3) Player Cards lack JavaScript-based frame-busting code that could be disabled anyway with iframe sandbox attributes.

## Attacker mindset
An attacker recognized that Twitter's defense-in-depth approach had critical gaps in legacy browser support. They identified that the most restrictive defense (CSP2) wasn't universally deployed and that the fallback defenses (SAMEORIGIN and frame-busting JS) could be individually circumvented. The attacker leveraged the trusted nature of Player Cards and their prominent display on timelines to create a highly credible, low-friction attack that could self-propagate through social sharing.

## Defensive takeaways
- Implement multiple non-redundant security controls with independent mechanisms rather than relying on browser support for newer standards
- Never assume X-Frame-Options SAMEORIGIN provides clickjacking protection against determined attackers; it can be bypassed with redirect chains
- CSP frame-ancestors directive should be combined with alternative protections for older browsers rather than being the sole defense
- Validate iframe embedding in application logic, not just HTTP headers; restrict what types of content can be embedded in user-facing cards
- Implement frame-busting code in JavaScript but don't rely solely on it; combine with sandbox attribute restrictions that you control
- Consider using anti-clickjacking tokens or same-site cookies for sensitive actions on high-trust pages
- Restrict Player Card capabilities to prevent arbitrary iframe embedding; whitelist allowed card properties and validate content
- Perform browser-specific security testing, especially for older versions with limited standard support

## Variant hunting
Search for similar clickjacking vectors in: (1) other Twitter card types (summary, photo, gallery) that might allow arbitrary HTML/iframe embedding, (2) third-party widgets or embeds that use iframes without proper framing controls, (3) applications relying solely on X-Frame-Options without CSP or frame-busting JS, (4) any user-controlled content that can embed iframes within trusted pages, (5) redirect-chain exploitation of SAMEORIGIN headers on other platforms

## MITRE ATT&CK
- T1190
- T1566
- T1539
- T1598

## Notes
This report demonstrates a sophisticated understanding of browser security mechanisms and their limitations. The researcher identified that 'defense in depth' only works when all layers are actually effective. The wormable aspect is critical—by making the attack payload auto-propagate through tweets, the attacker doesn't need to convince users to visit malicious sites; the attack comes through trusted social feeds. The PoC reportedly demonstrated automated tweeting, suggesting potential for account takeover or massive spam campaigns. Twitter likely patched this by disabling arbitrary iframe embedding in Player Cards or implementing stricter origin validation beyond just the card domain.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an issue where player card is vulnerable to clickjacking in certain browsers. This may result in something similar to XSS worm and many other critical damages.

##Details
Twitter Player Card allows a website to embed a custom player(html) into an iframe in a tweet. There are currently 2-3 security features in place to defend clickjacking on Twitter:
1. ```X-Frame-Options: SAMEORIGIN``` covering the whole twitter.com domain
2. ```Content-Security-Policy: frame-ancestors 'self'``` ditto
3. JS-based frame-buster in some pages (but not all)

For (1), SAMEORIGIN only checks if the embedded frame is on the same origin of the top window. For example, attacker can do something like twitter.com -> attacker.com -> twitter.com to evade it. More details can been seen from here: https://bugzilla.mozilla.org/show_bug.cgi?id=725490 
For (2), this is the only way to correctly prevent framing from other websites (it performs the check against the ancestor list). However this is a CSP2 directive so not all browsers support it. For example, Safari and IE do not support it.
For (3), using the sandbox attribute of iframe can disable JS of a frame, hence anti-frame-buster

Since Player Card is shown on a Tweet (on twitter.com), attacker can embed an iframe which embeds a Twitter page so that attacker can overlay it with "bait" content to lure victims to click on it.

The impact is huge because of the following facts:
* The card displays directly on the user's timeline, making the attack less suspicious to normal clickjacking
* The click is very subtle that victims cannot notice what's happened behind the scene
* Wormable because attacker can make victims tweet arbitrary content to spread it
* Can perform click-based critical actions, like follow, retweet, favorite... etc
* If sent as promoted tweet, it can target even more victims, also player is directly expanded

##Repo step
1. Clone the Player Card started bundle here: https://github.com/twitterdev/cards
2. Change the card's property *twitter:player* to a custom HTML file
3. In the HTML file, embed iframe to a Twitter page, e.g. ```<iframe src="//twitter.com"></iframe>```
4. Post the link in a Tweet (make sure the domain is white-listed)
5. Expand the tweet in Safari or IE, it will show that a Twitter page is embedded

Documentation of Player Card: https://dev.twitter.com/cards/types/player

##PoC

https://twitter.com/AttackerCanvas/status/637859735501279232 (**Open with Safari or IE**)

Video demo: https://vimeo.com/137725491 (password: click)

The PoC demonstrates how the attack can be conducted. There will be a fake video to lure victims to click to play it. After clicking the victim will automatically post a tweet with content "Pwn3d!".

</details>

---
*Analysed by Claude on 2026-05-24*
