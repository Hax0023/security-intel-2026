# DOM Based XSS in mycrypto.com via Unencoded Fragment Injection

## Metadata
- **Source:** HackerOne
- **Report:** 324303 | https://hackerone.com/reports/324303
- **Submitted:** 2018-03-10
- **Reporter:** bigshaq
- **Program:** MyCrypto (HackerOne #324303)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Cross-site Scripting (XSS) - DOM, HTML Injection, Content Spoofing, Phishing Vector
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in mycrypto.com where user-supplied input from URL fragments is rendered without sanitization. While AngularJS XSS protection blocks JavaScript execution via href/src attributes, attackers can inject arbitrary HTML to perform phishing, content spoofing, and clickjacking attacks.

## Attack scenario
1. Attacker crafts malicious URL with HTML payload in fragment: https://mycrypto.com/#send-transaction<div/class="header__wrap"><a/href=javascript:alert(0)>...</a></div>
2. Victim clicks attacker-supplied link or receives it via phishing email
3. Browser navigates to mycrypto.com and renders the fragment in the DOM
4. Application's JavaScript extracts fragment without sanitization and inserts into page output
5. Attacker's HTML injected into page DOM, potentially overlaying fake login forms or transaction screens
6. Victim interacts with spoofed content, potentially entering credentials or approving fake transactions

## Root cause
The application directly embeds URL fragment content into the DOM without HTML encoding. The code at line 4072 of mycrypto-master.js prints the 'connected successfully' message and related fragment content without sanitization, despite AngularJS protection existing for specific attributes (href/src). This protection doesn't cover general HTML injection vectors.

## Attacker mindset
Attacker identified that while JavaScript execution is blocked by Angular XSS protection, the underlying vulnerability remains exploitable for HTML/content injection. Recognizing that phishing and UI spoofing are viable attack paths even without code execution, the attacker demonstrated responsible disclosure by reporting despite JavaScript being filtered.

## Defensive takeaways
- Encode all user input, especially from URL fragments, before inserting into DOM using textContent or proper HTML encoding functions
- Never rely solely on attribute-level XSS protection; apply defense-in-depth with output encoding at insertion points
- Use DOMPurify or similar libraries for safe HTML sanitization if rich content must be rendered
- Implement Content Security Policy (CSP) headers to limit injection attack impact
- Validate and sanitize URL fragments on both client and server side
- Use framework features properly: AngularJS ng-bind vs ng-bind-html; prefer ng-bind for user input
- Implement input validation to reject unexpected fragment formats
- Regular security testing for DOM-based vulnerabilities distinct from reflected/stored XSS

## Variant hunting
Check other URL fragments (#send-transaction, #receive, etc.) for similar injection points
Test SVG/XML injection via DOM insertion for potential bypass of Angular protection
Investigate other client-side templating operations that may use unencoded fragments
Look for other attributes beyond href/src that Angular protection may miss (data-*, aria-*, event handlers via HTML)
Test for mutation XSS (mXSS) vectors that bypass sanitization during DOM manipulation
Examine if Angular protection can be bypassed through encoding variations or nested elements

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1204.001: User Execution - Malicious Link
- T1566.002: Phishing - Spearphishing Link
- T1608.005: Stage Capabilities - Deliver Exploit
- T1598.003: Gather Victim Information - Web 3.0 Credentials

## Notes
Report demonstrates good security research methodology by identifying that XSS vulnerability persists even when JavaScript execution is blocked. The attacker responsibly noted inability to achieve RCE but correctly identified phishing/spoofing risks. This is a classic example of defense bypass - Angular's targeted XSS protection on attributes missed the broader HTML injection vector. The vulnerability is particularly critical for cryptocurrency applications where UI spoofing could lead to financial loss through fake transaction approvals or credential theft.

## Full report
<details><summary>Expand</summary>

##Description & PoC
The "connected successfully" message is printed out without any output sanitation:
{F271357}
This is how it's being printed(this code snippet is taken from mycrypto-master.js, line 4072): 
{F271359}

An attacker can simply put his payload at the link and it'll be embedded within the page output:
```
https://mycrypto.com/#send-transaction<div/class="header__wrap"><a/href=javascript:alert(0)><h1>pwn3d</h1></a><img/src=//unskid.me/dist/jesus.gif></div>
```
{F271358}


##Notes
As you can see, I couldn't get any javascript running, that's because the application has an AngularJS XSS protection that goes through ALL the href\src\similiar attributes in the DOM and checks if it has a malicious content/XSS attempts with a tough regex(based on a whitelist). Couldn't bypass that.
Some screenshots of the "angular-XSS-blocker" from the chrome debugger :
{F271362}
{F271361}
Once it's triggered and see a malicious attempt(isImg==false), the malicious <a> tag:
```
<a href="javascript:alert(0)">click here</a>
```
turns into:
```
<a>click here</a>
```

## Impact

Although i did not get running javascript i still think that it's worth reporting because, well, still..anyone can inject other HTML code in that part of the application and it should be encoded. It can lead to other things like phishing/content spoofing/clickjacking.

The hacker selected the **Cross-site Scripting (XSS) - DOM** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://mycrypto.com/#here

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-12*
