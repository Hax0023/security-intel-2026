# Reflective XSS in IE11 via Vulnerable Flash File (video-js.swf)

## Metadata
- **Source:** HackerOne
- **Report:** 182160 | https://hackerone.com/reports/182160
- **Submitted:** 2016-11-14
- **Reporter:** opnsec
- **Program:** Portswigger (PortSwigger Web Security Academy)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Insecure Deserialization, Unsafe Flash Parameter Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A reflective XSS vulnerability exists in portswigger.net through a vulnerable Flash file (video-js.swf v3.2.0) that accepts user-controlled JavaScript code via the readyFunction parameter. While modern browsers block this via CSP, Internet Explorer 11 fails to enforce the CSP policy, allowing arbitrary JavaScript execution in the context of portswigger.net.

## Attack scenario
1. Attacker identifies outdated video-js.swf library (v3.2.0) hosted at portswigger.net/burp/tutorials/video-js/
2. Attacker discovers the Flash file accepts readyFunction parameter that executes JavaScript code
3. Attacker crafts malicious URL with JavaScript payload in readyFunction parameter
4. Attacker sends phishing link to victim user with IE11 and active Flash plugin
5. Victim opens link in IE11; CSP policy is not enforced by browser
6. Flash file executes payload, allowing access to victim's cookies, session tokens, or sensitive page data on portswigger.net

## Root cause
Combination of three factors: (1) outdated Flash library with parameter injection vulnerability, (2) unsafe parameter handling in video-js.swf allowing code execution, (3) CSP policy not enforced by Internet Explorer 11 browser

## Attacker mindset
Target legacy browser users (IE11 still used in enterprise environments) with outdated Flash libraries. Flash files were historically prone to XSS when accepting JavaScript parameters. Attacker exploits browser's CSP enforcement gap rather than the Flash vulnerability itself.

## Defensive takeaways
- Remove or sandbox all Flash content; migrate to HTML5 video players
- Maintain inventory of third-party Flash files and monitor for CVEs
- Implement strict Content Security Policy and verify enforcement across browsers
- Host Flash files on sandboxed subdomains with limited privileges
- Disable Flash plugin support or restrict to allowlist of trusted sites
- Test CSP policies specifically on legacy browsers (IE11) used by enterprise users
- Implement input validation on Flash parameters even if accepting them seems necessary
- Use modern alternatives (HTML5 video, DASH, HLS) instead of Flash

## Variant hunting
Hunt for other Flash files on the domain with similar parameter injection patterns. Check for readyFunction, onReady, callback, or similar parameters in other .swf files. Investigate other video.js or legacy multimedia libraries. Test other browsers with CSP enforcement gaps (older Safari, Opera versions).

## MITRE ATT&CK
- T1190
- T1204.1
- T1566.002
- T1657

## Notes
This vulnerability is particularly notable because it demonstrates CSP bypass in IE11 - the CSP header was present but not enforced. Flash-based XSS was a common vector pre-2015 but remains relevant for legacy environments. The researcher properly suggested sandboxing as an additional layer of defense rather than relying solely on CSP.

## Full report
<details><summary>Expand</summary>

Hello Portswigger Security Team,

There is a reflective XSS vulnerability in portswigger.net. The flash file `https://portswigger.net/burp/tutorials/video-js/video-js.swf` is from an old video.js library (version 3.2.0) which is vulnerable to XSS.
This XSS will be blocked by CSP instruction `object-src https://portswigger.net/knowledgebase/papers/;` but it will execute on browsers that don't enforce this CSP like Internet Explorer 11.

POC link : https://portswigger.net/burp/tutorials/video-js/video-js.swf?readyFunction=alert%28document.domain%2b'%20XSSed!'%29

POC instructions :
- Open the POC link in Internet Explorer 11 with flash active
- The javascript payload executes in `https://portswigger.net`
(Tested on Windows 10)

Mitigation :
To solve this issue, replace the old `https://portswigger.net/burp/tutorials/video-js` library with the updated video.js library from http://videojs.com/. It is also better to host any swf file on a sandbox subdomain.

Regards,

Enguerran @opnsec

</details>

---
*Analysed by Claude on 2026-05-12*
