# IDOR on DoD Website exposes FTP users and passes linked to all accounts!

## Metadata
- **Source:** HackerOne
- **Report:** 228383 | https://hackerone.com/reports/228383
- **Submitted:** 2017-05-14
- **Reporter:** cdl
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
https://████/██████/ is vulnerable to Insecure Direct Object Reference. The application does not validate whether or not who a Push Server belongs to thus allowing an attacker to view the credentials of any FTP / sFTP server linked to any user's account. 

## Impact
An attacker can view anybody's FTP server information, thus **compromising** the user's FTP servers. This also allow

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

**Description:**
https://████/██████/ is vulnerable to Insecure Direct Object Reference. The application does not validate whether or not who a Push Server belongs to thus allowing an attacker to view the credentials of any FTP / sFTP server linked to any user's account. 

## Impact
An attacker can view anybody's FTP server information, thus **compromising** the user's FTP servers. This also allows an attacker to **update** or **edit** the Push Server in the ██████████ CMS.

## Step-by-step Reproduction Instructions
1. Log into or create an account on `https://██████████/██████████`
2. Now visit `https://████████/█████/filepush/ftp/303/` 

You will be able to see my ftp server details and you will be able to update or delete it!

An attacker can bruteforce the id to see if the server gives back a valid response. The attacker can then log into the person's FTP servers with the credentials stolen using this vulnerability, giving them full access to private / confidential information!

Example: `https://██████████/█████████/filepush/ftp/1/`

Hostname: ██████
Username: ██████
Password: █████
Path: /from_pub/cr/████████

`https://█████████/████/filepush/ftp/<ID>/`

## Suggested Mitigation/Remediation Actions
Check whether or the user's account should have access to the specified Push Server

</details>

---
*Analysed by Claude on 2026-05-24*
