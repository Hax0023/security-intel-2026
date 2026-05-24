# Insecure Client-Side JWT Generation for Zendesk SSO - Hardcoded Secret Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 638635 | https://hackerone.com/reports/638635
- **Submitted:** 2019-07-09
- **Reporter:** xh3n1
- **Program:** Trint
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Insecure Cryptographic Storage, Hardcoded Credentials, Client-Side Secret Exposure, Authentication Bypass, JWT Misuse, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Trint's app.trint.com implements Zendesk SSO using client-side JWT generation with a hardcoded HMAC secret embedded in minified JavaScript source maps. An attacker can extract the secret, forge arbitrary JWT tokens, and impersonate any customer to access their Zendesk support tickets and account data.

## Attack scenario
1. Attacker accesses app.trint.com and downloads the minified JavaScript bundle and corresponding source map file
2. Attacker searches source map for 'REACT_APP_ZENDESK_SECRET' and extracts the hardcoded secret: 'oq1HJ4jXo99Wt41bwvLh9BXBVdgpi52CjkXbThow7UhWQGtJ'
3. Attacker uses jwt.io or similar tool to craft a malicious JWT payload with victim's email address and current timestamp, signed with the extracted secret
4. Attacker constructs URL: 'https://trintsupport.zendesk.com/access/jwt?jwt=[FORGED_JWT_TOKEN]'
5. Attacker navigates to the URL and gains authenticated access as the impersonated victim in Zendesk
6. Attacker accesses victim's support tickets, communication history, and potentially sensitive business information

## Root cause
The JWT signing operation was implemented on the client-side instead of the server-side, requiring the HMAC secret to be embedded in client-accessible JavaScript code. Additionally, source maps were deployed to production, enabling easy extraction of the secret from minified code.

## Attacker mindset
An attacker recognizes that client-side cryptographic operations require secrets to be accessible to the browser, making secrets inherently compromised. Source maps provide a convenient roadmap to find sensitive configuration. The Zendesk JWT SSO implementation trusts any validly-signed token without additional server-side verification, making forged tokens immediately actionable.

## Defensive takeaways
- Never perform JWT signing or cryptographic operations on the client-side; always generate security tokens on trusted server infrastructure
- Never embed secrets, API keys, or credentials in client-accessible code, environment variables, or source maps
- Disable source map generation in production builds, or strip sensitive information from them
- Implement server-side validation and additional context checks (IP whitelist, session binding, rate limiting) before accepting JWT tokens
- Use short-lived tokens with additional anti-forgery mechanisms (CSRF tokens, state validation)
- Rotate Zendesk secrets immediately upon exposure and implement secret rotation policies
- Implement Content Security Policy (CSP) headers to restrict JavaScript execution and exfiltration
- Monitor and alert on unusual Zendesk authentication patterns or access from unexpected IPs

## Variant hunting
Search for other hardcoded secrets in environment variables exposed in source maps (REACT_APP_*, VUE_APP_*, similar patterns)
Identify other OAuth/SAML/OIDC integrations implemented client-side across the Trint platform
Check for similar JWT generation patterns in other JavaScript bundles or third-party integrations
Audit other Trint services (trint.com, support.trint.com, etc.) for similar credential exposure in source maps or compiled assets
Review git history and deployment artifacts for accidental secret commits
Examine API endpoints that accept user-supplied JWT tokens for proper signature verification and claims validation

## MITRE ATT&CK
- T1190
- T1199
- T1552
- T1556
- T1078
- T1021

## Notes
The vulnerability is particularly severe because: (1) source maps were publicly available alongside minified code, dramatically lowering the barrier to exploitation; (2) the Zendesk JWT implementation trusts any validly-signed token without additional context validation; (3) the secret was high-entropy suggesting it was a genuine Zendesk-provided credential, not a placeholder. The reporter properly noted that while Zendesk's JWT SSO design is sound per documentation, the implementation in app.trint.com violated fundamental security principles. This is a textbook example of 'secrets in client-side code' and highlights why security-critical operations must always be server-side.

## Full report
<details><summary>Expand</summary>

## Summary:
app.trint.com implements SSO to Zendesk, it does this by using JWT as described at https://support.zendesk.com/hc/en-us/articles/203663816-Enabling-JWT-JSON-Web-Token-single-sign-on

This functionality has not been implemented securely because the JWT generation happens in the client-side. This is done by the Zendesk secret being hardcoded in the JavaScript code.
The secret is used to create JSON Web Tokens and then you can use the generated token to impersonate any customer in Zendesk. (therefore potentially getting access to their support tickets)

Whilst support.trint.com is marked as out of scope for the program, the described vulnerability isn't caused by Zendesk. The vulnerable component is in app.trint.com.

## Assessment
The JavaScript source map files are available next to the minified production files. This significantly makes analyzing this issue easier.

- JavaScript file: https://app.trint.com/static/js/app.e984c9df.js
- Sourcemap file: https://app.trint.com/static/js/app.e984c9df.js.map

Looking at some of the UI views, I stumbled upon `static/js/modules/auth/pages/ZendeskLoadingPage.js`. I've attached a stripped version which shows the JWT generation:

```js
[snip]
import { ZENDESK_DOMAIN } from 'modules/core/constants/index';

const { REACT_APP_ZENDESK_SECRET } = process.env;

[snip]

function RedirectToZendesk(props) {
  const { user, history } = props;

  function generateZendeskTokenAndRedirect() {
    const TIME_NOW_OBJECT = moment(Date.now());
    try {
      const payload = {
        iat: TIME_NOW_OBJECT.unix(),
        jti: uuid.v4(),
        name: `${user.profile.firstName} ${user.profile.lastName}`,
        email: user.username,
      };

      // encode zendesk token
      const zendeskToken = jwt.sign(payload, REACT_APP_ZENDESK_SECRET);
      window.location = `${ZENDESK_DOMAIN}/access/jwt?jwt=${zendeskToken}`;
    } catch (err) {
      history.push('/error');
    }
  }

  useEffect(
    () => {
      generateZendeskTokenAndRedirect(user);
    },
    [user],
  );

  return <Loader />;
}

[snip]

export default ZendeskLoadingPage;
```

Searching for `REACT_APP_ZENDESK_SECRET` in the sourcemap will show the JWT secret: 

```js
var REACT_APP_ZENDESK_SECRET = "oq1HJ4jXo99Wt41bwvLh9BXBVdgpi52CjkXbThow7UhWQGtJ";
```

Generating the JWT on the client-side like this allows anyone to mint an arbitrary JWT. It would probably be better to generate this on the server-side.

## Reproduction steps

- As logged-in user press "Support" on https://app.trint.com
- Intercept the traffic and see the call to `https://trintsupport.zendesk.com/access/jwt?jwt=[JWT_TOKEN]`
- Logout of Zendesk
- Put the JWT token from above URI into https://jwt.io and decode it.

Example:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NjI3MDk2NTksImp0aSI6IjIxZDAyOTg3LWU3YWItNDQ5MC05N2Q3LTc2YTBmMzJhOTVjOCIsIm5hbWUiOiJUZXN0IFRlc3QiLCJlbWFpbCI6ImIzODcxNjk0QHVyaGVuLmNvbSJ9.mnnx7dbpXbvU7xr5Bp5pad2eHVN01mSsXApmZoFj73c
```

```
{
  "iat": 1562709659,
  "jti": "21d02987-e7ab-4490-97d7-76a0f32a95c8",
  "name": "Test Test",
  "email": "b3871694@urhen.com"
}
```

- Now we can continue with tampering the JWT 
  - Change IAT to the current Unix timestamp
  - Change JTI to a random UUID v4
  - Change email to the victim email address
  - Insert `oq1HJ4jXo99Wt41bwvLh9BXBVdgpi52CjkXbThow7UhWQGtJ` as HMAC secret.
- Use the resulting JWT in a call to `https://trintsupport.zendesk.com/access/jwt?jwt=[JWT_TOKEN]`. You will be logged in as the victim.

## Impact

Access to the Zendesk account of Trint customers. This includes potentially the support history of said user.

I haven't verified whether the same SSO flow can also be used against Zendesk administrators. If so, the risk would be higher.

</details>

---
*Analysed by Claude on 2026-05-24*
