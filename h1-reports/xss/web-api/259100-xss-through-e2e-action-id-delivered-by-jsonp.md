# XSS through __e2e_action_id Parameter Delivered via JSONP in Quora

## Metadata
- **Source:** HackerOne
- **Report:** 259100 | https://hackerone.com/reports/259100
- **Submitted:** 2017-08-11
- **Reporter:** 0xnan
- **Program:** Quora
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Output Encoding, JSONP Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The __e2e_action_id parameter in POST requests to /server_call_POST endpoint is not properly escaped when reflected in JavaScript code, allowing XSS injection. An authenticated attacker can exploit the /server_call_POST?_m=edit action combined with JSONP channel updates to deliver XSS payloads to other users without their interaction.

## Attack scenario
1. Attacker makes authenticated POST request to /server_call_POST?_m=edit with malicious __e2e_action_id parameter like ',alert(1),'
2. The edit action sends an update message to the victim's channel (main-w-dep3105-xxxxx) instead of immediate response
3. Victim's browser receives JSONP callback from tch.quora.com/up/chan updates endpoint containing the unescaped __e2e_action_id
4. JSONP callback executes and includes the reflected action ID in require('actions').finishAction() call
5. JavaScript payload executes in victim's browser context with full session privileges
6. Attacker gains ability to perform actions as victim, steal session data, or redirect to phishing pages

## Root cause
The __e2e_action_id parameter is concatenated directly into JavaScript code without HTML or JavaScript escaping before being returned in JSON/JSONP responses. The application trusts user-supplied action IDs as safe identifiers when they should be treated as untrusted input.

## Attacker mindset
An insider or authenticated user exploiting the assumption that action IDs are randomly generated and non-user-controllable. The attacker recognizes that while /server_call_POST prevents direct action ID control, the /server_call_POST?_m=edit method broadcasts updates through JSONP channels, creating a reliable delivery mechanism to other users without requiring victim interaction.

## Defensive takeaways
- Implement proper output encoding for all user-controlled parameters before inserting into JavaScript contexts - use JSON.stringify() or JavaScript-specific escaping
- Validate __e2e_action_id server-side to match expected format [0-9a-z] and reject non-conforming values
- Avoid reflecting user input directly into code generation - use parameterized APIs instead
- Apply Content Security Policy (CSP) to prevent inline script execution and limit JSONP usage
- Sanitize all data before broadcasting to channel subscribers, treating channel messages as untrusted user input
- Use structured data serialization (protobuf, messagepack) instead of JavaScript code generation for RPC responses
- Implement proper CORS and JSONP callback validation to prevent callback injection attacks

## Variant hunting
Check other /server_call_POST?_m=* methods that reflect request parameters in JavaScript responses
Audit all JSONP endpoints across *.tch.quora.com for similar reflection vulnerabilities
Search for other window_id or channel parameters that might trigger similar broadcast behaviors
Investigate if other authenticated action methods use channel delivery mechanisms with unescaped parameters
Test API responses that construct function calls with user-supplied string arguments
Check for DOM-based XSS in rpc.js library where JSONP responses are processed

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This is a sophisticated chained vulnerability requiring authentication but achieving reliable XSS delivery without victim interaction. The attacker exploited the architectural difference between synchronous responses (/server_call_POST?_m=load_menu) and asynchronous channel-based updates (/server_call_POST?_m=edit). The JSONP delivery mechanism is key - it bypasses same-origin policy and guarantees the payload executes when the victim's browser makes update requests. The report demonstrates excellent vulnerability research by identifying both the XSS flaw and a practical exploitation chain.

## Full report
<details><summary>Expand</summary>

#Summary:

The `__e2e_action_id` params used with POST requests to `/server_call_POST?_m=*` endpoint is not properly escaped when reflected back on a response allowing to inject Javascript.
Also, another issue on some methods (such as `/server_call_POST?_m=edit`) allows - with a *strong* premise discussed on the description - *any* authenticated user to deliver the vulnerability to another user without any interaction.

# Description

## XXS
On the Web Application http://www.quora.com most user actions are performed as POST on `/server_call_POST?_m=*`, implementing AJAX architecture.
On the client side these requests are processed by  `./shared/core/rpc.js` library that in turns uses the library `./actions.js` to define "actions" which have an ID `__e2e_action_id` and some methods such as startAction() and **finishAction(id, ...)**.  
The `__e2e_eaction_id` is generated for every request with `id = (1e3 * e.startTime + Math.floor(1e3 * Math.random())).toString(36)` so its value is intended to be composed by [0-9a-z].

When a user performs an action, this ID is embedded on the POST request and with some methods (for
example `/server_call_POST?_m=load_menu`) its content is reflected back as first argument of
finishAction().  For example a "normal" call, with `__e2e_action_id=esko02tjqe` is the following (I've omitted most headers/params/data):

```
curl 'https://www.quora.com/webnode2/server_call_POST?_v=####&_m=load_menu'  
-data 'json=...&__e2e_action_id=esko02tjqe&...'

> POST /webnode2/server_call_POST?_v=█████&_m=load_menu HTTP/1.1
> Host: www.quora.com
> Cookie: █████████████████████
...
< HTTP/1.1 200 OK
< Content-Type: application/json; charset=utf-8
< Server: nginx
< 
{"value": {
     "html": ..., 
      "css": .......,                             (↓↓↓↓↓↓ reflected ID)
       "js": "require('actions').finishAction('esko02tjqe', {\"controller\": \"webnode2\", \"action\": \"server_call_POST\", \"standard\": {}, \"serverTime\": 34511, \"mustReport\": true});\n            var webnode = require('shared/core/webnode');\n   ....     "}, 
   "pmsg": null}
```
Since no escaping is performed, it is possible to inject code, for example setting `__e2e_action_id=',alert(),'` which will produce:
```
...
 "js": "require('actions').finishAction('',alert(),'', {\"cont... "}, 
...
```
creating a valid js section that execute `alert()`.
Fortunately this vulnerability can't be triggered as it is because this would require the malformed request to be sent by Quora.com since it is `./shared/core/rpc.js` that execute the response (that has a content type of `application/json`) and seems that there is no way to directly set the `__e2e_action_id` on a session of Quora (a new one is generated  for each action).

## Deliver the XSS using JSONP

I've noticed another "vulnerability" that can be chained with the aforementioned to be able to effectively
deliver the XSS to an user.
When an user is on Quora, to its page is associated a "channel" (I hope this is the correct name) such as `main-w-dep3105-32490323....` and there is always a request that try to fetch new "update" from a
channel (restarted each time it returns).  
This request is `update` on *.tch.quora.com, for example:

```
REQUEST
https://tch969298.tch.quora.com/up/chan43-8888/updates?&callback=jsonp<callback_name>&channel=main-w-dep3105-32490323....&hash=16762940...

POSSIBLE RESPONSE:
jsonp<callback_name>({"messages":["require.whenReady(\"main\", function() {\n ... ,"min_seq":1591113381})
```

The action `/server_call_POST?_m=edit` (used for example when an user change its profile description), do not behave like `/server_call_POST?_m=load_menu` (described in the first section). What I mean is that they do not reply with the response `{"value": {"html": ..., "css": ...., "js": ...}, "pmsg": ""}` to update the page but they reply with a response `{"value": null, "pmsg": null}` and *deliver the update through a message on the channel of the user*.

For example after a `/server_call_POST?_m=edit` with `__e2e_action_id=eskrisktsq` the `/update?` request reply with:
```
jsonp<callback_name>({"messages":["require.whenReady(\"main\", function()
 {require('actions').finishAction('eskrisktsq' ... <other data of the edit action>
                                     ↑↑↑↑↑
             (__e2e_action_id of the _m=edit call reflected)
     
```
on which `eskrisktsq` is the `__e2e_action_id` used on the `_m=edit` call vulnerable to XSS.
The fact that `_m=edit` sent a message to the channel `main-w-dep3105-32490323....` it's because this channel is specified as parameter on the request `_m=edit`:
```
curl 'https://www.quora.com/webnode2/server_call_POST?_v=███████&_m=edit' 
--data 'json={
"args":[],"kwargs":{the data of the edit}}&
revision=███████████&
formkey=███████████&
postkey=███████████&
window_id=dep3105-32490323....&                          ← specified here
_lm_window_id=dep3105-32490323....&                      ←   and here
__e2e_action_id=eskrisktsq&
&__vcon_json=[█████]&.....' 
```

The real problem is that this method **do not check if the specified channel is associated to user session who performed the call**. So what could happen is that the attacker can send the XSS to
a specified channel name that will be triggered as soon as the `update?` request (of the victim user) receives the evil data, without any interaction of the victim.
The *effect* of `_m=edit` (eg: change the profile description) is applied to the Attacker profile (since on the request are used Cookies, formkey and postkey of the Attacker) but *the finishAction() message* (vulnerable to XSS) is sent to the *victim* channel name.

I can confirm that this behavior is not present on other methods: for example with `_m=load_menu` if you try to change the `window_id` you obtain a 500 Internal Server Error, this should demonstrate that there is some check missing on methods such as `_m=edit`.  
I've not tested other methods, anyway I think that all the methods that reply with `{"value": null, "pmsg": null}` are vulnerable but not the ones that reply with the update directly (as `_m=load_menu` does) .

The *strong* premise said on the summary is that an attacker should know the victim channel_name and, that seems not easy to obtain, but if there are ways to do this, this vulnerability will become a serious problem since no victim interaction is required to perform the attack.

Anyway is still possible to do a bruteforce on channel name spreading the attack on random users. To this end I want to call on your attention some pro/cons aspect for the attacker:

   0. There could be easy ways that I did not find to leak valid channel_name
   1. The attack can't be stopped from browser XSS filters
   2. The XSS seems to work only on Quora.com (Android do not use `__e2e_action_id`, IOs not tested)
   3. A channel_name is composed of `dep<4 digit[0-9]>-<up to 19 digit[0-9]>`. Valid 4 digits for `dep`
 can be leaked using `https://www.quora.com/check_livedeps/index?window_id=dep3304-`
  that seems to respond with "ok" if the 4 digits (in this case 3304) are part of a channel alive.
   4. the remaining part is infeasible to enumerate (10^19), but should be noted that:
     -  doing the evil request returns an HTTP status code 200, so the attack can be distributed on multiple Attacker's Quora Profiles created for the attack, and metrics such as increased error rate (http 500) do not highlight any attack.
     - if the XSS is sent to a channel_name that is not used by any user and Quora assigns this
       channel_name, up to 5minutes **later** the evil request was sent, the XSS is delivered correctly.
       (BTW I do not know if Quora would assign a channel name on which a message is already "pending")
     -I think the attacker can keep busy some channels name (reducing the space to enumerate),
logging and executing the same code that Quora uses to attach a channel to an user, e.g:   

````
 require("tchannel_up").start(0, "main-w-dep3104-34040...", "2287...

</details>

---
*Analysed by Claude on 2026-05-12*
