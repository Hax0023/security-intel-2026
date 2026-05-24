# Cross site scripting - XSRF Token

## Metadata
- **Source:** HackerOne
- **Report:** 858255 | https://hackerone.com/reports/858255
- **Submitted:** 2020-04-24
- **Reporter:** a9hora
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Please follow below mentioned steps for reproducing the vulnerability.
1. Open URL: https://nextcloud.com/enterprise/buy/
2. Fill up valid name and email address and put payload in other fields.
    
    Payload/s:
			<img src="x" onload=alert(document.cookie);>
			<svg/onload=alert(document.cookie);>	
3. Submit it
4. Open email address you mentioned in the email field.
5. Open up the email source

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

Please follow below mentioned steps for reproducing the vulnerability.
1. Open URL: https://nextcloud.com/enterprise/buy/
2. Fill up valid name and email address and put payload in other fields.
    
    Payload/s:
			<img src="x" onload=alert(document.cookie);>
			<svg/onload=alert(document.cookie);>	
3. Submit it
4. Open email address you mentioned in the email field.
5. Open up the email source.
6. You will be prompted with xsrf-token.

## Impact

As an attacker is getting the xsrf-token, he can utilize it in later attack such as, CSRF.

</details>

---
*Analysed by Claude on 2026-05-24*
