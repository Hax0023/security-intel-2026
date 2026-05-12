# DOM Based Reflected Cross Site Scripting in Outdated Swagger UI

## Metadata
- **Source:** HackerOne
- **Report:** 2321874 | https://hackerone.com/reports/2321874
- **Submitted:** 2024-01-16
- **Reporter:** nhx1
- **Program:** MTN (Bug Bounty Program)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
An outdated version of Swagger UI running on notification-server-v2.sz-my.mtn.com is vulnerable to DOM-based reflected XSS. An attacker can inject malicious scripts via the configUrl parameter which gets executed in the victim's browser. This could lead to account takeover for applications under the *.mtn.com domain.

## Attack scenario
1. Attacker identifies that notification-server-v2.sz-my.mtn.com is running vulnerable Swagger UI version
2. Attacker crafts a malicious URL with configUrl parameter pointing to attacker-controlled JSON file containing XSS payload
3. Attacker sends crafted URL to victim via phishing email, social engineering, or malicious website
4. Victim clicks the link and visits the vulnerable Swagger UI page with malicious configUrl parameter
5. Swagger UI processes the configUrl parameter without proper sanitization and executes the XSS payload
6. Attacker's JavaScript executes in victim's browser, allowing session hijacking, credential theft, or account takeover

## Root cause
The Swagger UI version used does not properly sanitize the configUrl parameter before processing it. The parameter is reflected in the DOM and executed as code without validation or encoding. Outdated versions lack security patches for known Swagger XSS vulnerabilities.

## Attacker mindset
Reconnaissance-focused attacker who identified an easy target (outdated software with known vulnerabilities). Low effort exploitation - reusing known Swagger exploits. Targeting widespread platform (*.mtn.com) for maximum impact and account compromise potential.

## Defensive takeaways
- Immediately upgrade Swagger UI to the latest patched version
- Implement strict input validation and sanitization for all URL parameters, especially configUrl
- Use Content Security Policy (CSP) headers to restrict script execution origins
- Encode all user-controlled data before inserting into DOM
- Implement regular vulnerability scanning for outdated dependencies
- Maintain an inventory of all versions running on internal assets
- Apply security patches promptly across all environments
- Use allowlist validation for configUrl to only accept trusted configuration sources

## Variant hunting
Check other Swagger instances on mtn.com for same vulnerability
Test other URL parameters in Swagger UI for similar reflection/execution flaws
Look for other outdated versions of popular frameworks (Springfox, etc.) on internal assets
Test query parameters in index.html for direct injection points
Check if other notification-server versions (v1, v3) have similar issues
Look for similar DOM-based XSS in other swagger-ui distributions across the organization

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1003

## Notes
Report lacks detailed reproduction steps and payload details, but core vulnerability is clear. The use of external surge.sh domain for hosting payload demonstrates typical attacker methodology. This is a classic case of outdated software running in production with known CVEs. The *.mtn.com domain scope indicates potential for subdomain takeover through account compromise.

## Full report
<details><summary>Expand</summary>

## Summary:
I hope you're doing well. I stumbled upon one of your assets. Upon further inspection I realized that the asset was running an outdated version of Swagger. 
The outdated version of Swagger is well-known for Cross-Site Scripting vulnerabilities so I went ahead and attempted to test it in  https://notification-server-v2.sz-my.mtn.com/.  Turns out, it's vulnerable to Cross-Site Scripting. To reproduce it, please follow the steps of reproduction. I have not assessed the full impact of this vulnerability but it is highly probable that a malicious actor could exploit to takeover accounts of applications hosted under *.mtn.com. I hope this gets patched soon. If there's some additional information that you need from my side, please let me know. Thank you. 

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Go to the following URL https://notification-server-v2.sz-my.mtn.com/index.html?configUrl=https://jumpy-floor.surge.sh/test.json
  1. Observe the alert pop up like in the screenshot below
  

{F2983813}

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

A malicious actor could execute arbitrary scripts

</details>

---
*Analysed by Claude on 2026-05-12*
