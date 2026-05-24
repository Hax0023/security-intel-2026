# Clickjacking/URL Masking via HTML Link Spoofing in Brave Browser

## Metadata
- **Source:** HackerOne
- **Report:** 204198 | https://hackerone.com/reports/204198
- **Submitted:** 2017-02-07
- **Reporter:** dhiraj-mishra
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, URL Spoofing, Phishing
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Brave browser fails to properly validate or display the actual target URL of links, allowing attackers to create HTML pages where the visual URL indicator (shown on mouseover) differs from the actual navigation target. An attacker can craft malicious HTML files that trick users into clicking links they believe lead to legitimate sites (e.g., google.com) while actually redirecting to phishing or malicious destinations (e.g., datarift.blogspot.in).

## Attack scenario
1. Attacker creates a malicious HTML file (click.html) that contains a link with misleading visual properties
2. The HTML link is crafted so the browser's URL preview shows a legitimate domain (google.com) when user hovers over it
3. The actual href attribute or JavaScript redirect handler points to a different malicious domain (datarift.blogspot.in)
4. Victim visits the attacker's page via social engineering or phishing email
5. Victim sees the link pointing to google.com in the status bar and clicks it
6. Victim is redirected to the attacker's phishing site instead, where credentials or sensitive data can be harvested

## Root cause
The browser's URL preview mechanism does not properly validate or sanitize the displayed URL against the actual navigation target. The vulnerability likely stems from improper handling of HTML link attributes, JavaScript event handlers, or lack of verification between what is displayed in the status bar and the actual href destination.

## Attacker mindset
An attacker would exploit this to conduct large-scale phishing campaigns by creating seemingly legitimate links that actually redirect to credential harvesting pages, malware distribution sites, or other malicious infrastructure. The spoofing creates trust through visual deception, making users more likely to enter credentials or interact with the malicious page.

## Defensive takeaways
- Implement strict URL validation to ensure the displayed URL in the status bar matches the actual navigation target
- Sanitize and verify all href attributes and link targets before rendering URL previews
- Disable JavaScript-based URL manipulation techniques that allow href spoofing
- Add visual security indicators that highlight potential URL mismatches to users
- Consider implementing content security policies that restrict navigation hijacking
- Validate links through the DOM inspection process to detect discrepancies between displayed and actual URLs
- Educate users to verify complete URLs rather than relying on status bar indicators

## Variant hunting
Test other HTML attributes that control link behavior (data attributes, event handlers, fetch redirects)
Check JavaScript-based navigation methods (window.location, location.href) for spoofing possibilities
Test iframe-based clickjacking combined with URL masking
Investigate meta refresh tags and their URL display behavior
Test form-based redirects with hidden action attributes
Examine how the browser handles Unicode and homograph attacks in displayed URLs
Test redirect chains where intermediate pages show different URLs

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1199 - Trusted Relationship
- T1149 - Deobfuscation/Decoding

## Notes
The report includes a proof-of-concept HTML file and video demonstration. The vulnerability affects Brave browser version 0.13.2 running on Windows 6.1 with Chromium 54.0.2840.100. This is a UI/UX security issue that undermines user trust in the browser's security indicators. The attacker can easily distribute the malicious HTML through email, websites, or social engineering. The vulnerability is particularly dangerous because it exploits user reliance on the browser's visual security cues.

## Full report
<details><summary>Expand</summary>

I am able to reproduce the bug in :
Brave: 0.13.2 
rev: 25b1199fb6154b089cbad37926483239495b9800 
Muon: 2.0.19 
libchromiumcontent: 54.0.2840.100 
V8: 5.4.500.41 
Node.js: 7.0.0 
Update Channel: dev 
os.platform: win32 
os.release: 6.1.7601 
os.arch: x64

Steps to reproduce : 
1. Open click.html 
2. Then try to visit google.com 
OR 
http://hackies.in/click.html

Visually the browser says you(user) will be visiting google.com but it actually goes to 
datarift.blogspot.in 
An attacker may craft the link and may perform phishing attack or spoofing and etc.

Just do a mouseover on the link and see left bottom the URL says the browser will be visiting google.com but actually goes to datarift.blogspot.in 

In case if the repro doesn't works please perform the testcase 1 more time. 
Attaching the test case and the click.html file and Video POC for reference

</details>

---
*Analysed by Claude on 2026-05-24*
