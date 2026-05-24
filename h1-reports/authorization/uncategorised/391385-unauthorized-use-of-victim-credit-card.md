# Unauthorized Credit Card Charges via Framable Checkout Endpoint (Missing Clickjacking Protection)

## Metadata
- **Source:** HackerOne
- **Report:** 391385 | https://hackerone.com/reports/391385
- **Submitted:** 2018-08-07
- **Reporter:** hk755a
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Clickjacking, Cross-Site Request Forgery (CSRF), Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Yelp checkout deal endpoint lacks clickjacking protection and can be embedded in hidden iframes on attacker-controlled websites. An attacker can trick authenticated users into unknowingly authorizing purchases from their saved credit cards by embedding the framable checkout page and overlaying invisible buttons.

## Attack scenario
1. Attacker identifies that yelp.com/checkout/deal/* endpoint is framable (missing X-Frame-Options header)
2. Attacker creates malicious HTML page embedding the Yelp checkout endpoint in a hidden iframe with transparent opacity
3. Attacker positions an invisible or disguised clickable element over the checkout 'Purchase' button within the iframe
4. Attacker distributes the malicious page via social engineering (Yelp Talk forums, social media, phishing links)
5. Victim clicks the visible element while authenticated to Yelp in another tab, unknowingly clicking the hidden purchase button
6. Victim's saved credit card is charged for an unwanted deal (demonstrating $450 unauthorized charge in POC)

## Root cause
The checkout endpoint lacks adequate HTTP headers (X-Frame-Options: DENY or SAMEORIGIN) to prevent embedding in cross-origin iframes, combined with insufficient CSRF token validation or token binding to the user's active session context.

## Attacker mindset
Opportunistic attacker seeking either direct financial gain by creating deals and stealing customer payments, or causing reputational/financial damage to Yelp and its users. Low barrier to entry makes this attractive for mass exploitation.

## Defensive takeaways
- Implement X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors 'none' on all sensitive transaction endpoints
- Strengthen CSRF token validation with double-submit cookies or SameSite cookie attributes (SameSite=Strict for checkout flows)
- Require explicit user interaction (CAPTCHAs, multi-step confirmation) for financial transactions
- Implement rate limiting on checkout endpoints to detect automated abuse
- Add visual security indicators (framing detection) to warn users if they're accessing Yelp checkout outside expected context
- Monitor for unusual transaction patterns and implement step-up authentication for large purchases
- Conduct security headers audit across all user-sensitive endpoints

## Variant hunting
Search for other framable endpoints handling sensitive operations: payment methods, account changes, subscription upgrades, reservation confirmations. Test X-Frame-Options header presence on all endpoints processing user directives. Review CSP policies for frame-ancestors directive gaps. Test other Yelp subdomains and legacy endpoints for clickjacking vulnerabilities.

## MITRE ATT&CK
- T1190
- T1566
- T1040

## Notes
Classic clickjacking vulnerability with real financial impact. The report demonstrates effective POC with video evidence. Severity is amplified because Yelp stores credit cards and users are authenticated in separate tabs, reducing friction for exploitation. The vulnerability allows fraud without any technical interaction with Yelp systems themselves—purely a client-side attack.

## Full report
<details><summary>Expand</summary>

#SUMMARY
Yelp user's credit cards are at risk of being compromised
There's a way by which a malicious attacker can make unauthorized purchases from the victim's credit card.
Just by getting the victim to some external website and clicking on it, the victim would have eventually paid for some unwanted deal unknowingly from his saved credit card on yelp. (Please see the POC which shows a $450 deal)

#DESCRIPTION:
The endpoint yelp.com/checkout/deal/****?biz_id={}&fsid={} is Framable, which means a sample deal page like this:
https://www.yelp.com/checkout/deal/16OJ1G_Ev7STx0HELIDzyA?biz_id=Ydf5dgFsGhMSP61Ht7TekA&return_url=%2Fbiz%2Fbutcher-and-the-burger-chicago
Could be embedded as an hidden iframe on some HTML page. 
Watch the video attached to see how the exploit really looks like.


#EXPLOIT SCENARIOS:
*The attacker could simply host the exploit page (attached to this report) on some webpage and use social networking sites to share it across the world. One simple way could be spreading it through Yelp's Talk section itself, so as to get valid yelp users easily.* 

I mainly envision the vulnerability to be exploited in the following ways:
==**1.) Attacker creates a deal himself and uses this vulnerability to steal money from the victim.**==
==**2.) Attacker just goes on causing monetary loss for the victim, with no personal monetary gain.**==

#POC
*You may want to watch the 1 min video attached with the report*

Step 1.) Log into your yelp account on your fresh or incognito browser window.

Step 2.) Open the attached "Yelp Credit Card Misuse by framable deals page" Webpage in another window.

Step 3.) Click on the slightly visible Purchase button. 

The vulnerability's exploitation impact is high as it causes unauthorized credit card use of the victim!
Do let me know if there are any questions.

## Impact

Yelp users credit card protection is certainly compromised. Worthy customer's bear monetary losses.  
Apart from money the faith of users on yelp for their card's security is also lost leading to customer/business loss to yelp.
Such attacks running in the wild, are heavy threat to an organization's reputation.

</details>

---
*Analysed by Claude on 2026-05-24*
