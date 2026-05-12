# Potential RCE and XSS via File Upload with Known Data Directory Path

## Metadata
- **Source:** HackerOne
- **Report:** 678727 | https://hackerone.com/reports/678727
- **Submitted:** 2019-08-21
- **Reporter:** rcejules
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Remote Code Execution, Cross-Site Scripting, Arbitrary File Upload, Path Traversal, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Nextcloud allows authenticated users to upload PHP files which can be executed by directly accessing them via a predictable path when the data directory is located within the web root. An attacker with a user account and knowledge of the username can upload malicious PHP scripts and execute arbitrary code by navigating to /data/username/files/shell.php.

## Attack scenario
1. Attacker creates or obtains a valid Nextcloud user account (e.g., username 'attacker')
2. Attacker determines or guesses the data directory path (default: /var/www/nextcloud/data) and username structure
3. Attacker uploads a malicious PHP script (e.g., shell.php) through the Nextcloud file upload interface
4. Attacker constructs direct URL to the uploaded script: https://nextcloud.domain.com/data/attacker/files/shell.php
5. Attacker accesses the URL directly, bypassing Nextcloud's file viewing restrictions and triggering PHP execution
6. Arbitrary PHP code executes with web server privileges, allowing command execution, data exfiltration, or server compromise

## Root cause
Nextcloud places user data in a predictable directory structure within the web-accessible root and does not prevent direct HTTP access to uploaded PHP files. The default configuration example suggests placing data at /var/www/nextcloud/data, and username-based folder names are predictable, allowing attackers to construct valid URLs to execute uploaded scripts.

## Attacker mindset
An authenticated attacker with basic account creation privileges can leverage weak assumptions about directory structure and naming conventions to achieve code execution. The attacker assumes standard default configurations are used and that username information is public or easily guessable, eliminating the need for directory enumeration.

## Defensive takeaways
- Never store web-accessible data directories within the web root; use paths outside document root (e.g., /var/lib/nextcloud/data or /opt/nextcloud/data)
- Implement unpredictable user folder naming by appending cryptographic seeds or UUIDs to usernames
- Disable PHP execution in user data directories via .htaccess rules (deny php execution) or web server configuration
- Validate and restrict file uploads to safe extensions; reject executable file types like .php, .phtml, .php3, .php4, .php5
- Serve uploaded files with Content-Disposition: attachment headers to force downloads instead of execution
- Implement strict access controls ensuring uploaded files cannot be accessed via direct HTTP requests
- Use Content Security Policy headers to prevent inline script execution
- Regularly audit configuration examples to ensure they don't enable insecure defaults

## Variant hunting
Search for similar misconfigurations in other file sharing platforms (Pydio, ownCloud, Seafile). Look for setups where user-uploaded content is within web-accessible directories without execution restrictions. Test instances using default installations and common directory structures like /data/, /uploads/, /files/. Check for other executable extensions (.phtml, .php3, .php4, .php5, .pht, .phps) that might bypass filters.

## MITRE ATT&CK
- T1190
- T1434
- T1083
- T1078
- T1505
- T1059
- T1105

## Notes
Report demonstrates a classic configuration vulnerability rather than a code flaw. The vulnerability requires three conditions: valid user account, default/predictable data directory path, and data directory within web root. Many organizations deploying Nextcloud likely follow the sample configuration provided in official documentation, making this practical to exploit. The vulnerability is mitigated by proper system configuration rather than application-level fixes alone. XSS variant mentioned (HTML file upload) would have similar impact if served with executable MIME types.

## Full report
<details><summary>Expand</summary>

#potential RCE and XSS via file upload requiring user account and default settings

##Requirements
1. User account that can upload files (NO admin)
2. User account name on creation (usually the same as on creation/displayed name)
3. data directory inside of nextcloud server folder (suggested by /var/www/nextcloud/config/config.sample.php)

##Tested on
current release
Version 16.0.4.1
stable
Build: '2019-08-14T18:57:27+00:00 a1a245e88202d834f08f4c2e4451dcbe9baee3aa'

##Basic idea
On nextcloud php files can be uploaded, but when clicked they are only shown in a text editor. If the URL to our skript is known, we get code execution. 
A RCE will work if the server has set it's data directory inside the nextcloud server folder and the username is known. 

##config example
The following is located in /var/www/nextcloud/config/config.sample.php:
[https://github.com/nextcloud/server/blob/master/config/config.sample.php]
~~~~
 *
 * Default to ``data/`` in the Nextcloud directory.
 */
'datadirectory' => '/var/www/nextcloud/data',
~~~~
If this config is used, RCE is possible.

##Attack scenario: 
Short video attached.
(To reproduce use a nextcloud instance and setup a user named attacker. Use any php script called shell.php, and set the datadirectory to /var/www/nextcloud/data)

1. Login to obtained user account (assume his name is "attacker")
2. upload malicious php script. (assume it is called "shell.php")
3. navigate to https://www.ournextclouddomain.com/data/attacker/files/shell.php
4. see some shells poppin

This is possible since we know the direct path to our php script.

Note: This can also be used for XSS since we can upload any html file!

##Prevention
1. user accounts could extend a seed on their foldername like attacker-19320143158015
2. usage of a custom seed inside the data directory.
3. different config than on the example

## Impact

RCE, extract ser data or modify config file (if no special permissions are set), take over the server, also XSS is possible

</details>

---
*Analysed by Claude on 2026-05-12*
