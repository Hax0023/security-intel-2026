# Facebook App API credentials leaked in the APK

## Metadata
- **Source:** HackerOne
- **Report:** 1641475 | https://hackerone.com/reports/1641475
- **Submitted:** 2022-07-19
- **Reporter:** chip_sec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** uncategorised

## Summary
GlassWire version 1,1,26,0b (F1827380) contains Facebook App API credentials (https://developers.facebook.com/docs/facebook-login/guides/access-tokens?locale=en_US#apptokens) in the GlassWire.exe file.
App ID: `660471650708388`
App Secret: `71a2d003a5ecfab4f4ad86dfb70b74e0`

To check that token is work run:  
`curl "https://graph.facebook.com/oauth/access_token?client_id=660471650708388&client_sec

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
