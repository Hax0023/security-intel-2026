# Clickjacking on authorized page https://wakatime.com/share/embed

## Metadata
- **Source:** HackerOne
- **Report:** 244967 | https://hackerone.com/reports/244967
- **Submitted:** 2017-07-01
- **Reporter:** silv3rpoision
- **Program:** WakaTime (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /share/embed endpoint on wakatime.com lacks X-Frame-Options header protection, allowing attackers to embed the page in an iframe and perform clickjacking attacks. The vulnerability specifically impacts authenticated users who may inadvertently perform unintended actions through UI redressing techniques on the Dashboard.

## Attack scenario
1. Attacker identifies that https://wakatime.com/share/embed lacks X-Frame-Options header
2. Attacker creates a malicious HTML page containing an invisible iframe pointing to the vulnerable endpoint
3. Attacker tricks authenticated WakaTime users into visiting the malicious page (via phishing, social engineering, etc.)
4. Attacker overlays legitimate-looking UI elements (buttons, links) on top of the invisible iframe
5. User clicks on attacker's decoy UI element, but the click actually targets the embedded WakaTime page
6. Unintended actions are performed on the authenticated WakaTime account (e.g., modifying settings, sharing data, or triggering other sensitive operations)

## Root cause
The application fails to implement the X-Frame-Options security header on the /share/embed endpoint, allowing the page to be framed by external domains. This absence of framing protection, combined with the endpoint being accessible to authenticated users, creates a clickjacking vulnerability.

## Attacker mindset
The attacker exploits a common misconfiguration in web applications where developers forget to implement framing protections. By targeting authenticated users, the attacker gains access to authenticated contexts without requiring credential theft, leveraging user trust in legitimate page layouts.

## Defensive takeaways
- Implement X-Frame-Options: DENY header on all sensitive endpoints, especially authenticated pages
- Use Content-Security-Policy frame-ancestors directive as a modern alternative/complement to X-Frame-Options
- Apply consistent security headers across all endpoints and review them during development
- Test all pages for clickjacking vulnerabilities using browser DevTools or automated security scanners
- Implement additional CSRF protections and user interaction confirmations for sensitive operations
- Consider SameSite cookie attributes to limit cross-site request contexts
- Regularly audit endpoints that handle user data or allow state changes

## Variant hunting
Search for other endpoints lacking X-Frame-Options headers, particularly: share/*, embed/* endpoints, dashboard pages, settings pages, API authentication pages, and any page handling sensitive user operations. Check for inconsistent header implementation across subdomains and test POST/DELETE endpoints for clickjacking vulnerability.

## MITRE ATT&CK
- T1185
- T1583.001
- T1589.002

## Notes
This is a straightforward clickjacking vulnerability report. The researcher correctly identified the missing security header and provided clear remediation steps. However, the report lacks specificity about actual impact (no proof of concept of what actions could be performed) and doesn't quantify the risk level. The vulnerability is authenticated-only, which reduces but doesn't eliminate the risk. The suggested fix (X-Frame-Options: DENY) is appropriate but may be too restrictive if legitimate embedding is required; SAMEORIGIN would be a less restrictive alternative. The report's informal tone suggests a lower experience level but the technical content is accurate.

## Full report
<details><summary>Expand</summary>

Hii,
https://wakatime.com/share/embed is vulnerabel to clickjaking.
Description:
I found the resource on https://wakatime.com/share/embed, which can be vulnerable to the Clickjacking.

Impact
The resource without X-Frame-Options potentially vulnerable to the Clickjacking. The vulnerability exist only for authenticated users (possible UI redressing in the Dashboard).As it is on a authenticated page so a attacker make many benefits of it and can click jack any user

Step-by-step Reproduction Instructions

Go to the https://wakatime.com/share/embed
Look to the response headers. or Create .html file with next content: <iframe src="https://wakatime.com/share/embed"></iframe>

Suggested Mitigation/Remediation Actions
Adding X-Frame-Options: DENY header will solve this problem.

Thnx plzz review it and fix as soon as possible.

Regards Piyush kumar

</details>

---
*Analysed by Claude on 2026-05-24*
