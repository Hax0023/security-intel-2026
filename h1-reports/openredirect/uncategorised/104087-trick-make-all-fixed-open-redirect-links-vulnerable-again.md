# Trick to Make All Fixed Open Redirect Links Vulnerable Again via SVG File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 104087 | https://hackerone.com/reports/104087
- **Submitted:** 2015-12-08
- **Reporter:** s1ck-sec
- **Program:** Slack
- **Bounty:** Unknown - Report #104087
- **Severity:** high
- **Vuln:** Open Redirect, SVG Code Execution, Insufficient Input Validation, Bypass of Previous Fix
- **CVEs:** None
- **Category:** uncategorised

## Summary
A previous open redirect vulnerability in Slack's checkcookie endpoint was patched to only redirect to slack.com or its subdomains. However, this vulnerability can be bypassed by uploading an SVG file containing JavaScript in the onload handler and using the SVG URL as the redirect parameter. When a user clicks the link, the SVG executes malicious code that redirects to an attacker-controlled domain.

## Attack scenario
1. Attacker creates malicious SVG file with onload event handler containing window.location redirect to attacker domain
2. Attacker uploads SVG file to Slack via file upload feature and generates public sharing link
3. Attacker crafts URL using Slack's checkcookie endpoint with redir parameter pointing to the uploaded SVG URL
4. Attacker sends phishing link to victim (e.g., via email or message)
5. Victim clicks the link and is redirected through Slack's checkcookie endpoint
6. SVG file loads in victim's browser and executes onload handler, redirecting to attacker's malicious domain

## Root cause
Slack's patch only validated the redirect destination domain but failed to address the root cause: improper handling of file upload URLs in redirect parameters. SVG files uploaded to files.slack.com are executed with embedded scripts rather than served as plain text, allowing script execution within the redirect chain.

## Attacker mindset
After discovering the previous fix only validates destination domains, attacker identifies that Slack's own file hosting domain (files.slack.com) is trusted and bypasses the redirect validation. By abusing SVG's onload event handler capability, attacker achieves the same phishing outcome through a different code path, demonstrating that input validation without addressing execution contexts is insufficient.

## Defensive takeaways
- Content-Type validation alone is insufficient - enforce Content-Disposition: attachment headers for user-uploaded files to prevent execution
- Whitelist redirect destinations at the parameter validation level, not just the final target domain
- Disable script execution in uploaded SVG files by serving with appropriate headers (Content-Security-Policy, X-Content-Type-Options: nosniff)
- Treat trusted internal domains (like files.slack.com) as potential attack vectors when they can host user-supplied content
- Implement defense-in-depth: validate redirects, sanitize file uploads, and control file execution contexts independently
- Review all similar endpoints for redirect vulnerabilities after patching one instance

## Variant hunting
Look for other file upload endpoints that generate public URLs and can be used in redirect chains
Test image formats (PNG, GIF, JPG) for metadata-based code execution or polyglot vectors
Check HTML file uploads for similar bypass potential with script tags or event handlers
Investigate data: URIs or blob: URIs as redirect parameters to execute inline code
Test other redirect endpoints beyond checkcookie for similar whitelist bypass vulnerabilities
Look for other Slack endpoints that accept URL parameters and pass them to client-side processing

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1598 - Phishing for Information

## Notes
This is a critical bypass of a previous security fix (Report #2622) that demonstrates insufficient patch depth. The vulnerability chain combines open redirect with arbitrary code execution through SVG onload handlers. The attacker leverages Slack's own infrastructure (files.slack.com) as a trusted source to bypass domain whitelist validation. This report exemplifies why security patches must address root causes rather than symptoms, and why file upload features require multiple layers of protection.

## Full report
<details><summary>Expand</summary>

this trick make all fixed open redirect links vulnerable again
in this resolved report "https://hackerone.com/reports/2622"
before fixing
this link "https://slack.com/checkcookie?redir=http://www.example.com" redirect victim to "http://www.example.com"

after fixing
this link "https://slack.com/checkcookie?redir=http://www.example.com" only redirect to "https://www.slack.com/" or "https://subdomain.slack.com/"

the trick
=
1- use slack account to upload .svg file contain this code
<code>
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<svg
 onload="window.location='http://www.example.com'"
 xmlns="http://www.w3.org/2000/svg">
</svg>
</code>

2-make public link for svg file "https://files.slack.com/files-pri/T0E7QLVLL-F0G41EG2W/redirect.svg?pub_secret=7a6caed489"

3- complete link "https://slack.com/checkcookie?redir=https://files.slack.com/files-pri/T0E7QLVLL-F0G41EG2W/redirect.svg?pub_secret=7a6caed489"

4-when user click this link will redirect to "http://www.example.com"

in this accepted and Bounty report "https://hackerone.com/reports/2622"
when user click this link "https://slack.com/checkcookie?redir=http://www.example.com" the result is redirect user to "http://www.example.com"
in my report it's the same result

you should stop execute svg files and display its's code like  HTML files

 

</details>

---
*Analysed by Claude on 2026-05-24*
