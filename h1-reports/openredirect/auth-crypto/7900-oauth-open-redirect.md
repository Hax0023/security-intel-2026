# OAuth Open Redirect via requestTokenAndRedirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 7900 | https://hackerone.com/reports/7900
- **Submitted:** 2014-04-17
- **Reporter:** melvin
- **Program:** Respond.ly
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, OAuth Misconfiguration, URL Validation Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can exploit an open redirect vulnerability in the Twitter OAuth flow by manipulating the `requestTokenAndRedirect` parameter to redirect authenticated users to attacker-controlled domains while the OAuth token and verifier are accessible. This enables phishing attacks and token harvesting by redirecting victims after they authorize their Twitter account.

## Attack scenario
1. Attacker identifies the vulnerable OAuth endpoint at `/_oauth/twitter/?requestTokenAndRedirect=` parameter
2. Attacker crafts a malicious URL with `requestTokenAndRedirect` pointing to attacker's domain or phishing page
3. Attacker sends the crafted URL to victims via email, social media, or other channels
4. Victim clicks the link and authorizes their Twitter account through the legitimate OAuth flow
5. After authorization, the victim is redirected to the attacker's domain instead of the intended service
6. Attacker captures OAuth tokens, verifier, and can perform actions on behalf of the victim

## Root cause
The application fails to validate or whitelist the destination URL in the `requestTokenAndRedirect` parameter before performing the redirect after OAuth authorization, allowing arbitrary domain redirects.

## Attacker mindset
An attacker would exploit this to perform credential phishing, OAuth token theft, account takeover, or privilege escalation by gaining access to victim's Twitter account credentials and OAuth tokens during the authorization flow.

## Defensive takeaways
- Implement strict URL validation using a whitelist of allowed redirect domains
- Use domain comparison logic that prevents subdomain bypasses and protocol confusion
- Validate redirect URLs against a predetermined list of safe internal application URLs only
- Implement URL parsing libraries that properly handle edge cases and encoding bypasses
- Log and monitor redirect parameters for suspicious patterns
- Use explicit allowlisting rather than blocklisting for OAuth redirect URIs
- Consider using state tokens to prevent open redirect and CSRF attacks
- Test OAuth flows with various redirect payload types during security testing

## Variant hunting
Check for open redirects in other OAuth provider integrations (Facebook, Google, GitHub)
Test similar parameters: `redirect`, `callback`, `return_to`, `next`, `destination`
Look for URL encoding bypasses: `%2e%2e/`, double encoding, Unicode encoding
Test protocol confusion: `javascript:`, `data:`, `file://` URIs
Check for subdomain bypass: `app.respond.ly.attacker.com`
Test whitelist bypasses: `respond.ly.attacker.com`, `respond.ly@attacker.com`
Review other OAuth-dependent features for similar validation issues

## MITRE ATT&CK
- T1598
- T1566
- T1589
- T1190

## Notes
This is a critical OAuth-related vulnerability as it combines open redirect with authentication flows. The token and verifier being accessible during the redirect makes this particularly dangerous for token hijacking. The simplicity of the fix (whitelisting) contrasts with the severity of impact, making this a high-priority security issue for any OAuth-dependent application.

## Full report
<details><summary>Expand</summary>

An attacker can use an open redirect vulnerability in the Twitter OAuth process to redirect someone to his/her webpage, while also obtaining the OAuth token and verifier of the victim. 

The vulnerability is right here: https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com. When someone authorizes their Twitter account using that URL, the redirect will go to https://hackerone.com.

Recommendation: make sure the `requestTokenAndRedirect` paramater only accepts hosts on whitelisted domains.

</details>

---
*Analysed by Claude on 2026-05-24*
