# Resource Consumption Denial of Service via Beaker Session Cookie in Ubiquiti EdgeMax v1.10.6

## Metadata
- **Source:** HackerOne
- **Report:** 406614 | https://hackerone.com/reports/406614
- **Submitted:** 2018-09-06
- **Reporter:** grampae
- **Program:** Ubiquiti
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (Resource Exhaustion), Path Traversal/Full Path Disclosure, Improper Input Validation, Insufficient Rate Limiting
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Ubiquiti EdgeMax v1.10.6 web management portal is vulnerable to resource exhaustion attacks through the beaker.session.id cookie parameter. An attacker can flood the /var/run/beaker/container_file/ directory with cache files by sending requests with varying session IDs, eventually consuming all available disk space and causing the device to become unresponsive and requiring a hard power cycle to recover.

## Attack scenario
1. Attacker discovers target EdgeMax device running v1.10.6 via network scanning or Google dork queries
2. Attacker crafts HTTP requests with crafted beaker.session.id cookies (249 characters or less) to avoid error pages
3. Attacker sends multiple requests with unique session ID payloads using an automated script or tool
4. Each request causes Beaker session framework to create a new *.cache file in /var/run/beaker/container_file/
5. After approximately 50% of /run mount is consumed, web portal begins returning 500 errors and becomes unavailable
6. Once /run is full, /var/log fills with error messages; eventually device stops responding entirely and requires hard reset

## Root cause
The Beaker session management library creates persistent cache files for each unique session ID without proper validation, rate limiting, or disk space quota enforcement. The application fails to sanitize or validate session cookie length and uniqueness, allowing an attacker to create unlimited cache files. Additionally, no cleanup mechanism or disk space monitoring is implemented to prevent exhaustion attacks.

## Attacker mindset
Opportunistic network attacker seeking easy-to-execute denial of service against network infrastructure. The attacker recognizes that many default-configured EdgeMax devices are internet-facing and can be discovered via simple scanning. The low barrier to entry (basic HTTP requests, no authentication required) combined with severe impact (complete device failure requiring physical intervention) makes this an attractive attack vector for disruption campaigns or botnet-style resource consumption attacks.

## Defensive takeaways
- Implement strict rate limiting on all HTTP endpoints, especially those handling session-related requests
- Enforce maximum session cookie length and validate format before processing
- Implement disk quota and monitoring systems to prevent /var/run or /var/log from filling completely
- Add automatic cache file cleanup mechanisms with size/age-based retention policies
- Monitor and alert on unusual patterns of unique session creation
- Implement request throttling per source IP address for unauthenticated endpoints
- Deploy file descriptor and inode monitoring to detect rapid file creation attacks
- Sanitize error messages to prevent full path disclosure in error pages
- Consider using in-memory session storage with bounded caches instead of file-based storage
- Implement graceful degradation when disk space approaches capacity limits

## Variant hunting
Test other Ubiquiti EdgeOS products for identical Beaker session handling vulnerabilities
Investigate if other cookie parameters (beyond beaker.session.id) lack proper validation
Check for similar resource exhaustion vectors through other file creation mechanisms in the web portal
Test if other authentication bypass or session manipulation techniques exist in the same parameter
Examine if path traversal is possible within the session ID payload itself to write files to other directories
Investigate whether the vulnerability affects other Ubiquiti products using Beaker framework (Dream Machine, UDM, etc.)
Test if authenticated sessions are handled differently or have additional protections

## MITRE ATT&CK
- T1190
- T1499
- T1526
- T1566

## Notes
This is a pre-authentication denial of service requiring no credentials, making it a critical infrastructure risk. The attacker demonstrated pragmatic awareness of weaponization potential through Python automation and Google dorks for target discovery. The 5-minute timeline to complete DoS is particularly dangerous. The vulnerability chain reveals two separate issues: (1) input validation flaw allowing path disclosure on payloads >250 chars, and (2) resource exhaustion on valid payloads ≤249 chars. Recovery requires physical access/power cycling, escalating impact significantly. The report format suggests this was submitted to HackerOne's Ubiquiti program but bounty amount was redacted or not provided at time of report.

## Full report
<details><summary>Expand</summary>

Resource consumption Denial of service.

1: The request below shows that when you feed the beaker.session.id cookie variable a payload of 250 characters or more, the web management portal will produce an error page showing full path disclosure and more as shown in screenshots error1.png and error2.png.  

GET / HTTP/1.1
Host: 192.168.1.100
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: beaker.session.id=v8iG24fDKn8x5uD3V2uICZA1FJEoUJpqH5VTa03xB5blDRNOe5AfFp2GNIBpDX8th1IO8sS5ejsz4Swm175nUvipwU211S4n4RtCv0A6r18fsgJbrrbmhFT9k2cAXF3yyg0Uu0B0wPOWP7BOrMVnXp44aHoXSfJ06ZXk7HrD5J5R9AZIgQLmGutM9ESNxw3CVJtW4Rfxeh7JE2AD04B3g78FxRgBxY82I2Gzf6ZPMsc39d37LM90dd9cFA
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
-----------------------------------------------------------

2: When providing a valid length payload of 249 characters or less it will be stored as a *.cache filename in the /var/run/beaker/container_file/ directory,this can easily be turned in to a denial of service by filling up the space of the device with unique beaker.session.id requests.  The web portal will display either a 500 error as shown in DOS1.png or a python error screen as shown in DOS2.1.png and DOS2.2.png.  Typically the web portal will stop functioning after the /run mount has reached 50% by sending requests using iterations of 1-15681 as a beaker.session.id variable, however any length of payload can be used up to 249 characters.  This can be recovered from by deleting all files within the /var/run/beaker/container_file/ directory.


Although once the /run mount can not accept any more files /var/log will start to fill up with complaints about not being able to write to /var/run/beaker/container_file/, then after /var/log fills up the device will stop responding all together until it has been power cycled.  

3: I have created a video showing you how it is accomplished, I stopped the video at only 7% resources consumed on the /run mount as the video would be pretty long if we waited until the edgerouter went offline.  I am hoping this is enough for you to be able to reproduce this.  I am thinking that this could be fairly bad if made in to a python script along with google dorks and automation.  Or even a python script that someone has to only enter in an IP address and it will take the router offline in about 5 minutes or so until the router owner unplugs and plugs it back in.

## Impact

Any resources served by the edgemax device will be unavailable until the physical device has it's power cycled, then it should function as normal.  However it would be easy to just perform the attack again after it has been brought back online.

</details>

---
*Analysed by Claude on 2026-05-24*
