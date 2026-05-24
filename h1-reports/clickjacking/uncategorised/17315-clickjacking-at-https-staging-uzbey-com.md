# Clickjacking Vulnerability at staging.uzbey.com

## Metadata
- **Source:** HackerOne
- **Report:** 17315 | https://hackerone.com/reports/17315
- **Submitted:** 2014-06-23
- **Reporter:** vineet
- **Program:** Uzbey
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The staging.uzbey.com domain is vulnerable to clickjacking attacks due to the absence of X-Frame-Options and Content-Security-Policy headers that would prevent the site from being framed. An attacker can overlay the vulnerable site in a transparent iframe and trick users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious webpage hosting the vulnerable site in a transparent iframe with reduced opacity
2. Attacker overlays clickable elements (buttons, links) on top of the framed content to create a disguised UI
3. Victim visits the attacker's webpage believing they are interacting with legitimate content
4. Victim clicks on what appears to be benign elements but actually clicks hidden buttons from the framed site
5. Hidden actions execute on the vulnerable site in the victim's browser context with their session privileges
6. Attacker achieves unauthorized actions such as account modifications, fund transfers, or privilege escalation

## Root cause
The web application fails to implement HTTP security headers (X-Frame-Options or Content-Security-Policy frame-ancestors directive) to prevent embedding in iframes from untrusted origins.

## Attacker mindset
Attackers identify staging/development environments with lax security controls as low-hanging fruit for demonstrating vulnerability chains. The absence of clickjacking protections enables social engineering attacks to bypass user intent verification and execute state-changing operations.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all responses
- Add Content-Security-Policy header with frame-ancestors 'self' directive
- Disable iframe embedding entirely unless explicitly required for specific use cases
- Implement frame-busting JavaScript as a secondary defense layer
- Use SameSite cookie attribute to limit CSRF/clickjacking impact
- Apply security headers consistently across production, staging, and development environments
- Require user action confirmation with distinct interaction patterns for sensitive operations
- Conduct regular security scanning to detect missing protective headers

## Variant hunting
Check if other subdomains (api., admin., internal.) share the same vulnerability
Test for drag-and-drop clickjacking variants using HTML5 features
Attempt clickjacking on CSRF-protected endpoints to bypass token validation
Investigate if JSON responses can be rendered as HTML through MIME-type confusion
Test cursor-based attacks combining clickjacking with pointer events
Search for autocomplete-based clickjacking on form submissions

## MITRE ATT&CK
- T1190
- T1185
- T1566.002
- T1539

## Notes
Report demonstrates basic proof-of-concept for clickjacking. The staging environment designation suggests pre-production testing phase. This vulnerability typically has medium severity unless combined with CSRF vulnerabilities or sensitive operations. The reporter could have enhanced the report by identifying specific high-value actions vulnerable to clickjacking (e.g., account deletion, permission grants).

## Full report
<details><summary>Expand</summary>

hi, i found your site is vulnerable to clickjacking.
poc:    
<html><head>
<title>  testing </title>
<style>

frame {

opacity: 0.5;
border: none;
position: absolute;
top: 0px;
left: 0px;
z-index: 1000;
}
</style>
</head>
<body>
<script>
   window.onbeforeunload = function()
   {
      return " Do you want to leave ?";
   }
</script>
<p> site is vulnerable for Clickjacking! by Vineet bhardwaj</p>
<iframe id="frame" width="100%" height="100%" src="https://staging.uzbey.com/"></iframe>
</body>
</html>


please check the attachment ...



</details>

---
*Analysed by Claude on 2026-05-24*
