# Open Redirect at https://oauth.secure.pixiv.net OAuth Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 972601 | https://hackerone.com/reports/972601
- **Submitted:** 2020-09-02
- **Reporter:** zimmer75
- **Program:** Pixiv
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, OAuth Misconfiguration, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An open redirect vulnerability exists in Pixiv's OAuth authorization endpoint that allows attackers to redirect users to arbitrary domains when an invalid scope parameter is provided. This can be exploited for phishing attacks to steal user credentials by redirecting authenticated users to attacker-controlled domains.

## Attack scenario
1. Attacker crafts a malicious OAuth authorization URL with an invalid scope value (e.g., 'ggg') and a redirect_uri pointing to an attacker-controlled phishing domain
2. Attacker distributes the malicious link via social engineering (email, messages, forums, etc.) to Pixiv users
3. Victim clicks the link and is redirected through Pixiv's OAuth authorization page
4. Due to insufficient validation of the redirect_uri when scope is invalid, the victim is redirected to the attacker's phishing site instead of the legitimate redirect_uri
5. Victim's browser displays the attacker's phishing page, which mimics Pixiv's login interface
6. Victim enters their Pixiv credentials into the phishing site, compromising their account

## Root cause
The OAuth authorization endpoint fails to properly validate the redirect_uri parameter when the scope parameter contains invalid values. The server should reject requests with invalid scopes before processing redirect parameters, or consistently validate redirect_uri against a whitelist regardless of other parameter validity. The vulnerability suggests the validation logic either skips redirect_uri validation during error handling or uses separate validation paths.

## Attacker mindset
An attacker seeks to exploit trust in Pixiv's official OAuth flow to conduct credential harvesting attacks. By leveraging the open redirect vulnerability, they can bypass user skepticism about untrusted domains since the redirect originates from Pixiv's official infrastructure. The attacker likely discovered this through fuzzing scope parameters or analyzing error handling paths in the OAuth implementation.

## Defensive takeaways
- Implement strict whitelist-based validation of redirect_uri parameters for all OAuth flows, enforced before processing any other parameters
- Validate and reject invalid scope values early in request processing, but ensure redirect_uri validation occurs independently
- Apply consistent security checks across all code paths (happy path, error handling, and edge cases)
- Implement server-side validation of redirect_uri format and domain registration, not relying on client-side validation
- Log and monitor invalid scope attempts combined with mismatched redirect_uri values as suspicious activity
- Use OAuth 2.0 PKCE extension to add additional protection against redirect manipulation attacks
- Conduct security testing of OAuth endpoints with fuzzing of all parameters to identify validation bypasses

## Variant hunting
Test other OAuth endpoints (/token, /revoke) for similar redirect_uri validation bypasses
Fuzz other optional OAuth parameters (state, nonce, etc.) to see if invalid values bypass redirect validation
Test with valid scopes but invalid other parameters to determine if validation order matters
Attempt double-encoding or URL manipulation of redirect_uri to bypass validation
Check if POST-based authorization endpoints have the same vulnerability
Test with subdomain takeover scenarios to see if partially validated redirect_uri domains are vulnerable
Verify if other query parameters can be injected to manipulate redirect behavior

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Credential Dumping
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1187 - Forced Authentication

## Notes
This is a classic open redirect vulnerability in OAuth implementations. The specific trigger (invalid scope causing redirect validation bypass) suggests a code path issue where error handling doesn't apply the same security checks as normal request processing. The vulnerability is particularly dangerous because it leverages Pixiv's trusted domain to deliver users to phishing sites. The reporter provided clear reproduction steps but did not include impact assessment regarding whether valid OAuth codes could be obtained through this vector. This vulnerability could potentially be chained with other attacks if the attacker can obtain valid authorization codes through the redirect.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello @pixiv security team,  i hope you are well, i noticed you can redirect users to another domain if you send an invalided scope.

**Vulnerable Url**

* `https://oauth.secure.pixiv.net/v2/auth/authorize?client_id=Y1olfIApoCNuSGzx9kTgIbf5Wk4R&redirect_uri=https%3A%2F%2Fsketch.pixiv.net%2Fsession%2Fpixiv%2Fcallback&response_type=code&scope=read-email+read-x-restrict+read-birth+write-upload+read-profile+write-profile+read-favorite-users&state=security_token%3D5cb310fefea19a5cb56307af3488a816921413bc70b5b142%2Crequest_type%3Ddefault`

## Steps To Reproduce:

  *   In the request looks for the **scope** parameter and change his value to *ggg*.
 
  *    Looks for the **redirect_uri** parameter and change it for an arbitrary domain, i.e `https://example.com`

  *   Open the link in your browser and done.
  
  *   `https://oauth.secure.pixiv.net/v2/auth/authorize?client_id=Y1olfIApoCNuSGzx9kTgIbf5Wk4R&redirect_uri=https%3A%2F%2Fexample.com%2Fsession%2Fpixiv%2Fcallback&response_type=code&scope=ggg&state=security_token%3D5cb310fefea19a5cb56307af3488a816921413bc70b5b142%2Crequest_type%3Ddefault`

{F972733}

## Impact

It may lead users to a phishing site and an attacker can steals his credentials.

</details>

---
*Analysed by Claude on 2026-05-24*
