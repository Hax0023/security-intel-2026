# Open Redirection via X-FORWARDED-HOST Header on publishers.basicattentiontoken.org

## Metadata
- **Source:** HackerOne
- **Report:** 369447 | https://hackerone.com/reports/369447
- **Submitted:** 2018-06-21
- **Reporter:** ulalalaunana
- **Program:** Basic Attention Token (BAT)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirection, Host Header Injection, HTTP Response Splitting
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application processes 302 HTTP redirects without properly validating the X-FORWARDED-HOST header, allowing attackers to inject arbitrary hostnames. An attacker can manipulate this header to redirect users to malicious external sites, facilitating phishing and credential theft attacks.

## Attack scenario
1. Attacker identifies that publishers.basicattentiontoken.org issues 302 redirects on authentication failure or session expiration endpoints
2. Attacker crafts a malicious request to /publishers/expired_auth_token endpoint with a valid publisher_id parameter
3. Attacker injects X-FORWARDED-HOST: attacker.com header into the intercepted request
4. Server constructs redirect response using the attacker-controlled header value instead of the legitimate host
5. Victim receives 302 response with Location header pointing to attacker.com
6. Victim's browser follows redirect to attacker's phishing site where credentials are harvested

## Root cause
The application trusts the X-FORWARDED-HOST header without validation when constructing redirect URLs. This header is typically used only by reverse proxies and should not be directly used in redirect logic without allowlist verification. The application likely constructs Location headers using untrusted user input or proxy headers.

## Attacker mindset
Attackers recognize that 302 redirects are commonly trusted by users, especially in authentication flows. By controlling the destination host via headers, they can perform advanced phishing attacks where URLs appear legitimate yet redirect to malicious domains. This is particularly effective against publisher/advertiser accounts handling financial transactions.

## Defensive takeaways
- Never trust X-FORWARDED-HOST, X-FORWARDED-PROTO, or similar proxy headers for security decisions without strict allowlist validation
- Use only the canonical hostname from server configuration when constructing redirect URLs
- Implement whitelist-based validation for all redirect destinations (relative URLs preferred)
- Reject requests with suspicious proxy headers that don't match expected reverse proxy infrastructure
- Use HTTP Strict-Transport-Security (HSTS) to prevent protocol downgrade attacks via redirects
- Log and monitor requests containing X-FORWARDED-* headers to detect suspicious patterns
- Implement Content-Security-Policy headers to mitigate phishing impact

## Variant hunting
Check other redirect endpoints (logout, post-login, password reset) for similar vulnerabilities
Test X-FORWARDED-PROTO for protocol injection (http vs https)
Examine X-FORWARDED-FOR and X-ORIGINAL-HOST headers for similar redirect injection
Test if X-FORWARDED-HOST works in conjunction with path traversal (e.g., /../attacker.com)
Check if the vulnerability exists on subdomains or alternate endpoints
Test with double-encoded payloads and Unicode characters in the header
Investigate if other BAT properties (brave.com, basicattentiontoken.org) have similar issues

## MITRE ATT&CK
- T1598.003
- T1598.002
- T1566.002
- T1021.004
- T1557.002

## Notes
This is a classic open redirection vulnerability exacerbated by blind trust in proxy headers. The report lacks proof-of-concept screenshot detail but the vulnerability appears straightforward to reproduce. The BAT publisher platform handles financial accounts, making this particularly critical for phishing attacks. The blanket statement 'every 302 HTTP CODE' suggests systemic implementation of insecure redirect logic across the application rather than isolated instances.

## Full report
<details><summary>Expand</summary>

#Summary
i guess every 302 HTTP CODE on 
>https://publishers.basicattentiontoken.org
possible to OpenRedirection

## Steps To Reproduce:

1. I edited the request when i got redirected from this request url

>https://publishers.basicattentiontoken.org/publishers/expired_auth_token?publisher_id=587fb66a-9fdb-4419-9d05-f38ce41666ca

587fb66a-9fdb-4419-9d05-f38ce41666ca = PUBLISHER_ID

>https://publishers.basicattentiontoken.org/publishers/587fb66a-9fdb-4419-9d05-f38ce41666ca

2. Add this header to the request and page willbe direct to injectedurl

>X-FORWARDED-HOST : injectedurl.com

Proof :
{F310965}

## Supporting Material/References:

  * BurpSuite
  * TextEditor

## Impact

A web application accepts a user-controlled input that specifies a link to an external site, and uses that link in a Redirect. This simplifies phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
