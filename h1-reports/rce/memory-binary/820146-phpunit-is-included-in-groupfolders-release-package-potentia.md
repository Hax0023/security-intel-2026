# PHPUnit eval-stdin.php in Nextcloud groupfolders Release Package Enables RCE

## Metadata
- **Source:** HackerOne
- **Report:** 820146 | https://hackerone.com/reports/820146
- **Submitted:** 2020-03-16
- **Reporter:** ledfan
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Arbitrary Code Execution, Insecure Dependency, Unsafe File Inclusion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The groupfolders release tarball contains PHPUnit code in the vendor directory, including the dangerous eval-stdin.php file that evaluates PHP code from stdin. When accessible via web (in configurations without index.php rewriting), unauthenticated attackers can execute arbitrary PHP code via HTTP POST requests with FastCGI/CGI integration. Multiple Nextcloud apps (groupfolders, carnet, discoursesso, extract) are affected.

## Attack scenario
1. Attacker identifies Nextcloud installation with groupfolders app and discovers vendor directory is web-accessible due to missing URL rewriting
2. Attacker crafts HTTP POST request to eval-stdin.php endpoint without authentication
3. HTTP request body containing malicious PHP code is passed to server via standard input stream (php://stdin) when using FastCGI/CGI
4. eval-stdin.php evaluates the provided PHP code from stdin stream in server context
5. Attacker achieves remote code execution with web server privileges
6. Attacker can exfiltrate data, modify application behavior, or pivot to internal systems

## Root cause
PHPUnit testing framework was bundled in release tarballs as a development dependency, including eval-stdin.php utility. The vendor directory lacks adequate access controls via web server configuration, and eval-stdin.php's design to evaluate stdin input creates RCE risk when exposed to untrusted input via HTTP POST requests under CGI/FastCGI SAPI.

## Attacker mindset
Opportunistic reconnaissance targeting public Nextcloud installations. Attacker scans for accessible vendor directories and PHPUnit presence, tests for missing URL rewriting rules, then crafts POST payload to eval-stdin.php for immediate code execution without requiring authentication.

## Defensive takeaways
- Never include development/testing dependencies (PHPUnit, composer.phar, etc.) in production release packages
- Implement strict web server configuration to deny access to vendor/, .git/, and other non-public directories
- Use .htaccess or nginx config to prevent direct execution of PHP files in vendor directories
- Enforce URL rewriting (index.php) as default routing mechanism to prevent direct file access
- Conduct security audits of release packages before distribution
- Implement file-level access controls: mark eval-stdin.php and similar utilities as non-executable
- Use dependency manifests to distinguish development-only dependencies and exclude from releases
- Regularly scan releases for high-risk files from common frameworks

## Variant hunting
Search for other PHP packages bundling dangerous utilities: composer.phar in vendor/bin, phpstan bin files, infection.phar, Psalm binaries. Check other Nextcloud apps and extensions for same bundling pattern. Investigate if Laravel, Symfony, or WordPress plugins have similar vendor inclusion issues. Look for eval(), assert(), or create_function() accessible via web in any bundled testing frameworks.

## MITRE ATT&CK
- T1190
- T1505.003
- T1526
- T1083
- T1059.007

## Notes
Reporter acknowledged exploitation difficulty due to server configuration requirements (FastCGI/CGI required, not all PHP setups affected equally). However, vulnerability remains critical for affected configurations. Same vulnerability previously discovered in PrestaShop. Multiple Nextcloud apps confirmed affected, indicating systematic distribution issue. Exploitation does not require authentication when index.php rewriting is absent.

## Full report
<details><summary>Expand</summary>

The groupfolders tarball contains the phpunit code in the vendor directory (https://github.com/nextcloud/groupfolders/releases/download/v6.0.2/groupfolders.tar.gz) .
As discussed on https://thephp.cc/news/2020/02/phpunit-a-security-risk this really is a potential security risk.
The phpunit code contains a file called `eval-stdin.php` which evaluates the contents of `php://stdin`.
Note that the same issue was discovered in PrestaShop which according to thephp.cc claims:

```
I was contacted by the vendor of PrestaShop, an Open Source E-Commerce software, on January 6, 2020. They informed me that eval-stdin.php can be exploited for remote code execution when PHPUnit is publicly available on the web server and FastCGI is used to integrate PHP with that web server.
```

I was not able to exploit this using different FastCGI configurations. However, again according to phpcc:

```
An HTTP post payload can only be accessed via the php://stdin stream if PHP is used by the web server via CGI or FastCGI. I was not sure if php://stdin really behaves like this, so I reached out to PHP core developers. Joe Watkins and Christoph M. Becker were able to confirm that php://stdin behaves like this and that its implementation is based on the specifications for CGI and FastCGI, which mandate access to the request payload via the standard input stream.
```

If the Nextcloud is configured so that the url still contains `index.php` I was able to access the `eval-stdin.php` file without authentication.
Note that the following apps also include the phpunit package:
 - https://apps.nextcloud.com/apps/carnet
 - https://apps.nextcloud.com/apps/discoursesso
 - https://apps.nextcloud.com/apps/extract

## Impact

According to the PHP core developers and PrestaShop the `eval-stdin.php` makes it possible to perform RCE.
My research shows that in at least certain circumstances (i.e., index.php is not rewritten) the `eval-stdin.php` file is accessible.

</details>

---
*Analysed by Claude on 2026-05-12*
