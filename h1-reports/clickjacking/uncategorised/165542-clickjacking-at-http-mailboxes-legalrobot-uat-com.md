# Clickjacking Vulnerability at mailboxes.legalrobot-uat.com

## Metadata
- **Source:** HackerOne
- **Report:** 165542 | https://hackerone.com/reports/165542
- **Submitted:** 2016-09-03
- **Reporter:** amir0ezat
- **Program:** Legal Robot
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application at mailboxes.legalrobot-uat.com lacks clickjacking protections and can be embedded in iframes on arbitrary external websites. An attacker can overlay malicious UI elements on top of the legitimate application to trick users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious website hosting the vulnerable application in a hidden or transparent iframe
2. Attacker overlays fake UI elements (buttons, links) on top of the embedded application using CSS positioning and opacity techniques
3. Victim visits the attacker's website believing they are interacting with legitimate content
4. Victim clicks on what appears to be innocent UI but actually triggers actions within the framed application (e.g., approving documents, changing settings, transferring data)
5. Unintended actions are executed in the user's authenticated session within the legitimate application
6. Sensitive operations are completed without the user's knowledge or explicit consent

## Root cause
The application does not implement the X-Frame-Options HTTP response header or Content-Security-Policy frame-ancestors directive to prevent embedding in iframes on external domains.

## Attacker mindset
An attacker seeks to leverage the trust users have in the legitimate application to perform unauthorized actions without detection. Clickjacking is particularly effective against applications handling legal documents or sensitive operations where users may be careless about visual confirmation.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all responses
- Alternatively, use Content-Security-Policy with frame-ancestors directive to restrict framing origins
- Implement frame-busting JavaScript code as defense-in-depth (though headers are primary control)
- Use anti-clickjacking tokens or frame validation for sensitive operations
- Validate Referer headers for state-changing requests
- Ensure security headers are applied consistently across all endpoints and environments (including UAT)

## Variant hunting
Check if other subdomains or environments (staging, dev) have similar protections
Test whether X-Frame-Options header varies by endpoint or HTTP method
Verify if CSP frame-ancestors is implemented on production but missing on UAT
Check for bypass techniques using HTML5 sandbox attributes
Test nested iframe scenarios to bypass SAMEORIGIN restrictions
Examine if the application has custom frame-busting code that could be circumvented

## MITRE ATT&CK
- T1189
- T1566

## Notes
This is a UAT environment vulnerability which indicates the application may also be vulnerable in production if protections were not properly implemented. The writeup is basic but clearly demonstrates the vulnerability through proof-of-concept HTML. The application appears to handle legal documents, making clickjacking a particularly serious risk as users could unknowingly approve or modify important legal content.

## Full report
<details><summary>Expand</summary>

<html>
   <head>
     <title>Clickjack test</title>
   </head>
   <body>
     <center><p>Website is vulnerable to clickjacking!</p></center>
     <center><iframe src="http://mailboxes.legalrobot-uat.com/" width="1000" height="600"></iframe></center>
   </body>
</html>

</details>

---
*Analysed by Claude on 2026-05-24*
