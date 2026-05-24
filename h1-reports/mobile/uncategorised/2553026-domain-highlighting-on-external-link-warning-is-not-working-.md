# Domain Highlighting Malfunction in External Link Warning on Mobile Chrome & Edge

## Metadata
- **Source:** HackerOne
- **Report:** 2553026 | https://hackerone.com/reports/2553026
- **Submitted:** 2024-06-17
- **Reporter:** sarthakbhingare015
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** UI/UX Security Bypass, Homograph Attack Enablement, Cross-Browser Inconsistency, Security Control Failure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The external link warning interstitial page fails to highlight destination domains on Chrome and Edge mobile browsers, allowing attackers to craft deceptive URLs that users cannot verify before navigation. This security control bypass re-introduces previously patched homograph and URL obfuscation vulnerabilities, enabling social engineering attacks where users are tricked into visiting malicious sites believing they are legitimate.

## Attack scenario
1. Attacker crafts a deceptive URL using techniques like decimal IP notation (google.com@1234567890/download/file) or URL encoding (www.hackerone.com%2F...@evil.com/) that obscures the true destination
2. Attacker distributes the malicious link via social engineering (phishing email, message, etc.) targeting mobile users
3. Victim clicks the link on Chrome or Edge mobile browser
4. The external link warning interstitial page displays but fails to highlight the actual destination domain due to browser-specific rendering bug
5. Victim cannot visually verify the destination and proceeds, trusting the warning system worked correctly
6. Victim is redirected to attacker-controlled server (e.g., 1234567890 IP or evil.com) where credentials/malware can be harvested

## Root cause
Client-side JavaScript code for domain highlighting in the external link warning interstitial page contains browser-specific bugs that prevent proper DOM manipulation or CSS styling on Chrome and Edge mobile platforms. This is likely a rendering/JavaScript execution issue specific to mobile Chromium-based browsers, possibly related to viewport dimensions, DOM event timing, or CSS selector failures.

## Attacker mindset
An attacker would recognize this regression as a golden opportunity to exploit users on mobile devices where security awareness is lower. They would specifically craft URLs to bypass homograph detection while leveraging the non-functional highlighting to create plausible deniability—the warning page still appears, but offers no protective information, giving false confidence.

## Defensive takeaways
- Implement comprehensive cross-browser and cross-device automated testing for all security-critical UI components before deployment
- Use regression testing suite to catch re-emergence of previously fixed vulnerabilities
- Add automated visual regression testing (screenshot comparison) for security warning pages across all major browsers and viewports
- Implement server-side domain validation and highlighting as fallback rather than relying solely on client-side JavaScript
- Create unit and integration tests specifically for URL parsing and domain extraction logic across various URL obfuscation techniques
- Establish code review checklist for security-critical features to flag deviations from past fixes
- Monitor analytics for unusual external link warning dismissal patterns that might indicate UI functionality failure
- Consider implementing Content Security Policy and other defense-in-depth measures that don't rely on visual user comprehension

## Variant hunting
Test domain highlighting on other mobile browsers (Samsung Internet, UC Browser, Opera Mobile)
Test with additional URL obfuscation techniques (Unicode normalization, mixed case homographs, IPv6 notation)
Verify if highlighting fails only on mobile or also on responsive/zoomed desktop views
Check if the issue affects other warning interstitials (HTTPS downgrades, site reputation warnings)
Test with extremely long URLs, special characters, and internationalized domain names
Verify behavior across different Chrome/Edge versions and Android versions

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1187 - Forced Authentication
- T1589.001 - Gather Victim Identity Information: Credentials

## Notes
This is a regression of previously patched issues (#113070, #59469, #271324), indicating either incomplete fix implementation, code rollback, or inadequate test coverage. The cross-browser nature suggests environment-specific code paths or build differences. The impact is elevated because it affects security warnings designed to protect users—when these fail silently, they create false confidence and are more dangerous than no warning at all.

## Full report
<details><summary>Expand</summary>

There have been multiple issues with External Link Warning in the past. Sometimes it's Homograph, sometimes more than 2 slashes in link, sometimes domain highlighting and/or weird markdown. And these all have been fixed.

Recently, I've noticed a strange issue with Chrome and Edge browsers on mobile. The highlighting of domains doesn't work at all on External Link Warning interstitial page. None of the links are highlighted. Similar issues were fixed in the past by HackerOne (you can see the bug references below). It seems like these problems have appeared again in the code.

### Steps To Reproduce

1. Log into your account on your mobile from either Latest version of Microsoft Edge browser or Google Chrome.
1. Click on links mentioned below in **Impact** section.
1. Observe that none External link warning interstitial page highlights domain.

## Test cases: Google Chrome, Microsoft Edge & Firefox👇

- Below are the images from Chrome browser along with Chrome's details:
{F3363744} {F3363747} {F3363766}

- Below are the images from Microsoft Edge browser along with Edge's details:
{F3362316} {F3362317} {F3363753}

- Below are the images from Firefox Browser along with Firefox's details:
{F3362321} {F3362323} {F3363752}

## Impact

- https://google.com@1234567890/download/safest_file: Browsers automatically convert decimal to IP address. Upon clicking the link from mobile on Edge or Chrome browser, nothing is highlighted in External link warning interstitial page, as a result user may be fooled thinking that it is redirected to **google.com** but in reality it will be redirected to a attacker's controlled server.
- www.hackerone.com%2Fbugs%3Fsubject=user&report_id=81070&view=all&substates%5B%5D=new&substates%5B%5D=triaged&substates%5B%5D=needs-more-info&substates%5B%5D=resolved&substates%5B%5D=not-applicable&substates%5B%5D=informative&substates%5B%5D=duplicate&substates%5B%5D=spam&text_query=@evil.com/&sort_type=latest_activity&sort_direction=descending&limit=25&page=1: This is a clever URL to trick user thinking that it is being redirected to a valid website. But in reality it is being redirected to **evil.com**.

The domain highlighting functionality is meant to let users know where is the browser redirecting upon proceeding. But in Edge & Chrome browser on Mobile, this functionality is not working as intended. As a result a malicious actors would take advantage of this to fool users into redirecting to malicious sites.

## Reference bugs fixed in past by HackerOne
#113070 - Multiple issues with Markdown and URL parsing
#59469 - Fake URL + Additional vectors for homograph attack
#271324 - Homograph fix Bypass 

</details>

---
*Analysed by Claude on 2026-05-24*
