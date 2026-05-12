# POST-Based Reflected XSS in dailydeals.mtn.co.za

## Metadata
- **Source:** HackerOne
- **Report:** 1451394 | https://hackerone.com/reports/1451394
- **Submitted:** 2022-01-17
- **Reporter:** shuvam321
- **Program:** MTN (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), POST-based XSS, ColdFusion Parameter Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in dailydeals.mtn.co.za where unsanitized POST parameters (specifically CFID) are reflected back in HTTP responses without proper encoding. An attacker can craft a malicious form that, when submitted by a victim, executes arbitrary JavaScript in the victim's browser context.

## Attack scenario
1. Attacker creates a malicious HTML form targeting dailydeals.mtn.co.za with XSS payload in the CFID parameter containing SVG OnLoad event handler
2. Attacker hosts this form on attacker-controlled domain or injects it into legitimate site via social engineering
3. Victim visits attacker's page or receives link via phishing email/message
4. Victim's browser automatically submits the POST form to vulnerable endpoint
5. Server reflects CFID parameter value unsanitized in response HTML
6. Victim's browser parses malicious SVG payload and executes JavaScript confirm(1) demonstrating code execution

## Root cause
ColdFusion application fails to sanitize or HTML-encode the CFID session parameter before reflecting it in HTTP responses. The application likely uses ColdFusion's session management but outputs the CFID value directly without using proper output encoding functions like htmlEditFormat() or encodeForHTML().

## Attacker mindset
An attacker would recognize that ColdFusion applications commonly pass session identifiers (CFID/CFTOKEN) as parameters and often reflect these in responses. By crafting a POST-based attack, the attacker bypasses typical browser Same-Origin Policy protections that would block GET-based XSS. The choice of SVG with OnLoad event demonstrates knowledge of modern XSS bypass techniques that may evade simple script tag filtering.

## Defensive takeaways
- Always HTML-encode all user-supplied input and dynamic values before reflecting them in HTML context using framework-specific functions (htmlEditFormat in ColdFusion)
- Implement Content Security Policy (CSP) headers to restrict execution of inline scripts and external resources
- Use httpOnly and Secure flags on session cookies to prevent JavaScript access to sensitive tokens
- Validate and whitelist POST parameter values, rejecting or sanitizing suspicious patterns
- Implement input validation on both client and server side, rejecting parameters containing HTML/JavaScript syntax
- Use ColdFusion's built-in security features like CFPARAM with proper validation
- Apply output encoding appropriate to context (HTML, JavaScript, URL, CSS) depending on where data is rendered
- Regular security testing and code review, particularly for session handling and parameter reflection

## Variant hunting
Check for similar parameter reflection in CFTOKEN, other ColdFusion session variables (JSESSIONID, SESSIONID)
Test other endpoints that accept POST parameters with similar structure (search functionality, form submissions)
Investigate if GET variants exist alongside POST endpoints (common in legacy applications)
Search for other ColdFusion template files (.cfm) that may process and reflect these parameters
Test other cookie/session parameters from MTN applications and related subdomains
Examine whether persistent/stored XSS variants exist if parameters are saved in user profiles or databases
Check for DOM-based XSS if JavaScript processes these parameters client-side

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing (email-based vector for malicious form link)

## Notes
This is a straightforward reflected XSS in a POST parameter. The vulnerability is practical and impactful because POST-based XSS can be weaponized through malicious forms hosted externally or injected into legitimate sites. ColdFusion applications are historically vulnerable to parameter reflection issues due to flexible type handling and legacy coding practices. The CFID/CFTOKEN parameters are ColdFusion-specific session identifiers that should never be trusted for output without encoding. The bounty amount was not disclosed in the report, which is unusual for HackerOne reports and may indicate the report was not accepted or is still under resolution.

## Full report
<details><summary>Expand</summary>

## Summary:
Dear Team ,
I have found a post based reflected XSS in https://dailydeals.mtn.co.za/ .

## Steps To Reproduce:

1.Create a html file with following content .

<form action="https://dailydeals.mtn.co.za/index.cfm?GO=CRAVE_ESTABLISHMENTS_LIST" method="POST"><input type="hidden" name="location_id" value="0"><input type="hidden" name="suburb" value="0"><input type="hidden" name="search_phrase" value=""><input type="hidden" name="submit_search" value="Search"><input type="hidden" name="m" value=""><input type="hidden" name="cpID" value=""><input type="hidden" name="CFID" value="a611fd5d-822a-4c08-a032-bcac1551f032'&quot;<!--><Svg OnLoad=(confirm)(1)-->"><input type="hidden" name="CFTOKEN" value="0"></form><script>document.forms[0].submit()</script>

2.Open the HTML file in any web-browser. 
  
3.Cross site Scripting will be triggered .

## Impact

Attacker can exploit this vulnerability to steal users cookies , redirect them to arbitrary domain and perform various attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
