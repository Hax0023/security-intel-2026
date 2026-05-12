# DOM XSS via Unsanitized URL Parameters in iframe src Attribute

## Metadata
- **Source:** HackerOne
- **Report:** 1073725 | https://hackerone.com/reports/1073725
- **Submitted:** 2021-01-07
- **Reporter:** mechatech84
- **Program:** Omnipod (Insulet Corporation)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Insufficient Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
DOM-based XSS vulnerability exists on multiple Omnipod pages where URL query parameters are directly concatenated into an iframe's src attribute without sanitization. An attacker can inject malicious payloads through crafted URLs to execute arbitrary JavaScript in the victim's browser context.

## Attack scenario
1. Attacker crafts malicious URL with XSS payload in query parameters: https://www.omnipod.com/freedom/birthdate-confirmation?sid=value&#'onload='alert(document.domain)
2. Attacker distributes URL via email, social media, or other communication channels targeting Omnipod users
3. Victim clicks the malicious link while authenticated to Omnipod services
4. Vulnerable JavaScript code extracts query parameters and directly concatenates them into iframe src attribute
5. Browser parses the injected onload event handler and executes arbitrary JavaScript
6. Attacker's script executes in victim's session context, potentially stealing session cookies, credentials, or performing unauthorized actions

## Root cause
The vulnerable code directly concatenates window.location query parameters into an iframe src attribute without proper URL encoding or sanitization. The script uses `loc.split('?')[1]` to extract parameters and builds srcstring with string concatenation: `srcstring = 'https://na.myomnipod.com/lic-p4-proc?' + params`. This allows breaking out of the src attribute context with special characters and injecting event handlers.

## Attacker mindset
Opportunistic attacker seeking to exploit healthcare application for credential harvesting, session hijacking, or malware distribution. The medical/personal health context makes this particularly attractive for targeted phishing campaigns that could compromise sensitive diabetes management data and user privacy.

## Defensive takeaways
- Always URL-encode user-controlled input before inserting into HTML attributes, especially href and src attributes
- Use encodeURIComponent() for individual parameters or leverage URL constructor API to safely build URLs
- Implement Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Use DOM manipulation methods that auto-escape (createElement, textContent) instead of document.write with concatenated strings
- Validate and whitelist expected query parameter names and formats before processing
- Apply input validation on server-side to reject malformed or suspicious parameter values
- Implement frame-ancestors CSP directive to control which domains can embed your iframes
- Regular security testing including manual review of DOM-manipulation code and automated XSS scanning

## Variant hunting
Search codebase for: 1) window.location string operations followed by document.write(), 2) Direct concatenation of URL parameters into src/href attributes, 3) split() operations on location.toString() without subsequent validation, 4) Other pages using similar iframe injection patterns (e.g., /freedom/*, /pif/*, other funnel pages), 5) Similar vulnerable patterns in other medical device vendor portals with patient registration/confirmation flows

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing
- T1059: Command and Scripting Interpreter - JavaScript

## Notes
This is a classic DOM XSS vulnerability in a healthcare context, making it particularly severe due to potential access to PHI (Protected Health Information). The fact it affects multiple pages suggests systemic code reuse of the vulnerable pattern. The sid parameter appearing in examples suggests this may be part of a healthcare provider integration flow, increasing the attack surface. Report lacks information on bounty amount and response timeline from Omnipod security team.

## Full report
<details><summary>Expand</summary>

## Summary:
DOM based XSS was found on multiple pages (and may exist on still more pages)

## Steps To Reproduce:
1. Navigate to the following URL:
https://www.omnipod.com/freedom/birthdate-confirmation?sid=a1t2J000005vUzlQAE&#'onload='alert(document.domain)
2. Observe alert box appears containing the domain from which the injected script is executed.
NOTE: The value of the sid parameter does not seem to matter for this vulnerability

OR

1. Navigate to the following URL:
https://www.omnipod.com/pif/thanks-freedom?&#'onload='alert(document.domain)
2. Observe alert box appears containing the domain from which the injected script is executed.

## Supporting Material/References:
There are two screenshots attached that demonstrate these vulnerabilities

This appears to be the vulnerable script:

<script>
 var loc = window.location.toString();
 var params = loc.split('?')[1];
 //var srcstring = "https://na-sandbox.myomnipod.com/test-lic-p4-proc?" + params;
 var srcstring = "https://na.myomnipod.com/lic-p4-proc?" + params;

document.write("<iframe id='frame' name='frame' src='" + srcstring + "' width='950'></iframe>");
 </script>

## Impact

An attacker could use Cross-Site Scripting to modify the appearance of the site to deface it, to log user keystrokes, to create forms on your site which request confidential information that is then sent to the attacker, or even hijack user sessions.

</details>

---
*Analysed by Claude on 2026-05-12*
