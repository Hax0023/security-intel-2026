# Unauthenticated CRXDE Lite/CRX Access Leads to PII Disclosure in AEM

## Metadata
- **Source:** HackerOne
- **Report:** 1095830 | https://hackerone.com/reports/1095830
- **Submitted:** 2021-02-04
- **Reporter:** mit0z
- **Program:** Unknown (Redacted)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Broken Authentication, Information Disclosure, Inadequate Access Controls, Sensitive Data Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
An Adobe Experience Manager (AEM) instance exposed CRXDE Lite/CRX developer console without authentication, allowing unauthenticated attackers to query the content repository and retrieve personally identifiable information. The attacker could execute queries to find sensitive data and access it via exposed endpoints.

## Attack scenario
1. Attacker discovers AEM instance running on accessible domain
2. Attacker navigates to CRXDE Lite interface (typically /crx/de or /crx) without authentication
3. Attacker uses query functionality to search for sensitive content (e.g., 'admin' keyword)
4. Attacker executes JCR query to retrieve matching nodes from content repository
5. Attacker identifies endpoint URLs exposing retrieved data in JSON format
6. Attacker accesses endpoint to exfiltrate PII including user profiles, credentials, or personal information

## Root cause
AEM CRXDE Lite/CRX development console was exposed to the internet without proper authentication or access control restrictions. The default configuration or misconfiguration allowed unauthenticated users to access query functionality and retrieve sensitive repository data through accessible endpoints.

## Attacker mindset
An attacker would recognize exposed developer tools as high-value targets. CRXDE Lite provides direct access to the content repository, making it ideal for reconnaissance and data extraction. The presence of executable query functionality significantly amplifies the impact.

## Defensive takeaways
- Restrict CRXDE Lite and CRX console access to specific IP ranges or behind authentication/VPN
- Disable CRXDE Lite in production environments or remove dispatcher rules allowing access
- Implement strong authentication (OAuth, SAML) for all development interfaces
- Apply principle of least privilege to repository queries and limit query results
- Audit and monitor access to /crx/* and /crxde/* paths
- Use dispatcher/load balancer rules to block external access to development endpoints
- Regularly scan for exposed development consoles and admin interfaces
- Implement network segmentation to isolate AEM instances

## Variant hunting
Check for exposed CRX explorer at /crx/explorer
Test /crx/de/default.html and variations for unauthenticated access
Attempt to access package manager at /crx/packmgr without authentication
Query content repository via /bin/querybuilder.json with various search terms
Test for exposed AEM system console at /system/console
Check for accessible /api/* endpoints that expose repository data
Probe for backup/archived versions of CRXDE accessible via different paths
Test query execution via POST requests to various query endpoints

## MITRE ATT&CK
- T1190
- T1526
- T1595
- T1592
- T1087
- T1083
- T1040

## Notes
The report contains significant redactions making detailed analysis difficult. The vulnerability is critical because CRXDE Lite is explicitly documented as a development tool that should never be accessible in production. AEM administrators should follow Adobe's security hardening guidelines which explicitly recommend disabling CRXDE in production via dispatcher configuration. This vulnerability class (exposed development consoles) is common in misconfigured enterprise applications.

## Full report
<details><summary>Expand</summary>

hi team ,
i found that aem is running on``` ████████ ``` and CRXDE Lite/CRX is exposed to unauthenticated user that can lead to information disclosure

POC
====
1-visit ``` https://██████//██████████ ```
2-go to query and search for admin then execute
3-go to this endpoint to retrieve the information 
```
https://████████//████████/███
```
[+]Request
```
GET //███/███ HTTP/1.1
Host: ████
Connection: close
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en-XA;q=0.9,en;q=0.8
Cookie: oauth-configid=██████


```
[+]Response
```
HTTP/1.1 200 OK
Date: Thu, 04 Feb 2021 22:23:42 GMT
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: application/json;charset=utf-8
Content-Length: 1789
Connection: close
Set-Cookie: ███████; path=/; Httponly; Secure
Strict-Transport-Security: max-age=31536000; includeSubDomains
Set-Cookie: f5avraaaaaaaaaaaaaaaa_session_=█████████; HttpOnly; secure
Set-Cookie: █████████; Path=/

████████

```

█████████

## Impact

PII exposure

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1-visit ``` https://████████//█████████ ```
2-go to query and search for admin then execute
3-go to this endpoint to retrieve the information 
```
https://█████//███████/████
```

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
