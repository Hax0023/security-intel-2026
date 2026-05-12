# chrome://brave Navigation via Bookmarks Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 415178 | https://hackerone.com/reports/415178
- **Submitted:** 2018-09-27
- **Reporter:** qab
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper Access Control, URI Scheme Bypass, Privilege Escalation, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Brave browser failed to properly restrict navigation to the privileged chrome://brave URI when accessed through bookmarks, even with CTRL+click or middle-click navigation. This vulnerability could be chained with other exploits to achieve remote code execution by tricking users into bookmarking a malicious URL via drag-and-drop, then opening it through bookmark interactions.

## Attack scenario
1. Attacker hosts a proof-of-concept HTML page on the web that instructs users to save it locally
2. When the PoC is opened from the local filesystem, it displays a popup window containing an anchor tag
3. User drags the anchor tag into their browser's bookmark bar, creating a bookmark to chrome://brave
4. Attacker instructs user to open the bookmark using CTRL+click, middle-click, or right-click 'open in new tab'
5. Browser navigates to the restricted chrome://brave URI due to the bookmark bypass
6. Attacker chains this with chrome://brave RCE vulnerability (report 395737) to achieve code execution

## Root cause
Brave's URI navigation security checks failed to properly validate the source of navigation when the destination was accessed through bookmarks. The browser distinguished between direct navigation and bookmark-based navigation but did not enforce the same restrictions for both paths, allowing bookmarks to bypass URI scheme protections.

## Attacker mindset
A creative attacker who discovered a multi-step exploitation chain by combining user interaction tricks (drag-and-drop bookmarking) with URI scheme bypasses and chaining to existing RCE vulnerabilities. The attacker demonstrated sophisticated understanding of browser security boundaries and social engineering by requiring minimal user interaction while maximizing impact.

## Defensive takeaways
- Enforce consistent URI navigation restrictions regardless of the source (direct, bookmark, link, or redirect)
- Implement strict whitelist validation for all chrome:// URI access attempts
- Apply the same security checks to all navigation methods including bookmark activation
- Consider warning users before opening bookmarks to restricted URIs
- Audit drag-and-drop functionality to prevent unexpected bookmark creation or modification
- Implement Content Security Policy headers to prevent unauthorized local file handling
- Chain vulnerability analysis: when fixing XSS-to-RCE chains, ensure all entry points are secured

## Variant hunting
Test other restricted URI schemes (chrome://, about://, brave://) through various navigation methods
Investigate bookmark sync functionality for potential remote exploitation vectors
Examine all drag-and-drop handlers for security implications
Test navigation from different contexts: frames, workers, service workers, extensions
Analyze bookmark import/export functionality for injection possibilities
Research whether other Chromium-based browsers have similar bypass issues
Test combinations of this bypass with other local file disclosure vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1566 - Phishing
- T1553 - Subvert Trust Controls
- T1578 - Modify Cloud Compute Infrastructure

## Notes
This report demonstrates a sophisticated multi-vulnerability exploitation chain. The attacker identified that bookmark-based navigation bypassed URI scheme restrictions, and proposed chaining this with local file disclosure (report 415167) and RCE vulnerabilities (report 395737) to create a complete attack requiring only user interaction. The local filesystem requirement was seen as bypassable through hypothetical local file XSS techniques. The vulnerability affected Brave 0.24.0 and underlying Chromium 69.0.3497.100. The Muon framework (Brave's then-current architecture) may have contributed to the security gap.

## Full report
<details><summary>Expand</summary>

## Summary:

'chrome://brave'  can be navigated to using the middle mouse click (or normal click with CTRL held) IFF coming from a bookmark. I am also using a small bug to actually trick a user into bookmarking our crafted URL through drag and drop.

## Products affected: 
Brave: 0.24.0 
V8: 6.9.427.23 
rev: f657f15bf7e0e0c50a2b854c6b05edb59bfc556c 
Muon: 8.1.6 
OS Release: 10.0.17134 
Update Channel: Release 
OS Architecture: x64 
OS Platform: Microsoft Windows 
Node.js: 7.9.0 
Brave Sync: v1.4.2 
libchromiumcontent: 69.0.3497.100

## Steps To Reproduce:

1. Host attached PoC in any web
2. Once opened, you will be instructed to save the html file locally and open it this way
3. Open the saved PoC from local disk
4. Click anywhere to open a popup
5. Drag the anchor tag into the main window bookmark bar (if you never bookmarked anything then just right click and bookmark)
6. Hold CTRL and click on the new bookmark, or right click and press "open in new tab"

## Impact

Navigating to chrome://brave is a bad thing since it can lead to RCE ( https://hackerone.com/reports/395737 )
 
We can also use another bug I filed ( https://hackerone.com/reports/415167 ) which can detect local files. If there is a way to drop HTML files into the local disk (cache or some other possibility) we can then try to use bug 415167 to bypass having to know OS username and any potentially salted folders. If this is achievable we can skip the part where we need to download and open PoC locally. 

It would go something like:

1. Open PoC from web
2. PoC will somehow drop HTML in local disk (I have heard in other reports of possible local file XSS)
3. Using bug 415167 we try to guess OS username + folder path to dropped HTML file
4. Use the bookmark trick as described above.
5. Instruct user to open bookmark with either method described above.

</details>

---
*Analysed by Claude on 2026-05-12*
