# DOM XSS via Shopify.API.remoteRedirect PostMessage Origin Validation Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 576532 | https://hackerone.com/reports/576532
- **Submitted:** 2019-05-10
- **Reporter:** yxw21
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (DOM-based XSS), Improper Origin Validation, PostMessage Security Flaw
- **CVEs:** None
- **Category:** web-api

## Summary
Shopify's embedded app JavaScript failed to properly validate the origin of PostMessage events before processing Shopify.API.remoteRedirect commands, allowing arbitrary JavaScript execution. An attacker with theme modification capabilities could inject malicious payloads that execute with admin privileges when other administrators access compromised pages.

## Attack scenario
1. Attacker with store theme write access injects malicious script containing postMessage sender that repeatedly sends remoteRedirect messages with javascript: protocol URIs
2. Attacker crafts social engineering or stores payload on compromised theme, then tricks or waits for store administrator to visit the page
3. Administrator visits the page containing the payload while logged into the Shopify admin dashboard
4. Injected script opens a new window to the admin themes page and sends PostMessage events with XSS payload
5. Vulnerable embeddedApp-*.js processes the postMessage without validating sender origin, executes handleRemoteRedirect() with attacker-controlled location
6. JavaScript in remoteRedirect location parameter (javascript:alert(document.domain)) executes in admin context, allowing credential theft or account compromise

## Root cause
The PostMessage event listener in embeddedApp-*.js lacked proper origin validation when processing Shopify.API.remoteRedirect commands. The case statement directly called handleRemoteRedirect(t.location) without verifying the message source was from a trusted origin, allowing any window to send redirect messages with javascript: URIs that would be processed as navigation targets.

## Attacker mindset
An insider or compromised theme developer exploited theme write permissions to inject persistent XSS. The attack leverages admin trust in their own store configuration and the assumption that postMessage sources are inherently trusted. The attacker recognized that admin-level compromises are more valuable than customer compromises.

## Defensive takeaways
- Always validate PostMessage origin using event.origin against a strict whitelist of expected origins before processing any commands
- Implement strict Content Security Policy (CSP) with script-src restrictions to prevent javascript: protocol execution
- Validate and sanitize all redirect locations; reject javascript:, data:, and other dangerous protocols
- Use a URL parsing library to validate redirect targets before applying them
- Implement origin pinning for sensitive PostMessage communications between parent and embedded frames
- Apply the principle of least privilege to theme modification permissions
- Monitor and audit PostMessage usage across embedded applications for security gaps

## Variant hunting
Search for other PostMessage handlers in Shopify assets that lack origin validation (focus on admin/embedded contexts)
Review other protocol handlers (http://, https://, etc.) that might be vulnerable to similar origin spoofing
Examine theme injection vectors beyond direct script injection (meta tags, event handlers, CSS expressions)
Test other administrative surfaces that use PostMessage for cross-origin communication
Look for similar patterns in other Shopify embedded apps and partner applications
Review related report #422043 for similar PostMessage validation issues in other endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1539 - Steal Web Session Cookie
- T1598 - Phishing - Social Engineering
- T1204 - User Execution
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter

## Notes
This vulnerability builds upon similar PostMessage issues (reference #422043). The attack requires either theme write permissions or the ability to trick an admin into visiting a malicious page. The javascript: protocol execution in a redirect context is particularly dangerous in admin panels where session tokens and sensitive operations are available. The 500ms interval in the PoC accounts for timing issues in window loading and message delivery.

## Full report
<details><summary>Expand</summary>

hi, team, after I read the report #422043, I found another monitor postmessage, and did not correctly verify the origin, leading to dom xss, using the store theme can write js this feature, we can modify a theme for the following Payload, 
```
<script>
  function attack(){
  	var ctx=window.open('https://cuxuri.myshopify.com/admin/themes');
    var interval;
    interval=setInterval(function(){
      if(window.attackSuccess){
        clearInterval(interval);
      }else{
        ctx.postMessage(`{"message":"Shopify.API.remoteRedirect","data":{"location":"javascript:alert(document.domain)"}}`);
      }
    },500);;
  }
</script>
<a href="javascript:attack()" style="display:block;text-align:center;width:100%;height:300px;line-height:300px;background:#000;color:#fff;">click me start attack</a>
```
then log in to the store, access the page containing the payload, you can trigger xss, 
such as:

{F487966}

Problem code:
```
https://cdn.shopifycloud.com/web/assets/latest/embeddedApp-ab64a8a13eb3f06403cb2acf67e20576a144bf2d3625807923872e8adf469a14.js
case de.RemoteRedirect:
                            this.handleRemoteRedirect(t.location);
                            break;
```

## Impact

Attack other administrators

</details>

---
*Analysed by Claude on 2026-05-12*
