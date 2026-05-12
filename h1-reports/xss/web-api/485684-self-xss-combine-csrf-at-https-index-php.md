# Stored XSS via CSRF-enabled Self XSS in index.php arg2 Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 485684 | https://hackerone.com/reports/485684
- **Submitted:** 2019-01-25
- **Reporter:** manshum12
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Lack of Input Validation, Missing CSRF Token
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability in the arg2 parameter of index.php was combined with the absence of CSRF token protection to create a reflected XSS attack. An attacker can craft a malicious HTML form that, when visited by a victim, executes arbitrary JavaScript in their browser without requiring user interaction beyond visiting the page.

## Attack scenario
1. Attacker identifies self-XSS in arg2 parameter requiring user interaction to exploit
2. Attacker discovers POST request lacks CSRF token validation on the vulnerable endpoint
3. Attacker crafts HTML file with hidden form containing XSS payload in arg2 parameter
4. Attacker distributes HTML file via email, messaging, or hosts on external website
5. Victim opens HTML file or clicks link in authenticated browser session
6. Browser auto-submits form via JavaScript, bypassing self-XSS requirement for manual parameter injection

## Root cause
Two compounding security flaws: (1) Insufficient input sanitization on arg2 parameter allowing JavaScript injection, (2) Absence of CSRF token validation enabling cross-origin form submission that bypasses the self-XSS constraint

## Attacker mindset
Bypass self-XSS limitation by leveraging CSRF to force authenticated victim to submit malicious payload. Convert low-impact self-XSS into high-impact reflected XSS affecting any user. Deliver via social engineering to execute session hijacking, credential theft, or malware distribution.

## Defensive takeaways
- Implement mandatory CSRF token validation on all state-changing POST/PUT/DELETE requests
- Apply strict input validation and HTML entity encoding on arg2 and all user-supplied parameters
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Implement output encoding using context-aware sanitization libraries
- Use SameSite cookie attribute (Strict/Lax) to mitigate CSRF attacks
- Perform security code review focusing on parameter handling in AJAX endpoints
- Implement Web Application Firewall rules to detect XSS payloads in requests

## Variant hunting
Test all AJAX endpoints (task=azrul_ajax) for similar CSRF+XSS combinations
Check other parameters (arg1, arg3, func values) for XSS vulnerabilities without CSRF protection
Audit all form submissions in community and related modules for CSRF token presence
Fuzz POST parameters with various encoding schemes (URL, HTML entity, Unicode) to bypass filters
Test other Joomla components for missing CSRF tokens in AJAX handlers
Search for similar patterns in register, login, and profile update functions

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1539

## Notes
Reporter successfully demonstrated PoC with auto-submitting form and history.pushState() to hide referrer. The vulnerability chain is critical because it converts a low-impact self-XSS into a weaponizable attack. The use of HTML entity encoding in payload obscures intent but does not prevent execution. Joomla-based application with custom AJAX handlers in community module. No indication of successful remediation or bounty amount provided in report.

## Full report
<details><summary>Expand</summary>

Hi Team,

I found that https://█████████/index.php has vulnerability by XSS in arg2 parameter. Anyway there is no csrf token tied with the post request. As a result this csrf flaw can make the self-xss as a global reflected xss.

CSRF to XSS PoC 

<html>
<body>
<script>history.pushState('', '', '/')</script>
<form action="https://██████████/index.php" method="POST">
<input type="hidden" name="█████████" value="1" />
<input type="hidden" name="task" value="azrul&#95;ajax" />
<input type="hidden" name="option" value="community" />
<input type="hidden" name="func" value="register&#44;ajaxCheckEmail" />
<input type="hidden" name="no&#95;html" value="1" />
<input type="hidden" name="arg2" value="&#91;&quot;&#95;d&#95;&quot;&#44;&quot;raygame2222&#37;40af&#46;miljvbi9&lt;img&#32;src&#61;a&#32;onerror&#61;alert&#40;1&#41;&gt;lk2ko&quot;&#93;" />
<input type="submit" value="Submit request" />
</form>
</body>
</html>

You just need to copy and paste the POC into notepad++ then open it with using firefox or google chrome . After i believe you can see xss window pop up

## Impact

i can using this CSRF file send it to people then wide variety of actions, such as performing arbitrary actions on the victim's behalf, and logging their keystrokes.

</details>

---
*Analysed by Claude on 2026-05-12*
