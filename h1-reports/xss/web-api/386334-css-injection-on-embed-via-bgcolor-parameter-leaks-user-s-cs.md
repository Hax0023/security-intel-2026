# CSS Injection on /embed/ via bgcolor Parameter Leaks CSRF Token and Enables XSS

## Metadata
- **Source:** HackerOne
- **Report:** 386334 | https://hackerone.com/reports/386334
- **Submitted:** 2018-07-24
- **Reporter:** nahamsec
- **Program:** Chaturbate
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** CSS Injection, Information Disclosure, CSRF Token Leakage, Cross-Site Scripting (XSS), Content-Type Confusion
- **CVEs:** None
- **Category:** web-api

## Summary
A CSS injection vulnerability exists in the /embed/admin/ endpoint through the bgcolor parameter, allowing attackers to break out of CSS context and inject arbitrary CSS rules. This enables enumeration and theft of CSRF tokens through CSS-based information disclosure techniques. Combined with endpoints returning HTML content-type, attackers can achieve reflected XSS.

## Attack scenario
1. Attacker crafts malicious URL with bgcolor parameter containing CSS payload: }*{background:red
2. Injected CSS breaks out of the intended style context and applies arbitrary rules to page elements
3. Using CSS attribute selectors and exfiltration techniques, attacker enumerates the CSRF token value from hidden form fields or meta tags
4. Attacker obtains the valid CSRF token for the victim's session
5. Attacker identifies vulnerable endpoints like POST /choose_broadcaster_chat_color that return text/html content-type
6. Attacker combines CSRF token with reflected XSS payload to execute arbitrary JavaScript in victim's browser context

## Root cause
Insufficient input validation and sanitization of the bgcolor parameter before interpolation into CSS context. The application fails to properly escape or validate URL parameters used in style attributes, allowing CSS metacharacters to break out of the intended style declaration and inject arbitrary CSS rules.

## Attacker mindset
An opportunistic attacker conducting reconnaissance to identify multiple chained vulnerabilities for maximum impact. The researcher demonstrates methodical vulnerability chaining - starting with CSS injection for information disclosure, then pivoting to CSRF token theft, and finally combining with XSS endpoints for full exploitation. The request for collaboration suggests awareness of attack complexity and intent to fully weaponize the chain.

## Defensive takeaways
- Implement strict input validation for all user-supplied parameters before CSS interpolation
- Use CSS-specific output encoding functions rather than generic HTML encoding
- Sanitize or reject CSS metacharacters (braces, asterisks, semicolons) in user input
- Implement Content Security Policy (CSP) headers to restrict style injection impacts
- Ensure CSRF tokens are marked as HTTPOnly and Secure, preventing CSS-based exfiltration
- Validate Content-Type headers and ensure HTML endpoints don't accept untrusted user input for XSS prevention
- Implement strict CORS policies for embedded content
- Use parameterized CSS frameworks that don't allow style injection
- Conduct security review of all /embed/ endpoints for similar injection vectors

## Variant hunting
Search for other endpoints using user-controlled parameters in style contexts (bgcolor, color, theme parameters). Examine all /embed/ variants and similar iframing endpoints. Review other HTML-returning endpoints that accept user input without proper encoding. Check for similar CSS injection in other color/theme customization features across the application.

## MITRE ATT&CK
- T1190
- T1539
- T1598
- T1566
- T1187

## Notes
The researcher explicitly acknowledges the vulnerability chain is incomplete ('I haven't gotten that far yet') and requests collaboration from a co-discoverer, indicating this is a sophisticated multi-stage exploitation requiring coordination. The POC domains (d0nut.pythonanywhere.com) appear to be researcher-controlled environments demonstrating token exfiltration methodology. The missing impact section suggests the report may have been incomplete at submission time.

## Full report
<details><summary>Expand</summary>

Hi there,

There's a CSS injection here: https://chaturbate.com/embed/admin/?bgcolor=%7D*%7Bbackground:red&tour=nvfS&disable_sound=0&campaign=iNSGX 

```
  body, div#main, div.content, div.block, div.section {margin: 0px; padding: 0px;}
  body {min-width:800px;}
  div.content {width: 100%;}
  
  body {background: }*{background:red;}

```

This allows an attacker to enumerate the CSRF token. Once the CSRF token is enumerated, we can 

#POC 
1. Go to `http://d0nut.pythonanywhere.com/demo/token_stealing/7GTt5qD1LD273WYkJyaR/reset`
2. Now go to `http://d0nut.pythonanywhere.com/demo/token_stealing/7GTt5qD1LD273WYkJyaR` and let it do it's magic :) 

{F324052}

There are numerous endpoints like `POST /choose_broadcaster_chat_color` where it returns `Content-Type: text/html; charset=utf-8` that could potentially allow a hacker to combine the two for XSS (I haven't gotten that far yet)


 **Do you mind asking your HackerOne contact to allow collaboration on your program, so I can invite another researcher that helped me exploit this fully?**

Thanks,
Ben

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-12*
