# DOM Based XSS in www.hackerone.com via PostMessage (bypass of #398054)

## Metadata
- **Source:** HackerOne
- **Report:** 499030 | https://hackerone.com/reports/499030
- **Submitted:** 2019-02-21
- **Reporter:** honoki
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** DOM-based XSS, Postmessage origin validation bypass, Insufficient origin check
- **CVEs:** None
- **Category:** web-api

## Summary
A previous XSS fix in Marketo's forms2.min.js was bypassed through inadequate origin validation. An attacker could register a domain with a similar prefix (e.g., app-sj17.ma) to pass the vulnerable indexOf() check, allowing malicious postMessage events to execute JavaScript in the context of www.hackerone.com.

## Attack scenario
1. Attacker registers a Marcaronian .ma domain (app-sj17.ma) that matches the prefix of the legitimate Marketo domain (app-sj17.marketo.com)
2. Attacker hosts a malicious HTML page on the registered domain containing postMessage code that sends crafted XSS payloads
3. Victim visits attacker's malicious page or is redirected to it through social engineering
4. The vulnerable origin check using indexOf() incorrectly validates the malicious origin as legitimate since 'app-sj17.ma' begins with 'app-sj17'
5. Malicious postMessage event is processed by the vulnerable Marketo code, executing JavaScript
6. Attacker achieves code execution in the context of www.hackerone.com or performs phishing attacks in non-CSP-protected browsers

## Root cause
Marketo's origin validation uses indexOf() to check if the postMessage origin matches the expected domain. The check verifies if the expected origin appears at the start of the received origin string (0 === i.indexOf(a.originalEvent.origin)), but this logic is inverted or misapplied. An attacker can craft a domain prefix that passes this insufficient string matching, allowing any domain starting with the vulnerable pattern to be accepted.

## Attacker mindset
Resourceful and creative - demonstrates understanding that domain registration can be weaponized to exploit insufficient string-based origin validation. The attacker identifies that the fix attempted by Marketo was incomplete and finds an unconventional bypass by purchasing a domain in a lesser-known TLD (.ma) rather than attempting technical manipulation.

## Defensive takeaways
- Use strict equality or regex anchoring for origin validation instead of indexOf() - validate complete domain matches with proper delimiters
- Implement whitelist-based origin validation that checks exact matches or uses proper URL parsing APIs
- Use window.location.origin or URL constructor for proper origin comparison instead of string matching
- Apply Content Security Policy (CSP) with frame-ancestors directive to mitigate postMessage-based attacks
- Validate postMessage data structure and type, not just origin
- Consider using Cross-Origin Resource Sharing (CORS) headers appropriately
- Implement defense-in-depth by validating both origin and message content signatures

## Variant hunting
Search for similar postMessage handlers using indexOf() for origin validation across Marketo-integrated sites. Look for other third-party embedded content (analytics, forms, payment processors) that may use similar vulnerable validation patterns. Test for bypasses using similar-prefix domains across different TLDs (.io, .co, .dev, etc.)

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
This is a particularly clever vulnerability that combines technical understanding with creative domain registration strategy. The attack demonstrates that security patches must use proper cryptographic or strict matching approaches rather than simple string operations. The vulnerability is especially impactful because it affects the widely-used HackerOne bug bounty platform and could grant access to sensitive security data. The €60 cost of domain registration makes this attack economically viable for attackers.

## Full report
<details><summary>Expand</summary>

**Summary**

The security fix by Marketo to resolve the issue reported by @adac95 in #398054 can be bypassed by purchasing an .ma domain for €60.

**Description**

The issues described by @adac95 in #398054 remain insufficiently resolved because of an inadequate security check by Marketo in the following piece of JavaScript in `forms2.min.js`
```javascript
if (a.originalEvent && a.originalEvent.data && 0 === i.indexOf(a.originalEvent.origin)) {
    var b;
    try {
        b = j.parseJSON(a.originalEvent.data)
    } catch (c) {
        return
    }
    b.mktoReady ? f() : b.mktoResponse && e(b.mktoResponse)
}
```
Since the variable `i` resolves to `https://app-sj17.marketo.com/[...]`, an attacker can bypass this check by registering the Marcarian domain `app-sj17.ma` for €60. I have done so for the sake of a good POC,  but the registration process is slow. I will comment on this issue when the POC is live.

### Steps To Reproduce

0. Wait for the POC to be live (registration of my .ma domain is in progress)
1. Browse to my POC running on https://app-sj17.ma/marketo/post2.html (note that this is literally the POC written by @adac95)
2. Note the malicous redirect is still successfully executed;

## Impact

An attacker could be able to execute JavaScript in the context of the www.hackerone.com application, if the victim user makes use of a browser which does not support CSP. The attacker could also perform a limited phishing attack in Firefox or Microsoft Edge.

</details>

---
*Analysed by Claude on 2026-05-12*
