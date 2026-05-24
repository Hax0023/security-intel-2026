# Stored XSS / Bypassing .htaccess protection in http://nodebb.ubnt.com/

## Metadata
- **Source:** HackerOne
- **Report:** 202354 | https://hackerone.com/reports/202354
- **Submitted:** 2017-01-31
- **Reporter:** inhibitor181
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

While I was looking at your renewn SSL certificated, I have noticed the following link : http://nodebb.ubnt.com/

I have seen that this link was protected by htaccess password, but I have decided to run a nmap scan. By running the following :

```
sudo nmap -sSV -p- 104.131.159.88 -oA stage_ph -T4
```

one of the open ports was this : `4567/tcp open   tram?`

And, to my surprise the ip `10

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

Hello,

While I was looking at your renewn SSL certificated, I have noticed the following link : http://nodebb.ubnt.com/

I have seen that this link was protected by htaccess password, but I have decided to run a nmap scan. By running the following :

```
sudo nmap -sSV -p- 104.131.159.88 -oA stage_ph -T4
```

one of the open ports was this : `4567/tcp open   tram?`

And, to my surprise the ip `104.131.159.88:4567`, as well as `http://nodebb.ubnt.com:4567/` were available from internet and unprotected.

Here, I have found a nodeBB instance and I have managed to create a persisted XSS by using the  upload API, that does not properly sanitize the file names and automatically sets wrong mime types. 

Normally, it seems that the user is allowed to upload only images, but the stored XSS was possible by injecting malicious html in the exif data and changing the file name to .html.

I have attached a video with the POC, as well as the exif image.

I have not managed to RCE, but it is also worth noting that uploading the file with the .php extension and writing php content using exif IS possible.



</details>

---
*Analysed by Claude on 2026-05-24*
