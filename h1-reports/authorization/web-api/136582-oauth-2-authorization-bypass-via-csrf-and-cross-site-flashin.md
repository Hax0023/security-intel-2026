# OAuth 2 Authorization Bypass via CSRF and Cross-Domain Flash Policy Abuse

## Metadata
- **Source:** HackerOne
- **Report:** 136582 | https://hackerone.com/reports/136582
- **Submitted:** 2016-05-05
- **Reporter:** opnsec
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Request Forgery (CSRF), Cross-Domain Policy Misconfiguration, Authorization Bypass, Flash Security Policy Abuse, Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
A misconfigured crossdomain.xml policy file at api.vimeo.com/oauth allows attackers to use Flash to bypass OAuth authorization mechanisms and gain full app privileges over victim accounts. By explicitly loading the overly-permissive parent directory policy, attackers can exfiltrate OAuth tokens from the /authorize endpoint without user interaction. The vulnerability requires only that the victim be logged into Vimeo and click a malicious link with an active Flash player.

## Attack scenario
1. Attacker creates a webpage hosting a malicious Flash file (evil.swf) that calls Security.loadPolicyFile()
2. Attacker tricks or socially engineers a logged-in Vimeo user into visiting the attacker's webpage
3. The malicious Flash file loads the parent-level crossdomain.xml from api.vimeo.com/oauth/ which permits access from any domain (*)
4. Flash now allows cross-domain requests to child directories, including the sensitive /oauth/authorize endpoint
5. The evil.swf makes an XMLHttpRequest to https://api.vimeo.com/oauth/authorize and extracts the authorization token from the response
6. Attacker uses the stolen token to complete the OAuth flow and authorize their malicious app, gaining full API access to the victim's Vimeo account

## Root cause
The crossdomain.xml file at api.vimeo.com/oauth/ is configured with 'allow-access-from domain="*"', which applies to the directory and all child directories per Flash specifications. The sensitive OAuth authorization endpoint at /oauth/authorize should not be accessible to cross-domain Flash requests, but the permissive parent policy allows an attacker to explicitly load it via Security.loadPolicyFile(), bypassing the more restrictive child directory policy that would normally block the request.

## Attacker mindset
An attacker recognizes that overly-permissive CORS/crossdomain policies at parent directory levels can be exploited to access sensitive child resources. By understanding Flash's policy file precedence rules, the attacker can manipulate which policy file Flash uses for validation. The attacker abuses the implicit trust users have in being logged in, using social engineering to trick victims into visiting malicious pages where Flash silently performs unauthorized OAuth operations.

## Defensive takeaways
- Never use wildcard domain policies (domain="*") in crossdomain.xml files, especially for directories containing sensitive OAuth endpoints
- Implement explicit authentication checks on authorization endpoints rather than relying solely on policy files
- Use SameSite cookie flags and anti-CSRF tokens to prevent unauthorized state changes via cross-origin requests
- Move sensitive OAuth endpoints to isolated subdomains with restrictive or no crossdomain.xml policies
- Implement CSRF tokens that cannot be exfiltrated via cross-domain requests (incorporate into response body, not headers alone)
- Monitor and deprecate Flash usage; implement equivalent protections for modern cross-origin mechanisms (CORS)
- Use HTTP-only, Secure, SameSite cookies for authorization tokens to prevent exfiltration via client-side scripts
- Validate that authorization responses are only served to authenticated sessions via proper state management
- Implement Content Security Policy (CSP) headers to restrict Flash loading and cross-origin requests

## Variant hunting
Scan for other wildcard crossdomain.xml policies on other Vimeo subdomains (api, www, developer, etc.)
Check if other OAuth endpoints besides /authorize are similarly exposed (token endpoint, refresh endpoints)
Investigate if similar misconfigured policies exist on related video platforms (YouTube, Dailymotion, etc.)
Test if CORS headers are similarly misconfigured and exploitable via XMLHttpRequest without Flash
Examine if other authentication mechanisms (SAML, API keys) are exposed through the same policy files
Look for other sensitive directories with overly-permissive crossdomain.xml files that could leak session data
Test if Flash-based attacks can be chained with XSS to escalate impact on modern browsers

## MITRE ATT&CK
- T1190
- T1012
- T1539
- T1528
- T1566
- T1199
- T1185

## Notes
This report demonstrates a sophisticated understanding of Flash security policy mechanics and their interaction with OAuth flows. The vulnerability is particularly severe because it requires no user interaction beyond the initial page visit, and affects all users logged into Vimeo. The mitigation strategy suggested (moving authorize endpoint to a different subdomain or using redirects) is sound. Flash vulnerabilities like this became increasingly relevant as Flash was widely used for multimedia and video playback on the web. The report was filed in 2016 when Flash was still prevalent; similar CORS misconfiguration vulnerabilities persist in modern implementations.

## Full report
<details><summary>Expand</summary>

Hello Vimeo Security Team,

There is a vulnerability in api.vimeo.com/oauth which allows an attacker to gain full App privilege over a Vimeo victim user account without user approval, just by having the victim open a link to the attacker webpage.

Proof of Concept link :
http://opnsec.com/vimeo/vimeoOAuth2Bypass.html

POC requirements :
-Tested on Windows 8.1/10 with Firefox 46, Chrome 50, Internet Explorer 11 
-Flash must be active
-You must be logged in Vimeo

POC instructions :
1. Open the POC link
2. Wait a few seconds
3. The leaked infos from OAuth authorization will show in the box. 
4. You can then check your vimeo Apps setting page at https://vimeo.com/settings/apps to see that the app 'OAuthBypass' is in the list of authorized Apps

----------------------

Technical info :

The vulnerability comes from the crossdomain file api.vimeo.com/oauth/crossdomain.xml which is set to 'allow-access-from domain="*" '.This means that any domain can load data with Flash from the directory 'api.vimeo.com/oauth/' AND FROM THE FOLDER'S CHILD DIRECTORIES, including the directory https://api.vimeo.com/oauth/authorize 
The url https://api.vimeo.com/oauth/authorize should not be accessible to cross domain flashing because it contains the Token to allow the App to gain access to the user account.

You can verify the Flash behavor in Adobe Flash documentation on security :
http://help.adobe.com/en_US/as3/dev/WS5b3ccc516d4fbf351e63e3d118a9b90204-7c85.html#WS11001817-24CB-48a4-AA10-59468865F751

"A URL policy file applies only to the directory from which it is loaded <b>and to its child directories."<b>

What happens when flash AS3 loads https://api.vimeo.com/oauth/authorize is that :
1. By default Flash check the Master crossdomain.xml file, which in this case is 'permitted-cross-domain-policies="by-content-type" ' which means that the policy will be based on a directory base.  
2. Then by default Flash will try to load https://api.vimeo.com/oauth/authorize/crossdomain.xml which is not allowing cross site request at all. In this case, flash will not let the cross domain request and the Vimeo OAuth is safe

HOWEVER, if the evil.swf flash calls 'Security.loadPolicyFile("api.vimeo.com/oauth/crossdomain.xml")'
before loading url https://api.vimeo.com/oauth/authorize then Flash will allow cross domain request on api.vimeo.com/oauth/ and on any child directory including https://api.vimeo.com/oauth/authorize. In that case, flash will never check https://api.vimeo.com/oauth/authorize/crossdomain.xml because api.vimeo.com/oauth/crossdomain.xml is enough for him to allow the cross domain request on https://api.vimeo.com/oauth/authorize

I hope my explaination is clear enough. In conclusion, a call to 'Security.loadPolicyFile("https://api.vimeo.com/oauth/crossdomain.xml")' will allow any domain to read the source code of https://api.vimeo.com/oauth/authorize.

From there, an attacker can steal the Token of the user and do all the authorization process (Obtaining Authentication credentials via redirect) without the need of user interaction.

Vulnerability Mitigation :

To remove the vulnerability, you just need to move the https://api.vimeo.com/oauth/authorize to another subdomain like www.vimeo.com/oauth/authorize or to another directory like api.vimeo.com/authorize where there is no allowing crossdomain.xml file between the root folder level and the "authorize" level.
To keep the same implementation for the app developpers you can make a simple redirection from https://api.vimeo.com/oauth/authorize to the new, protected "authorize"  location. That way flash will not be able to follow the redirection and only legitimate user will be able to validate App authorization.

-------------

If you need more info like POC source code or if the POC doesn't work feel free to contact me.

Regards,

Enguerran Gillier
&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;
&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;

</details>

---
*Analysed by Claude on 2026-05-24*
