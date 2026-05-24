# SSRF - pivoting in the private LAN

## Metadata
- **Source:** HackerOne
- **Report:** 1364797 | https://hackerone.com/reports/1364797
- **Submitted:** 2021-10-10
- **Reporter:** adrian_t
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** CVE-2021-22970
- **Category:** web-api

## Summary
The upload from remote servers features allows me to perform SSRF attack on the private LAN servers.

this features checks the following
* http response code needs to be 200 - easy, a non issue for attackers really
* checks the file exension   (can be bypassed with something like  http://192.168.1.148/index.php/test.png  - anything after index.php/  is ignorred and I control the file extension as 

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

The upload from remote servers features allows me to perform SSRF attack on the private LAN servers.

this features checks the following
* http response code needs to be 200 - easy, a non issue for attackers really
* checks the file exension   (can be bypassed with something like  http://192.168.1.148/index.php/test.png  - anything after index.php/  is ignorred and I control the file extension as well)
* some checks are performed on the IP, but any public and PRIVATE ips are allowed

I can read web  apps from the internal network, fingerprint them and exploit them (using GET only exploits).

This is how I've managed to read an phpinfo file from my local LAN:

http://192.168.1.157/info.php/test.html

The file is fetched, saved by the CMS locally (or S3) and then the output can be downloaded by the attacker as you can see in the attached screenshots.

ps: crayons

## Impact

An attacker can pivot in the private LAN and exploit local network apps.

</details>

---
*Analysed by Claude on 2026-05-24*
