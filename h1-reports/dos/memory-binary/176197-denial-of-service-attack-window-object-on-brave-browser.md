# Denial of Service Attack via Unvalidated window.close() in Brave Browser

## Metadata
- **Source:** HackerOne
- **Report:** 176197 | https://hackerone.com/reports/176197
- **Submitted:** 2016-10-16
- **Reporter:** sahiltikoo
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Improper Input Validation, Design Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
Brave browser fails to properly validate window.close() calls, allowing arbitrary scripts to close the current window without user confirmation or script-origin verification. This violates browser security standards where only windows opened by scripts should be closeable by those scripts, enabling attackers to forcibly close user windows via malicious HTML.

## Attack scenario
1. Attacker crafts HTML file containing javascript:window.close(self) link or event handler
2. Attacker tricks victim into opening HTML file in Brave browser (via email, malicious website, etc.)
3. Victim clicks link or triggers the JavaScript event containing window.close()
4. Brave browser executes window.close() without validating if script opened the window
5. Parent/current window closes immediately without confirmation dialog
6. User loses their active session and browser window is unexpectedly terminated

## Root cause
Brave browser implements insufficient validation when processing window.close() method calls. The browser does not verify the origin/source relationship (whether the calling script actually opened the target window) before allowing window closure, deviating from W3C standards that require such verification.

## Attacker mindset
An attacker would leverage this to disrupt user experience through forced window closure. This could be combined with social engineering to make users believe their browser or computer is malfunctioning, or used to interrupt critical user activities. The low barrier to exploitation (simple HTML link) and lack of user confirmation make this attractive for harassment or disruption campaigns.

## Defensive takeaways
- Implement strict origin verification before allowing window.close() - only permit closing windows that were explicitly opened by the same script
- Add user confirmation dialogs when scripts attempt to close windows they did not open
- Follow W3C Window specification standards which explicitly restrict window.close() to windows opened by scripts
- Audit other browser APIs for similar insufficient validation of script permissions
- Test browser against W3C compliance test suites for window object behavior
- Consider implementing Content Security Policy restrictions on window operations

## Variant hunting
Test window.open() followed by window.close() from different origins/protocols
Test dynamically generated iframe window closure attempts
Test popup window closure via parent window scripts
Test window.close() in event handlers (onclick, onload, onmouseover, etc.)
Test window.close() in service workers and web workers
Test timing attacks with delayed window.close() calls
Test window.close() behavior across different Brave versions and configurations

## MITRE ATT&CK
- T1561.001
- T1499.004

## Notes
Report identifies valid security issue but classification as 'Remote DoS' is somewhat overstated - impact is limited to closing the current browser window. Reporter correctly notes Firefox and Chrome properly implement W3C window closure restrictions. The POC uses javascript: protocol handler which is deprecated. Report demonstrates good security awareness by comparing against reference implementations.

## Full report
<details><summary>Expand</summary>

## Summary:
hey there,

The Brave browser is vulnerable to window object based denial of
service attack. The brave browser fails to sanitize a check when window.close()
function is called in number of dynamically generated events.. The
function is called in a suppressed manner and kills the parent window
directly by default which makes it vulnerable to denial of service attack.

When an attacker sends an html file to victim :-

<html>
<title>Brave Window Object  Remote Denial of Service.</title>
<head></head>
 
<body><br><br>
<h1><center>Brave Window Object  Remote Denial of Service</center></h1><br><br>
<h2><center>Proof of Concept</center></br></br> </h2>
 
 
<center>
<b>Click the  below link to Trigger the Vulnerability..</b><br><br>
<hr></hr>
 
<hr></hr>
<b><center><a href="javascript:window.close(self);">Brave  Window Object  DoS Test POC</a></center>
 
</center>
</body>
 
 
</html>

Here window.close() method should be sanitized and should not close the current window.I tested it in Firefox and chrome(Linux platform) and this widow object is validated there and current window doesn't close.
 
This security issue is a result of design flaw in the browser.Scripts must not close windows that were not opened by script,if script specific code is designed.
There must be a parent window confirmation check prior to close of window.
 

## Products affected: 

Latest Brave browser in Linux(Kali Linux)

## Steps To Reproduce:

1 Open the HTML file in brave browser in your Linux platform
2 click on the link provided 
3 You will see the current window i.e. the window in which the HTML file was opened closes.

## Supporting Material/References:

I have added a video POC and the html file.


</details>

---
*Analysed by Claude on 2026-05-24*
