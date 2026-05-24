# Open Redirect in securegatewayaccess.com / secure.chaturbate.com via prejoin_data Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 400982 | https://hackerone.com/reports/400982
- **Submitted:** 2018-08-27
- **Reporter:** inhibitor181
- **Program:** Chaturbate (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, CWE-601: URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the /post endpoint on both secure.chaturbate.com and securegatewayaccess.com domains. The application constructs a Location header based on user-controlled prejoin_data parameter when a valid weg_digest is present, allowing attackers to redirect users to arbitrary domains. This vulnerability can be chained with the /external_link endpoint for multi-stage redirect attacks.

## Attack scenario
1. Attacker crafts a malicious URL containing a valid weg_digest parameter and attacker-controlled prejoin_data parameter pointing to evil.com
2. Attacker sends the URL to target users via phishing email or social engineering
3. Victim clicks the link, which appears to originate from trusted Chaturbate domain
4. Application validates the weg_digest and processes the request, constructing redirect Location header from prejoin_data parameter
5. User is silently redirected to attacker's evil.com domain without warning
6. Attacker can host phishing pages mimicking Chaturbate login or payment forms to steal credentials

## Root cause
The application fails to validate and sanitize the prejoin_data parameter before using it to construct the Location header. The reliance on weg_digest for request validation provides false security as it only validates request authenticity, not the legitimacy of the redirect destination.

## Attacker mindset
An attacker would leverage the apparent legitimacy of the Chaturbate domain in the URL to bypass user trust mechanisms. The two-domain vulnerability increases attack surface. The ability to chain this with /external_link creates a sophisticated multi-stage redirect attack that obscures the final destination through URL encoding, making detection more difficult.

## Defensive takeaways
- Implement strict whitelist validation for all redirect destinations, never construct URLs from user input
- Use relative redirects (e.g., '/internal/path') instead of absolute URLs when possible
- If absolute URLs are required, validate against a whitelist of allowed domains
- Implement URL parsing libraries that properly handle edge cases and prevent domain spoofing
- Separate authentication/authorization (weg_digest validation) from redirect destination validation
- Add security headers like Content-Security-Policy to prevent open redirects
- Review all endpoints that construct Location headers or perform redirects
- Implement logging/alerting for redirect attempts to suspicious domains

## Variant hunting
Search for other endpoints accepting redirect parameters: /login, /callback, /return, /redirect, /forward, /link, /goto. Check for similar digest/token validation mechanisms that may have the same flaw. Examine both primary domain and related subdomains (api., admin., secure., gateway.). Look for other parameters that might construct URLs (next_url, return_url, target, destination, callback_url). Test with different URL encoding schemes and double-encoding to bypass validation.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Email
- T1600 - Weaken Encryption
- T1556 - Modify Authentication Process

## Notes
The researcher appropriately marked as Medium rather than Low due to the dual-domain impact (securegatewayaccess.com noted as critical). The weg_digest parameter appears to be a HMAC or cryptographic signature, suggesting the application may have weak key management or the attacker obtained a valid digest. The chained redirect technique through /external_link is particularly clever as it layered obfuscation. No bounty amount was disclosed in the public report.

## Full report
<details><summary>Expand</summary>

##Summary##
Hello, I have found that if there is a valid `weg_digest` parameter in the in the GET request to https://secure.chaturbate.com/post and other parameters are invalid, a Location header will be automatically constructor based on the contents of the `prejoin_data` parameter. This allows someone to change the base root and create an open redirect.

Even more, it has been observed that this specific request also works under the https://securegatewayaccess.com domain and an open redirect can also be created from that domain.

PS : Because this affects both URL's and `securegatewayaccess.com` seems to be a critical I have marked this as medium instead of low.

## Steps To Reproduce:
- Call in browser this URL :

```
https://securegatewayaccess.com/post?prejoin_data=domain%2Fevil.com/?=&weg_digest=eacde2b0b10379e9848390da67ed883666fe083a9ad892fae85c590ddd354e8c
```

- Or under the secure.chaturbate domain this URL :

```
https://secure.chaturbate.com/post?prejoin_data=domain%2Fevil.com/?=&weg_digest=eacde2b0b10379e9848390da67ed883666fe083a9ad892fae85c590ddd354e8c
```

- This can also be linked with the /external_link request from the root url to create a chained redirect :

```
https://chaturbate.com/external_link/?url=https%3A%2F%2Fsecure.chaturbate.com%2Fpost%3Fprejoin_data%3Ddomain%252Fevil.com%2F%3F%3D%26weg_digest%3Deacde2b0b10379e9848390da67ed883666fe083a9ad892fae85c590ddd354e8c
```

All requests will have as answer this header :

```
Location: http://evil.com/?=/tipping/purchase_tokens/
```

## Supporting Material/References:
N/A

## Impact

Open redirect that facilitate potential phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
