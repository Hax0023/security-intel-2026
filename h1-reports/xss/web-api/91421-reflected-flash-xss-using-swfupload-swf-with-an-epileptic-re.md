# Reflected Flash XSS in swfupload.swf with Epileptic Reloading Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 91421 | https://hackerone.com/reports/91421
- **Submitted:** 2015-10-01
- **Reporter:** fransrosen
- **Program:** Imgur
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Unsafe Flash Parameter Handling, Improper Input Validation, Client-Side Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The swfupload.swf file hosted on imgur.com accepts unsanitized HTML parameters (buttonText, buttonImageURL, buttonTextStyle) that are rendered in the Flash control. While the Flash button event handler normally intercepts clicks, an attacker can cause rapid reloads of the SWF to create a race condition where malicious HTML is briefly clickable before the Flash overlay takes control, allowing arbitrary JavaScript execution.

## Attack scenario
1. Attacker identifies that swfupload.swf accepts URL parameters like buttonText and buttonTextStyle
2. Attacker crafts malicious HTML/JavaScript payload in these parameters (e.g., <a href="javascript:alert(document.domain)">CLICKME</a>)
3. Attacker creates a webpage with an iframe containing the malicious SWF URL
4. Attacker sets JavaScript to reload the iframe every 300ms, causing constant re-rendering of the Flash content
5. During the brief window between SWF reloads, the HTML layer becomes clickable
6. Victim's rapid clicking during reload cycles triggers the XSS payload, executing attacker's JavaScript in the imgur.com origin

## Root cause
The swfupload.swf component failed to properly sanitize HTML parameters before rendering them. Additionally, the Flash overlay's event handler did not persist across rapid reload cycles, creating a timing vulnerability. The SWF was directly accessible on the main domain with modifiable parameters rather than being isolated or having strict parameter validation.

## Attacker mindset
An attacker identified that security controls (the Flash button event capture) could be bypassed through precise timing exploitation. The attacker recognized that rapid state changes create temporary security windows and leveraged the Flash reload mechanism as a way to continuously recreate these windows, increasing the probability of successful click interception.

## Defensive takeaways
- Never trust user-supplied HTML content in Flash parameters; sanitize or reject HTML input entirely
- Host Flash components on separate, isolated subdomains with strict Content Security Policy headers
- Implement input validation whitelist for all Flash parameters; reject unexpected formats
- Use Content Security Policy (CSP) to prevent inline JavaScript execution and restrict script sources
- Consider deprecating Flash usage entirely in favor of modern web standards with better security models
- Implement rate-limiting on Flash reload requests to prevent rapid re-initialization exploitation
- Never expose Flash object parameters directly in URL query strings; use server-side configuration
- Add frame-busting code to prevent Flash embedding in iframes from untrusted origins

## Variant hunting
Search for other Flash components on the domain accepting URL parameters for HTML/styling
Test other Flash-based upload/file handling components for similar parameter injection vulnerabilities
Check for other deprecated Flash files that may be accessible and modifiable (e.g., swfobject.js patterns)
Test if other parameters in swfupload.swf (buttonImageURL, etc.) allow XSS or file inclusion
Investigate if any Flash components are cached and accessible via direct URL manipulation
Look for similar race conditions in any client-side rendering mechanisms with overlays or event handlers
Test if CORS or Flash crossdomain.xml allows cross-origin SWF loading for parameter manipulation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing
- T1204 - User Execution

## Notes
This report is notable for its creative exploitation technique using rapid reloading to create a race condition window. The 300ms interval creates continuous opportunities for user interaction with the malicious HTML before the Flash overlay re-establishes control. The reporter's humorous note about an 'epileptic reaction' highlights the poor user experience and unusual attack vector. The recommended mitigation (moving SWF to separate domain) is sound but incomplete—proper input sanitization is equally critical. This vulnerability exemplifies the security risks of Flash components and validates the industry move away from Flash-based solutions.

## Full report
<details><summary>Expand</summary>

Hi,
This was a fun one.

So I noticed you're using swfupload.swf which is hosted on the main domain, imgur.com. This swfupload.swf as some settings you can use to modify the button on the upload. You can actually insert HTML into the Flash, but the button event (that you select yourself using another parameter) is taking over the MouseClick-event from the HTML-content you provide.

However, if you're really quick, you can actually catch the even in the HTML anyway. So by making a page that would reload the SWF constantly (from cache that is) you can make a page that looks like this:
```
<iframe src="about:blank" id="x"></iframe>

<script>u='https://imgur.com/include/flash/swfupload.swf?buttonDisabled=&buttonText=%3Ca%20%20href=%22javascript:alert(document.domain)%22%3ECLICKME<br />CLICKME<br />CLICKME<br />CLICKME<br />CLICKME<br />CLICKME<br />CLICKME<br />CLICKME%3C/a%3E&buttonImageURL=/&buttonTextStyle=a{color:%23ff00ff}&buttonAction=-120&buttonCursor=-2';
setInterval(function(){document.getElementById('x').contentWindow.location=u},300)</script>
```

That will reload the content over and over, and if you click the text in the right time, the XSS will trigger.

I think I got an epileptic reaction out of testing this, but it was fun anyway, haha. You should probably move the swfupload.swf to another domain, and just embed it on imgur.com since that will give you the same options as today, but without the possibility to access the SWF directly and inject the parameters on your domain.

PoC-image attached.

Cheers,
Frans

</details>

---
*Analysed by Claude on 2026-05-12*
