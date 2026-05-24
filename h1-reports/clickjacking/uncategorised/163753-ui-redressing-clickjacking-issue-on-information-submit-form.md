# UI Redressing (Clickjacking) on Beta Program Information Submission Form

## Metadata
- **Source:** HackerOne
- **Report:** 163753 | https://hackerone.com/reports/163753
- **Submitted:** 2016-08-27
- **Reporter:** khizer47
- **Program:** Legal Robot (via HackerOne)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The beta program information submission form lacks clickjacking protections, allowing an attacker to overlay the form in a transparent iframe and trick users into submitting personal information (name, email, company). The absence of X-Frame-Options or Content-Security-Policy headers enables this attack.

## Attack scenario
1. Attacker creates a malicious webpage with a transparent iframe embedding the target form
2. Attacker overlays attractive content (game, prize, survey) on top of the framed form to hide it from user view
3. Unsuspecting user clicks on the decoy content believing they are interacting with the visible page
4. User's click actually targets form fields in the hidden iframe beneath
5. User accidentally submits PII (name, email, company) to the attacker's controlled backend or logs
6. Attacker collects harvested information for phishing, spam, or social engineering campaigns

## Root cause
The application fails to implement anti-clickjacking headers (X-Frame-Options: DENY or SAMEORIGIN) or Content-Security-Policy frame-ancestors directive. The form accepts submissions without verifying the origin context, allowing cross-origin framing.

## Attacker mindset
An attacker seeks to harvest user personal information at scale through deception. By exploiting trust in the legitimate domain, they can conduct credential harvesting, build marketing lists, or perform targeted social engineering. Low effort, high reward reconnaissance attack.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN HTTP header on all pages containing forms
- Deploy Content-Security-Policy with frame-ancestors 'self' directive
- Add frame-busting JavaScript as defense-in-depth (though headers are primary)
- Implement SameSite cookie attribute to prevent session hijacking via clickjacking
- Validate form submission origin using Referer or Origin headers
- Educate users about phishing and clickjacking risks
- Consider implementing CSRF tokens and re-authentication for sensitive forms

## Variant hunting
Check for clickjacking protection on all authenticated forms (password reset, payment, account changes)
Test other subdomains and applications owned by Legal Robot for missing X-Frame-Options
Verify CSP headers don't use overly permissive frame-ancestors policies (e.g., * or data:)
Look for forms handling financial data, account credentials, or sensitive submissions
Test if JavaScript frame-busting can be bypassed using sandbox attributes or opener manipulation
Assess forms with high-value PII collection (SSN, banking details) for clickjacking risk

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1199

## Notes
This is a straightforward clickjacking vulnerability proof-of-concept with minimal technical sophistication but real business impact. The researcher demonstrates understanding of the attack mechanism with a clear HTML test case. The form's collection of PII (name, email, company) makes it an attractive target. Legal Robot should prioritize patching this on all web properties. The vulnerability is pre-authentication, increasing exposure surface.

## Full report
<details><summary>Expand</summary>

I found that There is a Form for Submitting User Information for applying for Beta Program. 
But this has NO Protection against Clickjacking Issue & also this form needs the following inputs that can b somewhat useful for an attacker.

#Information Like: 
Name: 
Email: 
Company 

Following is HTML code i used to test it!

<html>
	<--Clickjacking Test by KHizer--> 
	<style>
		iframe { 
		width: 800px; 
		height: 500px; 
		position: absolute; 
		top: 0; left: 0; 
		filter: alpha(opacity=50); 
		opacity: 0.5; 
		}  
	</style>
	<iframe src="https://www.legalrobot.com/">
</html>

Screen shots attached :D

Thanks,
KHIZER JAVED

</details>

---
*Analysed by Claude on 2026-05-24*
