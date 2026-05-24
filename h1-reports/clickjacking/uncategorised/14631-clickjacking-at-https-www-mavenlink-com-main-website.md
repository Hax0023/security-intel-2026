# Clickjacking Vulnerability at mavenlink.com Main Website

## Metadata
- **Source:** HackerOne
- **Report:** 14631 | https://hackerone.com/reports/14631
- **Submitted:** 2014-06-03
- **Reporter:** vineet
- **Program:** Mavenlink
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The main Mavenlink website lacks X-Frame-Options headers, allowing the site to be framed within attacker-controlled pages. An attacker can overlay transparent iframes to trick users into performing unintended actions on the vulnerable domain through clickjacking attacks.

## Attack scenario
1. Attacker creates a malicious webpage with an invisible iframe pointing to mavenlink.com
2. Attacker overlays interactive elements (buttons, links) on the framed content with reduced opacity or transparency
3. User visits the attacker's webpage believing they are interacting with legitimate content
4. User clicks on what appears to be a benign button, but actually clicks on hidden Mavenlink elements
5. Without user knowledge, actions are performed on the victim's Mavenlink account (fund transfers, profile changes, etc.)
6. Attack succeeds if user is authenticated to Mavenlink in another browser tab

## Root cause
Missing or misconfigured X-Frame-Options HTTP security header and absence of Content-Security-Policy frame-ancestors directive. The server does not prevent its pages from being embedded in frames controlled by other origins.

## Attacker mindset
Low-effort reconnaissance and exploitation. Researcher identified a straightforward framing vulnerability with proof-of-concept code. The attacker sees an opportunity to manipulate authenticated users into performing sensitive actions without their explicit awareness.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN value on all sensitive pages
- Deploy Content-Security-Policy header with frame-ancestors directive to restrict framing
- Implement frame-busting JavaScript as secondary defense (though not foolproof)
- Use SameSite cookie attributes to mitigate CSRF risks in framing scenarios
- Apply user interaction confirmation for sensitive operations
- Regularly audit HTTP security headers across all application domains

## Variant hunting
Search for other Mavenlink subdomains lacking X-Frame-Options headers. Identify related applications, partner portals, or legacy domains under Mavenlink's control. Test authentication flows, payment processing pages, and administrative dashboards for similar framing vulnerabilities. Check for inconsistent header implementation across different URI paths.

## MITRE ATT&CK
- T1187
- T1598

## Notes
This is a straightforward clickjacking PoC with minimal effort exploitation. The researcher notes this is a duplicate finding on a different domain from a previous submission. The vulnerability is easily exploitable against authenticated users but requires successful social engineering to lure victims to the attacker's malicious page. The PoC uses opacity and onbeforeunload techniques typical of clickjacking attacks.

## Full report
<details><summary>Expand</summary>

Hello , i found clickjacking on main webpage.
<html><head>
<title> CSRF testing </title>
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
<p> site is vulnerable for clickjacking! by Vineet bhardwaj</p>
<iframe id="frame" width="100%" height="100%" src="https://www.mavenlink.com/"></iframe>
</body>
</html>


same as last bug but its on other domain.... and its valid too 
waiting for positive response....
thanks 


</details>

---
*Analysed by Claude on 2026-05-24*
