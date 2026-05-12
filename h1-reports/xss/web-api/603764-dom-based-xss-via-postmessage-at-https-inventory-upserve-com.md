# DOM Based XSS via Insecure postMessage Origin Validation at inventory.upserve.com/login/

## Metadata
- **Source:** HackerOne
- **Report:** 603764 | https://hackerone.com/reports/603764
- **Submitted:** 2019-06-08
- **Reporter:** gamer7112
- **Program:** Upserve
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** DOM-based XSS, Insecure postMessage Origin Validation, Unsafe eval(), Origin Spoofing
- **CVEs:** None
- **Category:** web-api

## Summary
The login page at inventory.upserve.com receives postMessages with insufficient origin validation using substring matching (indexOf) instead of strict equality checks. An attacker can create a malicious domain like 'https://hq.upserve.com.attacker.com' to bypass the check and execute arbitrary JavaScript via the eval() function, potentially stealing login credentials.

## Attack scenario
1. Attacker registers a domain like 'hq.upserve.com.attacker.com' or crafts a subdomain under their control
2. Attacker creates a malicious HTML page hosted on that domain containing postMessage code that sends an 'exec' payload
3. Attacker tricks a victim into visiting the malicious page (via phishing, social engineering, or ad injection)
4. Victim's browser establishes a window reference to inventory.upserve.com/login/
5. Malicious postMessage bypasses origin check due to substring matching and triggers eval() with attacker payload
6. Attacker captures login credentials, session tokens, or performs account takeover actions

## Root cause
The origin validation uses `~e.origin.indexOf("https://hq.upserve.com")` which performs substring matching rather than strict equality comparison. This allows any origin containing the string 'https://hq.upserve.com' to pass validation. Additionally, the use of eval() to execute arbitrary code from postMessage is fundamentally unsafe regardless of origin validation.

## Attacker mindset
An attacker recognized that substring-based origin validation is a common implementation mistake. By understanding how indexOf() works and that domain registration/subdomain control can include trusted domain names, they identified a bypass vector. The presence of eval() made the payload delivery straightforward, and targeting a login page maximizes the value of any XSS exploitation.

## Defensive takeaways
- Always use strict equality checks for origin validation: use `e.origin === "https://hq.upserve.com"` instead of indexOf()
- Never use eval() to execute code from postMessages; use safer alternatives like JSON.parse() for data or structured message protocols
- Implement a whitelist of allowed origins and validate against it explicitly
- Consider using Content Security Policy (CSP) to restrict eval() execution globally
- Use postMessage only for passing data, not executable code; implement a command-based architecture if cross-origin RPC is needed
- Apply defense-in-depth: validate origin, validate data structure, validate individual fields, and avoid dangerous functions
- Regularly audit all postMessage listeners for security issues

## Variant hunting
Hunt for similar patterns: (1) Search for other postMessage listeners using indexOf/includes for origin checks across application domains, (2) Look for eval(), Function(), setTimeout() with string arguments in postMessage handlers, (3) Audit subdomains and related domains for reverse origin validation bypasses, (4) Check for postMessage handlers without explicit origin validation, (5) Review any cross-origin iframe communication patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1187 - Forced Authentication
- T1539 - Steal Web Session Cookie

## Notes
This is a classic example of security implementation mistakes: (1) substring matching instead of exact matching for origin validation, and (2) use of eval() for code execution. The vulnerability is particularly severe because it targets a login page where credentials are at highest risk. The report URL appears to have the POC domain redacted (████████), suggesting the reporter responsibly disclosed without publishing the actual exploit details publicly.

## Full report
<details><summary>Expand</summary>

#Description
DOM based XSS is possible at https://inventory.upserve.com/login/ due to insecure origin checking when receiving a postMessage.

#POC
1. Visit https://hq.upserve.com.████████/upserve_xss.html
2. Click link
3. View alert on https://inventory.upserve.com

#Vulnerable Code
```javascript
window.addEventListener("message", function(e) {
  if (~e.origin.indexOf("https://hq.upserve.com")) {
    if (e.data && typeof e.data == "object") {
      try {
        if (e.data["exec"]) {
          eval(e.data["exec"]);
        }
      } catch (err) {
        console.log(err);
      }
    } else {
      console.log("Non-object passed");
    }
  } else {
    console.log("Incorrect origin: " + e.origin.toString());
    return;
  }
});
```
The origin check simply determines if "https://hq.upserve.com" is anywhere in the origin so an origin like "https://hq.upserve.com.mydomain.com" will pass this check just fine.

## Impact

Due to the page being a login page, login credentials could be logged and stolen when a victim goes to login.

</details>

---
*Analysed by Claude on 2026-05-12*
