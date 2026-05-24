# Potential RCE and XSS via File Upload with Predictable Path and Default Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 678727 | https://hackerone.com/reports/678727
- **Submitted:** 2019-08-21
- **Reporter:** rcejules
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Arbitrary File Upload, Remote Code Execution (RCE), Cross-Site Scripting (XSS), Path Traversal, Insufficient Access Controls
- **CVEs:** None
- **Category:** web-api

## Summary
Nextcloud allows authenticated users to upload PHP files that can be executed directly if the data directory is configured to the default location within the webroot and the username is known. An attacker with a user account can upload a malicious PHP script and access it via a predictable URL path, leading to remote code execution or XSS via HTML uploads.

## Attack scenario
1. Attacker creates or compromises a low-privilege Nextcloud user account (e.g., 'attacker')
2. Attacker uploads a malicious PHP script (e.g., 'shell.php') to their Files folder via the Nextcloud web interface
3. Attacker determines the predictable file path based on the default data directory configuration (/var/www/nextcloud/data/attacker/files/shell.php)
4. Attacker navigates directly to the uploaded PHP file URL via the web browser
5. Web server executes the PHP script in the webroot, granting the attacker arbitrary code execution
6. Attacker can modify config files, extract user data, pivot to other accounts, or upload HTML files for XSS attacks

## Root cause
The vulnerability stems from multiple misconfigurations: (1) default data directory located within the webroot instead of outside it, (2) predictable username-based folder structure in the data directory, (3) PHP files are directly executable when accessed via HTTP, and (4) insufficient file type restrictions or execution prevention mechanisms

## Attacker mindset
An attacker with basic system knowledge would recognize that default configurations are commonly used and that usernames are often publicly visible or easily guessable. By combining weak file upload controls with path predictability, the attacker can achieve code execution without admin access, making this a valuable exploitation vector for lateral movement or initial persistence.

## Defensive takeaways
- Configure the data directory outside the webroot or in a non-executable directory
- Implement randomized folder naming schemes (e.g., append random seeds or UUIDs) for user data directories
- Disable PHP execution in the data directory via .htaccess, nginx config, or web server rules
- Implement strict file type validation and whitelist allowed upload extensions
- Store uploaded files with randomized names disconnected from original filenames
- Use Content-Disposition: attachment headers to force download instead of browser execution
- Implement proper access controls ensuring data directories are not web-accessible
- Regularly audit default configurations and provide secure-by-default settings
- Monitor for suspicious file upload patterns or access to uploaded files

## Variant hunting
Search for similar issues in other file storage/collaboration platforms (Seafile, OwnCloud, Pydio) where user directories may be web-accessible. Check for other Nextcloud upload handlers that may bypass restrictions. Investigate whether other file types (.phtml, .php5, .phar) bypass the PHP execution model. Look for misconfigured reverse proxies or CDNs that serve user-uploaded content without proper headers.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1434 - External Remote Services
- T1200 - Traffic Signaling
- T1652 - User Execution
- T1583 - Acquire Infrastructure

## Notes
This vulnerability requires specific conditions: (1) user account access, (2) knowledge of username, and (3) non-standard but recommended default configuration. The report indicates this affects Nextcloud 16.0.4.1. The vulnerability is mitigated if the data directory is properly configured outside the webroot, which some deployments may already do. The XSS variant via HTML file upload is also notable as it affects confidentiality and could be used for session hijacking.

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
*Analysed by Claude on 2026-05-24*
