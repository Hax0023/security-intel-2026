# Denial of Service in Brave Browser via Malformed Alert() Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 176066 | https://hackerone.com/reports/176066
- **Submitted:** 2016-10-16
- **Reporter:** sahiltikoo
- **Program:** Brave Browser
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Input Validation, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
A maliciously crafted HTML file containing an excessively large parameter in a JavaScript alert() function causes the Brave Browser to crash on Linux systems, logging out the user. The vulnerability stems from insufficient input validation and resource handling when processing alert() dialog parameters.

## Attack scenario
1. Attacker creates a malicious HTML file with an alert() function containing an extremely large string parameter
2. Attacker sends the HTML file to a victim via email, messaging, or hosts it on a website
3. Victim opens the file in Brave Browser on a Linux system
4. Browser attempts to render the alert dialog with the oversized parameter
5. Browser memory or processing resources become exhausted
6. Browser crashes with error message 'OH! something went wrong' and user is logged out

## Root cause
The Brave Browser fails to validate or limit the size of parameters passed to the alert() JavaScript function, allowing attackers to exceed reasonable memory/processing thresholds, causing a crash when the browser attempts to allocate resources for the dialog box.

## Attacker mindset
Exploit a simple but effective vector (alert() function) requiring minimal technical sophistication to craft a DoS payload. Target user availability by forcing browser crashes and session termination, demonstrating browser robustness issues.

## Defensive takeaways
- Implement strict input size limits on all JavaScript dialog functions (alert, confirm, prompt)
- Add resource consumption guardrails to prevent excessive memory allocation
- Validate and truncate excessively large strings before passing to UI rendering components
- Implement graceful error handling rather than full application crashes
- Add fuzz testing for JavaScript built-in functions with extreme/malformed inputs
- Consider sandboxing or resource limits for dialog box rendering
- Monitor for suspicious patterns of oversized parameters in security telemetry

## Variant hunting
Test other dialog functions: confirm(), prompt() with oversized parameters
Attempt nested alert() calls with large parameters
Test with special characters, Unicode, or binary data in oversized parameters
Investigate console.log() and other output functions with large payloads
Check if vulnerability affects other Chromium-based browsers
Test on other platforms (macOS, Windows) for cross-platform impact
Attempt DOM manipulation with extremely large elements
Test iframe injection with similar payloads

## MITRE ATT&CK
- T1499
- T1190

## Notes
Vulnerability appears to be platform-specific (Linux/Kali Linux mentioned). The proof-of-concept file is referenced but content details not provided in report. Severity is medium rather than high since it requires user interaction (opening file). The complete payload size is not disclosed in the writeup, limiting reproducibility analysis. Report lacks technical depth regarding memory consumption patterns or specific Brave version information.

## Full report
<details><summary>Expand</summary>



## Summary:
Hey there,

Basically,an HTML sent by an attacker to a victim can cause dos attack(whole system log's out) when that file is opened by the victim in his brave browser.This vulnerability is occurring because browser is not able to handle the input passed in alert() JavaScript function.This bug has been tested on latest brave browser in Linux platform.

## Products affected: 

Brave's Browser in Linux(Kali Linux)

## Steps To Reproduce:


1 create an html file like :-

Brave.html( it is attached as POC below) i couldn't write the content of file here because the value inside alert() parameter is too large to be displayed here.

2 Open the file in your Brave browser in Linux platform.

## Supporting Material/References:

I have attached an html file below just download it and open it up in brave browser on linux system and 

screen will show "OH! something went wrong and you will be logged out".


</details>

---
*Analysed by Claude on 2026-05-24*
