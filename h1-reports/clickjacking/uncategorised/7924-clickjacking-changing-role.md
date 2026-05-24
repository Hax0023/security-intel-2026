# Clickjacking - Changing User Role via Framing Attack

## Metadata
- **Source:** HackerOne
- **Report:** 7924 | https://hackerone.com/reports/7924
- **Submitted:** 2014-04-17
- **Reporter:** smiegles
- **Program:** Respond.ly
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application lacks clickjacking protection, allowing attackers to frame the page with zero opacity and overlay invisible buttons to trick users into changing their account role. An attacker can craft a malicious webpage that frames the target application and positions invisible UI elements over legitimate buttons to perform unauthorized actions on behalf of the victim.

## Attack scenario
1. Attacker creates a malicious webpage that embeds the target application in an invisible iframe (opacity: 0)
2. Attacker overlays deceptive content (e.g., 'Click here to win a prize') on top of the framed page
3. Attacker calculates the position of the role-change button within the iframe and places a hidden clickable element at the same coordinates
4. Victim visits the malicious webpage and clicks on what they believe is legitimate content
5. The click actually triggers the role-change button within the framed application, changing the victim's role without their knowledge
6. Attacker gains elevated privileges or access to victim's account with the new role permissions

## Root cause
The application does not implement X-Frame-Options or Content-Security-Policy headers to prevent framing, and likely lacks additional protections against UI redressing attacks such as frame-busting code or user interaction confirmation dialogs for sensitive actions.

## Attacker mindset
An attacker recognizes that sensitive actions (role changes) lack adequate protection against framing attacks. They understand that users are unlikely to notice invisible overlays and that modern browsers allow cross-origin framing by default. The attacker seeks to escalate privileges or modify account settings through social engineering combined with technical exploitation.

## Defensive takeaways
- Implement X-Frame-Options header (DENY or SAMEORIGIN) to prevent page framing
- Deploy Content-Security-Policy with frame-ancestors directive to restrict framing contexts
- Add frame-busting JavaScript code as defense-in-depth measure
- Require explicit user confirmation (CSRF token + additional verification) for sensitive actions like role changes
- Implement User Interaction Verification (CAPTCHA, re-authentication) for privilege escalation operations
- Use clickjacking protection libraries or middleware to detect and prevent attacks
- Test application security with clickjacking scanning tools regularly

## Variant hunting
Search for other sensitive actions within the application that may be vulnerable to the same clickjacking attack (account deletion, password changes, permission modifications). Test whether the frame-busting protections work across different browsers and whether other headers (STS, CSP) provide additional protection layers.

## MITRE ATT&CK
- T1189 - Service Injection
- T1566 - Phishing
- T1656 - Impersonation

## Notes
This is a classic clickjacking vulnerability affecting privilege escalation. The POC demonstrates the vulnerability with minimal complexity. The report lacks details about the specific role change mechanism and whether additional protections (CSRF tokens, confirmation dialogs) were present. Early HackerOne report (2014) from a period when clickjacking was more common due to widespread lack of awareness about X-Frame-Options headers.

## Full report
<details><summary>Expand</summary>

Hi,

I'm able to frame the page, when I make a frame with a opacity of 0 and a button at the position of the role switch I can change the role without the victim knowing that.

a POC screen :
http://prntscr.com/3ay0mh

a POC code : 
`<iframe src="https://app.respond.ly" style="width:100%;height:100%;margin:0;border:0;"></iframe>`

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
