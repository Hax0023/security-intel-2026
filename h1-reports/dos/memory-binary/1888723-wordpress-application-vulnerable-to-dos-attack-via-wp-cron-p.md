# WordPress DoS via wp-cron.php Resource Exhaustion

## Metadata
- **Source:** HackerOne
- **Report:** 1888723 | https://hackerone.com/reports/1888723
- **Submitted:** 2023-02-28
- **Reporter:** 0r10nh4ck
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Unrestricted Resource Consumption
- **CVEs:** None
- **Category:** memory-binary

## Summary
The WordPress wp-cron.php script can be exploited to cause a Denial of Service by sending a large number of requests, exhausting server resources and rendering the application unavailable. An unauthenticated attacker can trigger excessive concurrent cron execution without rate limiting, leading to server overload and HTTP 502 errors.

## Attack scenario
1. Attacker identifies the target WordPress installation's wp-cron.php endpoint
2. Attacker uses a tool like doser.py to generate hundreds or thousands of rapid requests to wp-cron.php
3. Each request triggers WordPress to execute scheduled cron tasks and consume CPU/memory resources
4. Without rate limiting or request throttling, multiple concurrent cron processes accumulate and overwhelm the server
5. Server becomes resource-constrained, unable to process legitimate requests
6. Application becomes unresponsive, returning 502 Bad Gateway errors and causing service downtime

## Root cause
wp-cron.php is publicly accessible without authentication or rate limiting. WordPress executes cron tasks on every page load (if triggered), allowing attackers to force resource-intensive operations repeatedly. The default cron mechanism has no built-in protection against rapid concurrent requests.

## Attacker mindset
An attacker seeks to disrupt service availability with minimal effort. The wp-cron.php endpoint is a known WordPress component that is easily discoverable and requires no authentication. By automating requests, the attacker can overwhelm the target with minimal technical sophistication, making this an attractive low-skill attack vector.

## Defensive takeaways
- Disable DISABLE_WP_CRON in wp-config.php and replace with server-side cron jobs to prevent user-triggered execution
- Implement rate limiting and request throttling on wp-cron.php at the web server level (nginx/Apache)
- Restrict wp-cron.php access via IP whitelisting or loopback-only access if possible
- Monitor for unusual spikes in wp-cron.php requests and implement alerting
- Use a Web Application Firewall (WAF) to detect and block DoS patterns targeting wp-cron.php
- Configure proper resource limits (CPU, memory) at the application and OS level
- Implement load balancing and auto-scaling to handle traffic spikes
- Ensure WordPress and all plugins are updated to the latest versions

## Variant hunting
Check if other WordPress admin-related scripts are similarly vulnerable to resource exhaustion (wp-admin/admin-ajax.php, wp-json endpoints)
Test REST API endpoints for similar DoS vulnerabilities without authentication
Investigate whether plugin hooks/filters in wp-cron can be abused for additional resource consumption
Look for similar patterns in other PHP-based CMS platforms with scheduled task mechanisms
Test if wp-cron.php respects HTTP request limits or connection pooling protections

## MITRE ATT&CK
- T1498
- T1499
- T1190

## Notes
This is a classic resource exhaustion DoS attack exploiting an unauthenticated, publicly accessible endpoint. The vulnerability is not a code flaw but rather a design choice in WordPress that prioritizes convenience over security. The reported impact (502 errors, downtime) was validated with a proof-of-concept video. The mitigation steps are standard WordPress hardening practices. The redacted information suggests this was reported on a live target, indicating responsible disclosure was followed.

## Full report
<details><summary>Expand</summary>

**Description:**
Hi team,

The WordPress application is vulnerable to a Denial of Service (DoS) attack via the wp-cron.php script. This script is used by WordPress to perform scheduled tasks, such as publishing scheduled posts, checking for updates, and running plugins.

An attacker can exploit this vulnerability by sending a large number of requests to the wp-cron.php script, causing it to consume excessive resources and overload the server. This can lead to the application becoming unresponsive or crashing, potentially causing data loss and downtime.

I found this vulnerability at https://████████ endpoint.

## References

https://developer.wordpress.org/plugins/cron/

## Impact

A successful attack on this vulnerability can result in the following consequences:

    - Denial of Service (DoS) attacks, rendering the application unavailable.
    - Server overload and increased resource usage, leading to slow response times or application crashes.
   -  Potential data loss and downtime.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Get the doser.py script at https://github.com/Quitten/doser.py
2. Use this command to run the script:
```
python3 doser.py -t 999 -g 'https://█████/wp-cron.php'
```
3. Go to https://████ after 1000 requests of the doser.py script.
4. The site returns code 502.
5. See the video PoC.

## Suggested Mitigation/Remediation Actions
To mitigate this vulnerability, it is recommended to disable the default WordPress wp-cron.php script and set up a server-side cron job instead.
Here are the steps to disable the default wp-cron.php script and set up a server-side cron job:

   1.  Access your website's root directory via FTP or cPanel File Manager.
   2.  Locate the wp-config.php file and open it for editing.
   3.  Add the following line of code to the file, just before the line that says "That's all, stop editing! Happy publishing.":
```
define('DISABLE_WP_CRON', true);
```
   4.  Save the changes to the wp-config.php file.
   5. Set up a server-side cron job to run the wp-cron.php script at the desired interval. This can be done using the server's control panel or by editing the server's crontab file.



</details>

---
*Analysed by Claude on 2026-05-24*
