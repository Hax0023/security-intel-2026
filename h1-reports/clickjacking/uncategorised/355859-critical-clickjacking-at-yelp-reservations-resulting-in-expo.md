# Clickjacking at Yelp Reservations Exposing Private Data and Enabling Credit Card Misuse

## Metadata
- **Source:** HackerOne
- **Report:** 355859 | https://hackerone.com/reports/355859
- **Submitted:** 2018-05-22
- **Reporter:** hk755a
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Clickjacking, Missing Security Headers, Unauthorized Action, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Yelp's reservation pages lack X-Frame-Options headers, allowing attackers to embed them in hidden iframes on malicious websites. This enables attackers to trick users into making unintended reservations, exposing email/phone numbers, potentially causing monetary loss through cancellation fees, and disrupting legitimate business bookings.

## Attack scenario
1. Attacker creates a legitimate-looking website and embeds Yelp reservation pages as hidden iframes using CSS styling (opacity: 0, display: none, etc.)
2. Attacker lures victims to the malicious website through social engineering, links on Yelp itself, or social media
3. When victim unknowingly clicks a button/link on the attacker's page, they are actually clicking elements on the hidden iframe
4. Victim completes a restaurant reservation without consent, exposing their email, phone, and potentially payment information to the attacker's chosen business
5. Attacker can exploit this for data harvesting, fraudulent reservations, or denying legitimate bookings by filling all available slots
6. Victim discovers unauthorized reservations or unexpected charges, resulting in financial loss and trust erosion

## Root cause
Missing X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) allows embedding of reservation pages in iframes on third-party domains without restriction

## Attacker mindset
Opportunistic attacker exploiting UI/UX vulnerabilities to conduct large-scale clickjacking campaigns. Motivation includes data harvesting, fraud, competitive sabotage against businesses, or denial of legitimate service through slot reservation exhaustion

## Defensive takeaways
- Implement X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors 'none' headers on all pages handling sensitive user actions
- Apply Clickjacking protections to any page requiring authentication or involving financial/personal data transactions
- Implement SameSite cookie attributes (Strict/Lax) to prevent CSRF/clickjacking token bypass
- Add UI-level frame-busting JavaScript to detect and break out of unauthorized iframe embeddings
- Enforce framebreaker code: if (self !== top) { top.location = self.location; }
- Require user confirmation/CAPTCHA for sensitive actions like reservations
- Implement proper CSRF tokens validated per request for state-changing operations
- Monitor and audit unexpected referer headers in server logs to detect iframe abuse

## Variant hunting
Check all user-triggered transactions (bookings, payments, account modifications) for X-Frame-Options headers
Test other Yelp pages handling sensitive data (checkout, account settings, billing)
Identify other Yelp features allowing embedded content (reviews, photos, business pages) that could enable nested clickjacking
Search for similar header omissions in related business/reservation systems (OpenTable, Resy, etc.)
Test combinations of clickjacking with other vectors (CSRF, XSS in iframes) for chained attacks
Verify if attackers can use clickjacking to bypass rate limiting or bot detection on reservation endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (delivery of malicious link to attacker's website)
- T1539 - Steal Web Session Cookie (potentially capturing authenticated session via clickjacking)
- T1598 - Social Engineering (tricking users to visit malicious site)

## Notes
Report demonstrates understanding of clickjacking mechanics and real-world impact scenarios. The vulnerability affects both end-users (privacy, financial) and business owners (reservation fraud, lost revenue). Criticality depends on exploitation reach—social media distribution could affect thousands. Report lacks proof-of-concept video details but impact assessment is comprehensive. Key insight: vulnerabilities affecting marketplace trust (users + merchants) warrant higher severity despite traditional CVSS scoring limitations.

## Full report
<details><summary>Expand</summary>

Please have a look at this interesting article with precise explanation about Click-jacking security flaw:
https://www.linkedin.com/pulse/20141202104842-120953718-why-am-i-anxious-about-clickjacking/

In Yelp platform the response headers of the Reservation page does not contain the X-Frame-Options header, thus allowing malicious actors to embed these pages as hidden i-frames on some external or their own innocuous looking website. 
Upon successful exploitation the victim would have made unintentional reservation to some restaurant/bar and his Email Id/Mobile Number would have been shared with the business. 
All this would  happen without victim's  knowledge or consent.

Here's how a sample Reservation page looks like:
███

REQUEST RESPONSE HEADERS OF A RESERVATION PAGE:
██████

Please note the missing X-Frame-Options header in the response headers.

#POC:
For POC and steps to reproduce please watch the video 

#EXPLOIT SCENARIOS:
Please look at the different scenarios this could be exploited :

#==>(1) The attacker may himself register a business at yelp, copy and embed his own reservation url as hidden i-frame. Make reservation in the background upon victim's click. He gains email/mobile of the victim account.
#==>(2) He may reserve a table of some business that charges upon cancellation and the victim may face monetary loss. 
#==>(3) He may target a business and  try to restrict all the genuine bookings. It would be possible to do so by booking all table slots of different timings from all the different visitors that are coming to his malicious but genuine looking website.

The impact of this vulnerability depends on the number of visitors attacker might be able to bring to his website. This is not a very big deal in the presence of huge social media websites nowadays. Or he may paste link to his website somewhere on yelp (review/about/talk etc sections) platform itself so as to bring authenticated yelp users to his website.

## Impact

While the  overall risk may only be a medium rating; the impact is high as the vulnerability affects both the yelp users and also business owners

#The vulnerability impacts the victim in the following ways:
==>1.) Loss of Confidentiality: Private info such as Email/phone is disclosed
==> 2.) Unauthorized Reservations from User Account: This certainly is not wanted by any user.
==> 3.) Monetary loss upon Cancellation of reservation: Some businesses say they would charge upon 
cancellation of reservation.
==> 4.) Apart from this client's trust on Yelp platform is also lost.

#The vulnerability impacts the business owners in the following ways:
==>1.) Fake reservations may restrict genuine reservations:
Such Fake reservations may restrict genuine users from booking tables. And on the other end the business owners have no way to distinguish between fake and genuine ones.
This leads to customer/monetary loss to business owners itself.

</details>

---
*Analysed by Claude on 2026-05-24*
