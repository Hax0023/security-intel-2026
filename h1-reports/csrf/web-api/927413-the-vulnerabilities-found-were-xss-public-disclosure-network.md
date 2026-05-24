#  The vulnerabilities found were XSS, Public disclosure, Network enumeration via CSRF, DLL hijacking.

## Metadata
- **Source:** HackerOne
- **Report:** 927413 | https://hackerone.com/reports/927413
- **Submitted:** 2020-07-19
- **Reporter:** b71728d7009b6664f0e2350
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Summary
IP found using ping command- 52.77.124.190 Then I used nmap tool to find the indepth information. I used burp suite and DNS scanner but it was not fruitful. Then I
explored some GitHub repositories to perform thorough web-application testing. Using
Aquatone I found some hidden domains. The results of Maltego tool and Aquatone
differed a lot. The vulnerabilities found were XSS, Public discl

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

Summary
IP found using ping command- 52.77.124.190 Then I used nmap tool to find the indepth information. I used burp suite and DNS scanner but it was not fruitful. Then I
explored some GitHub repositories to perform thorough web-application testing. Using
Aquatone I found some hidden domains. The results of Maltego tool and Aquatone
differed a lot. The vulnerabilities found were XSS, Public disclosure, Network
enumeration via CSRF, DLL hijacking.

**Platform(s) Affected:** Website

Details:
1. We found a domain which compiles on auth.zomato.com which is running 443
TCP as is well understood that 443 is for SSH and it is brute forcible on the IP
address
2. The next utility which I used is gitSploit. It is basically is used to find the
vulnerability and I found around 10 of them, the category varies from low to
critical.

## Impact

Information Disclosure, Server Can be Hijacked although it is not updated

</details>

---
*Analysed by Claude on 2026-05-24*
