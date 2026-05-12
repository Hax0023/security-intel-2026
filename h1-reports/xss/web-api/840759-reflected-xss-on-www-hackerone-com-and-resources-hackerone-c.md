# Reflected XSS on www.hackerone.com and resources.hackerone.com

## Metadata
- **Source:** HackerOne
- **Report:** 840759 | https://hackerone.com/reports/840759
- **Submitted:** 2020-04-05
- **Reporter:** todayisnew
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Reflected Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** web-api

## Summary
Reflected XSS vulnerability discovered in the resources embed endpoint affecting both www.hackerone.com/resources/ and resources.hackerone.com domains. The vulnerability exists in query parameters (miniUrl and related parameters) that are not properly sanitized before being rendered in the response, allowing injection of arbitrary JavaScript code.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the miniUrl parameter with escaped script tags and SVG event handlers
2. Attacker sends the crafted URL to a victim via email, chat, or social media
3. Victim clicks the link while authenticated to HackerOne or in a session context
4. Browser renders the page and executes the injected JavaScript (confirm(location) in the PoC)
5. Attacker can steal session cookies, credentials, or perform actions on behalf of the victim
6. If exploit is chained with CSRF, attacker could modify account settings or access sensitive resources

## Root cause
Insufficient input validation and output encoding on the miniUrl parameter and related query parameters in the embed_mini endpoint. The application concatenates user-supplied input into HTML/JavaScript context without proper escaping or sanitization, allowing breakout from intended string context.

## Attacker mindset
Opportunistic researcher employing fuzzing/brute-force approach to discover reflected parameters that lack proper encoding. The attacker demonstrated patience and willingness to iterate through various payload encodings (URL encoding, tag closure techniques) to bypass basic filters. The mention of intermittent exploitation suggests awareness of potential WAF or rate-limiting defenses.

## Defensive takeaways
- Implement strict input validation on all query parameters, especially those intended for embedding or framing content
- Apply context-aware output encoding: HTML entity encoding for HTML context, JavaScript string escaping for JS context, URL encoding for URL parameters
- Use Content Security Policy (CSP) headers with strict directives (no inline scripts, script-src whitelist) to prevent XSS impact
- Employ a parameterized templating engine that auto-escapes by default rather than manual string concatenation
- Implement a Web Application Firewall (WAF) with XSS detection rules, though don't rely on it as primary defense
- Conduct security code review of all embed/iframe functionality and dynamic content generation
- Test all user-controlled parameters with XSS payloads during development (SAST/DAST)
- Consider using a markup sanitization library (DOMPurify, Bleach) if HTML content must be dynamically generated

## Variant hunting
Test all other embed parameters (miniTitle, miniColor, miniBg) for XSS via similar encoding bypasses
Check related endpoints that handle resource embedding or sharing functionality
Attempt variations with different encoding schemes: double URL encoding, UTF-8 bypasses, Unicode escapes
Test for DOM-based XSS by checking JavaScript that processes these parameters client-side
Investigate if authentication/session context affects filtering (reporter noted intermittent nature)
Check for stored XSS if embed parameters are cached or persisted in any way
Test for polyglot payloads that work across HTML, JavaScript, and URL contexts

## MITRE ATT&CK
- T1190
- T1059

## Notes
The reporter demonstrated admirable ethical behavior by donating the bounty to COVID-19 relief efforts. The 'intermittent' nature of exploitation is noteworthy and may indicate: (1) inconsistent filtering based on certain conditions, (2) JavaScript-based sanitization that fails under specific DOM states, (3) caching issues where some requests hit unfiltered code paths, or (4) WAF rules that don't catch all encoding variations. The simplified payload using SVG onload instead of traditional img onerror suggests awareness of potential filter rules. The vulnerability appears to be on a marketing/resources subdomain but could potentially be chained with other vulnerabilities or social engineering for higher impact.

## Full report
<details><summary>Expand</summary>

Good day :)

I hope your doing as well as can be during these difficult times.

I have found xss at 2 endpoints:

https://www.hackerone.com/resources/

and 

https://resources.hackerone.com

The payloads that work are here:

https://www.hackerone.com/resources/read/embed_mini/11690/122736?miniPop=false&alwaysCover=false&miniTitle=XSS+POC&miniColor=333333&miniLinkToTitle=true&miniUrl=http://example.com%22%22,})%3C/script%3E%3Csvg+onload=confirm(location)%3E&miniBg=FFFFFF&hideBg=true&width=380&height=330&sharing=true

https://resources.hackerone.com/resources/read/embed_mini/11690/122736?miniPop=false&alwaysCover=false&miniTitle=XSS+POC&miniColor=333333&miniLinkToTitle=true&miniUrl=http://example.com%22%22,})%3C/script%3E%3Csvg+onload=confirm(location)%3E&miniBg=FFFFFF&hideBg=true&width=380&height=330&sharing=true


I've attached screenshots, the xss is intermittent, I'm not sure why maybe a cookie, maybe ip blocking, I'm not sure, but it happens :)

If it helps for others I have no idea what I am doing most of the time and brute force try things until they work :) 

Always learning, always feeling I know so little, and so much to learn, its awesome working together we all contribute our knowledge and effort :)

I've been taking a break the last few weeks to help to support family in this time of need, any bounty that is awarded I'm adding hackforgood as a collaborator and donating 100% of the bounty.  

It is great that hackerone is implementing this option to let us if we are in the position to share to donate funds, we have the option via the platform :)

It was shared with me that "You can add hackforgood as a collaborator on your reports and weight your bounty percentage on how much you’d like to donate. Our team will submit donations at the end of each month to WHO’s Covid-19 Response Fund" hope it works here will give it a shot :)

As always I wish you well on your side of the screen, to your loved ones, and that you can find both mental and physical wellness as much as possible right now :)

-Eric

## Impact

xss on the site, low risk since a marketing site :)

</details>

---
*Analysed by Claude on 2026-05-12*
