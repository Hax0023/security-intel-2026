# Firebase Database Takeover in Zego Sense Android app

## Metadata
- **Source:** HackerOne
- **Report:** 1065134 | https://hackerone.com/reports/1065134
- **Submitted:** 2020-12-23
- **Reporter:** sheikhrishad0
- **Program:** Zego (com.zegocover.zego Android app)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insecure Direct Object References (IDOR), Inadequate Access Control, Information Disclosure, Hardcoded Credentials/Secrets, Cloud Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Zego Sense Android application hardcodes a publicly accessible Firebase Realtime Database URL in its source code with default insecure security rules, allowing unauthenticated read and write access to sensitive data. An attacker can directly access the database endpoint via HTTP requests to exfiltrate, modify, or delete data.

## Attack scenario
1. Attacker decompiles or inspects the Android app's resources (strings.xml) to extract the Firebase database URL
2. Attacker makes HTTP GET request to https://api-project-615509201590.firebaseio.com/.json to enumerate database structure and extract sensitive user data
3. Attacker crafts malicious HTTP PUT requests to inject arbitrary data into the database
4. Attacker deletes or modifies existing records via HTTP DELETE/PATCH requests
5. Attacker monitors database for ongoing updates to maintain persistence and track future usage
6. Attacker leverages exfiltrated data for identity theft, fraud, or sells data on underground markets

## Root cause
Firebase Realtime Database was deployed with default security rules (allow read/write to all) and the database URL was hardcoded in client-side code without implementing proper authentication mechanisms, API key restrictions, or security rules limiting access to authenticated users only.

## Attacker mindset
Opportunistic - searching for exposed cloud services by analyzing publicly available Android APK files; escalates to data theft and service disruption once database access is confirmed.

## Defensive takeaways
- Never hardcode or embed Firebase database URLs, API keys, or service endpoints in client-side code; use secure configuration management
- Implement strict Firebase Security Rules restricting read/write access to authenticated users with proper role-based access control
- Enable Firebase authentication (Firebase Auth, OAuth 2.0) and enforce token-based access
- Restrict API keys to specific services and IP ranges; use different API keys for different environments
- Regularly audit Firebase project IAM permissions and disable public access by default
- Use Firebase Storage/Firestore with encryption at rest and in transit for sensitive data
- Implement continuous monitoring and alerting for unauthorized database access patterns
- Conduct regular security audits of APK files to identify exposed credentials or endpoints
- Use secrets management tools (e.g., AWS Secrets Manager, HashiCorp Vault) for sensitive configuration

## Variant hunting
Search for similar patterns: hardcoded Firebase URLs in other Android/web applications, exposed Realtime Database endpoints (firebaseio.com domains), misconfigured Firestore instances, AWS DynamoDB endpoints without access controls, exposed MongoDB Atlas clusters, hardcoded API keys/tokens in application resources

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (misconfigured Firebase)
- T1526 - Cloud Service Discovery
- T1087 - Account Discovery (enumerate database structure)
- T1530 - Data from Cloud Storage (exfiltrate Firebase data)
- T1485 - Data Destruction (malicious modifications/deletions)
- T1592 - Gather Victim Identity Information
- T1040 - Network Sniffing (monitor API requests)

## Notes
Report demonstrates simple but critical misconfiguration commonly found in mobile applications. The PoC is straightforward: public HTTP requests to /.json endpoint return entire database. Hardcoded URLs in APK are trivially discoverable through decompilation. This likely affects all users of the app if any personal/sensitive data is stored in this database. Immediate remediation required.

## Full report
<details><summary>Expand</summary>

Hello Team,

Summary:
publicly available Firebase Database (api-project-615509201590.firebaseio.com)

Platform Affected: [android]
com.zegocover.zego

Steps To Reproduce:

in res/values/strings.xml

    <string name="firebase_database_url">https://api-project-615509201590.firebaseio.com</string>

POC:

    Go to https://api-project-615509201590.firebaseio.com/.json

{F1127099}

Exploit:

    import requests
    data= {"Exploit":"Successfull", "H4CKED BY": "Sheikh Rishad"}
    reponse = requests.put("https://api-project-615509201590.firebaseio.com/.json", json=data)


References:


There are guidelines available by Firebase to resolve the insecurities and misconfiguration, please follow this link:
https://firebase.google.com/docs/database/security/resolve-insecurities

Regards,
Sheikh Rishad

## Impact

This is quite serious because by using this database attacker can use this for malicious purposes and also an attacker can track this database if zego uses it for future perspective and at that time it will be much easier for the attacker to steal the data from this repository and later it will harm the reputation of the zego.

So please immediately change the rule of the database to private so that nobody can able to access it outside.

</details>

---
*Analysed by Claude on 2026-05-24*
