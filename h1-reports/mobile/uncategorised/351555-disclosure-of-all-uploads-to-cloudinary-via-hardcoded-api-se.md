# Disclosure of all uploads to Cloudinary via hardcoded API secret in Android app

## Metadata
- **Source:** HackerOne
- **Report:** 351555 | https://hackerone.com/reports/351555
- **Submitted:** 2018-05-14
- **Reporter:** bagipro
- **Program:** Reverb
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Hardcoded Credentials, Sensitive Information Disclosure, Insecure Configuration Management, API Key Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Cloudinary API secret and key were hardcoded in the Android application's CloudinaryFacade.java file, allowing attackers to access, modify, and delete all uploaded files stored in the Cloudinary account. The exposed credentials also revealed account usage statistics showing 36 million stored resources and 256 million derived resources.

## Attack scenario
1. Attacker decompiles the Reverb Android app using standard reverse engineering tools
2. Attacker discovers hardcoded Cloudinary credentials in com/reverb/app/CloudinaryFacade.java
3. Attacker extracts the API key (434762629715) and API secret from the config string
4. Attacker uses credentials to authenticate against Cloudinary API endpoints
5. Attacker performs unauthorized operations: viewing, modifying, replacing, or deleting user uploads and settings
6. Attacker queries the usage endpoint to enumerate account statistics and scope of compromise

## Root cause
Developers embedded full Cloudinary authentication credentials (both API key and secret) directly in source code instead of following security best practices which explicitly recommend including only the cloud_name client-side and keeping secrets server-side

## Attacker mindset
An attacker discovers this through routine APK decompilation and reverse engineering. The exposure is trivial to exploit—credentials are directly readable in source code without additional bypasses. The attacker recognizes immediate value in manipulating or stealing user-uploaded content at scale.

## Defensive takeaways
- Never hardcode API keys, secrets, or authentication credentials in client-side code (mobile, web, frontend)
- Use server-side proxies or backend intermediaries for all API calls requiring secret credentials
- Include only non-sensitive identifiers (cloud_name) in client applications
- Implement credential rotation policies and monitor API access logs for anomalous activity
- Apply static analysis and secret scanning tools (TruffleHog, GitGuardian) in CI/CD pipelines to prevent accidental commits
- Use environment variables or secure configuration management for any secrets that must exist in deployed code
- Implement rate limiting and anomaly detection on Cloudinary API endpoints to catch unauthorized bulk operations

## Variant hunting
Search for similar patterns in decompiled APKs: hardcoded 'cloudinary://' URLs, base64-encoded credentials in config files, AWS access keys in BuildConfig.java, Firebase database URLs with embedded secrets, hardcoded OAuth tokens in interceptors, and API keys in string resources or manifest metadata

## MITRE ATT&CK
- T1552.001 - Unsecured Credentials: Credentials In Files
- T1187 - Forced Authentication
- T1526 - Acquire Infrastructure
- T1087 - Account Discovery
- T1526 - Enumerate cloud storage buckets

## Notes
This report exemplifies a critical mobile security failure. APK decompilation is trivial and credentials in source code are fully exposed. The vulnerability affects not just the organization but all users whose uploads are stored in the compromised Cloudinary account. The attacker gained not only read access but full CRUD capabilities over 36M resources. This is a textbook example of why backend-for-frontend (BFF) architecture or secure token exchange mechanisms are essential for mobile applications handling user data.

## Full report
<details><summary>Expand</summary>

Hi, in file ``` com/reverb/app/CloudinaryFacade.java ``` you have hardcoded the following config:
```java
private static final java.lang.String CONFIG = "cloudinary://434762629765715:█████@reverb";
```
where ``` 434762629765715:████████ ``` is basic auth details.

It shouldn't be disclosed to third parties as official docs say (https://github.com/cloudinary/cloudinary_android):
> Note: You should only include the ``` cloud_name ``` in the value, the api secret and key should be left out of the application.

I was able to access your account data
{F297519}
{F297520}

Those keys give me ability to not only access the files, but also replace and delete them, change different their settings. Also this url https://api.cloudinary.com/v1_1/reverb/usage discloses statistics regarding stored files
```json
"requests":1894689201,
"resources":36029794,
"derived_resources":256178843
```

## Impact

Disclosure of all uploads to Cloudinary via hardcoded api secret in Android app

</details>

---
*Analysed by Claude on 2026-05-24*
