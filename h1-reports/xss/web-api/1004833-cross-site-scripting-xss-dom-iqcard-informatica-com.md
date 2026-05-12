# DOM-based Cross-Site Scripting (XSS) via document.location.replace()

## Metadata
- **Source:** HackerOne
- **Report:** 1004833 | https://hackerone.com/reports/1004833
- **Submitted:** 2020-10-10
- **Reporter:** rodtvs
- **Program:** Informatica
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in attach.html where user-supplied input from the URL query string is directly passed to document.location.replace() without sanitization. An attacker can execute arbitrary JavaScript or redirect users to malicious sites by crafting a malicious URL.

## Attack scenario
1. Attacker identifies the vulnerable attach.html endpoint that processes URL query parameters
2. Attacker crafts a malicious URL using javascript: protocol or external domain in the query string
3. Attacker sends the crafted URL to a victim via phishing email, social engineering, or malicious advertisement
4. Victim clicks the link, triggering the onload event which calls GetAttach() function
5. The vulnerable code extracts the query parameter and passes it directly to document.location.replace()
6. Malicious JavaScript executes in victim's browser or victim is redirected to attacker-controlled site

## Root cause
Unsafe handling of untrusted user input from document.location.search. The code directly uses the query parameter value in document.location.replace() without any validation, sanitization, or whitelisting. The substring() call only removes the leading '?' but does not prevent injection of javascript: protocol or external URLs.

## Attacker mindset
An attacker would view this as a low-effort, high-impact vulnerability. The attack requires minimal technical skill - simply crafting a URL with malicious payloads. The attacker could leverage it for credential harvesting via phishing redirects, malware distribution, session hijacking, or defacing the application's trust with users.

## Defensive takeaways
- Never directly use user-supplied input in document.location.replace() or similar redirect functions
- Implement strict URL validation by maintaining a whitelist of allowed redirect destinations
- Use a dedicated redirect function that validates the target URL against a safe domain list
- Avoid parsing URL parameters with document.location.search; use URLSearchParams API instead
- Remove or validate the javascript: protocol and other dangerous schemes before any redirect
- Implement Content Security Policy (CSP) headers to limit what can be executed
- Use security headers like X-Frame-Options and X-Content-Type-Options
- Conduct regular security code reviews focusing on DOM manipulation and redirect patterns

## Variant hunting
Search for similar patterns in other Informatica domains and applications where query parameters are used in location.replace(), location.href, or window.open() calls. Look for other endpoints with similar file patterns (player/, viewer/, etc.) that might have inherited this vulnerable pattern. Check for variations using hash-based routing (document.location.hash) that could be similarly exploited.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic DOM-based XSS with dual impact: arbitrary code execution and open redirect. The vulnerability is particularly dangerous because it abuses a trusted Informatica domain (iqcard.informatica.com) for phishing attacks. The report demonstrates both attack vectors clearly with practical PoC examples. The legacy code pattern suggests this may be an older codebase that was not modernized with security best practices.

## Full report
<details><summary>Expand</summary>

Hello all

I found a DOM based XSS at iqcard.informatica.com

# Description

After finding the path **iqcard.informatica.com/pub/fujitsu/fm3v2/player/attach.html**. I noticed that the code inside attach.html was vulnerable to DOM XSS, due to the fact of the javascript *document.location function. search*. The code below illustrates the code contained in the attach.html file

```
<HTML>
<HEAD>
<SCRIPT>
function GetAttach()
{
	var strSearch = document.location.search
	strSearch = strSearch.substring(1)
	
	document.location.replace(strSearch)
}
</SCRIPT>
</HEAD>
<BODY onload='GetAttach()'>


</BODY>
</HTML>
```
As can be seen through the code above, the variable * strSearch * receives everything that comes from the URL after the character? and then insert it into the function *document.location.replace ()*. Through this scenario we have some possibilities.

1 - We can direct the user to any page we want for example:

```
https://iqcard.informatica.com/pub/fujitsu/fm3v2/player/attach.html?evil.com
```


2 - We can run a DOM Based XSS, running the javascript schema, javascript: alert (1);

```
https://iqcard.informatica.com/pub/fujitsu/fm3v2/player/attach.html?javascript:alert(1)
```


# PoC 

I uploaded a video and an image.

## Impact

An attacker can redirect a user to a malicious page or execute XSS attacks against users of the application or use that domain as a phishing vector to attack other users of informatica.com

</details>

---
*Analysed by Claude on 2026-05-12*
