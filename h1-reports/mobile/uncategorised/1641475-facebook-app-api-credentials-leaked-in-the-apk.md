# Facebook App API Credentials Leaked in GlassWire Application Binary

## Metadata
- **Source:** HackerOne
- **Report:** 1641475 | https://hackerone.com/reports/1641475
- **Submitted:** 2022-07-19
- **Reporter:** chip_sec
- **Program:** GlassWire
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Hardcoded Credentials, Sensitive Information Disclosure, Improper Secrets Management, API Key Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Facebook App ID and App Secret were hardcoded in the GlassWire.exe binary, allowing extraction through static analysis or decompilation. The exposed credentials can be used to obtain valid access tokens and modify Facebook App settings without authorization. This directly violates Facebook's security guidelines which explicitly prohibit embedding app secrets in client-side code or application binaries.

## Attack scenario
1. Attacker downloads GlassWire installer version 1.1.26.0b and extracts the executable
2. Attacker uses reverse engineering tools (strings, hex editor, or decompiler) to analyze GlassWire.exe for embedded credentials
3. Attacker identifies and extracts the Facebook App ID (660471650708388) and App Secret (71a2d003a5ecfab4f4ad86dfb70b74e0)
4. Attacker crafts an OAuth request using the exposed credentials to obtain a valid Facebook access token
5. Attacker authenticates with Facebook API using the stolen app token and gains unauthorized access to app settings and resources
6. Attacker modifies app permissions, redirects, or exfiltrates data associated with the compromised Facebook application

## Root cause
Sensitive credentials were embedded directly in the compiled application binary during development instead of being retrieved from secure server-side infrastructure or environment variables at runtime. The development team failed to implement proper secrets management practices and did not sanitize binaries for sensitive data before distribution.

## Attacker mindset
An attacker with moderate technical skills can reverse engineer published applications to extract hardcoded secrets. This is an opportunistic vulnerability that requires only public tools and the ability to download the application. The attacker would recognize that embedded credentials in binaries are a common oversight and systematically search for API keys, tokens, and secrets that can be monetized or used for further compromise.

## Defensive takeaways
- Never embed API keys, secrets, or credentials in application binaries or client-side code
- Implement server-side authentication and API calls that proxy Facebook requests, keeping secrets on secure backend infrastructure
- Use environment variables, secure configuration management systems, or key vaults to manage sensitive credentials
- Conduct regular binary analysis and static code reviews to detect hardcoded secrets before release
- Implement secret scanning tools in CI/CD pipelines to prevent accidental credential commits
- Rotate and revoke any credentials that may have been exposed in previous releases
- Follow principle of least privilege for app credentials and enable detailed API logging and monitoring
- Consider code obfuscation as a supplementary (not primary) defense layer
- Establish a security baseline review before each release covering credential exposure risks

## Variant hunting
Search for other GlassWire versions and similar network monitoring applications for embedded third-party API credentials. Examine other applications that integrate with Facebook, Google, AWS, or other platforms for hardcoded tokens. Analyze compiled executables (.exe, .dll, .apk files) from popular utilities using strings analysis and hex dumps for patterns matching OAuth tokens, API secrets, and bearer token formats.

## MITRE ATT&CK
- T1589 - Gather Victim Identity Information
- T1588 - Obtain Capabilities
- T1552 - Unsecured Credentials
- T1187 - Forced Authentication
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts

## Notes
The vulnerability report demonstrates that the exposed credentials were functional and verified working through proof-of-concept API calls. GlassWire is a legitimate network monitoring tool, making this a supply chain concern where users running the application inadvertently expose their developers' Facebook app infrastructure. The report lacks specific information about patch timelines and whether the credentials were rotated immediately upon disclosure. This type of vulnerability affects all users of the affected version and persists as long as the binary is available for download from any source.

## Full report
<details><summary>Expand</summary>

GlassWire version 1,1,26,0b (F1827380) contains Facebook App API credentials (https://developers.facebook.com/docs/facebook-login/guides/access-tokens?locale=en_US#apptokens) in the GlassWire.exe file.
App ID: `660471650708388`
App Secret: `71a2d003a5ecfab4f4ad86dfb70b74e0`

To check that token is work run:  
`curl "https://graph.facebook.com/oauth/access_token?client_id=660471650708388&client_secret=71a2d003a5ecfab4f4ad86dfb70b74e0&redirect_uri=&grant_type=client_credentials"`  
You will get aresponse `{"access_token":"660471650708388|jboBZgqj64W1JXIAKIbtVz24FlQ","token_type":"bearer"}`

From the Facebook documentation https://developers.facebook.com/docs/facebook-login/guides/access-tokens#apptokens:  
> Note that because this request uses your app secret, it must never be made in client-side code or in an app binary that could be decompiled. It is important that your app secret is never shared with anyone. Therefore, this API call should only be made using server-side code.

## Impact

This token can be used to modify Facebook App settings.

</details>

---
*Analysed by Claude on 2026-05-24*
