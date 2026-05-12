# Stored XSS in Slack team.slack.com Markdown Editor via JavaScript URI in Links

## Metadata
- **Source:** HackerOne
- **Report:** 132104 | https://hackerone.com/reports/132104
- **Submitted:** 2016-04-18
- **Reporter:** fransrosen
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Input Validation Bypass, Protocol Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Slack's Markdown editor when editing posts, allowing attackers to inject javascript: URIs as links. By manipulating WebSocket requests during the undo operation, attackers can bypass client-side protections and execute arbitrary JavaScript when links are clicked in edit mode. The vulnerability affects all users who have edit permissions on the post.

## Attack scenario
1. Attacker creates a post with a normal link on team.slack.com
2. Attacker deletes the link and uses Ctrl+Z to trigger an undo WebSocket request
3. Attacker intercepts the WebSocket request and modifies the payload to inject a javascript: URI in the links object
4. Attacker sends the modified WebSocket request, storing the malicious link in the post
5. When any user with edit permission opens the post in edit mode, the javascript: URI is rendered as a clickable link
6. Clicking the link executes arbitrary JavaScript (e.g., alert(document.domain)) in the context of team.slack.com

## Root cause
The Markdown editor in edit mode lacks proper protocol validation for links in WebSocket requests, unlike the public slack-files.com version which implements regex check /^https?:/ to reject non-HTTP(S) protocols. The undo operation processes link data without sanitization, allowing javascript: URIs to be stored and executed.

## Attacker mindset
Exploit the edit mode's lack of protocol validation to bypass Slack's existing XSS protections. Target the WebSocket communication layer during undo operations where validation may be relaxed. Leverage the ability to share edit permissions to spread the payload to other team members.

## Defensive takeaways
- Implement consistent protocol validation across all modes (view, edit, preview) and all endpoints (team.slack.com, slack-files.com, WebSocket handlers)
- Validate and sanitize all link protocols before storing in database, not just during rendering
- Apply same security controls to undo/redo operations as to direct user input
- Implement Content Security Policy (CSP) to block javascript: URIs at the browser level
- Sanitize WebSocket payloads server-side with same rigor as HTTP request bodies
- Use allowlist approach for URL protocols rather than blocklist

## Variant hunting
Search for similar protocol validation bypasses in other Slack features: canvas editing, thread replies, reactions with custom emoji/links. Check for inconsistency between edit-mode and view-mode sanitization across all Slack surfaces. Investigate other WebSocket operations (copy/paste, drag-drop, undo/redo) for similar validation gaps.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The report demonstrates good security research methodology by identifying the validation gap between slack-files.com (safe) and team.slack.com edit mode (vulnerable), intercepting WebSocket traffic, and providing reproducible PoC. The ability to enable edit permissions for other users amplifies impact to team-wide XSS. The vulnerability specifically triggers in edit mode, suggesting client-side editor framework (likely JavaScript-based WYSIWYG editor) has weaker sanitization than post rendering engine.

## Full report
<details><summary>Expand</summary>

Hi,

I noticed while looking at an old article I made a while ago that some links were actually inserted as `javascript:`-links. Doing some modifications to these actually revealed that inside editing mode, no protection is added for getting arbitrary scripts to run. This means that by catching the modifications for the Web Socket, I was able to create a payload that would trigger on click (only inside Editing mode for some reason).

Here's the vulnerable socket-request I modified to get the payload in:

As you see in my post, I delete a link, then do a Ctrl+Z to undo it, putting back the link. I then capture that request and modify the request to insert the payload inside the `links` part:
```
{"type":"rocket","event":"rocket","payload":{"mm":[["fi",[],3,{"type":"unfurl","originalFragment":{"_bindings":{"attach":[[]],"mutation:post":[[]],"attached":[[]],"detach":[[]],"detached":[[]]},"_bindingLock":0,"_customData":[],"_data":{"type":"p","text":"javascript:alert(document.domain%29","tabbing":0,"links":{"javascript:alert(\"XSS\"%29":[0,22]},"formats":[]},"_dom":null,"_mutable":{"_lock":0},"_mutableGuard":{"_lock":0},"_parent":null,"_text":"javascript:alert(\"XSS\"%29","_tabbing":0,"_links":{"javascript:alert(\"XSS\"":{"_ranges":[{"_s":0,"_e":22}]}},"pendingUnfurls":[],"_formats":{"b":{"_ranges":[]},"i":{"_ranges":[]},"u":{"_ranges":[]},"strike":{"_ranges":[]},"code":{"_ranges":[]}}},"url":"javascript:alert(\"XSS\"%29"}]],"r":19,"$":15,"type":"mm","sel":[[3],0,[3],0]},"id":25}
```

Here's a PoC-image when clicking the link when I'm editing the post in my team:
{F87107}

Also, since you're able to get other people to edit it as well, by enabling "Let others edit this Post" you can get other people affected in your team. What's also interesting is that when creating a public link, that will be hosted on slack-files.com, there's a catcher for links that does not begin with `^http(s)?:` which is awesome, however, this is not the case when editing a post on the team domain, which is a bit worse, since it's not sandboxed at all.

This is the link to my team's post:
https://marqueexss.slack.com/files/marqueexss/F0283AA4K/__hello__a_name__n____href__javascript_alert__xss_____you___a_

Also, here's a link to the public post:
https://slack-files.com/T025M9QPZ-F0283AA4K-2989c27641
to show you that the link has indeed the `javascript:` uri, however, this little snippet is triggered, which is great:
```
if (protocol && /^https?:$/.test(protocol) === false) {
     e.preventDefault();
     if (console && typeof console.warn === "function") {
         console.warn("not following bad link from a post preview")
     }
}
```
(This code is not present in the Edit-mode on the team URL as mentioned above)

PoC-movie is attached showing the complete flow from editing to triggering the XSS. I've also verified that it will trigger for other users in the team if they edit the post. 

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-12*
