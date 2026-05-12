# Reflected XSS via POST Parameter in Water Control Application

## Metadata
- **Source:** HackerOne
- **Report:** 1003433 | https://hackerone.com/reports/1003433
- **Submitted:** 2020-10-09
- **Reporter:** ofjaaaah
- **Program:** U.S. Department of Defense (DoD)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the shefgraph-historic.cfm endpoint where POST parameters, specifically 'fld_frompor', are not properly sanitized or encoded before being reflected in the application response. An attacker can craft a malicious HTML form that submits specially crafted POST data containing JavaScript payloads to execute arbitrary code in a victim's browser.

## Attack scenario
1. Attacker identifies that the 'fld_frompor' POST parameter on shefgraph-historic.cfm is vulnerable to XSS
2. Attacker crafts a hidden HTML form containing malicious JavaScript payload in the fld_frompor parameter value: 1"<!--><Svg OnLoad=(confirm)(1)<!--
3. Attacker hosts this form on a controlled website or distributes it via phishing/social engineering to DoD users
4. Victim visits the attacker's page and the form auto-submits via JavaScript, sending the malicious POST request to the target application
5. The vulnerable application reflects the unsanitized payload back in the response, causing the JavaScript to execute in the victim's browser context
6. Attacker achieves arbitrary code execution and can steal session tokens, modify application data, or perform actions as the authenticated user

## Root cause
The application fails to properly encode or validate POST parameter values before reflecting them in the HTTP response. The parameter 'fld_frompor' accepts user input containing HTML/JavaScript without sanitization, allowing SVG-based event handlers to execute. The use of HTML comments (<!--) further helps bypass basic filters by breaking out of expected input contexts.

## Attacker mindset
The attacker demonstrates knowledge of multiple XSS bypass techniques: using SVG elements with event handlers, HTML comment syntax for context breakout, and form auto-submission via POST to bypass typical phishing/URL-based defenses. This suggests familiarity with OWASP testing methodologies and ColdFusion application vulnerabilities.

## Defensive takeaways
- Implement strict input validation on all POST parameters with allowlist-based approach for expected data formats
- Apply context-appropriate output encoding (HTML entity encoding) to all user-controlled data reflected in responses
- Use a Web Application Firewall (WAF) with rules to detect and block SVG/event handler injection patterns
- Implement Content Security Policy (CSP) headers to restrict inline script execution and limit event handler functionality
- Conduct security code review of all ColdFusion CFML code handling user inputs, particularly form parameters
- Utilize automated SAST tools to detect reflected XSS vulnerabilities in the codebase
- Implement regular security testing including DAST scanning against POST-based XSS vectors
- Apply principle of least privilege to user sessions to limit damage from XSS exploitation

## Variant hunting
Hunt for similar patterns: (1) Other .cfm endpoints accepting form parameters without encoding, particularly those with 'fld_' prefixes; (2) Parameters named 'from', 'to', 'range', 'value', 'input' in water/utility management systems; (3) CFML <cfdump>, <cfoutput>, or direct variable outputs without encodeForHTML(); (4) POST endpoints with sid/session parameters indicating potential authentication bypass chains; (5) Graph/report generation endpoints which commonly reflect user parameters; (6) Other DoD contractor applications using legacy ColdFusion frameworks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1059 - Command and Scripting Interpreter
- T1539 - Steal Web Session Cookie

## Notes
The vulnerability is particularly concerning in DoD context due to potential for lateral movement and access to critical infrastructure. The use of POST-based XSS rather than GET-based reduces URL-based detection but increases weaponization complexity. ColdFusion applications commonly suffer from this class of vulnerability due to unsafe variable handling. The researcher demonstrated responsible disclosure to DoD. The SVG+OnLoad+confirm pattern is a well-known bypass for basic filter rules.

## Full report
<details><summary>Expand</summary>

#XSS to POST 

URL =  █████████


Good morning team DoD..
I located an XSS on the site. 
I hope to help team DoD more and more. Thank you


```html
<form action=█████████/WaterControl/shefgraph-historic.cfm?sid=BL110 method=POST><input type=hidden name="fld_graphrslow" value="Y"><input type=hidden name="fld_graphrslow" value="N"><input type=hidden name="Submit" value="View Graph"><input type=hidden name="fld_from1" value="01/01/2020"><input type=hidden name="fld_to1" value="12/31/2020"><input type=hidden name="fld_displaytype" value="S"><input type=hidden name="fld_type1" value="Plot"><input type=hidden name="fld_frompor" value="1&quot;&lt;!--&gt;&lt;Svg OnLoad=(confirm)(1)&lt;!--"><input type=hidden name="fld_topor" value="1231"><input type=hidden name="fld_year1" value="2020"><input type=hidden name="fld_year2" value="2020"><input type=hidden name="fld_mon1" value="01"><input type=hidden name="fld_day1" value="01"><input type=hidden name="fld_mon2" value="12"><input type=hidden name="fld_day2" value="31"><input type=hidden name="fld_param" value="HG"><input type=submit value=XSS></form>
```

## Impact

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:

    Perform any action within the application that the user can perform.
    View any information that the user is able to view.
    Modify any information that the user is able to modify.
    Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

</details>

---
*Analysed by Claude on 2026-05-12*
