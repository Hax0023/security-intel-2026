# Insecure Data Storage in Vine Android App - Cleartext Credentials in SQLite Database

## Metadata
- **Source:** HackerOne
- **Report:** 44727 | https://hackerone.com/reports/44727
- **Submitted:** 2015-01-22
- **Reporter:** avicoder_
- **Program:** Twitter/Vine
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Data Storage, Cleartext Password Storage, Insufficient Cryptography, Local Data Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Vine Android application stores sensitive authentication credentials including usernames and passwords in cleartext within an unencrypted SQLite database located at /data/data/co.vine.android/databases/webview.db. This allows any malicious application with file system access or an attacker with physical device access to retrieve credentials directly from the database.

## Attack scenario
1. Attacker gains access to compromised Android device or installs malicious app requesting file system permissions
2. Malicious app or attacker with root access navigates to /data/data/co.vine.android/databases/ directory
3. Attacker opens webview.db SQLite database file using SQLite tools or custom code
4. Attacker queries database tables and extracts cleartext username and password fields
5. Attacker uses stolen credentials to authenticate to Vine service and access victim's account
6. Attacker performs account takeover, data theft, or impersonation on the victim's behalf

## Root cause
Developers failed to implement encryption for sensitive data at rest. The application stores authentication credentials directly in SQLite database without applying encryption, relying solely on Android sandbox protection which is insufficient against determined attackers and malicious applications with file access permissions.

## Attacker mindset
An attacker with local device access or malware deployment capability recognizes that Android's sandbox can be bypassed through permission exploitation or root access. They target the predictable default database path and extract plaintext credentials for account takeover with minimal effort.

## Defensive takeaways
- Implement encryption for all sensitive data at rest using Android Keystore System or EncryptedSharedPreferences
- Never store passwords in plaintext; use secure hashing with salt for credential storage
- Apply database-level encryption using SQLCipher for sensitive data in SQLite databases
- Use Android's KeyChain API for storing cryptographic keys separate from application data
- Implement certificate pinning to prevent man-in-the-middle attacks on authentication flows
- Apply file-level permissions to restrict access to sensitive database files
- Conduct secure coding training focused on mobile data protection
- Perform regular security audits of local storage implementations
- Use automated tools to detect cleartext credential storage during build process

## Variant hunting
Check other WebView databases and cache directories for sensitive data exposure
Examine SharedPreferences files for unencrypted sensitive information
Review application logs and temporary files for credential leakage
Inspect third-party library usage for improper data storage practices
Test other Android apps by same developer for similar storage vulnerabilities
Analyze backup files and exported data formats for plaintext credentials
Check if cookies or session tokens are similarly exposed in storage
Review JavaScript code executed in WebView for data exfiltration capabilities

## MITRE ATT&CK
- T1555 - Credentials from Password Stores
- T1056 - Input Capture (credential harvesting)
- T1005 - Data from Local System
- T1213 - Data from Information Repositories
- T1040 - Network Sniffing (if credentials transmitted unencrypted)
- T1566 - Phishing (credential stealing via malware)
- T1621 - Multi-Factor Authentication Interception

## Notes
This is a foundational insecure storage vulnerability demonstrating failure to implement basic secure coding practices. The webview.db location suggests improper use of WebView components to handle authentication. The reporter appropriately references OWASP Mobile Top 10 M2. This vulnerability would likely have HIGH impact as it directly enables account takeover of legitimate users.

## Full report
<details><summary>Expand</summary>

Hi Twitter,

   - **Vulnerability Class:**OWASP M2 : Insecure Data Storage 

Every application needs to store something secret, like a website username,password, cookies etc. , internal storage is the place to do it,  android sandbox prevents other applications from accessing this data but,In vine android app  developers have chosen to store secret information without any additional encryption in place.

   - **Where I found it?**

`/data/data/co.vine.android/databases/webview.db`

   - **POC:**Please see the screenshot of SQLite database.

   - **SEVERITY:**
What is more severe than clear text username password storage and with the JavaScript and file system access enabled , Its not going to be hard for attacker to steal this info from the database or the whole database.

   - **Reference**:
I believe in basics :https://www.owasp.org/index.php/Mobile_Top_10_2014-M2


Please revert if more information needed. It will be fine for me to spare more time in this vulnerability issue.  
#:)#
**Happy to help.**

Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
