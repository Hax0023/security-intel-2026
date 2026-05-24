# SAML Authentication Bypass through Unauthenticated addSamlProvider Meteor Call

## Metadata
- **Source:** HackerOne
- **Report:** 1049375 | https://hackerone.com/reports/1049375
- **Submitted:** 2020-12-03
- **Reporter:** fabianfreyer
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Improper Access Control, Insecure Direct Object References, Privilege Escalation
- **CVEs:** CVE-2020-29594
- **Category:** auth-crypto

## Summary
Rocket.Chat exposes an unauthenticated Meteor method `addSamlProvider` that allows attackers to create a duplicate SAML provider configuration without certificate validation. By disabling signature verification on the SAML provider, an attacker can forge SAML responses and authenticate as any user, including administrators.

## Attack scenario
1. Attacker identifies a Rocket.Chat instance with SAML authentication enabled (default provider named 'Default')
2. Attacker calls the unauthenticated Meteor method: Meteor.call('addSamlProvider', 'Default_cert')
3. The method creates a new SAML provider setting without requiring authentication or authorization
4. Attacker crafts a forged SAML response claiming to be an administrative user
5. Attacker submits the forged SAML response to the login endpoint using the new 'Default_cert' provider
6. The system validates the response without certificate verification (cert is null/false) and authenticates the attacker as the claimed user

## Root cause
The `addSamlProvider` Meteor method is exposed to unauthenticated clients without access control checks. Additionally, the SAML signature verification logic skips validation when the certificate setting is not configured, allowing bypass via provider duplication. The underlying server-side function is unnecessarily exposed as a client-callable RPC method.

## Attacker mindset
An unauthenticated attacker seeks to gain unauthorized administrative access. They recognize that SAML providers with missing certificates skip validation entirely, and that creating a duplicate provider configuration bypasses intended security constraints. This allows them to forge authentication credentials without needing to compromise the actual SAML provider or possess valid certificates.

## Defensive takeaways
- Enforce strict authentication and authorization checks on all Meteor methods, especially those modifying security-critical settings
- Never expose server-only administrative functions as client-callable methods
- Implement role-based access control (RBAC) for sensitive operations like authentication provider management
- Default to secure-by-default: require explicit certificate configuration before allowing SAML validation bypass
- Avoid creating duplicate or parallel authentication configurations that circumvent existing security controls
- Conduct regular RPC surface audit to identify unintended client exposure of sensitive functions
- Implement logging and alerting for SAML provider configuration changes

## Variant hunting
Search for other Meteor methods exposed without authentication that modify authentication-related settings (OAuth, LDAP, JWT providers)
Audit other signature verification routines for similar certificate-is-null bypass patterns
Check for other settings manipulation methods that allow creating duplicate or shadow configurations
Investigate if other authentication mechanisms have similar 'addProvider' style methods without access control
Review all Meteor.methods definitions for missing authentication guards on administrative functions

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1199
- T1550

## Notes
This vulnerability affects all versions of Rocket.Chat using meteor-accounts-saml (0.8.0+). The attack requires zero authentication and can result in immediate administrative compromise. The fix is straightforward: remove client-side exposure of the method. The root cause represents a fundamental architectural flaw in exposing server-side administrative functions as client-callable RPC endpoints.

## Full report
<details><summary>Expand</summary>

**Summary:** Rocket.Chat exposes an unauthenticated Meteor method `addSamlProvider`, which allows disabling SAML signature verification.

**Description:**

The `addSamlProvider` Meteor method sets a number of settings, among them a boolean flag that defaults to `false`:
```js
export const addSamlService = function(name: string): void {
	settings.add(`SAML_Custom_${ name }`, false, {
		type: 'boolean',
		group: 'SAML',
		i18nLabel: 'Accounts_OAuth_Custom_Enable',
	});
```

The provider `name` is entirely user-controlled in this case.

Secondly, if a SAML authentication provider does not have a certificate set, or the setting is falsy, no validation is performed:
```js
private verifySignatures(response: Element, assertionData: ISAMLAssertion, xml: string): void {
	if (!this.serviceProviderOptions.cert) {
		return;
	}
```

## Releases Affected:

  * all versions including `meteor-accounts-saml`, i.e. 0.8.0 and later.

## Steps To Reproduce (from initial installation to vulnerability):

On the login page of a Rocket.Chat instance supporting SAML authentication using a provider named `Default` (this is the default), run the following Meteor call:
```
Meteor.call("addSamlService", "Default_cert")
```

Then log in using an arbitrarily faked SAML response.

## Suggested mitigation

  * Remove the `addSamlProvider` Meteor method. All callers of the underlying function are server-side, therefore it needs not be exposed to the client.

## Impact

* An unauthenticated attacker can disable SAML certificate validation on an instance with SAML authentication enabled, and then log in as an arbitrary user with administrative privileges.

</details>

---
*Analysed by Claude on 2026-05-24*
