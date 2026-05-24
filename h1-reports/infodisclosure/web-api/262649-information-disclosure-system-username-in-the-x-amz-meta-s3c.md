# Information disclosure (system username) in the x-amz-meta-s3cmd-attrs response header on federation.data.gov

## Metadata
- **Source:** HackerOne
- **Report:** 262649 | https://hackerone.com/reports/262649
- **Submitted:** 2017-08-23
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
##Description
Hi. I just noticed, that you are extended the scope for the bounty program. I looked to the first resource - 
```
https://federation.data.gov/
```
I noticed, that the `x-amz-meta-s3cmd-attrs` response header returns sensitive information, like system username:
```
x-amz-meta-s3cmd-attrs:uid:0/gname:root/uname:root/gid:0/mode:33188/mtime:1482273904/atime:1482273904/md5:c9d60fd5a46044f

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

##Description
Hi. I just noticed, that you are extended the scope for the bounty program. I looked to the first resource - 
```
https://federation.data.gov/
```
I noticed, that the `x-amz-meta-s3cmd-attrs` response header returns sensitive information, like system username:
```
x-amz-meta-s3cmd-attrs:uid:0/gname:root/uname:root/gid:0/mode:33188/mtime:1482273904/atime:1482273904/md5:c9d60fd5a46044f7c58684a6c701ce54/ctime:1482273904
```
{F215241}

##Impact
The attacker can gain sensitive information about system username. In this case it was `root`, so i marked impact as `Low`. Still, the developers can have a good reason to not expose this information in the response header.

##Suggested fix
I found the related article, written by other researcher:
https://medium.com/@arbazhussain/username-disclose-at-s3-balsamiq-d98336d4012d
and issue in the s3cmd repository: https://github.com/s3tools/s3cmd/issues/67
where sugested fix is adding the `-- no-preserve` comand.

</details>

---
*Analysed by Claude on 2026-05-24*
