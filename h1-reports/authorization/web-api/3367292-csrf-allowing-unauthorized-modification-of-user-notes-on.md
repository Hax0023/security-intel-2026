# CSRF allowing unauthorized modification of user Notes

## Metadata
- **Source:** HackerOne
- **Report:** 3367292 | https://hackerone.com/reports/3367292
- **Submitted:** 2025-10-02
- **Reporter:** kanon4
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Insufficient CSRF Protection, Missing Token Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A CSRF vulnerability in the notes modification endpoint allows attackers to modify or delete user notes by tricking victims into clicking a malicious link. The endpoint lacks CSRF protection mechanisms such as token validation. An attacker who knows the victim's ID (easily obtainable if both are organization members) can craft a PoC that modifies notes when visited.

## Attack scenario
1. Attacker gains membership in the same organization as victim to enumerate user IDs
2. Attacker identifies victim's client_id through organization member listing or brute force
3. Attacker generates CSRF PoC HTML form with malicious note payload and victim's ID
4. Attacker hosts malicious HTML on external server or embeds in phishing email
5. Victim unknowingly visits the malicious page while authenticated to the vulnerable application
6. Browser automatically submits form with victim's session cookies, modifying or deleting notes without victim awareness

## Root cause
The endpoint responsible for saving/modifying user notes does not implement CSRF protection mechanisms such as anti-CSRF tokens, SameSite cookie attributes, or request origin validation. The application accepts state-changing POST requests based solely on session cookies without verifying legitimate user intent.

## Attacker mindset
Low-effort, high-impact attack with modest prerequisites. Attacker recognizes that organization membership provides easy reconnaissance to obtain victim IDs. The simplicity of the PoC generation and automated form submission indicates attacker sees this as easily weaponizable for mass exploitation or targeted account sabotage within organizations.

## Defensive takeaways
- Implement synchronizer tokens (CSRF tokens) on all state-changing endpoints; validate token presence and correctness on server-side
- Apply SameSite cookie attribute (Strict or Lax mode) to session cookies to prevent automatic inclusion in cross-origin requests
- Validate HTTP Origin and Referer headers for POST/PUT/DELETE requests and reject mismatched origins
- Use double-submit cookie pattern as defense-in-depth alongside token-based protection
- Implement Content Security Policy (CSP) headers to restrict form submission targets
- Require explicit user interaction or confirmation dialogs for sensitive operations like data deletion
- Audit all endpoints modifying user data for CSRF protection implementation
- Implement rate limiting on sensitive endpoints to reduce blast radius of automated attacks
- Log CSRF rejection events for security monitoring

## Variant hunting
Check if other state-changing endpoints (user profile updates, password changes, settings modifications) lack CSRF protection
Test if other organization-member accessible operations suffer similar CSRF flaws
Verify if API endpoints use different protection mechanisms or are entirely unprotected
Examine if file upload endpoints are similarly vulnerable to CSRF
Check if admin operations (user management, organization settings) have CSRF protection
Test if CSRF tokens are properly invalidated after logout or session expiration
Verify if tokens are bound to session or user, and whether tokens can be reused across requests

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
Report heavily redacted limiting full context. Severity justified by: (1) low attack complexity once client_id obtained, (2) easy reconnaissance within organization context, (3) potential for mass exploitation if organization-wide attacks performed, (4) data integrity/confidentiality impact. Attacker required organization membership suggests insider threat or targeted external attack. PoC provided shows production-ready exploitation capability.

## Full report
<details><summary>Expand</summary>

## Summary:

A CSRF vulnerability allows an attacker to change a user's notes simply by clicking a link

The attacker can modify or delete all information the user left  just by clicking a link

The root cause is that the endpoint `███████` does not appear to implement protection against CSRF attacks

Therefore, once the attacker knows the victim’s `id`, they can send a malicious link that will modify or completely delete the user’s notes

The complexity of this attack is that the attacker needs to be a member (invited) in the same organization as the victim on the site in order to obtain the victim’s correct ID to use in the link.

When you are a member of the organization you can obtain the victim’s ID very easily.

A second, less likely scenario is that the attacker guesses the victim’s ID as 1 if they are confident the user is newly registered on the site.

## Steps To Reproduce:


  1. Log in to your account at ███████████ after placing an order on the site
  1. After logging in, you will see your Shared Notes field
  1. Enter any text into the Shared Notes field and click Save Note
  1. Open Burp Suite and go to the HTTP history tab
  1. Find the request for the endpoint POST `█████`
  1. Right-click that request and choose `Engagement tools` → `Generate CSRF PoC`
  1. Edit the generated PoC so the `client_id` parameter is set to the target victim’s ID
  1. Upload the generated HTML file to any web hosting or your own site
  1. Visit the hosted page as a regular user (or trick the victim into visiting it). The victim’s Shared Note will be modified█████deleted when the page is loaded

**Affected endpoint**

```██████████ HTTP██████████████████2
Host: ████████████████████████
Cookie: ██████████
Content-Type: application██████████████x-www-form-urlencoded; charset=UTF-8
Te: trailers
Content-Length: 53

ajax=save_note&client_id={ID_victim}&note=I+Hacked+YOU&area=client
```

**CSRF PoC**

```html
<html>
  <body>
    <form action="███████████████">
      <input type="hidden" name="ajax" value="save&#95;note" ████████████████████████████>
      <input type="hidden" name="client&#95;id" value="{{ID_victim}}" ████>
      <input type="hidden" name="note" value="i&#32;hack&#32;you" ███████████████████████████████████>
      <input type="hidden" name="area" value="client" █████████>
      <input type="submit" value="Submit request" ███████████████████>
    <███████████form>
    <script>
      history.pushState('', '', '█████████████████████████████████');
      document.forms[0].submit();
    <█████████████████████████script>
  <████body>
<██████████████████████████████html>
```

## Supporting Material███████████References:

**PoC Video**

█████████████████████

## Impact

- Unauthorized modification or deletion of a user’s Notes
- Loss of important data or contact information stored in notes
- Attacker can inject malicious links or social-engineering instructions into notes (enables phishing)
- Privacy████████████████████compliance risk if notes contain sensitive or regulated data
- Increased blast radius when attacker is a member of the same organization (easy access to victim `client_id`)
- Low-effort, high-impact exploitability once client_id is known — warrants High severity

</details>

---
*Analysed by Claude on 2026-05-24*
