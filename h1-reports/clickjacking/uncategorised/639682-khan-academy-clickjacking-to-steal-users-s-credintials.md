# Clickjacking on Khan Academy OAuth Login to Steal User Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 639682 | https://hackerone.com/reports/639682
- **Submitted:** 2019-07-10
- **Reporter:** hack_im
- **Program:** Khan Academy
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, Missing X-Frame-Options Header, OAuth Token Exposure, Insufficient Access Controls
- **CVEs:** None
- **Category:** uncategorised

## Summary
Khan Academy's alert subdomain (alerta.khanacademy.org) lacks clickjacking protection and displays sensitive OAuth credentials (email, access tokens, client IDs) in error messages. An attacker can frame the login page and trick users into unknowingly clicking through OAuth prompts to steal authentication credentials.

## Attack scenario
1. Attacker crafts a malicious webpage containing an invisible iframe pointing to https://alerta.khanacademy.org login
2. Victim, already logged into Google account, visits attacker's webpage
3. Attacker overlays deceiving UI elements (fake buttons/content) aligned with the hidden OAuth login frame
4. Victim clicks what they believe are legitimate UI elements but actually triggers OAuth consent/login in the framed page
5. Khan Academy OAuth flow displays sensitive information (email, access token, client ID) in error messages visible through the frame
6. Attacker extracts credentials via JavaScript DOM access or screenshot manipulation

## Root cause
Missing X-Frame-Options/Content-Security-Policy headers allowing iframe embedding, combined with OAuth credentials and sensitive tokens displayed in client-side error messages without proper sanitization or hiding

## Attacker mindset
Exploit common user behavior of remaining logged into Google accounts combined with lack of clickjacking defenses to passively harvest OAuth tokens and credentials from users without their awareness

## Defensive takeaways
- Implement X-Frame-Options: DENY or Content-Security-Policy frame-ancestors directive on all authentication endpoints
- Never expose access tokens, authorization codes, or client IDs in error messages or client-side JavaScript
- Implement token binding and short-lived authorization codes (preferably server-side only)
- Add UI indicators for iframe detection (frame-busting techniques)
- Enforce SameSite cookie attributes on authentication cookies
- Implement proper CSRF tokens on OAuth flows
- Sanitize and restrict what information is displayed in error messages to users

## Variant hunting
Other Khan Academy subdomains with OAuth implementations lacking frame protection
Other sensitive endpoints displaying tokens/codes in error messages
Login flows for other Google OAuth integrations at Khan Academy
API endpoints that may return credentials in responses
Third-party integrations using Khan Academy OAuth

## MITRE ATT&CK
- T1187 - Forced Authentication
- T1056 - Input Capture (via clickjacking)
- T1539 - Steal Web Session Cookie
- T1598 - Phishing
- T1111 - Multi-Factor Authentication Interception

## Notes
Report demonstrates understanding of clickjacking but lacks technical depth in exploit mechanics. The core vulnerability is the combination of missing anti-framing headers and credential exposure in error messages. The access control issue (denying normal users) actually contributes to the vulnerability by forcing error message display. Report references Burp Suite PoC and video evidence (not included in text).

## Full report
<details><summary>Expand</summary>

#DESCRIPTION

1. It ask to login to https://alerta.khanacademy.org  with google account.
2. It doesn't give access to any normal user.
3. That's why after trying to login with GOOGLE account it shows a error message prompt with user's sensitive information including [email, code/access token and client id etc.]
4. Let's steal it via Click Jacking!

Note: If victim is already logged into his google account, attacker can easily steal victim's credintials including [email, code/access token and client id etc.]

#Usually we always logged into our google account, so it's quite easy to steal victim's credintials.

#Step to Re-Produce:

Step 1. Let's make [ Script+PoC ] via BurpSuite! {F526049}

Step 2. Login to your google account.

Step 3. Exploition!

Watch my proof of concept video carefully!

████

Cheers!

## Impact

Attacker can easily steal victim's credintials including [email, code/access token and client id etc.]

</details>

---
*Analysed by Claude on 2026-05-24*
