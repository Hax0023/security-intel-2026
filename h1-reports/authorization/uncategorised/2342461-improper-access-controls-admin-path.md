# Improper Access Controls - Admin Path Disclosure via HTML Inspection

## Metadata
- **Source:** HackerOne
- **Report:** 2342461 | https://hackerone.com/reports/2342461
- **Submitted:** 2024-02-01
- **Reporter:** aliyueka
- **Program:** MTN Nigeria (nin.mtn.ng)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal, Improper Access Control, Client-Side Information Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An admin path (../wp-admin/admin-ajax.html) was discovered exposed in HTML source code accessible through browser developer tools on the nin.mtn.ng website. This information disclosure reveals the application's internal directory structure and WordPress backend path. While the path itself is visible only to authenticated users with developer console access, it indicates improper handling of sensitive path information.

## Attack scenario
1. Attacker visits https://nin.mtn.ng/ website
2. Attacker clicks on 'Check your NIN Link Status' button
3. Attacker opens browser developer tools (Inspect Element)
4. Attacker discovers admin path ../wp-admin/admin-ajax.html in HTML source
5. Attacker maps application architecture and identifies WordPress installation
6. Attacker enumerates WordPress-specific vulnerabilities or attempts unauthorized admin access

## Root cause
The admin path is hardcoded or embedded in HTML source code without proper obfuscation or server-side routing abstraction. WordPress admin paths should not be exposed in client-side code; instead, relative URLs or abstracted endpoints should be used.

## Attacker mindset
Reconnaissance and reconnaissance. The attacker is performing initial information gathering to identify the technology stack (WordPress), directory structure, and potential entry points for further exploitation. Path disclosure enables targeting of known WordPress vulnerabilities.

## Defensive takeaways
- Never expose internal paths or admin endpoints in client-side HTML/JavaScript
- Use abstracted API endpoints instead of direct filesystem paths
- Implement server-side routing that masks internal directory structure
- Remove or obfuscate WordPress-specific paths and headers
- Apply HTTP security headers to prevent information disclosure
- Conduct regular source code reviews for sensitive information exposure
- Use Content Security Policy (CSP) headers
- Disable directory listing and WordPress version disclosure

## Variant hunting
Search for other hardcoded paths in HTML/CSS/JavaScript source
Check for exposed wp-config.php, .env, or configuration files
Scan for commented-out admin paths or development endpoints
Look for similar information disclosure in other MTN domain pages
Enumerate other WordPress-specific files (wp-json, xmlrpc.php, wp-login.php)
Check for path traversal attempts using discovered admin path
Search for exposed API keys or credentials in source code

## MITRE ATT&CK
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1592.001 - Gather Victim Host Information: Hardware
- T1526 - Scan Infrastructure
- T1589.002 - Gather Victim Identity Information: Credentials

## Notes
While the severity is medium due to being client-side information only, the exposure of WordPress admin paths combined with public access creates risk. The claim about stealing customer details, installing backdoors, and altering systems is speculative and depends on additional vulnerabilities in the WordPress installation or authentication mechanisms. The report lacks technical depth regarding actual exploitation impact. The path appears to be a static reference rather than an active attack vector, but it serves as valuable reconnaissance information for threat actors targeting this application.

## Full report
<details><summary>Expand</summary>

## Summary:
Go to https://nin.mtn.ng/ then click on "Check your NIN Link Status" then right click and click on "Inpect" and admin path is display at  web browser ../wp-admin/admin-ajax.html

## Steps To Reproduce:
STEP 1:
Go to https://nin.mtn.ng/
{F3021640}

STEP 2:
Click on "Check your NIN Link Status" 
{F3021641}

STEP 3:
Right click at the top of the page(On MTN Yellow Bar) and  then click on "Inspect"
{F3021642}
../wp-admin/admin-ajax.html
Admin Path

## Impact

1.) View Sensitive Information
2.) Steal Customers details
3.) Install backdoor
4.) Access different Components
5.) Alter System

</details>

---
*Analysed by Claude on 2026-05-24*
