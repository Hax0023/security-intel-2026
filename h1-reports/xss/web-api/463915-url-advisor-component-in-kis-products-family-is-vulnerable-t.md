# Universal XSS in Kaspersky Internet Security URL Advisor via Unvalidated postMessage

## Metadata
- **Source:** HackerOne
- **Report:** 463915 | https://hackerone.com/reports/463915
- **Submitted:** 2018-12-17
- **Reporter:** palant
- **Program:** Kaspersky
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Insecure postMessage Implementation, Clickjacking, Missing Origin Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Kaspersky Internet Security's URL Advisor component is loaded as first-party content in Microsoft Edge, allowing an XSS vulnerability to escalate to Universal XSS affecting all websites. The component accepts untrusted data via postMessage without origin validation and assigns it to link targets, enabling JavaScript URL execution via clickjacking.

## Attack scenario
1. Attacker hosts a malicious webpage that frames the URL Advisor balloon component from google.com or other high-value domains
2. Attacker crafts a postMessage containing a javascript: URL payload targeting sensitive operations
3. Attacker uses clickjacking techniques (transparent overlays, fake game interface) to trick user into clicking the injected link
4. User's click executes arbitrary JavaScript in the context of google.com or other framed domain
5. Attacker exfiltrates sensitive data (cookies, tokens, DOM content) from the victim domain
6. Attack is repeatable across any domain where URL Advisor is active due to first-party loading mechanism

## Root cause
URL Advisor frame is loaded as first-party content on every domain in Microsoft Edge rather than as third-party content from a dedicated domain. The component fails to validate the origin of incoming postMessage events before processing untrusted data and assigning it to DOM link targets. The lack of X-Frame-Options headers allows framing, enabling clickjacking attacks.

## Attacker mindset
An attacker recognizes that third-party security tools injected as first-party content create an amplification vector for XSS vulnerabilities. By combining unvalidated postMessage handling with clickjacking and the tool's presence on all domains, a single XSS becomes a universal attack. The attacker exploits the false sense of security users have when visiting legitimate domains.

## Defensive takeaways
- Never serve third-party UI components as first-party content; always load from a dedicated, isolated domain
- Implement strict origin validation for all postMessage event handlers using event.origin checks
- Sanitize and validate all data received via postMessage before DOM assignment, especially href attributes
- Apply X-Frame-Options: DENY and CSP frame-ancestors directives to prevent framing
- Use Content Security Policy to restrict javascript: URL execution in sensitive contexts
- Treat XSS in security software with elevated severity due to amplification to universal scope
- Perform security reviews of messenger communication patterns between components

## Variant hunting
Check for similar postMessage vulnerabilities in other Kaspersky Edge extensions or browser integrations
Audit other first-party loaded security components for unvalidated postMessage handlers
Test other Kaspersky products for similar architectural issues in different browsers
Search for instances where security tools are injected with insufficient origin validation
Review iframe sandbox attributes and CSP policies in security tool implementations

## MITRE ATT&CK
- T1190
- T1185
- T1566
- T1176
- T1187

## Notes
This vulnerability demonstrates a critical architectural flaw: using first-party loading for third-party security components transforms any XSS into a universal XSS affecting all websites. The reporter correctly identified that Firefox and Internet Explorer implementations using kis.v2.scr.kaspersky-labs.com avoid this issue entirely. The attack requires no privileges and has high user interaction (clickjacking), making it practical. The fix requires both patching the XSS and redesigning the architecture to match the more secure implementation in other browsers.

## Full report
<details><summary>Expand</summary>

**Summary**
In Microsoft Edge, URL Advisor UI is served as first-party content on every domain. So the XSS vulnerability I found in this UI automatically applies to all websites, it allows running code in the context of *any* domain.

**Description**
URL Advisor frame is located under https://www.google.com/<INJECT_ID>/ua/url_advisor_balloon.html and https://www.yahoocom/<INJECT_ID>/ua/url_advisor_balloon.html in Microsoft Edge (always the same INJECT_ID value). It gets its content from a message sent via `window.postMessage()` without validating message origin. Under some circumstances it will assign that data as link target, so a malicious website can make that link point to a javascript: URL. Clickjacking then allows making the user click that link - while sites like google.com use X-Frame-Options header to disallow framing, no such restrictions are in place for the url_advisor_balloon.html frame.

**Environment**
- Scope: Application
- Product name: Kaspersky Internet Security
- Product version: 19.0.0.1088
- OS name and version (incl SP): Windows 10.0.17134
- Attack type: Universal XSS
- Maximum user privileges needed to reproduce your issue: no privileges

**Steps to reproduce**
1. Download attached `server.py` and `universal_xss.html` to some directory on your computer and run `server.py` (Python 3 required). This is a very rudimentary HTTP server running on http://localhost:5000/, you could use some other web server as well.
2. Edit the file %WINDIR%\sysnative\drivers\etc\hosts as administrator and add the following line: `127.0.0.1 www.google.example.com`. Normally, you would just use a subdomain of a domain you own - the host name has to start with "www.google." for URL Advisor to apply to it.
3. Open Microsoft Edge and go to http://www.google.example.com:5000/universal_xss.html
4. As advised by the page, move your mouse and click somewhere on the page.

You will see an alert message saying: "Hi, this is JavaScript code running on www.google.com." That's the result of the code `alert('Hi, this JavaScript code is running on ' + document.domain)` executing in the context of the Google website. Injecting code into any other domain would have been easily possible as well.

**Recommendation**
This user interface should never be served as first-party, even once the vulnerability here is fixed. Any XSS vulnerability in Kaspersky code automatically elevates to Universal XSS otherwise, this is too dangerous. Frankly, I don't see why it is done in this way with Microsoft Edge - in Firefox and Internet Explorer the same UI is always served via kis.v2.scr.kaspersky-labs.com, so vulnerabilities here don't affect other websites.

## Impact

A malicious website can easily make users click by pretending to be a game. And while the user clicks, they will be allowing the attackers to inject code into various internet domains and exfiltrating data in the background.

</details>

---
*Analysed by Claude on 2026-05-12*
