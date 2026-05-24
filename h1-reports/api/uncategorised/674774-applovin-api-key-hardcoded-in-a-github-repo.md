# AppLovin API Key hardcoded in a Github repo

## Metadata
- **Source:** HackerOne
- **Report:** 674774 | https://hackerone.com/reports/674774
- **Submitted:** 2019-08-16
- **Reporter:** hackbotone_
- **Program:** Unknown
- **Bounty:** $280
- **Severity:** high
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hello,
I found a Sensitive Data Exposure in github/mopub-android-mediation project, the AppLovin UI API key is hardcoded in source code. 

And in the comment it's mentioned that 
##"This is a unique SDK Key from AppLovin. Get yours from the AppLovin UI".

Github Link:- https://github.com/mopub/mopub-android-mediation/blob/72804166ec9f3b79cc0dcfa96bd8c813f3252794/Testing/src/main/AndroidManifest.xm

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

Hello,
I found a Sensitive Data Exposure in github/mopub-android-mediation project, the AppLovin UI API key is hardcoded in source code. 

And in the comment it's mentioned that 
##"This is a unique SDK Key from AppLovin. Get yours from the AppLovin UI".

Github Link:- https://github.com/mopub/mopub-android-mediation/blob/72804166ec9f3b79cc0dcfa96bd8c813f3252794/Testing/src/main/AndroidManifest.xml#L60

Google Ads SDK reference link:- https://developers.google.com/admob/android/mediation/applovin

Thanks
Anshuman Pattnaik

## Impact

So if it's a production API key then it shouldn't be shown publicly in Github repo otherwise it can be used by other developers as it's a company property the API key should be secure as it's a monetize API key.

</details>

---
*Analysed by Claude on 2026-05-24*
