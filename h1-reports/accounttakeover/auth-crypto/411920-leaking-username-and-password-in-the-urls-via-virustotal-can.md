# Leaking Username and Password in the URLs via Virustotal, can leads to account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 411920 | https://hackerone.com/reports/411920
- **Submitted:** 2018-09-20
- **Reporter:** sumit7
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Information Exposure Through Sent Data
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi Dear @chaturbate team

**Vulnerability Type**
> Critical Information Leakage in URLs via Virustotal.

**Vulnerability Severity**
High. 

**Description**
During my regular testing, went to https://www.virustotal.com/#%2Fdomain%2Fchaturbate.com
After reviewing all URLs more and more, I got 2 Interesting and Critical Endpoints like this
1) https://chaturbate.com/accounts/autologin/?username=aman4a

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

Hi Dear @chaturbate team

**Vulnerability Type**
> Critical Information Leakage in URLs via Virustotal.

**Vulnerability Severity**
High. 

**Description**
During my regular testing, went to https://www.virustotal.com/#%2Fdomain%2Fchaturbate.com
After reviewing all URLs more and more, I got 2 Interesting and Critical Endpoints like this
1) https://chaturbate.com/accounts/autologin/?username=aman4aman&password=Sha1$f5b91$0d6c2c053145a088373344d6fa08e97ce31312c6&next=/accounts/stopemails/
2) https://chaturbate.com/accounts/autologin/?username=haydos1995&password=Sha1$b1d15$90623ee4d02216eb06947fea9770187dd1a1398c&next=/accounts/stopemails/
3) https://chaturbate.com/accounts/autologin/?username=haydos1995&password=Sha1$b1d15$90623ee4d02216eb06947fea9770187dd1a1398c&next=/b/haydos1995

Above URLs are leaking Sensitive Crediantals like Username and Password with Sha1. 
This Information helps attackers to get username and password by decryption of sha1.

Password always should be stripped from URLs.

## Impact

Account Takeover using username and decrypted password.

**Remediation**
> Remove Sensitive URLs before leaking username and password. Password should be not send in clear format in the urls. Critical Information like password should not send via URL without stripping.

Thank You.

Happy to Help.

Best Regards,
@smit

</details>

---
*Analysed by Claude on 2026-05-24*
