# ActiveStorage Exception with Whitespace Filenames Causing Application-Wide Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 713407 | https://hackerone.com/reports/713407
- **Submitted:** 2019-10-14
- **Reporter:** ninetynine
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Improper Input Validation, Exception Handling Flaw, File Handling Error
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can upload a profile picture with a specially crafted whitespace-based filename (such as '+', '%0d%0a', or '%20'), causing Rails ActiveStorage to throw an unhandled exception. This exception propagates across all pages displaying the profile picture, resulting in site-wide denial of service affecting multiple application sections.

## Attack scenario
1. Attacker authenticates to the platform and navigates to the profile picture upload feature
2. Attacker selects a legitimate image file to upload
3. Attacker intercepts the HTTP request and modifies the filename parameter to contain whitespace characters or URL-encoded whitespace ('%20', '%0d%0a') or special characters ('+')
4. Attacker forwards the modified request, causing the file to be stored with the malicious filename
5. When any user visits pages displaying the profile picture (profile page, hacktivity, programs, directory), ActiveStorage attempts to process the malformed filename and throws an exception
6. The unhandled exception causes HTTP 500 errors on multiple application pages, denying service to all users viewing content with the affected profile picture

## Root cause
Rails ActiveStorage lacks proper input validation and exception handling for filenames containing whitespace or special characters. The framework does not sanitize or validate filenames before storage, and when attempting to retrieve or process these files, it throws unhandled exceptions rather than gracefully degrading or rejecting invalid filenames during upload.

## Attacker mindset
The attacker discovered that file upload features often have weak input validation on metadata fields like filenames. By experimenting with special characters and whitespace, they identified that ActiveStorage fails to properly handle these edge cases. Recognizing that profile pictures appear across multiple pages, the attacker realized a single malicious upload could cascade into a widespread denial of service, maximizing impact with minimal effort.

## Defensive takeaways
- Implement strict filename validation at upload time, rejecting files with whitespace, control characters, or other special characters; normalize filenames to alphanumeric characters with hyphens/underscores
- Add comprehensive exception handling around file retrieval and processing to gracefully handle malformed filenames without exposing server errors to users
- Validate and sanitize all user-supplied input in file upload endpoints before persistence
- Implement rate limiting on file upload endpoints to prevent abuse
- Use generated filenames (UUIDs) instead of user-supplied names for storage, maintaining user-supplied names only in metadata
- Add monitoring and alerting for high rates of file serving errors that could indicate an attack
- Conduct security testing of file upload features with fuzzing techniques using special characters, whitespace, and encoding variations

## Variant hunting
Similar issues likely exist in other Ruby on Rails applications using ActiveStorage without proper filename validation. Other file upload features in the same application may have identical vulnerabilities if they accept user-supplied filenames. Applications handling file uploads from untrusted sources should be audited for improper whitespace and special character handling in filenames.

## MITRE ATT&CK
- T1499
- T1499.004
- T1190

## Notes
The report demonstrates a cascading failure pattern where a single malicious file upload affects multiple application pages. The attacker's use of URL encoding ('%20', '%0d%0a') suggests they were testing various encoding techniques to bypass validation. The impact is heightened because profile pictures are displayed across multiple high-traffic sections of the application. This type of vulnerability is particularly dangerous in community platforms where user-generated content appears ubiquitously.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi team, 
I've found an issue on the profile picture upload feature of your asset - https://hackerone.com, which can allow a malicious attacker to perform an application wide denial of service attack.
**Description:**
I was playing with the profile picture upload feature, then i observed that when we change the name of our profile picture to `+` , `%0d%0a` , or  `%20` and then refresh the profile page, it would give an internal server error. Then i observed the same behaviour at everyplace where my profile picture was being reflected for example the programs thanks section, hacktivity section or even the directory section. This leads to site wide Denial of Service that will deny all the users from performing any actions. 

### Steps To Reproduce

1. Login and visit edit profile page. 
2. Select a normal profile picture and click `Update Profile` button
3. Intercept this Request and change the filename to `+` by editing the request as shown in  ██████████
4. Turn off the intercept button and the refresh the update page.
5. Notice that it wont load. 
Now the similar behaviour can be observed at every place where your profile picture is shown.  

### Optional: Supporting Material/References (Screenshots)

 * █████

### Optional: Did you use [recon data made available by HackerOne](https://github.com/Hacker0x01/helpful-recon-data) to find this vulnerability?

no

## Impact

Application wide denial of service. The more places where the profile pictures are being shown, the higher the impact for example - hacktivity, program from page, thanks page, etc

</details>

---
*Analysed by Claude on 2026-05-24*
