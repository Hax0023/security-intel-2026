# Remote Code Execution in the Import Channel function

## Metadata
- **Source:** HackerOne
- **Report:** 236607 | https://hackerone.com/reports/236607
- **Submitted:** 2017-06-05
- **Reporter:** strukt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** businesslogic
- **CVEs:** None
- **Category:** memory-binary

## Summary
Hello,

Administrators are allow to import channels by visiting http://HOST/PATH_TO_EE/admin.php?/cp/channels/sets and uploading .zip archives that contain the information about the channels to be imported. The archives are then extracted into temporary directories, which are kept in the `/system/user/cache/cset/` directory. The problem is that, if the archive doesn't have all the required files f

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

Administrators are allow to import channels by visiting http://HOST/PATH_TO_EE/admin.php?/cp/channels/sets and uploading .zip archives that contain the information about the channels to be imported. The archives are then extracted into temporary directories, which are kept in the `/system/user/cache/cset/` directory. The problem is that, if the archive doesn't have all the required files for the import to be successful, the extracted files remain in their folders and an error is thrown to the administrator stating that a file doesn't exist in the archive.

This allows an administrator to upload .php scripts to the server, which is not allowed by default in ExpressionEngine as far as I can see.

###Steps to reproduce:
1- Download the attached .zip archive and browse to http://HOST/PATH_TO_EE/admin.php?/cp/channels/sets
2- Try to upload the zip file you just downloaded as the imported channel
3- Navigate to http://HOST/PATH_TO_EE/system/user/cache/cset/, which will show a directory listing of all the temporary directories, this is a problem by itself
4- If this is your first time trying this, you should find a single directory, click the directory's name and then click the test.php file and edit the URL in the address bar by adding "?cmd=whoami" to the URL
5- Notice that the command has executed and that the information is returned in the page

Regards,

</details>

---
*Analysed by Claude on 2026-05-24*
