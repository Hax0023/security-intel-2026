# Config Override via Non-Validated Query Parameter Enables XSS and Business Logic Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1082847 | https://hackerone.com/reports/1082847
- **Submitted:** 2021-01-21
- **Reporter:** fransrosen
- **Program:** Grammarly
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Improper Input Validation, Reflected XSS, Configuration Injection, Business Logic Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
The app.grammarly.com endpoint accepts a ?config= query parameter that bypasses TypeScript schema validation by leveraging properties missing from the schema definition. While properties are validated against HttpString patterns, undocumented config properties are not included in the validation schema, allowing attackers to inject arbitrary configuration values that can lead to reflected XSS or manipulation of application business logic.

## Attack scenario
1. Attacker identifies that the config parameter accepts JSON-encoded configuration objects
2. Attacker discovers that the TypeScript validation schema is incomplete and missing properties like 'sumoUrl', 'tonesUrl', 'institutionSuggestionsUrl' that exist in the live application
3. Attacker crafts a malicious query parameter with unvalidated config properties containing JavaScript payloads or malicious URLs
4. The JSON parser and validator accept the payload since the missing properties are not in the schema validation rules
5. The application merges the injected config into the application state without proper sanitization
6. The malicious config is reflected in the application, executing XSS or redirecting users to attacker-controlled endpoints

## Root cause
Incomplete TypeScript schema definition for configuration validation. The validator only checks properties explicitly defined in the schema (Partial<{...}>), allowing properties present in the live application but absent from the schema to bypass validation entirely. The validation chain assumes all possible config properties are enumerated in the schema, creating a gap between documented and actual configuration parameters.

## Attacker mindset
An attacker would recognize that security implementations relying on schema-based allowlisting are vulnerable if the schema is incomplete or doesn't match the actual application configuration in production. By discovering undocumented config properties through reverse engineering or application inspection, the attacker can bypass intended security controls while remaining technically within the validation framework.

## Defensive takeaways
- Maintain configuration schema consistency between documentation, code, and production deployments
- Implement explicit allowlist validation that rejects any properties not in the schema rather than silently ignoring them
- Use a default-deny approach: validate each property individually and reject unknown properties outright
- Audit all configuration properties in use across all environments and keep schema definitions synchronized
- Consider disallowing URL-based configuration injection entirely if not strictly necessary
- Implement CSP headers strictly to prevent XSS even if configuration can be injected
- Add runtime validation logging to detect attempts to inject unexpected configuration properties
- Regularly compare production configuration against validated schema to catch mismatches

## Variant hunting
Search for other endpoints accepting query parameters that pass through validation chains with potentially incomplete schemas
Identify all TypeScript schema definitions used for input validation and cross-reference with actual production configurations
Check for similar URL-based configuration injection in other Grammarly applications or related properties
Review git history to find if properties were added to production config without updating validation schemas
Test other Partial<{...}> schema definitions for similar incomplete property enumeration
Check environment-specific config files for properties not reflected in validation logic
Search for other query parameters or API endpoints that accept JSON configuration objects

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information (via malicious URLs in config)
- T1566 - Phishing (social engineering via reflected XSS)
- T1204 - User Execution (if XSS requires user interaction)
- T1539 - Steal Web Session Cookie (via reflected XSS)

## Notes
The researcher demonstrates impressive security maturity recognition, noting that TypeScript schema validation is a good practice but incomplete implementation defeats its purpose. The writeup emphasizes that this is not just an XSS issue but a configuration integrity problem with business logic implications. The discovery method likely involved analyzing minified/transpiled JavaScript to recover the schema definition and comparing it against actual network traffic or production configuration. The researcher responsibly highlighted the CSP protection as a secondary defense limiting impact. Grammarly's structured API-routes and overall security posture suggest this was a difficult finding requiring deep application analysis.

## Full report
<details><summary>Expand</summary>

Hi,

First, I just want to say after spending a few days on your assets that I'm really impressed by the high security standard of the apps exposed. It has not been easy to find issues. I really like the way you've structured your API-routes in a way that almost eliminates a bunch of access issues.

I did find an interesting path that resulted in some issues. I did not classify the issue below just as an XSS, since you can also change business logic depending on what parameters you are affecting. I used the XSS as an example of what you can do with this.

The issue is that the code on `app.grammarly.com` allows a `?config=`-parameter to be used:

```js
              , s = function(e, t) {
                const n = u.Monitoring.Logging.getLogger("config.parser");
                return Object(i.pipe)(t, c.h.chain(e=>Object(i.pipe)(c.b.tryCatchError(()=>JSON.parse(e)), c.b.mapLeft(n.handler("Parse error of the provided JSON config", {
                    config: e
                }).info), c.h.fromEither)), c.h.fold(()=>e, t=>Object(i.pipe)(ye.decode(t), c.b.mapLeft(ge.failure), c.b.mapLeft(e=>n.info("Validation error of the provided JSON config", {
                    config: t,
                    error: e
                })), c.b.fold(()=>e, t=>{
                    n.info("Load app with custom config", t);
                    const r = c.k.asks(()=>e);
                    return c.k.createFrom(r)(()=>t)(void 0)
                }
                ))))
            }(Object(d.b)(), a.query.get("config"))
```

As you see here, the `query.get("config")` passes through a chain, first JSON-parsing it, and then validating it against a TypeScript-schema. This is a great solution to prevent some issues, since the TypeScript contains a list of config parameters and their corresponding type:

```ts
Partial<{
    api: Partial<{
        authUrl: HttpString
        capiApiUrl: HttpString
        capiWsUrl: HttpString
        crashLogUrl: HttpString
        dapiUrl: HttpString
        doxUrl: HttpString
        felogUrl: HttpString
        gnarApi: Partial<{ url: HttpString }>
        institutionAdminUrl: HttpString
        institutionPrivateUrl: HttpString
        institutionUrl: HttpString
        irbisUrl: HttpString
        onlineTestUrl: HttpString
        proofitResultUrl: HttpString
        wsTest: HttpString
    }>
    desktop: Partial<{
        mac: Partial<{
            infoURL: HttpString
            installURL: HttpString
        }>
        windows: Partial<{
            infoURL: HttpString
            installURL: HttpString
        }>
    }>
    edu: Partial<{ adminPanelURL: HttpString }>
    extension: Partial<{
        chrome: Partial<{
            infoURL: HttpString
            installURL: HttpString
        }>
        firefox: Partial<{
            iconURL: HttpString
            infoURL: HttpString
            installURL: HttpString
        }>
        safari: Partial<{
            installURL: HttpString
        }>
    }>
    funnel: Partial<{
        accountDeleted: HttpString
        mainPage: HttpString
        resetPassword: HttpString
        signin: HttpString
        signup: HttpString
        subscribe: HttpString
        upgrade: HttpString
        plans: HttpString
    }>
    officeAddIn: Partial<{
        infoURL: HttpString
        installURL: HttpString
    }>
    support: Partial<{
        connectionTroubleshooting: HttpString
        contact: HttpString
        diagnosticTestPath: HttpString
        documentAcceptTrackedChanges: HttpString
        email: HttpString
        emailExistsKBUrl: HttpString
        login: HttpString
        mainPage: HttpString
        newRequest: HttpString
    }>
}>
``` 

The `HttpString` type is validating that the value is a string and begins with `^https?|wss?`. It does allow any URL you want, but since you have a limited list of `connect-src` in your Content-Security-Policy, unless there's another issue with one of the hosts in there, there's no data getting sent externally by overwriting these values.

However.

There are missing properties in the TypeScript-schema, which are still being used live. Looking at the `api`-property, the current config being used live contains the following ones as well:

```json
"institutionSuggestionsUrl": "https://institution.grammarly.com/api/institution/settings/suggestions",
"institutionTonesUrl": "https://institution.grammarly.com/api/institution/settings/tones",
"institutionVoxUrl": "https://institution.grammarly.com/api/institution/vox",
"mailApiUrl": "https://g-mail.grammarly.com",
"redirect": "https://redirect.grammarly.com/redirect",
"ssoUrl": "https://sso.grammarly.com"
"subscriptionUrl": "https://subscription.grammarly.com/api/v1",
"sumoUrl": "https://endpoint2.collection.us2.sumologic.com/receiver/v1/http/ZaVnC4dhaV0Bxac28IqT2frgzsjX7HEotu8EZEZr07YE9RWLCzrOMGwzO9aL6c_iSiidkEplFOod2igKIxz_7s2CHlXc2u-XuLpetEBK1fV6xjfN2Sw2gA==",
"tonesUrl": "https://institution.ppgr.io/api/tones",
```

Since these ones are not in the TypeScript-schema, and the schema is set as `Partial<{}>`, you can overwrite the additional parameters with whatever content you want. 

The interesting one I found for my PoC was the `api.redirect`. It's being used for navigating between sites, especially when you are linking to upgrading your plan:

{F1165873}

Another one when being upgraded, is the `account`-property which is completely missing from the TypeScript-schema. The `Subscription`-link in the menu of the editor uses `account.subscription`-property which is never validated either:

{F1165874}

Also, another thing being interesting is, if you use the `https://app.grammarly.com/docs/new`, the current URL is rewritten when the new document is created, but the config from our query parameter will still be injected properly, this makes it possible to hide the injection.

### PoC

The following PoC will work for both upgraded accounts and free users. Free users will get the payload triggered when they try upgrading to Premium from the editor:

{F1165875}

And paying users will get the payload trigger when clicking "Subscription" in the menu:

{F1165877}

```
https://app.grammarly.com/docs/new?config={%22account%22:{%22subscription%22:%22javascript:alert(document.domain)//%22},%22api%22:{%22redirect%22:%22javascript:alert(document.domain)//%22}}
```

Since the config is persistent during the session, going to the main page as a free user and clicking the upgrade to premium will also get it triggered, but you can link to the start page also with the config (this won't hide the payload however):

```
https://app.grammarly.com/?config={%22api%22:{%22redirect%22:%22javascript:alert(document.domain)//%22}}
```

{F1165878}

You can also modify the `crossPlatformOfficeAddin.infoURL` since it's also not a part of the schema:

```
https://app.grammarly.com/?config={%22crossPlatformOfficeAddin%22:{%22infoURL%22:%22javascript:alert(document.domain)//%22}}
```

{F1165879}

Here's a video showing both scenarios for free and premium:

{F1165872}

### Mitigation

I would first suggest to remove the `config`-parameter feature completely. The risk of adding new properties when using a partial TypeScript schema will just introduce this issue again if the schema is not updated. Another solution would be to change the properties in the schema which are critical into being non-partial, which means it can only contain the parts specified in the TypeScript-schema.

## Impact

The XSS-issue affects all browsers and is not mitigated by any CSP, since you allow `unsafe-inline` and `unsafe-eval`. Any calls can be made as the attacker, since the javascript runs on the proper origin as the code already interacting with your APIs. However, there are more parameters in the config to modify that might change other things as well, not just creating an XSS. For example, `desktop.windows.installURL` and `desktop.mac.installURL` would be very interesting to also modify into proper URLs without any XSS needed, since you wou

</details>

---
*Analysed by Claude on 2026-05-12*
