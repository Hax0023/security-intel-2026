# SWFUpload Open Redirect and Site Defacement via URL-Encoding Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 209520 | https://hackerone.com/reports/209520
- **Submitted:** 2017-02-28
- **Reporter:** todayisnew
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Site Defacement, Parameter Injection, URL Encoding Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The swfupload.swf file used for file uploads accepts unvalidated query string parameters that can be exploited to redirect users to arbitrary sites or inject malicious content. An attacker can bypass the parameter filtering mechanism by using invalid URL encoding sequences (e.g., %x instead of valid hex codes), allowing injection of arbitrary flash objects or images to deface the website.

## Attack scenario
1. Attacker identifies that Nextcloud uses vulnerable swfupload.swf from WordPress wp-includes directory
2. Attacker discovers the flash file accepts query string parameters like buttonImageURL and debugEnabled
3. Attacker crafts a malicious URL using invalid hex encoding (e.g., debugEn%xabled instead of debugEnabled) to bypass the parameter blacklist filter
4. Attacker creates a link with injected buttonImageURL parameter pointing to attacker-controlled image or malicious SWF file
5. Victim clicks the malicious link, which loads swfupload.swf with injected parameters
6. Flash rendering displays attacker's image/content on Nextcloud domain, achieving redirect or defacement

## Root cause
The swfupload.swf parameter filtering mechanism attempts to block dangerous query parameters by checking if they exist in a blacklist and deleting them. However, the filter only checks for exact parameter names. By introducing invalid URL encoding sequences (%x is not valid hex since x is not 0-F), the flash parameter parser fails to normalize the parameter name, causing it to bypass the filter while still being readable by the Flash runtime through root.loaderInfo.parameters.

## Attacker mindset
An attacker would seek to abuse this vulnerability to perform credential theft phishing attacks by redirecting trusted users to fake login pages, distribute malware through injected SWF files, deface high-traffic websites for notoriety, or inject malicious images/content to damage brand reputation.

## Defensive takeaways
- Never rely on blacklist-based parameter filtering; use whitelist validation instead
- Properly normalize all user input before validation to handle encoding variations (URL encoding, HTML entities, unicode, etc.)
- Avoid using deprecated Flash technology; migrate to modern alternatives like HTML5 file upload APIs
- Implement Content Security Policy (CSP) headers to restrict inline script execution and resource loading
- Keep third-party libraries and components updated, especially security-critical components like file upload handlers
- Validate all parameters against a strict whitelist of allowed values, not just parameter names
- Use cryptographic signing or tokens for flash file configuration rather than query parameters
- Perform security code review of Flash files, especially those handling user input or redirects

## Variant hunting
Search for other instances of swfupload.swf across web properties; check for similar parameter filtering patterns in ActionScript code that may be vulnerable to encoding bypasses; investigate other Flash-based upload components for identical filter mechanisms; test other special characters and encoding schemes (%25 for %, %2e for .) that might bypass filters.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability predates modern browser security practices. The researcher responsibly disclosed the vulnerability and provided clear explanation of the encoding bypass mechanism. The core issue is that URL decoding happens at different stages: the HTTP layer decodes %xx sequences first, but Flash parameter parsing happens after, creating a gap where invalid sequences can slip through filters. This is a classic example of bypass through encoding normalization differences between validation and execution contexts.

## Full report
<details><summary>Expand</summary>


Good day, I truly hope it treats you well on your side of the screen :)

I have found that your website uses the flash file: swfupload.swf to allow your users to upload files.

The tl;dr version of this bug report is it allows an open redirect to any site a non kind person may want to exploit or website defacement with the option to put any image on your site to share with others.  If not greatly in scope I understand, just wanted to help you be more secure :)

The link in question is:

http://www.nextcloud.com/wp-includes/js/swfupload/swfupload.swf?debugEn%xabled=true&buttonImag%xeURL=https://████████/PugOfConcept/pugOfConcept.swf

Friendly url shorted version:

https://tinyurl.com/zduxnhz

I've already created a fancy animated gif of the exploit in action so you can click, watch, and hopefully see a cute POC surprise on video end.

https://www.dropbox.com/s/0343g6qgjdz1y1r/nextcloud.com_swf_upload_open_redirect_2_27_2017.gif?dl=0

Defacement Link

http://www.nextcloud.com/wp-includes/js/swfupload/swfupload.swf?debug%%Enabled=true&buttonTe%%xt=&buttonImag%%eURL=http://██████████/PugOfConcept/nopuppies.jpg


Full report details:

a) Why Open Redirects can be harmful for your users and your company:
   https://www.owasp.org/index.php/Top_10_2010-A10-Unvalidated_Redirects_and_Forwards

b) The source of the most recent version of swfupload.swf is here:
   https://github.com/WordPress/secure-swfupload

The bad news is the newest version is vulnerable to the exploit (I will be reporting it to wordpress to fix hopefully)

They strongly suggest updating to a newer move secure version:
http://www.plupload.com/


c) How the exploit works:

When you visit a swf, query string parameters (what appears after the ?) can be passed along in the request:

http://myawesomewebsite.com/wp-includes/js/swfupload/swfupload.swf?   <debugEn%xabled=true?&buttonImag%xeURL=https://█████/PugOfConcept/pugOfConcept.swf>
	
Flash reads in these variables via a special variable: root.loaderInfo.parameters

The intended solution is that they tried to filter out if query string parameters were passed along in the request by checking for them and if the were passed to delete them.
   
	for(key in params)
	{
			if(query.hasOwnProperty(Utils.trim(key)))
		{
			delete params[key];
		}
	}


The trick is that Flash will filter and non valid url encoded variables from a string, so %00-%FF are valid ascii encoded strings, a = %61 b = %62 etc
I tricked the system with the variable passed "?debugEnabled=true" normally would be filtered, but with debugEn%xabled=true, the %x is a non valid hex string :)  Since Hex counts from 0-F There is no valid %x.

May you be well on your side of the screen :)

-Eric

Also vulnerable:



</details>

---
*Analysed by Claude on 2026-05-24*
