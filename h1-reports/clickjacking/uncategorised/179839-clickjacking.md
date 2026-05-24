# Clickjacking Vulnerability on Yelp Homepage

## Metadata
- **Source:** HackerOne
- **Report:** 179839 | https://hackerone.com/reports/179839
- **Submitted:** 2016-11-03
- **Reporter:** jessepinkman
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Yelp homepage (https://www.yelp.com/) is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP header, allowing the site to be embedded in iframes on attacker-controlled domains. An attacker can overlay transparent or opaque layers to trick users into clicking on unintended buttons or links, or capture keystrokes through invisible form fields.

## Attack scenario
1. Attacker creates a malicious webpage that embeds Yelp.com in an invisible or partially visible iframe
2. Attacker overlays transparent or opaque UI elements (buttons, forms) that correspond to critical Yelp actions (login, write review, follow user)
3. User visits attacker's webpage believing they are performing a harmless action
4. User's clicks intended for the attacker's page are actually redirected to the Yelp iframe beneath
5. Unintended actions are executed on Yelp (e.g., following malicious accounts, leaving fake reviews, changing account settings)
6. Attacker can also capture keystrokes if text input fields are positioned over invisible Yelp form fields

## Root cause
Yelp fails to implement the X-Frame-Options HTTP response header (should be set to DENY or SAMEORIGIN) to prevent the page from being framed by external domains. Without this protection, browsers allow any website to embed Yelp in an iframe.

## Attacker mindset
Attacker recognizes that clickjacking is a simple yet effective social engineering vector requiring minimal technical skill. The attacker can manipulate user interactions without credentials or exploit complex vulnerabilities, making it an attractive attack for driving fake engagement, phishing credentials through keystroke hijacking, or performing unauthorized actions on behalf of legitimate users.

## Defensive takeaways
- Implement X-Frame-Options: DENY header to prevent framing by any external domain
- Alternatively, use X-Frame-Options: SAMEORIGIN to allow framing only from same-origin pages
- Implement Content-Security-Policy (CSP) frame-ancestors directive as modern alternative/supplement
- Use frame-busting JavaScript code as legacy fallback (though can be bypassed)
- Apply UI protections: disable right-click on sensitive pages, use CSS isolation for critical controls
- Educate users about phishing and suspicious overlay behavior
- Implement clickjacking detection through monitoring unusual click patterns or iframe detection

## Variant hunting
Test all subdomains and user-facing pages (login, account settings, payment) for clickjacking
Verify if DENY vs SAMEORIGIN setting creates bypass opportunities across subdomains
Check if CSP frame-ancestors is properly configured without wildcard exceptions
Test mobile versions and APIs which may lack similar protections
Investigate if JavaScript frame-busting can be bypassed (e.g., via sandbox attribute)
Look for other UI redress attacks: drag-and-drop hijacking, tab nabbing, notification hijacking

## MITRE ATT&CK
- T1189
- T1566.002
- T1598.004

## Notes
This is a straightforward clickjacking report with a valid proof-of-concept. The PoC correctly demonstrates that Yelp.com can be embedded in an iframe without restrictions. Yelp likely issued a fix by adding X-Frame-Options header. The report lacks specific impact demonstration (e.g., triggering actual user actions) but the vulnerability class is well-understood and clearly explained. Common finding in bug bounty programs, typically rated medium severity due to requiring user interaction but enabling credential theft or unauthorized actions.

## Full report
<details><summary>Expand</summary>

hi there i have found a clickjacking vulnerability in your site
in the index (home page): https://www.yelp.com/
Clickjacking, also known as a "UI redress attack", is when an attacker uses multiple transparent or opaque layers to trick a user into clicking on a button or link on another page when they were intending to click on the the top level page. Thus, the attacker is "hijacking" clicks meant for their page and routing them to another page, most likely owned by another application, domain, or both.

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker. 
PoC:
<html>
   <head>
     <title>test yelp</title>
   </head>
   <body>
     <p> yelp.com is vulnerable to clickjacking!</p>
     <iframe src="https://www.yelp.com" width="500" height="500"></iframe>
   </body>
</html>

Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
