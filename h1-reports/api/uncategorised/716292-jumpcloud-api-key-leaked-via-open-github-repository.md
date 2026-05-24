# JumpCloud API Key leaked via Open Github Repository.

## Metadata
- **Source:** HackerOne
- **Report:** 716292 | https://hackerone.com/reports/716292
- **Submitted:** 2019-10-17
- **Reporter:** vinothkumar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Use of Hard-coded Credentials
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Summary:** Open Github Repo Leaking Starbucks JumbCloud API Key

**Description:** 
Team,

While going through Github search I discovered a public repository which contains Jumbcloud API Key of Starbucks. 

Repo:  [https://github.com/██████████/Project](https://github.com/██████████/Project).
File: [https://github.com/████/Project/blob/0d56bb910923da2fbee95971778923f734a25f68/getSystemUsers.go](h

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

**Summary:** Open Github Repo Leaking Starbucks JumbCloud API Key

**Description:** 
Team,

While going through Github search I discovered a public repository which contains Jumbcloud API Key of Starbucks. 

Repo:  [https://github.com/██████████/Project](https://github.com/██████████/Project).
File: [https://github.com/████/Project/blob/0d56bb910923da2fbee95971778923f734a25f68/getSystemUsers.go](https://github.com/████/Project/blob/0d56bb910923da2fbee95971778923f734a25f68/getSystemUsers.go)

```
req.Header.Add("x-api-key", "████████")
```

**POC**
* List systems ```
curl -H "x-api-key: ████████" "https://console.jumpcloud.com/api/systems"
``` There are multiple AWS instances present

* ```
curl -H "x-api-key: █████" "https://console.jumpcloud.com/api/systemusers"
```
* SSO Applications ```curl -H "x-api-key: ██████" "https://console.jumpcloud.com/api/applications"
``` AWS login SAM config is presents. This would leads to AWS account takeover

## Impact

This issue impact is critical as through this API anyone could 
* Execute commands on systems [https://docs.jumpcloud.com/1.0/commands/create-a-command](https://docs.jumpcloud.com/1.0/commands/create-a-command)
* Add/Remove users which has access to internal systems
* AWS Account Takeover

</details>

---
*Analysed by Claude on 2026-05-24*
